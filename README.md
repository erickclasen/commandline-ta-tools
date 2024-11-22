# commandline-ta-tools
Pulls data from CoinGecko on an hourly basis and provides text output and graphing tools that run from the command line.
## How it works
This code is meant to run on csv files that are created by running cg-current-prices.py hourly via CRON. This will create hourly-prices.csv.
EX: ```0 * * * * python3 /home/erick/python/ta/cg-current-prices.py > /home/erick/python/ta/cg-prices.log```

At midnight + 1 minute daily a CRON script can run that gets the tail of hourly-prices.csv and makes daily-prices.csv. CRON at midnight +1 minute on Sunday can get weekly-prices.csv
TBD: I will put up some data for this, via push???.
EX:  
```1 0 * * * tail -1 /home/erick/python/ta/hourly-prices.csv >> /home/erick/python/ta/daily-prices.csv ```

```1 0 * * SUN tail -1 /home/erick/python/ta/daily-prices.csv >> /home/erick/python/ta/weekly-prices.csv ```
Also there is a four hour tick as well, much of this code can be called to use the four hour prices. Here is the example line for CRON

```1 0,4,8,12,16,20 * * * tail -1 /home/erick/python/ta/hourly-prices.csv >> /home/erick/python/ta/four-hour-prices.csv```


When there is enough data the code will run by using the *-prices.csv files
For example buy-zone.py will use weekly only, others will use other timeframes and options.

The CSV files contain 9 currencies: 'BTC': 1, 'DOGE': 2, 'ETH': 3, 'FET': 4, 'ICP': 5,'LTC': 6, 'QNT': 7, 'SOL': 8, 'GRT': 9
I picked these based on what I was interested in at the time when I created this code out of the old Coinbase PRO API Code.... https://github.com/erickclasen/cbpro-cli-tools

### Index
There is also an Index that is created by normalizing against the prices of these currencies. Examine index-scaler.py for how the math to create the index works.

## The following are the descriptions and usage for code
## buy-zone.py
### Description

This Python script analyzes cryptocurrency price data, focusing on Bitcoin (BTC) and Ethereum (ETH) using weekly data due to limited historical data from CoinGecko. The script supports price analysis based on multiple technical indicators like moving averages, standard deviations, and 4-year cycle trends. It also calculates Mayer Multiple, Kijun, and other price targets for both short-term and long-term decision-making.

The script offers flexibility with daily or weekly price charts (when available) and performs linear regression for long-term trend forecasting.

### Usage

From the command line, the script accepts arguments for currency, timeframe, and chart type:

```bash
python3 script.py <currency> <timeframe> <chart_type>
```

- `<currency>`: The cryptocurrency symbol, e.g., BTC, ETH.
- `<timeframe>`: The number of weeks to display in the analysis (minimum: 208 weeks).
- `<chart_type>`: Either 'D' for daily or 'W' for weekly charting (daily not available until 2028).

#### Example

To run an analysis for Bitcoin over a 208-week timeframe using weekly data:

```bash
python3 script.py BTC 208 W
```
## candles.py
This Python script is designed to perform technical analysis on cryptocurrency data using various financial indicators such as RSI (Relative Strength Index), ROC (Rate of Change), and OBV (On-Balance Volume). It allows for flexible input through command-line arguments, enabling users to specify the cryptocurrency, time frame, and desired indicator.

The script reads in daily price data from a CSV file and calculates technical indicators, offering several features:
- **Command-line argument parsing**: It accepts inputs for the cryptocurrency symbol, time frame, and indicator type (e.g., RSI, ROC).
- **Financial calculations**: Functions are provided for calculating ROC, OBV, and RSI.
- **Statistical analysis**: The script can print basic price statistics and Fibonacci-based statistics on the price data.
- **Plotting**: Candlestick charts are generated using `mplfinance`, and additional plots are added for the chosen technical indicator.
- **CSV output**: The script also logs the statistical results to a CSV file.

### Usage

You can run this script from the command line to perform technical analysis on cryptocurrency data. The script requires Python 3 and the necessary libraries (`matplotlib`, `pandas`, `numpy`, `mplfinance`, `scikit-learn`, etc.) to be installed.

