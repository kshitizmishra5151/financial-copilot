from fastapi import APIRouter, HTTPException

from app.db.database import SessionLocal
from app.models.user import User
from app.schemas.auth import LoginRequest
from app.services.auth_service import (
    verify_password,
    create_access_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login")
def login(request: LoginRequest):

    db = SessionLocal()

    user = (
        db.query(User)
        .filter(User.email == request.email)
        .first()
    )

    if not user:

        db.close()

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        request.password,
        user.password
    ):

        db.close()

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={
            "sub": user.email
        }
    )

    db.close()

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }