from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from config import Config
from models import db, User, Book, BorrowRequest, BorrowHistory
# from dotenv import load_dotenv
import os

app = Flask(__name__)
app.config.from_object(Config)
app.config["SECRET_KEY"] = "supersecretkey"  # Replace with an environment variable in production
db.init_app(app)
librarian_email = os.getenv("LIBRARIAN_EMAIL")
librarian_password = os.getenv("LIBRARIAN_PASSWORD")

@app.route('/')
def home():
    return "Welcome to the Library Management System!"

def create_librarian():
    """Ensure a default librarian exists."""
    librarian_email = os.getenv("LIBRARIAN_EMAIL")
    librarian_password = os.getenv("LIBRARIAN_PASSWORD")
    
    if not librarian_email or not librarian_password:
        print("Error: Librarian email or password not set in environment variables.")
        return

    existing_librarian = User.query.filter_by(email=librarian_email).first()
    if not existing_librarian:
        librarian = User(
            name="Default Librarian",
            email=librarian_email,
            password=generate_password_hash(librarian_password, method='pbkdf2:sha256'),
            role="librarian"
        )
        db.session.add(librarian)
        db.session.commit()
        print("Librarian account created with email:", librarian_email)

# with app.app_context():
# def create_librarian():
#     """Ensure a default librarian exists."""
#     librarian_email = "admin@library.com"
#     existing_librarian = User.query.filter_by(email=librarian_email).first()
#     if not existing_librarian:
#         librarian = User(
#             name="Default Librarian",
#             email=librarian_email,
#             password=generate_password_hash("librarian123", method='pbkdf2:sha256'),
#             role="librarian"
#         )
#         db.session.add(librarian)
#         db.session.commit()
#         print("Librarian account created with email:", librarian_email)
# create_librarian()

# Authentication Middleware
def authenticate_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        return user
    return None

# Authentication Routes
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = authenticate_user(data['email'], data['password'])
    if user:
        session['user_id'] = user.id
        session['user_role'] = user.role
        return jsonify({"message": "Login successful!"}), 200
    return jsonify({"error": "Invalid email or password!"}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully!"}), 200

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if data.get('role') == 'librarian':
        return jsonify({"error": "You cannot create a librarian account!"}), 403
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(
        name=data['name'],
        email=data['email'],
        password=hashed_password,
        role='user'  # Only 'user' role is allowed through this endpoint
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"}), 201

# Middleware to check login status
def login_required(func):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Unauthorized! Please log in."}), 403
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

# Middleware to check librarian role
def librarian_required(func):
    def wrapper(*args, **kwargs):
        if 'user_role' not in session or session['user_role'] != 'librarian':
            return jsonify({"error": "Unauthorized! Only librarians are allowed."}), 403
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

# Librarian APIs
@app.route('/librarian/borrow-requests', methods=['GET'])
@login_required
@librarian_required
def view_borrow_requests():
    borrow_requests = BorrowRequest.query.all()
    return jsonify([
        {
            "id": req.id,
            "user_id": req.user_id,
            "book_id": req.book_id,
            "start_date": req.start_date,
            "end_date": req.end_date,
            "status": req.status
        } for req in borrow_requests
    ])

@app.route('/librarian/borrow-requests/<int:request_id>', methods=['PUT'])
@login_required
@librarian_required
def update_borrow_request(request_id):
    data = request.json
    borrow_request = BorrowRequest.query.get(request_id)
    if not borrow_request:
        return jsonify({"error": "Borrow request not found!"}), 404
    borrow_request.status = data['status']
    if data['status'] == 'approved':
        history_entry = BorrowHistory(
            user_id=borrow_request.user_id,
            book_id=borrow_request.book_id,
            borrow_date=borrow_request.start_date,
            return_date=borrow_request.end_date
        )
        db.session.add(history_entry)
    db.session.commit()
    return jsonify({"message": "Borrow request updated successfully!"})

# Library User APIs
@app.route('/books', methods=['GET'])
@login_required
def get_books():
    books = Book.query.all()
    return jsonify([
        {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "isbn": book.isbn,
            "copies": book.copies
        } for book in books
    ])

@app.route('/borrow', methods=['POST'])
@login_required
def request_borrow():
    user_id = session['user_id']
    data = request.json
    overlapping_request = BorrowRequest.query.filter(
        BorrowRequest.book_id == data['book_id'],
        BorrowRequest.start_date <= data['end_date'],
        BorrowRequest.end_date >= data['start_date'],
        BorrowRequest.status == 'approved'
    ).first()
    if overlapping_request:
        return jsonify({"error": "Book is already borrowed during this period!"}), 400
    borrow_request = BorrowRequest(
        user_id=user_id,
        book_id=data['book_id'],
        start_date=datetime.strptime(data['start_date'], "%Y-%m-%d"),
        end_date=datetime.strptime(data['end_date'], "%Y-%m-%d"),
        status='pending'
    )
    db.session.add(borrow_request)
    db.session.commit()
    return jsonify({"message": "Borrow request submitted!"}), 201

@app.route('/user/history', methods=['GET'])
@login_required
def view_user_history():
    user_id = session['user_id']
    history = BorrowHistory.query.filter_by(user_id=user_id).all()
    return jsonify([
        {
            "book_id": h.book_id,
            "borrow_date": h.borrow_date,
            "return_date": h.return_date
        } for h in history
    ])

@app.route('/user/download-history', methods=['GET'])
@login_required
def download_user_history():
    user_id = session['user_id']
    history = BorrowHistory.query.filter_by(user_id=user_id).all()
    csv_data = "Book ID,Borrow Date,Return Date\n"
    csv_data += "\n".join([
        f"{h.book_id},{h.borrow_date},{h.return_date}" for h in history
    ])
    return jsonify({"csv": csv_data})  # Replace with file download logic for production

@app.route('/librarian/books', methods=['POST'])
@login_required
@librarian_required
def add_book():
    data = request.json
    if not data.get("title") or not data.get("author") or not data.get("isbn"):
        return jsonify({"error": "Missing required fields: title, author, or isbn."}), 400

    existing_book = Book.query.filter_by(isbn=data['isbn']).first()
    if existing_book:
        return jsonify({"error": "A book with this ISBN already exists!"}), 400

    new_book = Book(
        title=data['title'],
        author=data['author'],
        isbn=data['isbn'],
        copies=data.get('copies', 1)
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book added successfully!", "book": {
        "id": new_book.id,
        "title": new_book.title,
        "author": new_book.author,
        "isbn": new_book.isbn,
        "copies": new_book.copies
    }}), 201

if __name__ == "__main__":
    with app.app_context():
        # Create all tables
        db.create_all()

        # Ensure default librarian exists after tables are created
        librarian_email = "admin@library.com"
        existing_librarian = User.query.filter_by(email=librarian_email).first()
        if not existing_librarian:
            librarian = User(
                name="Default Librarian",
                email=librarian_email,
                password=generate_password_hash(librarian_email, method='pbkdf2:sha256'),
                role="librarian"
            )
            db.session.add(librarian)
            db.session.commit()
            print("Librarian account created with email:", librarian_email)

    app.run(debug=True)