#### Command Syntax

```bash
python3 script.py <currency> <timeframe> <indicator>
```

#### Arguments

1. **`<currency>`**:  
   The cryptocurrency symbol you want to analyze (e.g., `BTC`, `ETH`).  
   **Example**: `BTC`

2. **`<timeframe>`**:  
   The number of days to include in the analysis.  
   **Example**: `365`

3. **`<indicator>`**:  
   The technical indicator to plot or analyze. Options include:
   - `RSI`: Relative Strength Index
   - `ROC`: Rate of Change
   - `STATS`: Generate and save statistical data without plotting indicators

   **Note**: The script currently supports `RSI` and `ROC` for subplot indicators. The `STATS` option allows you to generate statistical summaries without additional plots.

   **Example**: `RSI`

#### Examples

1. **Basic Usage with RSI Indicator**

   To analyze Bitcoin (`BTC`) over the past 365 days and plot the RSI indicator:

   ```bash
   python3 script.py BTC 365 RSI
   ```

2. **Specify a Different Timeframe with ROC Indicator**

   To analyze Ethereum (`ETH`) over the past 730 days and plot the ROC indicator:

   ```bash
   python3 script.py ETH 730 ROC
   ```

3. **Generate Statistics Without Plotting Indicators**

   To generate statistical data for Litecoin (`LTC`) over the past 500 days without plotting any technical indicators:

   ```bash
   python3 script.py LTC 500 STATS
   ```

#### Detailed Steps

1. **Prepare the Data:**

   Ensure you have the OHLC (Open, High, Low, Close) CSV file for the desired cryptocurrency. The CSV file should be named in the format `<currency>-ohcl.csv` (e.g., `BTC-ohcl.csv`) and contain a `Date` column for proper indexing.

2. **Run the Script:**

   Use the command syntax provided above to execute the script with your chosen parameters.

3. **View the Output:**

   - **Plots**: If an indicator (`RSI` or `ROC`) is specified, the script will display a candlestick chart with the selected technical indicator in a subplot.
   - **Statistics**: If `STATS` is chosen as the indicator, the script will print statistical summaries to the console and append them to a `stats.csv` file for future reference.

4. **Interpreting the Results:**

   - **Candlestick Chart**: Visualize price movements along with the selected technical indicator to identify trends and potential trading signals.
   - **Statistical Data**: Review metrics such as average price, standard deviation, Fibonacci levels, and return ratios to inform your trading strategy.

#### Additional Notes

- **Dependencies**: Ensure all required Python libraries are installed. You can install missing libraries using `pip`. For example:

  ```bash
  pip install matplotlib pandas numpy mplfinance scikit-learn
  ```

- **Data Integrity**: The script assumes that the CSV files are correctly formatted and contain the necessary columns. Verify your data files to prevent errors during execution.

- **Extensibility**: The script is designed to be easily extendable. You can add more technical indicators or modify existing ones as needed for your analysis.

#### Example Workflow

1. **Download or Prepare Data:**

   Obtain the OHLC data for your chosen cryptocurrency and save it as `<currency>-ohcl.csv`.

2. **Run the Script:**

   ```bash
   python3 script.py BTC 365 RSI
   ```

3. **Analyze the Output:**

   - View the generated candlestick chart with RSI subplot.
   - Check the console for statistical summaries.
   - If `STATS` was used, review the appended `stats.csv` for historical analysis.

This script provides a comprehensive tool for cryptocurrency traders and analysts to perform technical analysis, visualize trends, and make informed trading decisions based on historical data and key financial indicators.

## cg-current-prices.py

### Summary of the Cryptocurrency Price Fetching Script

This Python script retrieves live cryptocurrency prices from the CoinGecko API and appends them to a CSV file.

**Key Components:**

1. **Imports and Setup**:
   - Uses libraries like `requests`, `csv`, `json`, and `datetime`.
   - Defines global variables for file paths, retry limits, and delays.

2. **Functions**:
   - `live_dict_read()`: Reads a JSON file containing live values; creates it if missing.
   - `live_dict_write(live_dict)`: Saves the current state of the live dictionary to a JSON file.
   - `output_price_csv(out_list)`: Appends price data to a specified CSV file.
   - `get_crypto_prices(coin_ids)`: Fetches current cryptocurrency prices with retry logic for connection issues.

