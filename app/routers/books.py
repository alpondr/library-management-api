from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.models import Book, User, Category
from app.schemas.schemas import BookCreate, BookResponse, BookBase
from app.core.deps import get_current_admin_user, get_current_user

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    """Sadece 'admin' rolündeki kullanıcılar kitap ekleyebilir. (get_current_admin_user kullanıldı)"""
    
    # Pydantic'ten gelen şemayı SQLAlchemy modeline dönüştürüyoruz
    new_book = Book(
        title=book.title,
        description=book.description,
        stock=book.stock,
        published_year=book.published_year,
        author_id=book.author_id
    )
    
    # Eğer kitap eklenirken kategori ID'leri verildiyse Many-to-Many ilişkiyi kuruyoruz
    if book.category_ids:
        categories = db.query(Category).filter(Category.id.in_(book.category_ids)).all()
        # Eğer istenen kategorilerden bazıları veritabanında yoksa hata ver
        if len(categories) != len(book.category_ids):
            raise HTTPException(status_code=400, detail="Some category IDs are invalid or do not exist")
        # Kitabın kategorilerine bu listeyi ekliyoruz. SQLAlchemy köprü tabloya otomatik kayıt atar!
        new_book.categories = categories

    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, updated_book: BookBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    """Sadece 'admin' rolündeki kullanıcılar kitap bilgilerini güncelleyebilir."""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
        
    book.title = updated_book.title
    book.description = updated_book.description
    book.stock = updated_book.stock
    book.published_year = updated_book.published_year
    
    db.commit()
    db.refresh(book)
    return book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    """Sadece 'admin' rolündeki kullanıcılar kitap silebilir."""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
        
    db.delete(book)
    db.commit()
    return None

@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Sisteme giriş yapmış herhangi bir kullanıcı kitap detayını görebilir."""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
