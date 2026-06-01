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

    return new_transaction


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

    total = sum(transaction.amount for transaction in transactions)

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


@router.put("/{transaction_id}")
def update_transaction(
    transaction_id: int,
    transaction: TransactionCreate
):

    db = SessionLocal()

    existing_transaction = (
        db.query(Transaction)
        .filter(Transaction.id == transaction_id)
        .first()
    )

    if not existing_transaction:
        db.close()
        return {"error": "Transaction not found"}

    existing_transaction.user_id = transaction.user_id
    existing_transaction.amount = transaction.amount
    existing_transaction.category = transaction.category

    db.commit()
    db.refresh(existing_transaction)

    db.close()

    return existing_transaction


@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int):

    db = SessionLocal()

    transaction = (
        db.query(Transaction)
        .filter(Transaction.id == transaction_id)
        .first()
    )

    if not transaction:
        db.close()
        return {"error": "Transaction not found"}

    db.delete(transaction)
    db.commit()

    db.close()

    return {
        "message": "Transaction deleted successfully"
    }