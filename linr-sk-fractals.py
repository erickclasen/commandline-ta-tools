#!/usr/bin/python3
import numpy as np # create dummy data for training
import sys
import os 
import coretamodule as cm
import statsmod as st

def parse_arguments():
        arguments = len(sys.argv) - 1

        if arguments == 0:
            raise Exception("Missing command line parameter to parse.")
        elif arguments == 1:
            print("Currency: ",sys.argv[1])
            currency = sys.argv[1].upper()
            timeframe = 100
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
            print("Daily or Hourly or Weekly D/H/W? ",sys.argv[3])

            currency = sys.argv[1].upper()
            timeframe = int(sys.argv[2].upper())
            subplot = sys.argv[3].upper()
        else: # Anything else is false
            raise Exception("Invalid options on command line args.")
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
else:
        raise Exception("Bad 3rd CL Arg takes D or H or W  Daily or Hourly or Weekly timeframes.")



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

# Create x values that will be sequential and as long as the y_values
# Numpy array conversion!
# This was taken from the example that uses pyTorch to train on values.
# X values is just monotonic fill of integers for the length of y_values.
x_values = [i for i in range(len(y_values))]
print(x_values)
x_train = np.array(x_values, dtype=np.float32) # List to  numpy array
print(x_train)
x_train = x_train.reshape(-1, 1) # Reshape , horiz to vertical.
print(x_train)

# Ditto with the y_values
print(y_values)
y_train = np.array(y_values, dtype=np.float32)
print(y_train)
y_train = y_train.reshape(-1, 1)
print(y_train)

# Use sklearn linear regression
#from sklearn.linear_model import LinearRegression

X = x_train
Y = y_train

# Fudge the tails of the data into shorter lengths for multi regressions.
X20 = x_train[-20:]
Y20 = y_train[-20:]
X50 = x_train[-50:]
Y50 = y_train[-50:]


# 3x linear regression
#linear_regressor = LinearRegression()  # create object for the class
#linear_regressor.fit(X, Y)  # perform linear regression
#Y_pred = linear_regressor.predict(X)  # make predictions

#linear_regressor.fit(X20, Y20)  # perform linear regression
#Y_pred20 = linear_regressor.predict(X20)  # make predictions


#linear_regressor.fit(X50, Y50)  # perform linear regression
#Y_pred50 = linear_regressor.predict(X50)  # make predictions

# Plotting
#import matplotlib.pyplot as plt
#plt.scatter(X, Y)
#plt.plot(X, Y_pred, color='red')
#plt.show()


#plt.clf()

# Axes
#plt.title(currency+"-"+underlying+" "+subplot+"'ly Linear Regression Plot", color='black')
#plt.xlabel(subplot+"'ly Timeframe", color="black", fontsize=20)
#plt.ylabel('Price', color="black", fontsize=20)

#plt.plot(x_train, y_train, 'go', label='True data', alpha=0.5)
#plt.plot(x_train, y_train, '-', label='True data', alpha=0.75,linewidth=1.95)

#plt.plot(X, Y_pred, '--', label='Predictions '+str(timeframe), alpha=0.5,linewidth=2.5)
#plt.plot(X20, Y_pred20, '--', label='Predictions 20', alpha=0.5,linewidth=1.95,color="red")
#plt.plot(X50, Y_pred50, '--', label='Predictions 50', alpha=0.5,linewidth=1.95,color="violet")
#plt.plot([min(X),max(X)],[max(Y[:5]),max(Y[-5:])],label="X")

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

# Save and plot the figure.
#plt.legend(loc='best')
#save_fig(currency+"-"+underlying+"-price-linr")
#plt.show()


min10 = round(min(y_values[-10:]),4)
print("\nMin10",min10)
print("Max60",round(max(y_values[-60:]),4))
# add mean of these

sma5 = cm.simple_mov_avg(y_values,5)
sma20 = cm.simple_mov_avg(y_values,20)

stddev = st.stddev(y_values[-20:])

print("\nSMA5 and SMA20:",round(sma5,4),round(sma20,4))
print("1SD Bands:",round(sma20-stddev,4),round(sma20+stddev,4))
print("2SD Bands:",round(sma20-stddev*2,4),round(sma20+stddev*2,4))
print("\nStops:",round(min10,4),round(min10-stddev*1,4),round(min10-stddev*2,4))

