# Stocks-Analysis

The Stock Performance Dashboard aims to provide a comprehensive visualization and analysis of the Nifty 50 stocks' performance over the past year.

## Project Overview

This project consists of four main components:
1. Data extraction from Yaml format and transform into csv file
2. Data Analysis and visualization need to be done to filter the stocks based on their perfomance
3. Streamlit dashboard will show the top-perfoming and worst-performing stocks for the year
4. Powerbi dashboard will show the clear visualization to make the data easily accessible for users.

## Features

- **Interactive Filters**: Time period, sectors, individual stocks
- **Technical Analysis:**
    RSI (Relative Strength Index)
    MACD (Moving Average Convergence Divergence)
    Bollinger Bands
- **Comparative Analysis:**
    Correlation matrix
    Performance heatmaps
    Risk-return scatter plots

## Technologies Used

- Python 3.x
- Pandas (Data processing)
- Streamlit (Dashboard)
- Matplotlib/Seaborn (Visualization)
- Powerbi (Dashboard)


## Usage

### 1. Data extraction
Run the scraping script:
```bash
python convert.py
This will convert yaml data into csv files.
```
### 2. Combine and Clean Data
```bash
python combine.py
Creates combined_cleaned_file.csv with all stocks
```
### 3. Launch Dashboard
```bash
streamlit run stream.py
Access the interactive dashboard at http://localhost:8501
```
### 4 . Launch PowerbiDashboard
```bash
Attached the powerbi dashboard file.
```

## Dashboard Features


**1. Interactive Stock Explorer**
Multi-ticker comparison: Overlay up to 5 stocks on price charts
Timeframe selector: Daily/Weekly/Monthly views (1M/3M/1Y/5Y)
Sector filter: Isolate stocks by industry (Tech/Finance/Healthcare)

**2. Technical Analysis Toolkit**
Indicator toggles:
✅ 50-day & 200-day Moving Averages
✅ Bollinger Bands (±2σ)
✅ RSI with overbought(70)/oversold(30) markers
✅ MACD histogram + signal line crossover alerts

**3. Market Intelligence**
Heatmaps:
🔥 Real-time sector performance
🔥 Stock correlation matrix

