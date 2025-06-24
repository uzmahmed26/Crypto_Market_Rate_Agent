import streamlit as st
import requests

st.set_page_config(page_title="Crypto Market Agent", page_icon="💰")
st.title("💰 Crypto Market Rate Agent")

# Step 1: Popular coins dropdown + manual input
popular_symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'DOGEUSDT', 'SOLUSDT', 'XRPUSDT']
selected = st.selectbox("Choose a crypto symbol:", popular_symbols)
custom_symbol = st.text_input("Or enter a custom crypto symbol (e.g. ADAUSDT):")
symbol = custom_symbol.strip().upper() if custom_symbol else selected

# Step 2: Data fetch function
def get_crypto_data(symbol):
    base_url = "https://api.binance.com/api/v3/ticker"
    try:
        # Price
        price_url = f"{base_url}/price?symbol={symbol}"
        price_res = requests.get(price_url).json()

        # 24hr stats
        stats_url = f"{base_url}/24hr?symbol={symbol}"
        stats_res = requests.get(stats_url).json()

        return {
            "price": float(price_res["price"]),
            "change": float(stats_res["priceChangePercent"]),
            "high": float(stats_res["highPrice"]),
            "low": float(stats_res["lowPrice"])
        }

    except Exception as e:
        return None

# Step 3: On button click
if st.button("🔍 Get Price"):
    if symbol:
        with st.spinner("Fetching data..."):
            data = get_crypto_data(symbol)
            if data:
                st.success(f"📊 Current data for {symbol}:")
                st.metric("💵 Price (USDT)", f"${data['price']:,.2f}")
                st.metric("📈 24h Change", f"{data['change']}%", delta_color="inverse")
                st.metric("🔺 24h High", f"${data['high']:,.2f}")
                st.metric("🔻 24h Low", f"${data['low']:,.2f}")
            else:
                st.error("⚠️ Invalid symbol or API issue. Please try again.")
    else:
        st.warning("Please enter or select a crypto symbol.")
