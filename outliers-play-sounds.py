#!/usr/bin/python3
import os
import sys
import csv
from datetime import datetime

def find_outliers(asset, file_time_format):
    # Map asset names to CSV column indexes based on your format
    asset_columns = {
        'BTC': 1, 'DOGE': 2, 'ETH': 3, 'FET': 4, 'ICP': 5,
        'LTC': 6, 'QNT': 7, 'SOL': 8, 'GRT': 9
    }

    # Ensure valid asset and file format inputs
    if asset not in asset_columns:
        print("Error: Invalid asset '%s'." % asset)
        sys.exit(1)

    # Construct filename from file_time_format
    filename = file_time_format + "-prices.csv"

    # Read the CSV file
    try:
        with open(filename, newline='') as csvfile:
            data = list(csv.reader(csvfile))
    except FileNotFoundError:
        print("Error: File '%s' not found." % filename)
        sys.exit(1)

    # Extract the relevant asset prices
    asset_col_index = asset_columns[asset]
    prices = []
    timestamps = []

    for row in data[1:]:  # Assuming the first row is a header, skip it
        try:
            price = float(row[asset_col_index])
            timestamp = row[0]
            prices.append(price)
            timestamps.append(timestamp)
        except (IndexError, ValueError):
            continue

    if len(prices) < 2:
        print("Not enough data to calculate deltas.")
        sys.exit(1)

    # Calculate the price deltas (differences between consecutive prices)
    price_deltas = [prices[i] - prices[i - 1] for i in range(1, len(prices))]

    # Calculate the 2.5th and 97.5th percentiles of price deltas
    sorted_deltas = sorted(price_deltas)
    lower_bound = sorted_deltas[int(0.025 * len(sorted_deltas))]
    upper_bound = sorted_deltas[int(0.975 * len(sorted_deltas))]

    # Find and process outliers
    outliers_found = False
    for i, delta in enumerate(price_deltas):
        if delta < lower_bound or delta > upper_bound:
            outliers_found = True
            timestamp = timestamps[i + 1]  # The current timestamp corresponds to delta[i]
            previous_price = prices[i]
            current_price = prices[i + 1]
            percent_change = (delta / previous_price) * 100

            # Print the output with rounded values
            print("%s: Price = %.5f, Price Change = %.5f, (Change: %.2f%%)" % (
                timestamp, current_price, delta, percent_change))

            # Compare timestamp with system clock to determine if it's recent
            timestamp_dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")  # Parse the timestamp
            time_diff = datetime.now() - timestamp_dt

            # Play sounds if the move is recent (within the last minute)
            if time_diff.total_seconds() <= 60:
                if delta > 0:
                    os.system("aplay /home/erick/Music/birds/killdeer_song-Mike_Koenig-1144525481.wav")
                elif delta < 0:
                    os.system("aplay /home/erick/Music/birds/m*wav")

    if not outliers_found:
        print("No outliers found in price changes for %s in %s file." % (asset, file_time_format))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python find_outliers.py <asset> <file_time_format>")
        sys.exit(1)

    asset = sys.argv[1].upper()  # Asset name (e.g., BTC)
    file_time_format = sys.argv[2].lower()  # Time format (e.g., hourly, four-hour, daily, weekly)

    find_outliers(asset, file_time_format)

