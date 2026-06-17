import yfinance as yf

def get_market_data(symbol : str):
    stock = yf.Ticker(symbol)
    information = stock.info

    return{
        "symbol" : symbol,
        "current_price": information.get("current_price",0),
        "open": information.get("open",0),
        "high": information.get("high",0),
        "low": information.get("low",0),
        "volume": information.get("volume",0)
    }
