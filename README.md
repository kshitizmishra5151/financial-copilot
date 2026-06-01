# Financial Copilot

A FastAPI-powered personal finance backend that helps users track transactions, generate spending summaries, and receive AI-style financial insights.

## Features

### User Management
- Create users
- Retrieve user transactions

### Transaction Management
- Create transactions
- View all transactions
- Update transactions
- Delete transactions
- Calculate total spending
- Category-wise spending summary

### Financial Copilot
- Spending insights
- Natural language financial questions

Example:

Question:
"What is my total spending?"

Response:
"Your total spending is ₹10500.0."

---

## Tech Stack

- Python 3
- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker
- Swagger UI
- GitHub

---

## API Endpoints

### Users

| Method | Endpoint |
|----------|----------|
| POST | /users |
| GET | /users/{user_id}/transactions |

### Transactions

| Method | Endpoint |
|----------|----------|
| POST | /transactions |
| GET | /transactions |
| PUT | /transactions/{transaction_id} |
| DELETE | /transactions/{transaction_id} |
| GET | /transactions/total |
| GET | /transactions/summary |

### Copilot

| Method | Endpoint |
|----------|----------|
| GET | /copilot/insights |
| POST | /copilot/ask |

---

## Run Locally

### Clone Repository

```bash
git clone https://github.com/kshitizmishra5151/financial-copilot.git
cd financial-copilot
```

### Start PostgreSQL

```bash
docker-compose up -d
```

### Start Backend

```bash
cd backend
uvicorn app.main:app --reload
```

### Open Swagger

```text
http://127.0.0.1:8000/docs
```

---

## Sample Copilot Request

POST /copilot/ask

```json
{
  "question": "What is my total spending?"
}
```

Response

```json
{
  "answer": "Your total spending is ₹10500.0."
}
```

---

## Author

Kshitiz Mishra
