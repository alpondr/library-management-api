from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# =======================
# TOKEN ŞEMALARI
# =======================
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# =======================
# KULLANICI (USER) ŞEMALARI
# =======================
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool

    class Config:
        # Bu ayar Pydantic'in SQLAlchemy modellerini (dictionary yerine object formatını) okuyabilmesini sağlar
        from_attributes = True

# =======================
# KATEGORİ (CATEGORY) ŞEMALARI
# =======================
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True

# =======================
# YAZAR (AUTHOR) ŞEMALARI
# =======================
class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None

class AuthorCreate(AuthorBase):
    pass

class AuthorResponse(AuthorBase):
    id: int

    class Config:
        from_attributes = True

# =======================
# KİTAP (BOOK) ŞEMALARI
# =======================
class BookBase(BaseModel):
    title: str
    description: Optional[str] = None
    stock: int
    published_year: Optional[int] = None

class BookCreate(BookBase):
    author_id: int
    category_ids: List[int] = [] # Kitap oluştururken kategori ID'lerini liste olarak alacağız

class BookResponse(BookBase):
    id: int
    author: AuthorResponse
    categories: List[CategoryResponse] = [] # Dönüşte kitapla beraber kategorileri de listeleyeceğiz

    class Config:
        from_attributes = True

# =======================
# ÖDÜNÇ KAYDI (BORROW RECORD) ŞEMALARI
# =======================
class BorrowRecordBase(BaseModel):
    book_id: int

class BorrowRecordCreate(BorrowRecordBase):
    pass

class BorrowRecordResponse(BorrowRecordBase):
    id: int
    user_id: int
    borrow_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None

    class Config:
        from_attributes = True
