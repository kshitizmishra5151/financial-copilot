from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.db.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    amount = Column(Float)

    category = Column(String)

    merchant = Column(String, nullable=True)

    note = Column(String, nullable=True)

    date = Column(String, nullable=True)