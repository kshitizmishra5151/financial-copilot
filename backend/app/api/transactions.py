from fastapi import APIRouter
from app.schemas.transaction import TransactionCreate
from app.models.transaction import Transaction
from app.db.database import SessionLocal

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


@router.post("/")
def create_transaction(transaction: TransactionCreate):

    db = SessionLocal()

    new_transaction = Transaction(
        user_id=transaction.user_id,
        amount=transaction.amount,
        category=transaction.category
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    db.close()

    return {
        "id": new_transaction.id,
        "user_id": new_transaction.user_id,
        "amount": new_transaction.amount,
        "category": new_transaction.category
    }


@router.get("/")
def get_transactions():

    db = SessionLocal()

    transactions = db.query(Transaction).all()

    db.close()

    return transactions


@router.get("/total")
def get_total():

    db = SessionLocal()

    transactions = db.query(Transaction).all()

    total = 0

    for transaction in transactions:
        total += transaction.amount

    db.close()

    return {
        "total": total
    }


@router.get("/summary")
def get_summary():

    db = SessionLocal()

    transactions = db.query(Transaction).all()

    summary = {}

    for transaction in transactions:

        category = transaction.category

        if category not in summary:
            summary[category] = 0

        summary[category] += transaction.amount

    db.close()

    return summary