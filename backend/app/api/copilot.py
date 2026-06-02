from fastapi import APIRouter

from app.db.database import SessionLocal
from app.models.transaction import Transaction
from app.schemas.copilot import CopilotQuestion
from app.services.ai_service import ask_ai

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

    income = 0
    expenses = 0

    category_totals = {}

    for transaction in transactions:

        if transaction.category.lower() == "salary":
            income += transaction.amount
        else:
            expenses += transaction.amount

        if transaction.category not in category_totals:
            category_totals[transaction.category] = 0

        category_totals[transaction.category] += transaction.amount

    expense_categories = {
        k: v
        for k, v in category_totals.items()
        if k.lower() != "salary"
    }

    top_category = (
        max(expense_categories, key=expense_categories.get)
        if expense_categories else "None"
    )

    top_amount = (
        expense_categories[top_category]
        if expense_categories else 0
    )

    insight = (
        f"Income: ₹{income}, "
        f"Expenses: ₹{expenses}, "
        f"Savings: ₹{income - expenses}. "
        f"Highest expense category: {top_category} (₹{top_amount})."
    )

    db.close()

    return {
        "insight": insight
    }


@router.post("/ask")
def ask_copilot(request: CopilotQuestion):

    db = SessionLocal()

    transactions = db.query(Transaction).all()

    if not transactions:
        db.close()
        return {
            "answer": "No transactions found."
        }

    income = 0
    expenses = 0

    category_totals = {}

    for transaction in transactions:

        if transaction.category.lower() == "salary":
            income += transaction.amount
        else:
            expenses += transaction.amount

        if transaction.category not in category_totals:
            category_totals[transaction.category] = 0

        category_totals[transaction.category] += transaction.amount

    transaction_summary = f"""
Total Income: ₹{income}
Total Expenses: ₹{expenses}
Savings: ₹{income - expenses}

Category Breakdown:
"""

    for category, amount in category_totals.items():
        transaction_summary += f"{category}: ₹{amount}\n"

    answer = ask_ai(
        request.question,
        transaction_summary
    )

    db.close()

    return {
        "answer": answer
    }