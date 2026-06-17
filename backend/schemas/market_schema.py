from pydantic import BaseModel

class MarketResponse(BaseModel):
    symbol : str
    current_price : float
    open : float
    high : float
    low : float
    volume : int
    