# API Endpoints Documentation

This document provides details about the API endpoints available in the Library Management System backend, along with example requests and responses.

---

## Authentication Endpoints

### 1. `/login`
**Method**: `POST`

**Description**: Logs in a user.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "userpassword"
}
```

**Response**:
- Success (200):
```json
{
  "message": "Login successful!"
}
```
- Failure (401):
```json
{
  "error": "Invalid email or password!"
}
```

---

### 2. `/logout`
**Method**: `POST`

**Description**: Logs out the current user.

**Response**:
```json
{
  "message": "Logged out successfully!"
}
```

---

### 3. `/register`
**Method**: `POST`

**Description**: Registers a new user.

**Request Body**:
```json
{
  "name": "John Doe",
  "email": "johndoe@example.com",
  "password": "password123",
  "role": "user"
}
```

**Response**:
- Success (201):
```json
{
  "message": "User registered successfully!"
}
```
- Failure (403):
```json
{
  "error": "You cannot create a librarian account!"
}
```

---

## Librarian Endpoints

### 1. `/librarian/borrow-requests`
**Method**: `GET`

**Description**: Retrieves all borrow requests.

**Response**:
```json
[
  {
    "id": 1,
    "user_id": 101,
    "book_id": 202,
    "start_date": "2024-01-01",
    "end_date": "2024-01-15",
    "status": "pending"
  }
]
```

---

### 2. `/librarian/borrow-requests/<id>`
**Method**: `PUT`

**Description**: Updates the status of a borrow request.

**Request Body**:
```json
{
  "status": "approved"
}
```

**Response**:
- Success:
```json
{
  "message": "Borrow request updated successfully!"
}
```
- Failure (404):
```json
{
  "error": "Borrow request not found!"
}
```

---

### 3. `/librarian/books`
**Method**: `POST`

**Description**: Adds a new book to the library.

**Request Body**:
```json
{
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "isbn": "1234567890123",
  "copies": 5
}
```

**Response**:
- Success:
```json
{
  "message": "Book added successfully!",
  "book": {
    "id": 301,
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "isbn": "1234567890123",
    "copies": 5
  }
}
```
- Failure:
```json
{
  "error": "A book with this ISBN already exists!"
}
```

---

## User Endpoints

### 1. `/books`
**Method**: `GET`

**Description**: Retrieves all available books.

**Response**:
```json
[
  {
    "id": 1,
    "title": "1984",
    "author": "George Orwell",
    "isbn": "9780451524935",
    "copies": 3
  }
]
```

---

### 2. `/borrow`
**Method**: `POST`

**Description**: Submits a borrow request.

**Request Body**:
```json
{
  "book_id": 1,
  "start_date": "2024-01-01",
  "end_date": "2024-01-15"
}
```

**Response**:
- Success (201):
```json
{
  "message": "Borrow request submitted!"
}
```
- Failure (400):
```json
{
  "error": "Book is already borrowed during this period!"
}
```

---

### 3. `/user/history`
**Method**: `GET`

**Description**: Retrieves the borrowing history of the logged-in user.

**Response**:
```json
[
  {
    "book_id": 1,
    "borrow_date": "2024-01-01",
    "return_date": "2024-01-15"
  }
]
```

---

### 4. `/user/download-history`
**Method**: `GET`

**Description**: Downloads the user's borrowing history as a CSV.

**Response**:
```json
{
  "csv": "Book ID,Borrow Date,Return Date\n1,2024-01-01,2024-01-15"
}
```

---

