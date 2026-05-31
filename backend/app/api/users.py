from fastapi import APIRouter
from app.schemas.user import UserCreate
from app.models.user import User
from app.db.database import SessionLocal

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/")
def create_user(user: UserCreate):

    db = SessionLocal()

    new_user = User(
        name=user.name,
        email=user.email
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