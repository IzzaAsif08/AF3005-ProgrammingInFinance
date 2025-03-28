import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

import streamlit as st

import streamlit as st

def load_css(file_name):
    with open(file_name) as f:
        css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# Call the function to load the CSS
load_css("style.css")


st.title("🚀 CryptoGird: Smart Portfolio Tracker")

# User Input
st.sidebar.header("📌 Enter Your Portfolio")
cryptos = st.sidebar.multiselect("Select Cryptos", ["BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "XRP-USD"])
amounts = [st.sidebar.number_input(f"How many {crypto}?", min_value=0.0, step=0.01) for crypto in cryptos]

if cryptos:
    portfolio = pd.DataFrame({"Crypto": cryptos, "Amount": amounts})
    st.write("### Your Portfolio", portfolio)


if cryptos:
    prices = {crypto: yf.Ticker(crypto).history(period="1d")["Close"].iloc[-1] for crypto in cryptos}
    portfolio["Current Price (USD)"] = portfolio["Crypto"].map(prices)
    portfolio["Total Value (USD)"] = portfolio["Amount"] * portfolio["Current Price (USD)"]
    st.write("### Portfolio Value", portfolio)
    
    # Show total portfolio value
    total_value = portfolio["Total Value (USD)"].sum()
    st.success(f"💰 Total Portfolio Value: ${total_value:,.2f}")


if cryptos:
    fig = px.pie(portfolio, names="Crypto", values="Total Value (USD)", title="Portfolio Distribution")
    st.plotly_chart(fig)


if cryptos:
    num_assets = len(cryptos)
    volatility = portfolio["Current Price (USD)"].std()  # Approx risk measure
    health_score = max(0, 100 - (volatility * 5 + num_assets * 10))  # Custom formula
    
    st.write("### Portfolio Health Score")
    st.progress(int(health_score))


st.sidebar.header("📅 Backtesting")
time_period = st.sidebar.selectbox("Select Time Period", ["1y", "6mo", "3mo"])

if cryptos:
    hist_data = {crypto: yf.Ticker(crypto).history(period=time_period)["Close"] for crypto in cryptos}
    hist_df = pd.DataFrame(hist_data)

    st.write(f"### Backtesting for {time_period}")
    st.line_chart(hist_df)


import requests

st.sidebar.header("🐋 Whale Watcher")

if st.sidebar.button("Check Whale Transactions"):
    whale_api_url = "https://api.whale-alert.io/v1/transactions?api_key=your_api_key"
    response = requests.get(whale_api_url)
    
    if response.status_code == 200:
        whale_data = response.json()
        st.write("### Recent Whale Transactions")
        for tx in whale_data["transactions"][:5]:
            st.write(f"{tx['amount']} {tx['symbol']} moved worth ${tx['amount_usd']}")
    else:
        st.warning("Could not fetch whale transactions.")

st.sidebar.header("🎮 Crypto Prediction Game")

prediction = st.sidebar.radio("Where do you think BTC will be tomorrow?", ["Up", "Down", "Same"])
if st.sidebar.button("Submit Prediction"):
    st.sidebar.success("Prediction Submitted! Check tomorrow to see results.")
