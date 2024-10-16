#!/usr/bin/python3
from ichimoku import *
import sys


def parse_arguments():
        arguments = len(sys.argv) - 1

        if arguments == 0:
            raise Exception("Missing command line parameter to parse.")
        elif arguments == 1:
            print("Currency: ",sys.argv[1])
            currency = sys.argv[1].upper()
            tick = 'daily'
        elif arguments == 2: # OK parse out both, filename and option
            print("Currency: ",sys.argv[1])
            print("Tick Value: ",sys.argv[2])
            currency = sys.argv[1].upper()
            if sys.argv[2].upper() == 'W':
                tick = 'weekly'
	    # Show extended information like stops and sca charts.
            elif sys.argv[2].upper() == 'X':
                tick = 'daily'

            else:
                raise Exception("Invalid 2nd arg, w or W for weekly is acceptable. Or X for extended plots on daily.")
        else: # Anything else is false
            raise Exception("Invalid option, w or W is the only option for time scale.")
        return currency,tick

'''                  --------    MAIN	------			 '''

# Get teh args from teh cmmand line , the currency and the optional -w for weekly tick
currency_label,tick = parse_arguments()

# Kludge, import the one that is in line with the tick rate.
if tick == 'weekly':
        from ichimoku_wk import *
else:
        from ichimoku import *


# Open a file and write all of the lists to it row by row.
filename = currency_label + '-ohcl.csv'


# Load Sample Data into a dataframe
#df = pd.read_csv('./sample-data/ohcl_sample.csv',index_col=0)
df = pd.read_csv(filename ,index_col=0,parse_dates=True)

#Coinbase_BTCUSD_d.csv
# Initialize with ohcl dataframe
i = Ichimoku(df)
# Generates ichimoku dataframe
ichimoku_df = i.run()

# Plot ichimoku
i.plot_ichi(currency_label)

if tick == 'daily':
	i.plot_bb(currency_label)
	# Extended plots...
	if len(sys.argv) == 3:
		if sys.argv[2].upper() == 'X':	
			i.plot_stops(currency_label)
			i.plot_long_bb(currency_label)

