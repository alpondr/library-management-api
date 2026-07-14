from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.database import Base

# ==========================================
# ASSOCIATION TABLE (Many-to-Many İlişki İçin)
# ==========================================
# Bir kitabın birden fazla kategorisi olabilir, bir kategoride birden fazla kitap olabilir.
# SQLAlchemy'de bu ilişkiyi kurmak için aracı bir tablo (association table) oluştururuz.
book_category_association = Table(
    "book_category",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id"), primary_key=True)
)

# ==========================================
# DATABASE MODELS (Tablolarımız)
# ==========================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user") # "admin" veya "user" olacak
    is_active = Column(Boolean, default=True)

    # İlişki: Bir kullanıcının birden fazla ödünç kaydı olabilir
    borrow_records = relationship("BorrowRecord", back_populates="user")

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    bio = Column(String)

    # İlişki: Bir yazarın birden fazla kitabı olabilir
    books = relationship("Book", back_populates="author")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    # Many-to-Many İlişki: 'secondary' parametresi ile aracı tabloyu (association table) bağlıyoruz.
    books = relationship("Book", secondary=book_category_association, back_populates="categories")

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(String)
    stock = Column(Integer, default=0, nullable=False)
    published_year = Column(Integer)
    
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)

    # İlişkiler
    author = relationship("Author", back_populates="books")
    categories = relationship("Category", secondary=book_category_association, back_populates="books")
    borrow_records = relationship("BorrowRecord", back_populates="book")

class BorrowRecord(Base):
    __tablename__ = "borrow_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    
    borrow_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    due_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=True) # İade edilmediyse boş kalır

    # İlişkiler
    user = relationship("User", back_populates="borrow_records")
    book = relationship("Book", back_populates="borrow_records")
