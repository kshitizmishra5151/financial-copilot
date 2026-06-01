from fastapi import APIRouter
from app.db.database import SessionLocal
from app.models.transaction import Transaction

router = APIRouter(
    prefix="/copilot",
    tags=["Copilot"]
)


@router.get("/insights")
def get_insights():

    db = SessionLocal()

    transactions = db.query(Transaction).all()

    if not transactions:
        db.close()
        return {
            "insight": "No transactions found."
        }

    total_spent = sum(t.amount for t in transactions)

    category_totals = {}

    for transaction in transactions:

        if transaction.category not in category_totals:
            category_totals[transaction.category] = 0

        category_totals[transaction.category] += transaction.amount

    top_category = max(
        category_totals,
        key=category_totals.get
    )

    top_amount = category_totals[top_category]

    insight = (
        f"Your total spending is ₹{total_spent}. "
        f"Your highest spending category is {top_category} "
        f"with ₹{top_amount}. "
    )

    if len(category_totals) > 1:
        insight += "Category breakdown: "

        for category, amount in category_totals.items():
            insight += f"{category}: ₹{amount}, "

    db.close()

    return {
        "insight": insight
    }