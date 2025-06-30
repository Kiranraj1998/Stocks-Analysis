import os
import yaml
import pandas as pd
from datetime import datetime

def parse_datetime_from_filename(filename):
    """Parse datetime from filename with format YYYY-MM-DD_HH-MM-SS.yaml"""
    try:
        # Remove .yaml/.yml extension
        base_name = filename.split('.')[0]
        # Split into date and time parts
        date_part, time_part = base_name.split('_')[:2]
        
        # Parse date (YYYY-MM-DD)
        date_obj = datetime.strptime(date_part, '%Y-%m-%d').date()
        
        # Parse time (HH-MM-SS) but we'll just take HH-MM
        hour, minute, _ = time_part.split('-')
        time_str = f"{int(hour)}:{int(minute)}"  # Removes leading zeros
        
        # Combine into final format: MM/DD/YYYY H:MM
        formatted_date = date_obj.strftime('%m/%d/%Y')
        datetime_str = f"{formatted_date} {time_str}"
        
        # Also create a datetime object for proper sorting
        datetime_obj = datetime.strptime(f"{date_part} {hour}:{minute}", "%Y-%m-%d %H:%M")
        return datetime_str, datetime_obj
        
    except Exception as e:
        raise ValueError(f"Filename '{filename}' doesn't match expected format: {str(e)}")

def yaml_to_csv(yaml_root_dir, output_dir):
    """Convert YAML stock data to CSV files organized by symbol"""
    os.makedirs(output_dir, exist_ok=True)
    stocks_data = {}
    total_files = processed_files = 0
    
    print(f"Processing YAML files from {yaml_root_dir}...")
    
    for date_folder in os.listdir(yaml_root_dir):
        date_folder_path = os.path.join(yaml_root_dir, date_folder)
        if not os.path.isdir(date_folder_path):
            continue
            
        print(f"Processing {date_folder}...")
        
        for yaml_file in os.listdir(date_folder_path):
            if not yaml_file.lower().endswith(('.yaml', '.yml')):
                continue
                
            total_files += 1
            file_path = os.path.join(date_folder_path, yaml_file)
            
            try:
                # Get formatted datetime from filename
                formatted_datetime, datetime_obj = parse_datetime_from_filename(yaml_file)
                
                # Load YAML data
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                
                if not data:
                    print(f"Warning: Empty YAML file {yaml_file}")
                    continue
                    
                # Process each stock entry
                for stock_entry in data:
                    symbol = stock_entry['Ticker']
                    if symbol not in stocks_data:
                        stocks_data[symbol] = []
                        
                    stocks_data[symbol].append({
                        'Date': formatted_datetime,
                        'open': stock_entry['open'],
                        'high': stock_entry['high'],
                        'low': stock_entry['low'],
                        'close': stock_entry['close'],
                        'volume': stock_entry['volume'],
                        'Ticker': symbol,
                        'SortDateTime': datetime_obj  # For sorting only
                    })
                    
                processed_files += 1
                
            except ValueError as e:
                print(f"Skipping {yaml_file}: {str(e)}")
            except Exception as e:
                print(f"Error processing {yaml_file}: {str(e)}")
    
    # Save each symbol's data to CSV
    for symbol, data in stocks_data.items():
        df = pd.DataFrame(data)
        # Sort by the datetime object (oldest to newest)
        df = df.sort_values('SortDateTime')
        # Remove the temporary sorting column
        df = df.drop('SortDateTime', axis=1)
        # Ensure correct column order
        df = df[['Date', 'open', 'high', 'low', 'close', 'volume', 'Ticker']]
        output_path = os.path.join(output_dir, f"{symbol}.csv")
        df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"Saved {symbol}.csv (sorted chronologically)")
    
    print("\nConversion Complete:")
    print(f"Processed {processed_files} of {total_files} files")
    print(f"Created {len(stocks_data)} stock CSV files in {output_dir}")

# Run the conversion
yaml_to_csv('yamldata', 'stocks_csv')