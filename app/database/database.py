from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# .env dosyasındaki değişkenleri sisteme yükler
load_dotenv() 

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Veritabanı motorunu oluştururuz
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Veritabanı oturumlarını (session) yönetmek için bir sınıf oluştururuz
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tüm modellerimizin miras alacağı ana sınıf (Base sınıfı)
Base = declarative_base()

# Dependency Injection için kullanacağımız, her istekte veritabanı bağlantısı açıp kapatan fonksiyon
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
