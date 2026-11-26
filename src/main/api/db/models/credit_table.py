from src.main.api.db.base import Base
from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime

class Credit(Base):
    __tablename__ = 'credit'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('account.id'), nullable=False)
    amount = Column(Float, nullable=False, unique=True)
    term_months = Column(Integer, nullable=False, unique=True)
    balance = Column(Float, nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False)