# Library Management System

This project is a **Library Management System** built with **Flask**, providing a simple and efficient way to manage books, users, and borrowing activities.

## Features

### General
- User authentication (login, logout, registration)
- Session management

### For Librarians
- Add new books to the library
- View and manage borrow requests
- Approve or deny borrow requests
- Automatically record borrowing history upon approval

### For Users
- View available books
- Request to borrow books for a specific duration
- View borrowing history
- Download borrowing history as a CSV

## Project Structure

```
Library-Management-System/
├── app2.py            # Main application script
├── config.py          # Configuration for database and other settings
├── models.py          # Database models for User, Book, BorrowRequest, and 
├── library.db         # SQLite database (auto-generated)
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```

## Setup Instructions

### Prerequisites

- Python 3.7+
- pip (Python package installer)
- SQLite (optional, used as the default database)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Library-Management-System.git
   cd Library-Management-System
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with the following content:
   ```
   LIBRARIAN_EMAIL=your_librarian_email
   LIBRARIAN_PASSWORD= your_librarian_password
   ```

5. Initialize the database:
   ```bash
   python app2.py
   ```
   This will create a `library.db` file and set up the database schema. It will also create a default librarian account using the credentials in the `.env` file.

### Running the Application

1. Start the Flask server:
   ```bash
   python app2.py
   ```

2. Access the application in your browser at `http://127.0.0.1:5000`

## API Endpoints

### Authentication

| Method | Endpoint       | Description              |
|--------|----------------|--------------------------|
| POST   | `/login`       | Log in a user            |
| POST   | `/logout`      | Log out the current user |
| POST   | `/register`    | Register a new user      |

### Librarian APIs

| Method | Endpoint                        | Description                            |
|--------|----------------------------------|----------------------------------------|
| GET    | `/librarian/borrow-requests`    | View all borrow requests              |
| PUT    | `/librarian/borrow-requests/<id>` | Update a borrow request's status      |
| POST   | `/librarian/books`              | Add a new book                        |

### User APIs

| Method | Endpoint                 | Description                         |
|--------|---------------------------|-------------------------------------|
| GET    | `/books`                 | View all available books           |
| POST   | `/borrow`                | Request to borrow a book           |
| GET    | `/user/history`          | View user's borrowing history      |
| GET    | `/user/download-history` | Download borrowing history as CSV  |

## Default Librarian Account

The librarian account credentials are now stored in the `.env` file. Ensure to update the `.env` file with your desired email and password before initializing the database.

> **Note:** For security purposes, replace the secret key and default librarian credentials in production.

## Database Models

### User
- **id**: Primary Key
- **name**: User's name
- **email**: User's email (unique)
- **password**: Hashed password
- **role**: `librarian` or `user`

### Book
- **id**: Primary Key
- **title**: Book title
- **author**: Book author
- **isbn**: Book ISBN (unique)
- **copies**: Number of copies available

### BorrowRequest
- **id**: Primary Key
- **user_id**: Foreign Key (User)
- **book_id**: Foreign Key (Book)
- **start_date**: Borrowing start date
- **end_date**: Borrowing end date
- **status**: Request status (`pending`, `approved`, `denied`)

### BorrowHistory
- **id**: Primary Key
- **user_id**: Foreign Key (User)
- **book_id**: Foreign Key (Book)
- **borrow_date**: Borrowing date
- **return_date**: Returning date

## Future Improvements

- Add email notifications for borrow request approvals/denials
- Implement pagination for large datasets
- Enhance security with token-based authentication
- Add admin dashboard for better management

## License

This project is licensed under the [MIT License](LICENSE).

## Contributions

Contributions are welcome! Feel free to submit a pull request or open an issue.

## Contact

For any questions or feedback, feel free to contact:
- **Name**: Parth Prashant Pawar
