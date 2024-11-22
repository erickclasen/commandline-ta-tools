#!/usr/bin/python3
import matplotlib.pyplot as plt
import pandas as pd
import sys
import numpy as np
import csv

'''
https://www.thepythoncode.com/article/introduction-to-finance-and-technical-indicators-with-python

https://towardsdatascience.com/trading-toolbox-04-subplots-f6c353278f78


'''


def parse_arguments():
        arguments = len(sys.argv) - 1

        if arguments == 0:
            raise Exception("Missing command line parameter to parse.")
        elif arguments == 1:
            print("Currency: ",sys.argv[1])
            currency = sys.argv[1].upper()
            timeframe = 365
            subplot = 'RSI'
        elif arguments == 2: # OK parse out both, filename and option
            print("Currency: ",sys.argv[1])
            print("Time Frame Value: ",sys.argv[2])
            currency = sys.argv[1].upper()
            timeframe = int(sys.argv[2])
            subplot = 'RSI'
        elif arguments == 3: # OK parse out both, filename and option
            print("Currency: ",sys.argv[1])
            print("Time Frame Value: ",sys.argv[2])
            print("Indicator for Sub Plot (Or STATS for just data): ",sys.argv[3])

            currency = sys.argv[1].upper()
            timeframe = int(sys.argv[2])
            subplot = sys.argv[3].upper()

            # Check for Valid subplots, OBV is not used anymore as there is no volume with cg-data.
            valid_subplots = ['RSI', 'ROC']
            if subplot not in valid_subplots:
                raise ValueError(f"Invalid subplot name. Choose from {valid_subplots}.")

        else: # Anything else is false
            raise Exception("Invalid options on command line args.")
        return currency,timeframe,subplot

def roc(daily_data,lag=9):
        '''  use an indicator known as Rate of Change (ROC) '''
        # Add ROC to daily data
        daily_data['ROC'] = ( daily_data['Close'] / daily_data['Close'].shift(lag) -1 ) * 100

        return daily_data       

def obv(daily_data):
        ''' Sort of a fudge for OBV, get the abs value of the price 
            divided by last price for direction, mult by volume and 
            create a rolling sum to show a pseudo OBV.
        '''     
        #daily_data['OBV'] = (daily_data['Volume'] * (abs(daily_data['Close'].diff()) / daily_data['Close'].diff() -1)).rolling(20).sum()

        daily_data['OBV'] = (daily_data['Volume'] * abs(daily_data['Close'].diff()) / daily_data['Close'].diff()).cumsum()

        return daily_data

def RSI(series, window_length=14):
        '''
        https://stackoverflow.com/questions/20526414/relative-strength-index-in-python-pandas
        '''

        # Get the difference in price from previous step
        delta = series.diff()
        # Get rid of the first row, which is NaN since it did not have a previous 
        # row to calculate the differences
        delta = delta[1:] 

        # Make the positive gains (up) and negative gains (down) Series
        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0

        # Calculate the SMA
        roll_up2 = up.rolling(window_length).mean()
        roll_down2 = down.abs().rolling(window_length).mean()

        # Calculate the RSI based on SMA
        RS2 = roll_up2 / roll_down2
        RSI2 = 100.0 - (100.0 / (1.0 + RS2))

        return RSI2

def data_fib_stats(daily_data):
        ''' Print out some Fibonacci statistics on the  data for the timeframe involved. '''
        # Get the mean for the calculation of the mean multiplier.
        meanv = daily_data['Close'].mean()

        spread = max(daily_data['Close']) - min(daily_data['Close'])

        # Determine sensible level of rounding for the data depending on the price.
        # Use the trick of getting the integer of the value and measure the length of the string for how many digits.
        rounding = 5-len(str(int(spread)))

        min_price = min(daily_data['Close'])
        max_price = max(daily_data['Close'])

        # Kind of a patch to make sure this does not fail.
        if min_price == 0: # Prevent div/0
                min_price = 1e-10 

        print("\nHigh to Low Spread",spread,"Ratio of High/Low",round(max_price/min_price,2))
        print("\n Pivot points across",timeframe,"days. Plus Multiples of the mean price.")
        print(0,"\t",round(min_price,rounding)) # Start out with the min price.

        # To keep the math OK, use int's that are a 1000x of the decimal numbers sought after.
        for n in (382,500,618,1000,1618,2000,2618,3000,5000):
                x = n/1000
                print(x,"\t",round(min_price+spread*x,rounding),"\t",round(meanv*x,rounding))

        print() # Whitespae.


