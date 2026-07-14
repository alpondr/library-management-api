from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.security import SECRET_KEY, ALGORITHM
from app.database.database import get_db
from app.models.models import User
from app.schemas.schemas import TokenData

# Bu yapı sayesinde FastAPI otomatik olarak Swagger arayüzünde "Authorize" (kilit) butonu çıkartır
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Gelen JWT token'ını çözer, doğrular ve işlemi yapan mevcut User objesini veritabanından döndürür"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Token'ı çöz
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
        
    # Veritabanında email'e göre kullanıcıyı bul
    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
        
    return user

def get_current_admin_user(current_user: User = Depends(get_current_user)):
    """
    Sadece 'admin' rolündeki kullanıcıların geçmesine izin veren Role-Based Access Control (RBAC) bağımlılığı.
    Eğer rol 'admin' değilse 403 Hata kodu fırlatır.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have enough permissions (Admin role required)"
        )
    return current_user
