import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import plotly.express as px

# Set page config
st.set_page_config(layout="wide", page_title="Nifty 50 Stock Market Dashboard", page_icon="📈")

# Custom CSS for styling
st.markdown(
    """
    <style>
        .title {
            font-size:48px;
            font-weight:700;
            color:#00b4d8;
        }
        .subtitle {
            font-size:22px;
            color:#6c757d;
        }
        .footer {
            font-size:14px;
            color:gray;
            text-align:center;
            margin-top:40px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="title">📊 Nifty 50 Stock Market Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Interactive Visual Analytics for Informed Investing Decisions</div><br>', unsafe_allow_html=True)

@st.cache_data
def load_stock_data(csv_dir):
    stocks = {}
    for file in os.listdir(csv_dir):
        if file.endswith('.csv'):
            symbol = file.split('.')[0]
            df = pd.read_csv(os.path.join(csv_dir, file), parse_dates=['Date'])
            stocks[symbol] = df
    return stocks

@st.cache_data
def load_sector_data(sector_file):
    sector_df = pd.read_csv(sector_file)
    sector_df['Symbol'] = sector_df['Symbol'].str.split(':').str[-1].str.strip()
    return sector_df

@st.cache_data
def calculate_metrics(stocks, sector_df):
    results = {
        'yearly_returns': {}, 'volatility': {}, 'sector_returns': {},
        'daily_returns': {}, 'cumulative_returns': {}, 'monthly_returns': {}
    }

    for symbol, df in stocks.items():
        if len(df) < 2:
            continue
        df = df.sort_values('Date')
        df['daily_return'] = df['close'].pct_change()
        results['daily_returns'][symbol] = df[['Date', 'daily_return']]
        results['yearly_returns'][symbol] = (df.iloc[-1]['close'] - df.iloc[0]['close']) / df.iloc[0]['close']
        results['volatility'][symbol] = df['daily_return'].std()
        df['cumulative_return'] = (1 + df['daily_return']).cumprod() - 1
        results['cumulative_returns'][symbol] = df[['Date', 'cumulative_return']]
        df['month'] = df['Date'].dt.to_period('M')
        results['monthly_returns'][symbol] = df.groupby('month')['close'].apply(lambda x: (x.iloc[-1] - x.iloc[0]) / x.iloc[0])

    sector_mapping = sector_df.set_index('Symbol')['sector'].to_dict()
    sector_returns = {}
    for symbol, ret in results['yearly_returns'].items():
        sector = sector_mapping.get(symbol)
        if sector not in sector_returns:
            sector_returns[sector] = []
        sector_returns[sector].append(ret)
    results['sector_returns'] = {s: np.mean(r) for s, r in sector_returns.items()}
    return results

# Load data
csv_directory = 'stocks_csv'
sector_file = 'Sector_data.csv'
stocks = load_stock_data(csv_directory)
sector_df = load_sector_data(sector_file)
results = calculate_metrics(stocks, sector_df)

# Convert to DataFrames
yearly_returns_df = pd.DataFrame.from_dict(results['yearly_returns'], orient='index', columns=['Yearly Return'])
volatility_df = pd.DataFrame.from_dict(results['volatility'], orient='index', columns=['Volatility'])
sector_returns_df = pd.DataFrame.from_dict(results['sector_returns'], orient='index', columns=['Avg Return'])

# Tabs for dashboard
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Market Overview", "🏆 Top Performers", "🏭 Sector Performance",
    "⚡ Volatility", "📊 Correlation", "📉 Cumulative Returns"
])

with tab1:
    st.header("Market Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Total Stocks", len(stocks))
    green_stocks = (yearly_returns_df['Yearly Return'] > 0).sum()
    col2.metric("🟢 Green Stocks", green_stocks)
    red_stocks = (yearly_returns_df['Yearly Return'] <= 0).sum()
    col3.metric("🔴 Red Stocks", red_stocks)

with tab2:
    st.header("Top Performers")
    top_gainers = yearly_returns_df.nlargest(10, 'Yearly Return')
    top_losers = yearly_returns_df.nsmallest(10, 'Yearly Return')
    col1, col2 = st.columns(2)
    col1.write("**Top 10 Gainers**")
    col1.dataframe(top_gainers.style.format("{:.2%}").background_gradient(cmap="Greens"))
    col2.write("**Top 10 Losers**")
    col2.dataframe(top_losers.style.format("{:.2%}").background_gradient(cmap="Reds"))

with tab3:
    st.header("Sector-wise Performance")
    st.dataframe(sector_returns_df.style.format("{:.2%}").bar(subset=['Avg Return'], color=['#d65f5f', '#5fba7d']))
    fig = px.bar(sector_returns_df.reset_index(), x='Avg Return', y='index', orientation='h',
                 color='Avg Return', color_continuous_scale='Tealgrn', labels={'index': 'Sector'},
                 title="Average Yearly Return by Sector")
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.header("Volatility Analysis")
    top_volatile = volatility_df.nlargest(10, 'Volatility')
    st.dataframe(top_volatile.style.format("{:.4f}").background_gradient(cmap="Oranges"))
    fig = px.bar(top_volatile.reset_index(), x='Volatility', y='index', orientation='h',
                 title="Top 10 Most Volatile Stocks", color='Volatility',
                 color_continuous_scale='sunset')
    st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.header("Stock Correlation Matrix")
    returns_df = pd.DataFrame()
    for symbol, df in results['daily_returns'].items():
        if symbol in stocks:
            temp_df = df.set_index('Date')
            returns_df[symbol] = temp_df['daily_return']
    corr_matrix = returns_df.corr()
    fig, ax = plt.subplots(figsize=(16, 14))
    sns.heatmap(corr_matrix, annot=False, fmt=".2f", cmap='coolwarm', center=0, vmin=-1, vmax=1, ax=ax)
    ax.set_title("Stock Return Correlation Heatmap")
    st.pyplot(fig)

with tab6:
    st.header("Cumulative Returns Over Time")
    top_symbols = yearly_returns_df.nlargest(5, 'Yearly Return').index
    fig, ax = plt.subplots(figsize=(12, 6))
    for symbol in top_symbols:
        df = results['cumulative_returns'][symbol]
        ax.plot(df['Date'], df['cumulative_return'], label=symbol)
    ax.set_title("Cumulative Returns for Top 5 Performing Stocks")
    ax.set_ylabel("Cumulative Return")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

# Footer
st.markdown('<div class="footer">Made with ❤️ using Streamlit | Finance Data Analytics © 2025</div>', unsafe_allow_html=True)
