from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class CurrencyCalculateRequest(BaseModel):
    from_currency: str
    to_currency: str
    amount: float


class TradeRequest(BaseModel):
    from_date: str
    to_date: str


class UserStockPurchaseRequest(BaseModel):
    order_date: str
    symbol: str
    transaction_type: str
    order_quantity: float
    trade_price_value: float
    charges: float
    user_email: str
    order_date_obj: Optional[str]


class BlogPost(BaseModel):
    body: str
    author: str
    title: str
    slug: str
    published: bool
    # published_at: datetime
    created_by: str
    description: str
    tags: str
    categories: str
    image_url: str
