def simple_backtest(df, initial_capital = 100000):
    start_price = df["Close"].iloc[0]
    end_price = df["Close"].iloc[-1]
    shares = initial_capital / start_price
    final_value = shares * end_price
    total_return = ((final_value - initial_capital) / initial_capital) * 100
    return {"Initial Capital": initial_capital,
            "Final Value": final_value,
            "total_return": total_return}