3. **Main Execution**:
   - Initializes an output list and defines a list of cryptocurrency IDs.
   - Fetches prices, prints them, and appends the results to the output list.
   - Saves the timestamp and prices to the CSV file.

### Usage
1. Ensure Python and the `requests` library are installed.
2. The file is cg-current-prices.py
3. Run it using the command:
   ```bash
   python3 cg-current-prices.py
   ```
4. Check the specified CSV file for the collected prices. 

This script automates the process of gathering cryptocurrency prices for analysis or trading strategies. Called via CRON on an hourly basis
EX: 
``` 0 * * * * python3 /home/erick/python/ta/cg-current-prices.py > /home/erick/python/ta/cg-prices.log ```

## cg-to-ohcl.py
### Summary of the OHLC Data Processing Script (`cg-to-ohcl.py`)

This Python script processes cryptocurrency price data, calculates Open, High, Low, Close (OHLC) values, and exports the results to a CSV file. It utilizes live price data obtained from an external module.

**Key Components:**

1. **Imports and Setup**:
   - Uses libraries like `numpy`, `sys`, `os`, `datetime`, and `csv`.
   - Defines an `index_scaler` dictionary to normalize prices for various cryptocurrencies.

2. **Functions**:
   - `parse_arguments()`: Parses command-line arguments to retrieve the cryptocurrency currency code (e.g., BTC, ETH) provided by the user.

3. **Main Execution**:
   - Initializes empty lists for OHLC values, dates, and price data.
   - Imports live data using a core module (`coretamodule`).
   - Reads price data from a CSV file specified by the `ticker_filename`.
   - Calculates the number of days from a start date and maps offsets for date handling.
   - Loops through the price data to extract OHLC values for 24-hour periods:
     - **High (H)**: Maximum price within the period.
     - **Low (L)**: Minimum price within the period.
     - **Open (O)**: Price at the start of the period.
     - **Close (C)**: Price at the end of the period.
   - Formats dates and appends them to a list for CSV output.
   - Writes the results to a new CSV file named according to the currency label, including headers and the calculated OHLC data.

### Usage
1. Ensure Python is installed with access to the required libraries (`numpy`, `sys`, `os`, `csv`, and `datetime`).
2. Save the script as `cg-to-ohcl.py`.
3. Run it from the command line with the desired currency as an argument:
   ```bash
   python3 cg-to-ohcl.py BTC
   ```
4. The script will generate a CSV file named `BTC-ohcl.csv` (or for another specified currency) containing the OHLC data.

This script is designed for users needing to analyze cryptocurrency price movements in a structured format suitable for further analysis or visualization.

## coretamodule.py
Here's a summary of the `coretamodule.py` file:

### Summary of `coretamodule.py`

**Purpose:**  
`coretamodule.py` is a Python module designed for technical analysis in cryptocurrency algorithmic trading, utilizing the Coinbase Pro API. It centralizes common functions to improve code readability and maintainability across various trading scripts.

**Key Features:**

- **Technical Analysis Functions:** 
  - Implements several indicators such as Relative Strength Index (RSI), Exponential Moving Average (EMA), Simple Moving Average (SMA), and Efficiency Ratio.
  - Functions for assessing price trends (e.g., persistence of trends) and handling moving averages.

- **Data Handling Functions:**
  - Includes methods to read asset prices from CSV files and to check available assets in the user's Coinbase Pro account.
  - Functions for reading portfolio sizes and Ichimoku trading states from JSON files.

- **Modularity and Usability:**
  - Designed to be imported and used in other Python scripts.
  - Supports legacy code while providing updates to ensure compatibility with newer implementations.


Overall, this module serves as a foundational tool for implementing and testing trading strategies based on technical analysis in the cryptocurrency market. It supports the other Python code in
the directory.

## dca-in-out-manual-limits.py
### Summary of `dca-in-out-manual-limits.py`

