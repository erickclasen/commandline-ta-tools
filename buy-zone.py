#!/usr/bin/python3

'''
In October 2024 the data from CB Pro was cut off. Has to use CoinGecko which only
lets you go back 1 year. So patched in data in the weekly chart for BTC and ETH only.
Padded the rest with zeroes, re worked this file to use weekly data.
Allowing the option of daily for the future when the data fills up again.
'''


#import numpy as np # create dummy data for training
import sys
#import os 
import coretamodule as cm
import statsmod as st
import csv
import numpy as np

# Supress Numpy warning about version mismatch for now, too much clutter.
import warnings
warnings.filterwarnings("ignore")


def parse_arguments():
        arguments = len(sys.argv) - 1

        if arguments == 0:
            raise Exception("Missing command line parameter to parse.")
        elif arguments == 1:
            print("Currency: ",sys.argv[1])
            currency = sys.argv[1].upper()
            timeframe = 208
            subplot = 'W'
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
            raise Exception(" Daily timeframe not available until 10/2028!") 

            currency = sys.argv[1].upper()
            timeframe = int(sys.argv[2].upper())
            subplot = sys.argv[3].upper()
        else: # Anything else is false
            raise Exception("Invalid options on command line args.")

        # If timeframe < 208, make 208. Needs this for Mayer Multiple to work along with 2 year linear regression.
        if timeframe < 208:
                timeframe = 208

        return currency,timeframe,subplot

IMAGES_PATH = '/tmp'
def save_fig(fig_id, tight_layout=True, fig_extension="png", resolution=300):
    path = os.path.join(IMAGES_PATH, fig_id + "." + fig_extension)
    print("Saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution)


# ---------------------- MAIN. -------------------------
'''

4YMA Pricing Catagories

category	cuts	# days	low	high	category label
0	Very Cheap	(68.03399999999999, 145.406]	545.0	68.03399999999999	145.406	Very Cheap (68% - 145%)
1	Cheap	(145.406, 183.112]	545.0	145.406	183.112	Cheap (145% - 183%)
2	Average	(183.112, 239.734]	544.0	183.112	239.734	Average (183% - 240%)
3	Expensive	(239.734, 354.319]	545.0	239.734	354.319	Expensive (240% - 354%)
4	Very Expensive	(354.319, 1622.743]

...taken from https://ryanwingate.com/bitcoin/bitcoin-4-year-sma-analysis/

'''




underlying = 'USD'
product_label,timeframe,subplot = parse_arguments()

#live data
import coretamodule as cm

ticker_filename_daily = '/home/erick/python/ta/daily-prices.csv'
ticker_filename_weekly = '/home/erick/python/ta/weekly-prices.csv'

# Daily or hourly charting.
if subplot == 'W':
        ticker_filename = ticker_filename_weekly
elif subplot == 'D':
        ticker_filename = ticker_filename_daily
else:
        raise Exception("Bad 3rd CL Arg takes D or W, Daily or Weekly timeframes.")



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
curr_price = y_values[-1]
print("\nCurrent Price: ",curr_price)


# USING WEEKLY NUMBERS FOR NOW, APPROXIMATING!
# 8 weeks is close to 60 days for Kijun.
kijun = (max(currency_price_list[-8:]) + min(currency_price_list[-8:]))/2 

# MA's
sma3 = cm.simple_mov_avg(y_values,3) # 21 days close to 20
sma28 = cm.simple_mov_avg(y_values,28) # 200 Days
sma208 = cm.simple_mov_avg(y_values,208) # 4 Years

# BBand Std Dev of 20 days, 3 weeks approx
stddev = st.stddev(y_values[-3:])

mayer_mul = curr_price/sma28 # Approx 200 days
print("\nMayer Multiple:",round(mayer_mul,2))
if mayer_mul < 0.8:
	print(currency,"at Market Bottom with Mayer Mul < 0.8")
elif mayer_mul < 1.0:
        print(currency,"at Great DCA range with Mayer Mul < 1.0")
elif mayer_mul < 2.4:
        print(currency,"in DCA range with Mayer Mul < 2.4")
else:
        print(currency,"is out of DCA range with Mayer Mul > 2.4")


# Bracket in on the price targets.
print("\nCurrent Price Target in effect...")
if curr_price > kijun:
	print("Kijun Target:",kijun)
elif curr_price > round(sma3-stddev*2,4):
	print("2SD Bands Target:",round(sma3-stddev*2,4)) # Approx 20 days
elif curr_price > sma28:
	print("SMA200 Target",sma28) # APprox 200 days

# Print out true or false for what zones have been reached.
print("\nIs the price in the following zones...")
print("\nKijun Buy Zone: ",curr_price < kijun)
print("\n2SD Buy Zone: ",curr_price < (sma3-stddev*2))
print("\n200SMA Buy Zone: ",curr_price < sma28)



# --------------------- Long term 4 year cycle calculations ----------------
print("\n------- Long Term 4 Year Cycle -------\n")

# Ratio of price to 4 year MA.
ratio_cur_4YMA = curr_price/sma208
print("4YMA and Ratio: ",round(sma208,2),round(ratio_cur_4YMA,2),"\n")


# Where in the relative binning is the price in relationship to the sma1461.
if ratio_cur_4YMA*100 < 145.406:
        p = "Very Cheap"
elif ratio_cur_4YMA*100 < 183.112:
        p = "Cheap"
elif ratio_cur_4YMA*100 < 239.734:
        p = "Average"
elif ratio_cur_4YMA*100 < 354.319:
        p = "Expensive"
else:
        p = "Very Expensive"

print(currency,"is currently",p)

# Min Max and Mean for 4 Years, the entire set of y_values.
print("\n4Y Min:",min(y_values))
print("4Y Mean:",(max(y_values)+min(y_values))/2)
print("4Y Max:",max(y_values))
print("Price under 4YR mean buy zone:",curr_price < (max(y_values)+min(y_values))/2)


# -------------------- Linear Regression over 4 yrs -------------------------

# Create x values that will be sequential and as long as the y_values
# Numpy array conversion!
# This was taken from the example that uses pyTorch to train on values.
# X values is just monotonic fill of integers for the length of y_values.
x_values = [i for i in range(len(y_values))]
#print(x_values)
x_train = np.array(x_values, dtype=np.float32) # List to  numpy array
#print(x_train)
x_train = x_train.reshape(-1, 1) # Reshape , horiz to vertical.
#print(x_train)

# Ditto with the y_values
#print(y_values)
y_train = np.array(y_values, dtype=np.float32)
#print(y_train)
y_train = y_train.reshape(-1, 1)
#print(y_train)

# Use sklearn linear regression
from sklearn.linear_model import LinearRegression

X = x_train
Y = y_train

linear_regressor = LinearRegression()  # create object for the class
linear_regressor.fit(X, Y)  # perform linear regression
Y_pred = linear_regressor.predict(X)  # make predictions
print("\n4 Year Linear Regression Price:",Y_pred[-1])
print("Price under regressor buy zone:",curr_price < Y_pred[-1])
