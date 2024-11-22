#!/usr/bin/python3
#import numpy as np # create dummy data for training
import sys
#import os 
import coretamodule as cm
import statsmod as st
import csv


def parse_arguments():
        arguments = len(sys.argv) - 1

        if arguments == 0:
            raise Exception("Missing command line parameter to parse.")
        elif arguments == 1:
            print("Currency: ",sys.argv[1])
            currency = sys.argv[1].upper()
            timeframe = 200
            subplot = 'D'
        elif arguments == 2: # OK parse out both, filename and option
            print("Currency: ",sys.argv[1])
            print("Time Frame Value: ",sys.argv[2])
            currency = sys.argv[1].upper()
            timeframe = int(sys.argv[2])
            
            subplot = 'D'
        elif arguments == 3: # OK parse out both, filename and option
            print("Currency: ",sys.argv[1])
            print("Time Frame Value: ",sys.argv[2])
            print("Hourly,4 Hours, Daily or Weekly H/F/D/W? ",sys.argv[3])

            currency = sys.argv[1].upper()
            timeframe = int(sys.argv[2].upper())
            subplot = sys.argv[3].upper()
        else: # Anything else is false
            raise Exception("Invalid options on command line args.")

        # If timeframe < 200, make 200. Needs this for Mayer Multiple to work.
        if timeframe < 200:
                timeframe = 200

        return currency,timeframe,subplot