This Python script is designed for analyzing and visualizing cryptocurrency price data using various time frames. It utilizes linear regression to predict future price movements and includes features for calculating key financial metrics, such as simple moving averages (SMA) and Fibonacci retracement levels. The script can process data from different time intervals (hourly, daily, weekly) based on user input and applies an index scaling to normalize prices against a specified currency or underlying asset.

### Key Components

1. **Imports and Initial Setup**:
   - The script imports necessary libraries such as NumPy, sys, and os, and it uses custom modules (`coretamodule` for data handling and `statsmod` for statistical functions).
   - It defines an index scaler dictionary for various cryptocurrencies.

2. **Argument Parsing**:
   - The `parse_arguments` function handles command-line arguments for currency, time frame, and chart type (daily, hourly, or weekly).
   - It validates the input and assigns default values when needed.

3. **Data Loading**:
   - Based on the specified timeframe, it selects the appropriate CSV file containing price data.
   - It reads the data into a list of dictionaries.

4. **Price Calculation**:
   - If the specified currency is "INDEX," it computes normalized prices using the index scaler.
   - Otherwise, it extracts the price of the specified currency and divides by the underlying asset’s price.

5. **Data Preparation for Regression**:
   - It prepares x-values and y-values for regression analysis and reshapes them for compatibility with sklearn.
   - It also extracts subsets of the data for multi-regression (last 20 and 50 entries).

6. **Statistical Analysis**:
   - It calculates key financial metrics, such as the minimum and maximum prices over the last year, Fibonacci levels, and simple moving averages.

7. **Fractal Detection**:
   - The script identifies up and down fractals based on historical price data to assist in setting stop-loss levels.

8. **Plotting (commented out)**:
   - Although the plotting functionality is included, it is currently commented out. The script can visualize the regression results and historical prices if uncommented.

### Usage

To use the script, you will need to execute it from the command line with appropriate arguments. Here’s the syntax:

```bash
python dca-in-out-manual-limits.py <currency> [<timeframe>] [<D/H/W>]
```

**Parameters**:
- `<currency>`: The cryptocurrency to analyze (e.g., BTC, ETH).
- `<timeframe>` (optional): The number of days for which to fetch the price data (default is 365).
- `<D/H/W>` (optional): Specifies whether to use daily ('D'), hourly ('H'), or weekly ('W') data (default is daily).

### Example Command

```bash
python dca-in-out-manual-limits.py BTC 90 D
```

This command analyzes the Bitcoin price for the last 90 days using daily data. The script will output the calculated metrics and findings to the console.


## ichimoku.py -- Supports run.py

The `ichimoku.py` code is designed to calculate and visualize the Ichimoku Cloud indicator, a technical analysis tool used in trading to identify trends, support, and resistance levels. Here’s a brief description of its key components and functionalities:

### Overview
- **Class Definition**: The main class, `Ichimoku`, takes a DataFrame (`ohcl_df`) containing OHLC (Open, High, Low, Close) data and provides methods to compute the Ichimoku indicator components and plot them alongside price data.

### Key Features
1. **Initialization**:
   - The `__init__` method accepts an OHLC DataFrame, which must contain specific columns (Date, Open, High, Close, Low).

2. **Indicator Calculation** (`run` method):
   - Calculates five main components of the Ichimoku indicator:
     - **Tenkan-sen**: The short-term moving average over 20 periods.
     - **Kijun-sen**: The medium-term moving average over 60 periods.
     - **Senkou Span A**: The average of the Tenkan-sen and Kijun-sen, plotted 30 periods ahead.
     - **Senkou Span B**: The long-term moving average over 120 periods, plotted 30 periods ahead.
     - **Chikou Span**: The current closing price, plotted 30 periods back.
   - Extends the DataFrame with additional dates to accommodate future plotting of the cloud.

3. **Plotting Methods**:
   - **`plot_ichi`**: Creates a plot of the Ichimoku Cloud indicator with candlesticks, showing the Tenkan-sen, Kijun-sen, Senkou Span A, and Senkou Span B.
   - **`plot_candlesticks`**: Plots the price data as candlesticks (though the specific candlestick plotting code is commented out).
   - **`plot_channels`**: Adds additional price channels based on rolling highs and lows.
   - **`pretty_plot`**: Formats the plot with a specific aesthetic, including colors and labels.
   - Additional plotting methods are provided for Bollinger Bands and stop-loss channels.

