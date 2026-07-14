from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.database.database import get_db
from app.models.models import Book, User, BorrowRecord
from app.schemas.schemas import BorrowRecordResponse
from app.core.deps import get_current_user

router = APIRouter(
    prefix="/borrow",
    tags=["Borrowing"]
)

@router.post("/{book_id}", response_model=BorrowRecordResponse)
def borrow_book(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Bir kitabı ödünç alma işlemi (Sadece giriş yapmış kullanıcılar)"""
    
    # 1. Kitap sistemde kayıtlı mı diye kontrol et
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
        
    # 2. Stok kontrolü yap (Stokta hiç kalmamışsa hata ver)
    if book.stock <= 0:
        raise HTTPException(status_code=400, detail="Book is currently out of stock")
        
    # 3. Kullanıcı bu kitabı zaten ödünç almış ve henüz iade ETMEMİŞ mi?
    active_borrow = db.query(BorrowRecord).filter(
        BorrowRecord.user_id == current_user.id,
        BorrowRecord.book_id == book_id,
        BorrowRecord.return_date == None # İade edilmediğini gösterir
    ).first()
    
    if active_borrow:
        raise HTTPException(status_code=400, detail="You have already borrowed this book and haven't returned it yet.")
        
    # 4. Her şey tamamsa ödünç kaydını oluştur
    # Teslim tarihi (due_date) şu anki tarihten 14 gün sonrası olarak ayarlanıyor
    new_borrow = BorrowRecord(
        user_id=current_user.id,
        book_id=book_id,
        borrow_date=datetime.utcnow(),
        due_date=datetime.utcnow() + timedelta(days=14)
    )
    
    # 5. Kitabın stok sayısını 1 eksilt
    book.stock -= 1
    
    db.add(new_borrow)
    db.commit()
    db.refresh(new_borrow)
    
    return new_borrow


@router.post("/{book_id}/return")
def return_book(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Ödünç alınmış bir kitabı iade etme işlemi"""
    
    # 1. Kullanıcının, bu kitap için olan "açık" (iade edilmemiş) kaydını bul
    active_borrow = db.query(BorrowRecord).filter(
        BorrowRecord.user_id == current_user.id,
        BorrowRecord.book_id == book_id,
        BorrowRecord.return_date == None
    ).first()
    
    if not active_borrow:
        raise HTTPException(status_code=400, detail="You do not have an active borrow record for this book.")
        
    # 2. İade tarihini 'şimdi' olarak güncelle
    active_borrow.return_date = datetime.utcnow()
    
    # 3. Kitabın stok sayısını 1 geri arttır
    book = db.query(Book).filter(Book.id == book_id).first()
    if book:
        book.stock += 1
        
    db.commit()
    
    # Gecikme (Overdue) Kontrolü: Eğer iade tarihi, teslim tarihini geçmişse
    is_overdue = active_borrow.return_date > active_borrow.due_date
    status_message = "Book returned successfully."
    
    if is_overdue:
        status_message += " Note: The book was returned late (OVERDUE)!"
        
    return {
        "message": status_message, 
        "borrow_date": active_borrow.borrow_date,
        "due_date": active_borrow.due_date,
        "return_date": active_borrow.return_date,
        "was_overdue": is_overdue
    }
