from fastapi import FastAPI

from app.db.database import Base, engine

# Import models so SQLAlchemy creates the tables
from app.models.user import User
from app.models.transaction import Transaction

# Import routers
from app.api.users import router as user_router
from app.api.transactions import router as transaction_router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Register routers
app.include_router(user_router)
app.include_router(transaction_router)

@app.get("/")
def root():
    return {
        "message": "Financial Copilot Running"
    }