4. **Graphical Enhancements**:
   - Customizes plot aesthetics with background colors, grid styles, axis colors, and title formatting.

5. **Extensibility**: 
   - The class provides hooks for adding more analytical methods (e.g., Bollinger Bands and stop-loss plotting) to enhance trading decision-making.

### Conclusion
Overall, this `ichimoku.py` module provides a structured way to compute and visualize the Ichimoku Cloud, making it easier for traders to analyze market trends and make informed decisions based on historical price data.

## index-scaler.py - A utility to generate the index scaler.
Here's a concise summary of the `index-scaler.py` code:

---

### Summary of `index-scaler.py`

This script calculates an index value for a set of cryptocurrencies by determining the reciprocal of their prices and applying a scaling factor based on the number of currencies included. 

1. **Data Initialization**: The script initializes a dictionary (`price_dict`) with current cryptocurrency prices.

2. **Dictionary Length**: It prints the length of the dictionary to assess how many cryptocurrencies are being evaluated.

3. **Reciprocal Calculation**:
   - It creates a new dictionary (`new_dict`) that stores the reciprocal of each cryptocurrency price, scaled by the total number of currencies.
   - The base prices are printed for reference.

4. **Index Value Calculation**:
   - The script calculates the index value by summing the products of each cryptocurrency's price and its corresponding reciprocal.
   - A sanity check is performed to verify that the index value approximates 1, indicating a correctly calculated index.

5. **Output**: The script prints the number of currencies and the resulting index value for verification.

---

This script can be useful for constructing an index that reflects the combined value of a basket of cryptocurrencies, facilitating easier analysis of price movements in the overall market.

## linr-sk-fractals.py

Here's a summary and usage for the `linr-sk-fractals.py` file:

### Summary
The `linr-sk-fractals.py` script is a Python program designed to analyze cryptocurrency price data using linear regression and fractal analysis. It retrieves price data from CSV files, applies scaling factors to the prices based on a predefined index, and performs linear regression on the price data. The script calculates simple moving averages (SMA) and standard deviations to identify potential buy/sell signals based on price trends. Additionally, it identifies fractal points in the price history, which can help in setting trading stops. The program also allows users to specify different timeframes (daily, hourly, or weekly) and currencies.

### Key Components
- **Index Scaling**: The script uses predefined scaling factors for various cryptocurrencies.
- **Command-Line Arguments**: It accepts parameters for currency, timeframe, and type of subplot (daily, hourly, or weekly).
- **Data Handling**: It reads price data from CSV files based on the specified timeframe.
- **Linear Regression**: Implements linear regression to analyze price trends.
- **Fractal Detection**: Identifies up and down fractals in the price data to assist in trading decisions.
- **Statistical Analysis**: Computes simple moving averages and standard deviations for trend analysis.

### Usage
To run the script, use the following command in your terminal:

```bash
python3 linr-sk-fractals.py <currency> <timeframe> <D/H/W>
```

- `<currency>`: The cryptocurrency symbol (e.g., `BTC`, `ETH`, etc.).
- `<timeframe>`: The number of periods to analyze (e.g., `100` for the last 100 data points).
- `<D/H/W>`: The type of data to plot (D for daily, H for hourly, W for weekly).

### Example
To analyze Bitcoin prices over the last 100 daily data points, you would run:

```bash
python3 linr-sk-fractals.py BTC 100 D
```

### Notes
- Ensure that the required CSV files (`hourly-prices.csv`, `four-hour-prices.csv`, `daily-prices.csv`, `weekly-prices.csv`) are located in the specified path (`/home/erick/python/ta/`).
- The script also requires the `coretamodule` and `statsmod` modules for data handling and statistical calculations, respectively. Make sure these modules are available in your Python environment.

## linr-sk.py - came before linr-sk-fractals.py
Here's a brief summary of the provided Python script:

### Summary

The script is designed for financial data analysis and visualization, specifically focusing on cryptocurrencies. It performs the following key functions:

1. **Argument Parsing**: The script accepts command-line arguments for the currency, time frame, and plotting type (hourly, daily, weekly, or four-hour).

