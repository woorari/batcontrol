#!/usr/bin/env python3
"""
Script to convert test data CSV to load_profile.csv format.

The test data has:
- Timestamp in format "dd.MM.yyyy HH:mm" (5-minute intervals)
- Energy consumption in Wh

The load_profile.csv needs:
- month (1-12)
- weekday (0-6, 0=Monday)
- hour (0-23)
- energy (average in Wh)
"""

import pandas as pd
import sys
from pathlib import Path
from datetime import datetime

def convert_test_data_to_load_profile(input_file: str, output_file: str):
    """
    Convert test data CSV to load_profile.csv format.
    
    Args:
        input_file: Path to input CSV file (test data)
        output_file: Path to output CSV file (load_profile.csv)
    """
    print(f"Reading input file: {input_file}")
    
    # Read the CSV file, skipping the first two header rows (column names and format info)
    df = pd.read_csv(input_file, skiprows=2, names=['timestamp_str', 'energy_wh'])
    
    # Parse the timestamp from German format "dd.MM.yyyy HH:mm"
    df['timestamp'] = pd.to_datetime(df['timestamp_str'], format='%d.%m.%Y %H:%M')
    
    # Extract month, weekday, and hour
    df['month'] = df['timestamp'].dt.month
    df['weekday'] = df['timestamp'].dt.dayofweek  # 0=Monday, 6=Sunday
    df['hour'] = df['timestamp'].dt.hour
    
    # Aggregate 5-minute values to hourly values by summing
    # Group by date, hour, month, weekday and sum the energy
    df_hourly = df.groupby([
        df['timestamp'].dt.date,
        'month',
        'weekday',
        'hour'
    ])['energy_wh'].sum().reset_index()
    
    # Calculate mean energy per month, weekday, hour combination
    load_profile_data = []
    for month in range(1, 13):
        for weekday in range(7):
            for hour in range(24):
                # Filter data for this combination
                filtered = df_hourly[
                    (df_hourly['month'] == month) &
                    (df_hourly['weekday'] == weekday) &
                    (df_hourly['hour'] == hour)
                ]
                
                if len(filtered) > 0:
                    energy = filtered['energy_wh'].mean()
                else:
                    # If no data available, use overall mean
                    energy = df_hourly['energy_wh'].mean()
                
                load_profile_data.append({
                    'month': month,
                    'weekday': weekday,
                    'hour': hour,
                    'energy': energy
                })
    
    # Create DataFrame and save
    df_load_profile = pd.DataFrame(load_profile_data)
    df_load_profile.to_csv(output_file, index=False)
    
    print(f"Created load profile: {output_file}")
    print(f"Total entries: {len(df_load_profile)}")
    print(f"Energy range: {df_load_profile['energy'].min():.2f} - {df_load_profile['energy'].max():.2f} Wh")
    print(f"Mean energy: {df_load_profile['energy'].mean():.2f} Wh")


if __name__ == '__main__':
    # Default paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    input_file = project_root / 'docs' / 'test data' / 'Rieck_01012025-31122025.csv'
    
    # Allow command line arguments
    if len(sys.argv) > 1:
        input_file = Path(sys.argv[1])
    
    if not input_file.exists():
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)
    
    # Generate output filename with timestamp if not provided
    if len(sys.argv) > 2:
        output_file = Path(sys.argv[2])
    else:
        # Create filename with timestamp: load_profile_dd_mm_yyyy.csv
        timestamp = datetime.now().strftime('%d_%m_%Y')
        output_file = project_root / 'config' / f'load_profile_{timestamp}.csv'
    
    # Create output directory if it doesn't exist
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    convert_test_data_to_load_profile(str(input_file), str(output_file))

