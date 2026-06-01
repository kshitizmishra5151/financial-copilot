from fastapi import APIRouter

from app.db.database import SessionLocal
from app.models.transaction import Transaction
from app.schemas.copilot import CopilotQuestion

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
        f"with ₹{top_amount}."
    )

    db.close()

    return {
        "insight": insight
    }


@router.post("/ask")
def ask_copilot(request: CopilotQuestion):

    db = SessionLocal()

    transactions = db.query(Transaction).all()

    category_totals = {}

    for transaction in transactions:

        if transaction.category not in category_totals:
            category_totals[transaction.category] = 0

        category_totals[transaction.category] += transaction.amount

    question = request.question.lower()

    if "biggest" in question or "highest" in question:

        top_category = max(
            category_totals,
            key=category_totals.get
        )

        answer = (
            f"Your biggest expense category is "
            f"{top_category} with ₹{category_totals[top_category]}."
        )

    elif "food" in question:

        amount = category_totals.get("Food", 0)

        answer = f"You spent ₹{amount} on Food."

    elif "total" in question:

        total = sum(category_totals.values())

        answer = f"Your total spending is ₹{total}."

    else:

        answer = (
            "I can currently answer questions about "
            "total spending, food spending, and biggest expenses."
        )

    db.close()

    return {
        "answer": answer
    }