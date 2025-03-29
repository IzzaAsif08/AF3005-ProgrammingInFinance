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

# User Input: Buy Prices
portfolio["Buy Price (USD)"] = [st.sidebar.number_input(f"Buy Price for {crypto}?", min_value=0.0, step=0.01) for crypto in cryptos]

# Calculate Profit/Loss
portfolio["Profit/Loss (USD)"] = (portfolio["Current Price (USD)"] - portfolio["Buy Price (USD)"]) * portfolio["Amount"]
portfolio["Profit/Loss (%)"] = ((portfolio["Current Price (USD)"] - portfolio["Buy Price (USD)"]) / portfolio["Buy Price (USD)"]) * 100

st.write("### Profit/Loss Summary")
st.write(portfolio[["Crypto", "Profit/Loss (USD)", "Profit/Loss (%)"]])

# Show total profit/loss
total_profit_loss = portfolio["Profit/Loss (USD)"].sum()
if total_profit_loss >= 0:
    st.success(f"📈 Total Profit: ${total_profit_loss:,.2f}")
else:
    st.error(f"📉 Total Loss: ${total_profit_loss:,.2f}")



if cryptos:
    fig = px.pie(portfolio, names="Crypto", values="Total Value (USD)", title="Portfolio Distribution")
    st.plotly_chart(fig)


if cryptos:
    num_assets = len(cryptos)
    volatility = portfolio["Current Price (USD)"].std()  # Approx risk measure
    health_score = max(0, 100 - (volatility * 5 + num_assets * 10))  # Custom formula
    
    st.write("### Portfolio Health Score")
    st.progress(int(health_score))

# Allow custom date selection
st.sidebar.header("📅 Custom Backtesting")
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")

if cryptos and start_date and end_date:
    hist_data = {crypto: yf.Ticker(crypto).history(start=start_date, end=end_date)["Close"] for crypto in cryptos}
    hist_df = pd.DataFrame(hist_data)

    st.write(f"### Price History from {start_date} to {end_date}")
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

import requests

st.sidebar.header("📰 Crypto News")

news_api_url = "https://api.coingecko.com/api/v3/news"
response = requests.get(news_api_url)

if response.status_code == 200:
    news_data = response.json()
    top_news = news_data["data"][:5]  # Get top 5 news articles

    for article in top_news:
        st.sidebar.markdown(f"🔹 [{article['title']}]({article['url']})")
else:
    st.sidebar.warning("Could not fetch news.")


st.sidebar.header("🎮 Crypto Prediction Game")

prediction = st.sidebar.radio("Where do you think BTC will be tomorrow?", ["Up", "Down", "Same"])
if st.sidebar.button("Submit Prediction"):
    st.sidebar.success("Prediction Submitted! Check tomorrow to see results.")

st.sidebar.header("🚀 Market Movers")

trending_api_url = "https://api.coingecko.com/api/v3/search/trending"
response = requests.get(trending_api_url)

if response.status_code == 200:
    trending_data = response.json()
    trending_coins = trending_data["coins"][:5]  # Get top 5 trending coins

    for coin in trending_coins:
        name = coin["item"]["name"]
        symbol = coin["item"]["symbol"]
        price = coin["item"]["price_btc"]
        st.sidebar.write(f"🔥 {name} ({symbol.upper()}) - {price:.8f} BTC")
else:
    st.sidebar.warning("Could not fetch trending coins.")

