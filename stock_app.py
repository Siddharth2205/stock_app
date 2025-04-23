import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

st.set_page_config(page_title="📈 Stock Tracker", layout="centered")

# Title
st.title("📊 Stock Price Tracker")

# Input: stock ticker
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA, MSFT):", "AAPL").upper()

# Input: date range
period = st.selectbox(
    "Select Time Range:",
    ["5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "ytd", "max"],
    index=1
)

# Fetch stock data
if ticker:
    try:
        stock = yf.Ticker(ticker)
        current_price = stock.info["regularMarketPrice"]

        st.success(f"💵 Current Price of {ticker}: ${current_price}")

        hist = stock.history(period=period)

        if hist.empty:
            st.warning("No data found for this period.")
        else:
            st.line_chart(hist['Close'])

            with st.expander("📈 Show raw data"):
                st.dataframe(hist)

    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")
