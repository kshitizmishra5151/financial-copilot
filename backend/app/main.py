from fastapi import FastAPI

from app.db.database import Base, engine

from app.api.users import router as users_router
from app.api.transactions import router as transactions_router
from app.api.copilot import router as copilot_router
from app.api.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Financial Copilot API"
)


@app.get("/")
def root():
    return {
        "message": "Financial Copilot Running"
    }


app.include_router(users_router)
app.include_router(transactions_router)
app.include_router(copilot_router)
app.include_router(auth_router)