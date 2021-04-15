from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Trade:
    id: int
    tid: int
    ticker_id: int
    created_at: int
    price: Decimal
    amount: Decimal


TRADE_FIELDS = list(Trade.__annotations__.keys())
