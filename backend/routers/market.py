from fastapi import APIRouter
from backend.services.market_service import get_market_data
from backend.schemas.market_schema import MarketResponse

router = APIRouter()

@router.get("/market/{symbol}",response_model = MarketResponse)
def market(symbol : str):
    return get_market_data(symbol)