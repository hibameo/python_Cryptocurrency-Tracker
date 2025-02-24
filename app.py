import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Streamlit App Title
st.title("📊 Cryptocurrency Tracker")

# Get Data from CoinGecko API
api_url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 10,
    "page": 1,
    "sparkline": False
}

response = requests.get(api_url, params=params)
data = response.json()

# Convert Data to DataFrame
df = pd.DataFrame(data, columns=["id", "name", "symbol", "current_price", "market_cap", "total_volume"])
df.set_index("symbol", inplace=True)

# Show Data
st.subheader("📌 Current Market Prices")
st.dataframe(df)

# Select Coin for Visualization
coin_symbol = st.selectbox("Select a Cryptocurrency:", df.index)
coin_id = df.loc[coin_symbol]["id"]  # Get the correct CoinGecko ID

# Fetch Historical Data
hist_url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
hist_params = {"vs_currency": "usd", "days": "7", "interval": "daily"}
hist_response = requests.get(hist_url, params=hist_params)

# Check API Response
if hist_response.status_code == 200:
    hist_data = hist_response.json()
    
    # ✅ Check if "prices" exists in API response
    if "prices" in hist_data:
        prices = pd.DataFrame(hist_data["prices"], columns=["timestamp", "price"])
        prices["timestamp"] = pd.to_datetime(prices["timestamp"], unit="ms")

        # Plot Chart
        st.subheader(f"📈 {coin_symbol.upper()} Price Trend (Last 7 Days)")
        fig = px.line(prices, x="timestamp", y="price", title=f"{coin_symbol.upper()} Price Over Time")
        st.plotly_chart(fig)
    else:
        st.error("🚨 Error: 'prices' key not found in API response!")
        st.json(hist_data)  # Print API response for debugging
else:
    st.error(f"🚨 API request failed! Status Code: {hist_response.status_code}")