2. **Index Scaling**: It uses predefined scaling factors for different cryptocurrencies to normalize their prices.

3. **Data Loading**: It loads price data from CSV files based on the specified time frame.

4. **Currency Handling**: It differentiates between regular currencies and an index, applying appropriate scaling and calculating prices.

5. **Data Preparation**: It prepares the data for regression analysis by creating sequential x-values and reshaping the y-values for linear regression.

6. **Linear Regression**: It performs linear regression using the `scikit-learn` library to predict price movements over the specified time frame.

7. **Fractal Analysis**: The script identifies and plots up and down fractals based on historical price data to assist in potential trading decisions.

8. **Plotting**: It visualizes the true data and predictions using `matplotlib`, plotting the regression lines and fractal points, and saves the figure to a specified path.

This script integrates data analysis and visualization to assist users in understanding cryptocurrency price trends and making informed decisions.



## outliers-play-sounds.py

### Summary

The script `outliers-play-sounds.py` is designed to identify price outliers for a specified cryptocurrency asset from a CSV file containing price data. It calculates price changes (deltas) between consecutive price entries, determines the 2.5th and 97.5th percentiles of these changes to identify outliers, and plays specific sound alerts for recent significant price movements.

### Key Functions

- **find_outliers(asset, file_time_format)**: Main function that:
  - Validates the asset name and constructs the filename based on the provided time format.
  - Reads price data from a corresponding CSV file.
  - Calculates price deltas and identifies outliers based on the calculated percentiles.
  - Prints out details of outlier prices and plays a sound if the outlier is detected within the last minute.

### Usage

To run the script, execute the following command in the terminal:

```bash
python outliers-play-sounds.py <asset> <file_time_format>
```

- `<asset>`: The cryptocurrency asset name (e.g., BTC, DOGE).
- `<file_time_format>`: The time interval for the data file (e.g., hourly, four-hour, daily, weekly).

#### Example

```bash
python outliers-play-sounds.py BTC hourly
```

This command checks for outliers in the hourly price data for Bitcoin (BTC). The corresponding CSV file expected would be named `hourly-prices.csv`. If any price changes qualify as outliers, the script outputs the relevant data and plays sounds for recent significant movements.


## outliers-price-moves-3.4.py

### Summary

The script `outliers-price-moves-3.4.py` is designed to identify significant price movements (outliers) for specified cryptocurrency assets from a CSV file containing price data. It calculates the price changes (deltas) between consecutive prices, determines the 2.5th and 97.5th percentiles of these changes to identify outliers, and outputs relevant information about any identified outliers.

### Key Functions

- **find_outliers(asset, file_time_format)**: Main function that:
  - Validates the asset name and constructs the filename based on the provided time format.
  - Reads price data from the corresponding CSV file.
  - Calculates price deltas and identifies outliers based on the calculated percentiles.
  - Prints out details of any outlier prices, including timestamps and percentage changes.

### Usage

To run the script, execute the following command in the terminal:

```bash
python outliers-price-moves-3.4.py <asset> <file_time_format>
```

- `<asset>`: The cryptocurrency asset name (e.g., BTC, DOGE).
- `<file_time_format>`: The time interval for the data file (e.g., hourly, four-hour, daily, weekly).

#### Example

```bash
python outliers-price-moves-3.4.py BTC hourly
```

This command checks for outliers in the hourly price data for Bitcoin (BTC). The corresponding CSV file expected would be named `hourly-prices.csv`. If any price changes qualify as outliers, the script outputs the relevant data, including timestamps, price changes, and percentage changes. If no outliers are found, it will notify the user accordingly.

## outliers-price-move-sounds.py

### Summary

The `outliers-price-move-sounds.py` script identifies significant price changes (outliers) for specified cryptocurrency assets from a CSV file. It calculates the price deltas (differences between consecutive prices) using the Pandas library, determines the 2.5th and 97.5th percentiles to filter outliers, and outputs the details of any identified outliers. The script is designed to play specific sounds when outliers are detected, based on the direction of the price change (upward or downward).

### Key Functions

