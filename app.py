import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
import requests

# Load CSS
def load_css(file_name):
    with open(file_name) as f:
        css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

load_css("style.css")

st.title("🚀 CryptoGird: Smart Portfolio Tracker")

# User Input
st.sidebar.header("📌 Enter Your Portfolio")
cryptos = st.sidebar.multiselect("Select Cryptos", ["BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "XRP-USD"])
amounts = [st.sidebar.number_input(f"How many {crypto}?", min_value=0.0, step=0.01) for crypto in cryptos]

if cryptos:
    portfolio = pd.DataFrame({"Crypto": cryptos, "Amount": amounts})
    prices = {crypto: yf.Ticker(crypto).history(period="1d")["Close"].iloc[-1] for crypto in cryptos}
    portfolio["Current Price (USD)"] = portfolio["Crypto"].map(prices)
    portfolio["Total Value (USD)"] = portfolio["Amount"] * portfolio["Current Price (USD)"]
    st.write("### Your Portfolio", portfolio)
    st.success(f"💰 Total Portfolio Value: ${portfolio['Total Value (USD)'].sum():,.2f}")

    # User Input: Buy Prices
    buy_prices = [st.sidebar.number_input(f"Buy Price for {crypto}?", min_value=0.0, step=0.01) for crypto in cryptos]
    portfolio["Buy Price (USD)"] = buy_prices

    # Calculate Profit/Loss
    portfolio["Profit/Loss (USD)"] = (portfolio["Current Price (USD)"] - portfolio["Buy Price (USD)"]) * portfolio["Amount"]
    portfolio["Profit/Loss (%)"] = ((portfolio["Current Price (USD)"] - portfolio["Buy Price (USD)"]) / portfolio["Buy Price (USD)"]) * 100

    st.write("### Profit/Loss Summary", portfolio[["Crypto", "Buy Price (USD)", "Profit/Loss (USD)", "Profit/Loss (%)"]])
    total_profit_loss = portfolio["Profit/Loss (USD)"].sum()
    if total_profit_loss >= 0:
        st.success(f"📈 Total Profit: ${total_profit_loss:,.2f}")
    else:
        st.error(f"📉 Total Loss: ${total_profit_loss:,.2f}")

    # Pie Chart for Portfolio Distribution
    fig = px.pie(portfolio, names="Crypto", values="Total Value (USD)", title="Portfolio Distribution")
    st.plotly_chart(fig)

    # Portfolio Health Score
    num_assets = len(cryptos)
    volatility = portfolio["Current Price (USD)"].std()
    health_score = max(0, 100 - (volatility * 5 + num_assets * 10))
    st.write("### Portfolio Health Score")
    st.progress(int(health_score))

# Custom Backtesting
st.sidebar.header("📅 Custom Backtesting")
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")
if cryptos and start_date and end_date:
    hist_data = {crypto: yf.Ticker(crypto).history(start=start_date, end=end_date)["Close"] for crypto in cryptos}
    st.write(f"### Price History from {start_date} to {end_date}")
    st.line_chart(pd.DataFrame(hist_data))

# 🐋 **Whale Transactions**
st.sidebar.header("🐋 Whale Watcher")
if st.sidebar.button("Check Whale Transactions"):
    whale_api_url = "https://api.whale-alert.io/v1/transactions"
    api_key = "your_api_key"  # Replace with your valid API key

    headers = {"Authorization": f"Bearer {api_key}"}
    params = {"limit": 5}  # Fetch latest 5 transactions
    response = requests.get(whale_api_url, headers=headers, params=params)

    if response.status_code == 200:
        whale_data = response.json()
        transactions = whale_data.get("transactions", [])

        if transactions:
            st.write("### Recent Whale Transactions")
            for tx in transactions:
                symbol = tx.get("symbol", "Unknown")
                amount = tx.get("amount", 0)
                amount_usd = tx.get("amount_usd", 0)
                st.write(f"🔹 {amount} {symbol.upper()} moved worth ${amount_usd:,.2f}")
        else:
            st.warning("No whale transactions found.")
    else:
        st.error(f"❌ Error fetching whale transactions (Status Code: {response.status_code})")

# 📰 **Crypto News**
st.sidebar.header("📰 Crypto News")
news_api_key = "15acab4c6aff4853abe5ae351a0e13d8"  # Replace with your API key
news_api_url = f"https://newsapi.org/v2/everything?q=cryptocurrency&sortBy=publishedAt&language=en&apiKey={news_api_key}"

response = requests.get(news_api_url)
if response.status_code == 200:
    news_data = response.json()
    articles = news_data.get("articles", [])[:5]  # Get top 5 news articles

    if articles:
        for article in articles:
            st.sidebar.markdown(f"🔹 [{article['title']}]({article['url']})")
    else:
        st.sidebar.warning("No news articles found.")
else:
    st.sidebar.warning("Could not fetch news. Please check the API key or try again later.")

# 🎮 **Crypto Prediction Game**
st.sidebar.header("🎮 Crypto Prediction Game")
prediction = st.sidebar.radio("Where do you think BTC will be tomorrow?", ["Up", "Down", "Same"])
if st.sidebar.button("Submit Prediction"):
    st.sidebar.success("Prediction Submitted! Check tomorrow to see results.")

# 🚀 **Market Movers**
st.sidebar.header("🚀 Market Movers")
trending_api_url = "https://api.coingecko.com/api/v3/search/trending"
response = requests.get(trending_api_url)
if response.status_code == 200:
    trending_data = response.json()
    for coin in trending_data.get("coins", [])[:5]:
        name, symbol, price = coin["item"]["name"], coin["item"]["symbol"], coin["item"]["price_btc"]
        st.sidebar.write(f"🔥 {name} ({symbol.upper()}) - {price:.8f} BTC")
else:
    st.sidebar.warning("Could not fetch trending coins.")