def volume_profile(currency,daily_data):
        ''' Volume Profile, scatter plot of price -vs- volume with color determined by the relative daily volatility. '''
        #plt.title(currency+" Volume Profile with Volatility Contrast", color='black', fontsize=24)
        # Get the relative daily volatility High-Low/Close, Gives (0-1) normalized range of price movement.
        vlt = (daily_data["High"]-daily_data["Low"])/daily_data["Close"]
        #print(vlt.describe())
        daily_data.plot(kind="scatter",y="Close",x="Volume",c=vlt,colorbar=True,alpha=0.99)
        plt.show()

def price_binning(currency,daily_data):
        ''' Put the prices into bins to see how frequently the prices stay in a certain price range. '''
        # Axes
        plt.title(currency+" Price Bins", color='black', fontsize=24)
        plt.xlabel('Price', color='black', fontsize=20)
        plt.ylabel('Count', color='black', fontsize=20)

        daily_data["Close"].hist(bins=50,figsize=(20,15))
        plt.show()


def print_summary(daily_data):
        ''' Helper fxn to print out a brief summary of the data. '''
        print(daily_data.shape)
        print(daily_data.head(3))
        print(daily_data.tail(3))
        print()
        print(daily_data.describe())


def statistics(daily_data):
        ''' DO statistics on the price basic avg,stddev, return ratio and bbands type of info. '''
        import statsmod as st

        print("\nStatistics")
        avg_price = st.average(daily_data['Close'])
        std_dev = st.stddev(daily_data['Close'])

        ret_ratio = round(st.normed_return_ratio(daily_data['Close']),2)
        print("Avg Price: ",round(avg_price,2))
        print("Std Dev: ",round(std_dev,2))

        # Print out the bands around the std devations, much like bbands.
        print("\n")
        for m in range(1,8,1):
                n = m/2
                print(str(n)+" Std Dev Price Bands and %: ",round(avg_price - n*std_dev,2),round(avg_price + n*std_dev,2),round(std_dev*n*100/avg_price,2))


        print("\nReturn Ratio: ",ret_ratio)
        print("\n")

        return avg_price,ret_ratio


def write_stats_csv(currency,timeframe,daily_data,avg_price,ret_ratio):
        ''' Helper fxn to wrtie out the stas to a file for future use. '''
        with open("stats.csv", mode='a') as csv_file:
                writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                # Instead omaking a list, just write out the rows.
                writer.writerow([currency,timeframe,round(min(daily_data['Close']),2),round(max(daily_data['Close']),2),round(avg_price,2),ret_ratio])

#----------------- MAIN. --------------------

# Read the arguments for the currency and the look back time constant.
currency,timeframe,subplot = parse_arguments()

# Pull in data and then tail it off to the time constant from the cl args.
daily_data = pd.read_csv(currency+'-ohcl.csv',index_col=6,parse_dates=True)
daily_data = daily_data.tail(timeframe)

# Set the index to the date after using parse dates and using column 6, HDate
# as the index.
daily_data.index.name = 'Date'

# Print out the stats and a summary of the data
print_summary(daily_data)

# Calculate and print out basic statistics.
avg_price,ret_ratio = statistics(daily_data)


# This is a cheat to just print out the stats. If STATS in the 3rd command line var then print 
# out the data stats and quit.
if subplot.upper() == "STATS":
        write_stats_csv(currency,timeframe,daily_data,avg_price,ret_ratio)
        quit()

#print(daily_data['Close'].describe()) Descriing just the CLose prices.

data_fib_stats(daily_data)

# Optional plots
if subplot.upper() != "RSI":
        volume_profile(currency,daily_data)
        price_binning(currency,daily_data)



import mplfinance as mpf

# Do ROC,OBV and RSI always as we don't know which one is used until the 
# subplot is entered via command line and it is not a lot of overhead to calc them.
daily_data = roc(daily_data)
daily_data = obv(daily_data)
daily_data['RSI'] = RSI(daily_data['Close'], 14)


print(daily_data.tail(3))

# We create an additional plot placing it on the third panel
# This will plot out the available subplot by referencing the data in
# the series by using the cmd line arg passed in for subplot.
plot_b = mpf.make_addplot(daily_data[subplot], panel=1, ylabel=subplot)

# Fill NaN with zero if anything is missing.
daily_data[subplot].fillna(0, inplace=True)

#We pass the additional plot using the addplot parameter
mpf.plot(daily_data,type='candle',style='binance',addplot=plot_b,title=currency+'-USD Candlestick Chart',mav=(10,20,50,200),volume=False)
