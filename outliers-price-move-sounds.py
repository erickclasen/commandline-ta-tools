import pandas as pd
import sys

def find_outliers(asset, file_time_format):
    # Map asset names to CSV column indexes based on your format
    asset_columns = {
        'BTC': 1, 'DOGE': 2, 'ETH': 3, 'FET': 4, 'ICP': 5,
        'LTC': 6, 'QNT': 7, 'SOL': 8, 'GRT': 9
    }
    
    # Ensure valid asset and file format inputs
    if asset not in asset_columns:
        print("Error: Invalid asset '{asset}'.",asset)
        sys.exit(1)
    
    # Construct filename from file_time_format
    filename = file_time_format+"-prices.csv"
    
    # Read the CSV file
    try:
        data = pd.read_csv(filename, header=None)
    except FileNotFoundError:
        print("Error: File '{filename}' not found.",filename)
        sys.exit(1)
    
    # Extract the column corresponding to the asset
    asset_col_index = asset_columns[asset]
    prices = data.iloc[:, asset_col_index]
    
    # Calculate the price deltas (difference between consecutive prices)
    price_deltas = prices.diff().dropna()  # drop the first NaN value caused by diff()
    
    # Calculate the 2.5th and 97.5th percentiles of price deltas
    lower_bound = price_deltas.quantile(0.025)
    upper_bound = price_deltas.quantile(0.975)
    
    # Filter outliers: those that are below the lower bound or above the upper bound
    outliers = price_deltas[(price_deltas < lower_bound) | (price_deltas > upper_bound)]
    
    if not outliers.empty:
        # Print the timestamps, price deltas, and corresponding percent changes for outliers
        print("Outliers in price changes for {asset} in {file_time_format} file:",asset,file_time_format)
        for index, delta in outliers.items():
            timestamp = data.iloc[index, 0]  # Get the timestamp from the first column
            previous_price = prices.iloc[index - 1]  # Get the previous price
            current_price = prices.iloc[index]  # Get the current price
            percent_change = (delta / previous_price) * 100  # Percent change from previous price
            # Print the output with rounded values
            print(timestamp,": Price = ",current_price,", Price Change = ",delta,", (Change: ",percent_change,"%)")
    else:
        print("No outliers found in price changes for {asset} in {file_time_format} file.",asset,file_time_format)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python find_outliers.py <asset> <file_time_format>")
        sys.exit(1)
    
    asset = sys.argv[1].upper()  # Asset name (e.g., BTC)
    file_time_format = sys.argv[2].lower()  # Time format (e.g., hourly, four-hour, daily, weekly)
    
    find_outliers(asset, file_time_format)

'''
        # Print out the stats for the last 1000
        if ch != 'O' and date_ct > len(lines)-1000:
                print(d,"     ",date_ct,lines[n-1], lines[n],ch)
                if ch == 'D':
                        os.system("aplay /home/erick/Music/birds/m*wav")
                elif ch == 'U':
                        os.system("aplay /home/erick/Music/birds/killdeer_song-Mike_Koenig-1144525481.wav")
                else:
                        raise Exception("TRAP: Bad character. Not U, O or D.")
'''
