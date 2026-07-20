from fastapi import APIRouter
from services.market_service import get_market_data
from schemas.market_schema import MarketResponse

router = APIRouter()

@router.get("/market/{symbol}",response_model = MarketResponse)
def market(symbol : str):
    return get_market_data(symbol)