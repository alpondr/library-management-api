from fastapi import FastAPI
from app.routers import auth

app = FastAPI(title="Library Borrowing System API")

# Router'ları ana uygulamaya bağlıyoruz
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Welcome to Library Management API!"}
