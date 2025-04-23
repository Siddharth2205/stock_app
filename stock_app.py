import streamlit as st
import yfinance as yf
import requests

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


API_KEY = os.getenv("API_KEY")

st.set_page_config(page_title="🌍 Global Stock Tracker", layout="centered")
st.title("📈 Global Stock Price Tracker")

# 🌍 Region dropdown (for region-specific tickers)
region = st.selectbox("Choose a region for example tickers:", [
    "United States",
    "India",
    "United Kingdom",
    "Japan",
    "Germany",
    "Canada",
    "Australia",
    "France"
])

# Map region to valid exchange suffixes
valid_suffixes = {
    "United States": ["", ".NS", ".L", ".T"],
    "India": ["NS"],
    "United Kingdom": [".L"],
    "Japan": [".T"],
    "Germany": [".DE"],
    "Canada": [".TO"],
    "Australia": [".AX"],
    "France": [".PA"]
}

# Map region to example tickers
region_tickers = {
    "United States": ["AAPL", "TSLA", "MSFT"],
    "India": ["RELIANCE.NS", "INFY.NS"],
    "United Kingdom": ["BP.L", "HSBC.L"],
    "Japan": ["7203.T"],
    "Germany": ["BMW.DE"],
    "Canada": ["RY.TO"],
    "Australia": ["CBA.AX"],
    "France": ["AIR.PA"]
}

# Show the relevant example tickers for the region
st.info(f"Example tickers for {region}: {', '.join(region_tickers[region])}")

# Search company name
query = st.text_input("🔍 Search Company Name (e.g., Tesla, Infosys, Toyota):")
ticker = None

if query:
    response = requests.get(
        f"https://financialmodelingprep.com/api/v3/search?query={query}&limit=5&apikey={API_KEY}"
    )
    results = response.json()

    if results:
        # Filter results to match valid exchange suffixes for the selected region
        filtered_results = [
            f"{r['name']} ({r['symbol']})"
            for r in results if any(r['symbol'].endswith(suffix) for suffix in valid_suffixes[region])
        ]
        
        if filtered_results:
            selected = st.selectbox("Select company:", filtered_results)
            ticker = selected.split('(')[-1].strip(')')
        else:
            st.warning(f"No results found for {region} tickers.")
    else:
        st.warning("No results found.")

# Time range
period = st.selectbox("Select Time Range:", ["5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "ytd", "max"], index=1)

# Fetch & display stock data
if ticker:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        if "regularMarketPrice" in info:
            name = info.get("longName", "N/A")
            exchange = info.get("exchange", "N/A")
            price = info["regularMarketPrice"]

            st.success(f"**{name}** ({ticker})\n\n💵 Price: ${price} | 🌐 Exchange: {exchange}")

            hist = stock.history(period=period)

            if not hist.empty:
                st.line_chart(hist["Close"])
                with st.expander("📊 Show raw data"):
                    st.dataframe(hist)
            else:
                st.warning("No historical data found for this period.")
        else:
            st.error("⚠️ Invalid ticker or data not available.")
    except Exception as e:
        st.error(f"Error: {e}")

# 🌍 Global Help Guide (for other tickers)
with st.expander("🌍 See Global Ticker Examples"):
    st.markdown("""
    - **US**: AAPL, TSLA, MSFT  
    - **India (NSE)**: RELIANCE.NS, INFY.NS  
    - **UK (LSE)**: BP.L, HSBC.L  
    - **Japan (TSE)**: 7203.T (Toyota)  
    - **Germany (XETRA)**: BMW.DE  
    - **Canada (TSX)**: RY.TO  
    - **Australia (ASX)**: CBA.AX  
    - **France (Euronext)**: AIR.PA  
    """)