- **find_outliers(asset, file_time_format)**: 
  - Validates the asset name and constructs the filename based on the time format.
  - Reads price data from the corresponding CSV file using Pandas.
  - Calculates price changes (deltas) and identifies outliers based on the calculated percentiles.
  - Outputs relevant details about the outliers, including timestamps and percentage changes.

### Usage

To run the script, execute the following command in the terminal:

```bash
python outliers-price-move-sounds.py <asset> <file_time_format>
```

- `<asset>`: The cryptocurrency asset name (e.g., BTC, DOGE).
- `<file_time_format>`: The time interval for the data file (e.g., hourly, four-hour, daily, weekly).

#### Example

```bash
python outliers-price-move-sounds.py BTC hourly
```

This command checks for outliers in the hourly price data for Bitcoin (BTC). The corresponding CSV file expected would be named `hourly-prices.csv`. If any price changes qualify as outliers, the script will output the relevant data, including timestamps, price changes, and percentage changes. 

### Additional Notes

The script contains commented-out code for playing sounds in response to outliers based on specific characters (U for upward, D for downward), but it seems that section is not currently active. It is legacy for reference.

## outliers-price-moves.py

### Summary

The `outliers-price-moves.py` script analyzes cryptocurrency price data to identify significant price changes (outliers) based on the 2.5th and 97.5th percentiles of price deltas (the differences between consecutive prices). It reads data from a specified CSV file format, checks for valid asset input, and outputs the details of any detected outliers, including timestamps, current prices, price changes, and percentage changes.

### Usage

To run the script, execute the following command in the terminal:

```bash
python outliers-price-moves.py <asset> <file_time_format>
```

- `<asset>`: The cryptocurrency asset name (e.g., BTC, DOGE, ETH).
- `<file_time_format>`: The time interval for the data file (e.g., hourly, four-hour, daily, weekly).

#### Example

```bash
python outliers-price-moves.py ETH daily
```

This command checks for outliers in the daily price data for Ethereum (ETH). The corresponding CSV file expected would be named `daily-prices.csv`. If any price changes qualify as outliers, the script will print the relevant data, including timestamps and percentage changes. If no outliers are found, it will notify you accordingly.

## poly-linr-sk.py

### Description

`poly-linr-sk.py` is a Python script designed for performing polynomial linear regression on cryptocurrency price data. It uses Scikit-learn's polynomial features and regression models to fit a curve to the provided price data and visualize the results. The script accepts command-line arguments for the cryptocurrency symbol, time frame, and whether to plot daily, hourly, or weekly data. It scales the data and generates predictions, which are then plotted alongside the actual price data, with fractals identified for potential trading signals.

### Usage

To run the script, execute it from the command line with the following syntax:

```bash
python poly-linr-sk.py <currency> [<timeframe>] [<D/H/W>]
```

- **`<currency>`**: The cryptocurrency symbol (e.g., BTC, ETH).
- **`<timeframe>`** (optional): An integer representing the number of data points to consider (default is 100).
- **`<D/H/W>`** (optional): Specify 'D' for daily, 'H' for hourly, or 'W' for weekly data (default is daily).

### Example

To analyze the last 50 hourly data points for Bitcoin:

```bash
python poly-linr-sk.py BTC 50 H
```

### Dependencies

- `numpy`
- `scikit-learn`
- `matplotlib`

### Output

- A plot displaying:
  - Actual price data.
  - Predictions from polynomial regression and standard linear regression.
  - Identified fractals for potential buy/sell signals.

Make sure the required CSV files containing the price data are accessible at the specified paths in the script.

## rsi-fractals-avgs-bbands-txt-summary.py

### Summary
The `rsi-fractals-avgs-bbands-txt-summary.py` script is designed for analyzing cryptocurrency price data using various technical indicators. It reads price data from CSV files, calculates indicators such as the Relative Strength Index (RSI), Simple Moving Averages (SMA), and identifies fractals, which are used to determine potential buy/sell points. The script also computes volatility, efficiency ratios, and outputs the results to a CSV file for further analysis.

