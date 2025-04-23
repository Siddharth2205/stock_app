import yfinance as ysf
import matplotlib.pyplot as plt
ticker_symbol = input  ("Enter a stock ticker symbol(eg, AAPL,TSLA )").upper()
stock = ysf.Ticker(ticker_symbol)
try:
    current_price = stock.info['regularMarketPrice']
    print(f"\nCurrent price of {ticker_symbol}: ${current_price}")
except KeyError:
    print(f"⚠️ Unable to fetch price for '{ticker_symbol}'. Please check the ticker symbol.")
    exit()

hist = stock.history(period="1mo")

if hist.empty:
    print("⚠️ No historical data found.")
    exit()
    plt.figure(figsize=(10, 5))
plt.plot(hist.index, hist['Close'], marker='o', linestyle='-')
plt.title(f"{ticker_symbol} Closing Prices (Last 1 Month)")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.grid(True)
plt.tight_layout()
plt.show()