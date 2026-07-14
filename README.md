# Library Borrowing System API

This is a backend API project for a library borrowing system. I built this to learn and practice FastAPI, PostgreSQL, and SQLAlchemy.

## Features

- **Authentication:** User registration and login with JWT (JSON Web Tokens).
- **Role-Based Access Control:** 'admin' users can add/delete/update books, while 'user' role can only borrow/return them.
- **Book Management:** CRUD operations for books. Supports Many-to-Many relationships between Books and Categories.
- **Borrowing Logic:** Users can borrow books (decreases stock by 1, sets a 14-day due date). Returning a book increases the stock and checks if the return was overdue.
- **Search & Pagination:** Browse books by title, author, or category with pagination support.

## Tech Stack

- Python 3.11+
- FastAPI
- PostgreSQL & SQLAlchemy (ORM)
- Alembic (Migrations)
- Pydantic (Data validation)
- python-jose & passlib (JWT Auth)

## How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/alpondr/library-management-api.git
   cd library-management-api
   ```

2. **Create a virtual environment and install dependencies:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Set up the database:**
   - Create a PostgreSQL database.
   - Copy `.env.example` to `.env` and update the `DATABASE_URL` with your credentials.
   - Run migrations to create tables:
     ```bash
     alembic upgrade head
     ```

4. **Start the server:**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Test the API:**
   - Go to `http://127.0.0.1:8000/docs` in your browser to see the interactive Swagger UI and test the endpoints!
