import pandas as pd
import os

# Load sector data (ensure your sector CSV has columns: 'Symbol' and 'sector')
sector_df = pd.read_csv('Sector_data.csv')
sector_df['Symbol'] = sector_df['Symbol'].str.split(':').str[-1].str.strip()  # Clean symbols

# Combine all stock CSVs with sector info
all_data = []
for file in os.listdir('stocks_csv'):
    if file.endswith('.csv'):
        ticker = file.split('.')[0]
        df = pd.read_csv(os.path.join('stocks_csv', file))
        
        # Get sector or assign 'Unknown'
        sector_match = sector_df[sector_df['Symbol'] == ticker]
        df['Sector'] = sector_match['sector'].values[0] if not sector_match.empty else 'Unknown'
        df['Ticker'] = ticker
        
        all_data.append(df)

# Combine and save
pd.concat(all_data).to_csv('stocks_with_sectors.csv', index=False)
print(f"Combined {len(all_data)} files with sector data")