### Key Components
1. **Argument Parsing**: The script accepts command-line arguments for currency, time frame, and data frequency (daily, hourly, weekly, or four-hour).
2. **Data Handling**: It reads price data from specific CSV files based on the user's specified frequency and time frame.
3. **Fractal Calculation**: Identifies up and down fractals from historical price data.
4. **Technical Indicator Calculations**:
   - **SMA**: Computes various SMAs over different periods (5, 10, 20, 50, and 200).
   - **RSI**: Calculates the current RSI and tracks its max/min over the last 10 periods.
   - **Volatility**: Measures the asset's volatility based on standard deviation.
   - **Efficiency Ratio**: Calculates an efficiency ratio to analyze price movements.
5. **Output**: Writes the results, including currency performance and relative metrics, to a CSV file.

### Usage
To run the script, use the command line with the following syntax:
```bash
python3 rsi-fractals-avgs-bbands-txt-summary.py <currency> [<timeframe>] [<H/F/D/W>]
```

#### Parameters:
- `<currency>`: The currency to analyze (e.g., BTC, ETH).
- `<timeframe>` (optional): An integer representing the number of periods to analyze (default is 200).
- `<H/F/D/W>` (optional): Specify the data frequency as:
  - `H` for hourly
  - `F` for four-hour
  - `D` for daily
  - `W` for weekly

### Example Command
To analyze Bitcoin with a time frame of 300 days using daily data:
```bash
python3 rsi-fractals-avgs-bbands-txt-summary.py BTC 300 D
```

### Output
The output is written to a CSV file named `output-rsi-er-price-sma20-multiple.csv`, which includes:
- Current price
- RSI value
- Various SMA ratios
- Fractal indicators
- Volatility metrics

This script is useful for traders and analysts who want to monitor cryptocurrency price movements and make informed trading decisions based on technical analysis.

## run.py, which utilizes functions from `ichimoku.py`

### Summary
`run.py` is a Python script designed to analyze financial data using the Ichimoku trading indicator. It accepts command-line arguments to specify the currency to be analyzed and the time scale (daily or weekly) for the data. Based on the provided parameters, it loads OHLC (Open, High, Low, Close) data from a CSV file, generates Ichimoku data, and visualizes the results, including Bollinger Bands and extended plots if requested.

### Usage
To run the script, use the following command in the terminal:

```bash
python3 run.py <currency> [<option>]
```

- **`<currency>`**: The currency pair you wish to analyze (e.g., `BTCUSD`).
- **`<option>`** (optional):
  - **`W`** or **`w`**: Specifies weekly data.
  - **`X`** or **`x`**: Requests extended plots in addition to the daily analysis.

#### Examples
1. **Daily Analysis (Default)**:
   ```bash
   python3 run.py BTCUSD
   ```

2. **Weekly Analysis**:
   ```bash
   python3 run.py BTCUSD W
   ```

3. **Daily Analysis with Extended Plots**:
   ```bash
   python3 run.py BTCUSD X
   ```

### Important Notes
- Ensure that the CSV file named `<currency>-ohcl.csv` is present in the working directory, containing the required OHLC data.
- The script will raise exceptions for invalid inputs, ensuring users provide correct parameters.

## statsmod.py - module for basic statistics
Initially used on a RaspberryPI that was running Python and keeping the code light used this instead of importing math modules.

### Description
`statsmod.py` is a module that provides statistical functions for analyzing financial data, specifically focusing on calculating standard deviation and return ratios. The module includes the following functions:

- **`stddev(list)`**: Computes the standard deviation of a list of values, which is useful for measuring volatility in price data.
- **`average(list)`**: Calculates the mean average of a list of numbers.
- **`raw_return_ratio(list)`**: Determines the return ratio of a financial asset by comparing the current price to the initial price, normalized by the standard deviation.
- **`normed_return_ratio(list)`**: Similar to `raw_return_ratio`, but it normalizes the return by multiplying with the average price, providing a more standardized metric.

This module is intended to be imported and used by other scripts in the directory for statistical analysis of financial time series data.
## Notes
I tend to use candles.py, run.py, rsi-fractals-avgs-bbands-txt-summary.py, linr-sk-fractals.py and buy-zone.py mostly. The other files can be legacy or they were early builds.

Let me know if any of the descriptions are missing or do not line up right with the code as I might have missed something along the way as I worked though this fairly quickly.
