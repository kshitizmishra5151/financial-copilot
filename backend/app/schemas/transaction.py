from pydantic import BaseModel


class TransactionCreate(BaseModel):
    user_id: int
    amount: float
    category: str


class TransactionResponse(BaseModel):
    id: int
    user_id: int
    amount: float
    category: str

    class Config:
        from_attributes = True