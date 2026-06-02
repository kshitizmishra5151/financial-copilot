from fastapi import APIRouter

from app.schemas.user import UserCreate
from app.models.user import User
from app.models.transaction import Transaction
from app.db.database import SessionLocal
from app.services.auth_service import hash_password

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/")
def create_user(user: UserCreate):

    db = SessionLocal()

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    db.close()

    return {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email
    }


@router.get("/{user_id}/transactions")
def get_user_transactions(user_id: int):

    db = SessionLocal()

    transactions = (
        db.query(Transaction)
        .filter(Transaction.user_id == user_id)
        .all()
    )

    db.close()

    return transactions