IMAGES_PATH = '/tmp'
def save_fig(fig_id, tight_layout=True, fig_extension="png", resolution=300):
    path = os.path.join(IMAGES_PATH, fig_id + "." + fig_extension)
    print("Saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution)


# ---------------------- MAIN. -------------------------

underlying = 'USD'
product_label,timeframe,subplot = parse_arguments()

#live data
import coretamodule as cm

ticker_filename_hourly = '/home/erick/python/ta/hourly-prices.csv'
ticker_filename_4h = '/home/erick/python/ta/four-hour-prices.csv'
ticker_filename_daily = '/home/erick/python/ta/daily-prices.csv'
ticker_filename_weekly = '/home/erick/python/ta/weekly-prices.csv'

# Daily or hourly charting.
if subplot == 'W':
        ticker_filename = ticker_filename_weekly
elif subplot == 'D':
        ticker_filename = ticker_filename_daily
elif subplot == 'H':
        ticker_filename = ticker_filename_hourly
elif subplot == 'F':
        ticker_filename = ticker_filename_4h
else:
        raise Exception("Bad 3rd CL Arg takes D or H or W or F, Daily or Hourly or Weekly or 4 hour timeframes.")



# Parse out the currency and underlying if there is one.
# First split on the hyphen
currency_underlying = product_label.split("-")

# Test for the underlying, if not present assume it is USD
if len(currency_underlying) == 1:
        currency = currency_underlying[0] # The currency is 1st idx in.
        underlying = 'USD'
else:
        currency = currency_underlying[0] # Split them to currency and...
        underlying = currency_underlying[1] # underlying


print(currency,underlying)

currency_price_list = []

#price_list_of_dicts = cm.read_lines_from_csv_file(ticker_filename_hourly,extended=True)
price_list_of_dicts = cm.read_lines_from_csv_file(ticker_filename)

# Test
print(price_list_of_dicts[-1])

# IF currecy is the INDEX then wither plot out the index or plot it against an underlying currency
# Else allow default plotting against USD or a selected underlying, using it as a divisor.
if currency == 'INDEX':
        # NEsted loops, outer walk trough the list, inner walk through the dict and apply an index scaler to it.
        for line in price_list_of_dicts[-timeframe:]:
                index_value = 0 # Always reset this on every line.
                if underlying == 'USD': # No underlying, just divide by 1 a, NOOP.
                        divisor = 1
                else:
                    divisor = line[underlying] # Divide by the underlying asset

                # Inner loop, do the indexing math across the values of the dictionary.
                for key in cm.index_scaler:
                        #print(price_dict[key]*new_dict[key]) # Debug
                        index_value += line[key]*cm.index_scaler[key]
                # uild a list out of the values.
                currency_price_list.append(index_value/divisor) 
else:
        # Pull out the prices the normal way by extracting from the dict line by line
        for line in price_list_of_dicts[-timeframe:]:
                if underlying == 'USD': # No underlying assume USD, just divide by 1 a, NOOP.
                        divisor = 1
                else:
                    divisor = line[underlying] # Divide by the underlying asset

                currency_price_list.append(line[currency]/divisor)

# Clipped to the timefram already by the parsing of the list from the dict above.
y_values = currency_price_list

print("\nCurrent Price: ",y_values[-1])


# ------ FRACTALS -----------
# Plot the Williams Up and Down fractals as a helper to set stops.
# These are strict fractals, requiring 2 downs and 2 ups in price.
print("\nFractals\n")
dp = [0,0,0,0] # Array to hold the historic values
count = 0 # Keep a count to plot the point and print out the position.

# Run through the range of price values.
for price in y_values:

        # Make sure the historic data is populated. The find the fractals. 
        # This uses the current price and 4 historic values.
        if dp[3] > 0:
                # Find Down Fractals using if logic.
                if dp[3] > dp[2] and dp[2] > dp[1] and dp[1] < dp[0] and dp[0] < price:
                        print("Down: ",count-1,"\t\t",dp[1]) 
                        #plt.scatter(count-2,dp[1])
                # Find Up fractals using if logic.      
                if dp[3] < dp[2] and dp[2] < dp[1] and dp[1] > dp[0] and dp[0] < price:
                        print("Up: ",count-1,dp[1]) 
                        #plt.scatter(count-2,dp[1])


        # Save historic data by propigating the data forward in time
        for x in range(3,0,-1):
                dp[x] = dp[x-1]
        dp[0] = price # Current price always goes at the zero/now point.
        count+=1 # Keep track of the position in history.

# Min and Max Values
min10 = round(min(y_values[-10:]),4)
max60 = round(max(y_values[-60:]),4)

# Get Ichimoku Summary
tenken = (max(currency_price_list[-20:]) + min(currency_price_list[-20:]))/2
kijun = (max(currency_price_list[-60:]) + min(currency_price_list[-60:]))/2 
print("\nMin10",min10,"Max60",max60,"\tTenken",round(tenken,4),"Kijun",round(kijun,4)," T>K:",(tenken > kijun))

# MA's
sma5 = cm.simple_mov_avg(y_values,5)
sma10 = cm.simple_mov_avg(y_values,10)
sma20 = cm.simple_mov_avg(y_values,20)
sma50 = cm.simple_mov_avg(y_values,50)
sma200 = cm.simple_mov_avg(y_values,200)

stddev = st.stddev(y_values[-20:])

# The ratio of the ten over fifty is important, not the levels.
ten_fifty_ratio = round(sma10/sma50,2)

# How volatile is the asset.
volatility = stddev/sma20

# Calulate this now as it will be used a few times
er = cm.eff_ratio(y_values,timeframe)


print("\nSMA5,SMA20,SMA200:",round(sma5,4),round(sma20,4),round(sma200,4))
print("1SD Bands:",round(sma20-stddev,4),round(sma20+stddev,4))
print("2SD Bands:",round(sma20-stddev*2,4),round(sma20+stddev*2,4))
print("Rel. Volatility (sd/sma20)/ER:",round(volatility/er,3))

print("\nStops:",round(min10,4),round(min10-stddev*1,4),round(min10-stddev*2,4))

print("ER:",round(er,2))
# Calculate RSI and RSI_a an older RSI to look at slope.
rsi = cm.rsi(y_values,lookback=14)

#rsi_a = cm.rsi(y_values[:-7],lookback=14) # All but the last 7 time periods.

# Init the bounds fir min and max.
rsi_max = 0
rsi_min = 100 

# Find the min and max RSI in the last 10 periods.
for n in range(1,10):
        rsi_n = cm.rsi(y_values[:-n],lookback=14)
        if rsi_n > rsi_max:
                rsi_max = rsi_n
                max_loc = n
        if rsi_n < rsi_min:
                rsi_min = rsi_n
                min_loc = n
        
print("Min,Max RSI in lb 10,w/posn:",round(rsi_min),min_loc,"   ",round(rsi_max),max_loc,"   RSI now",round(rsi))

#print("RSI now",round(rsi))
print("Price/SMA20 and Mayer Multiple:",round(y_values[-1]/sma20,2),round(y_values[-1]/sma200,2))

# Post the ten/fifty ratio and a bool for quick look.
print("Ten/Fifty Day SMA Ratio:",ten_fifty_ratio, ten_fifty_ratio > 1)

# Write away the relative parameters to compare price action across currs.
# Open a file and write Currency and Multiple.
filename = 'output-rsi-er-price-sma20-multiple.csv'

# Index has no  underlying, unitless.
if currency == 'INDEX':
        underlying = '---'

with open(filename, mode='a') as csv_file:
    writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    out_list = []
    out_list.append(currency.ljust(5))
    out_list.append(underlying)
    #out_list.append(str(round(y_values[-1],4)))
    out_list.append(str(y_values[-1] < (sma20-stddev*2)).ljust(5))

    #Print current price and lower STD-DEV 2 and if price lower or not. 
    print(y_values[-1],(sma20-stddev*2),(y_values[-1] < (sma20-stddev*2)))

    out_list.append(str(round(rsi)).rjust(2))
    out_list.append(str(round(er,2)).ljust(4)) # ER

    out_list.append(str(round(y_values[-1]/sma20,2)).ljust(4)) # Price/ SMA20 Multiple
    out_list.append(str(round(y_values[-1]/sma200,2))) # Price/ SMA200 Multiple
    out_list.append(str(ten_fifty_ratio)) # TFR for the record
    out_list.append(str(round(volatility/er,2))) # Rel.Volatility as (sd/sma20)/er for the record

    writer.writerow(out_list)


