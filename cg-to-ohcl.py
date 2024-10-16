#!/usr/bin/python3
import numpy as np # create dummy data for training
import sys
import os 
from datetime import datetime
import csv

# The index scaler as calculated on 02/01/2021 via the index-scaler.py code
# Recalculated 9/30/2024 scaled to 2 base units.
index_scaler = {'BTC': 1.7254349821590024e-06, 'ETH': 4.248990864669641e-05, 'DOGE': 0.5079365079365079, 'FET': 0.7032348804500703, 'ICP': 0.011921793037672867, 'LTC': 0.0016315875346712351, 'QNT': 0.0014922255051183335, 'SOL': 0.0007113387395077536, 'GRT': 0.6032025228342315}



def parse_arguments():
        arguments = len(sys.argv) - 1

        if arguments == 0:
            raise Exception("Missing command line parameter to parse.")
        elif arguments == 1:
            print("Currency: ",sys.argv[1])
            currency = sys.argv[1].upper()

        else: # Anything else is false
            raise Exception("Invalid options on command line args.")
        return currency


# ---------------------- MAIN. -------------------------
H = []
L = []
O = []
C = []
D = []
V = []
# Append the real date to the CSV on the right so it is human readable.
final_d_str = []

# Have to append to this list when pulling the list for the currency out of the list of dicts
input_lines = []
date_lines = []


currency_label = parse_arguments()

#live data
import coretamodule as cm

ticker_filename = '/home/erick/python/ta/hourly-prices.csv'


#price_list_of_dicts = cm.read_lines_from_csv_file(ticker_filename_hourly,extended=True)
price_list_of_dicts = cm.read_lines_from_csv_file(ticker_filename)


print(price_list_of_dicts[-1])


# Calculate the number of days between the two dates
start_date = datetime(1970, 1, 1) # Linux zero day.
end_date = datetime(2023, 9, 29) # The start of the data, from which +1 is added on each loop reading it in.
offset = (end_date - start_date).days + 28  # Calc the offset then add some value that makes it line up, not sure, this might be lost data from Internet drops?

# Map the offset to the date ct which was used since legacy times.
date_ct = offset 


# Slice out a list from the list of dictionaries using a loop. Might be a better way, not sure.
for line in price_list_of_dicts:
        input_lines.append(line[currency_label])
        date_lines.append(line["time stamp"]) # Handle the Dates too, need for UOD.PY too!


# Format the date from the CBPRO format to just the date, then to an mdate.
correct_format = '%Y-%m-%d %H:%M:%S.%f'
d = datetime.strptime(date_lines[0], correct_format)
day_string = d.strftime('%Y-%m-%d')

print("Start of Data:",day_string)

testing = 20000 # How far of a lookback?

# How long is the input data, mostly for DEBUG.
print("Lines of input data:",len(input_lines))
# Set date to start of testing position, goto end and move back. Tricky fudge for the fact that matplotlib date conv has issues.
# So instead we take a reference against the first date in the data and move up by the length and set back by our testing data len.
date_ct = int(date_ct + len(input_lines)/24 - testing/24)

# Clip off the data that is going to be plotted.
lines = input_lines[-testing:]
d_lines = date_lines[-testing:]

# Mostly just for DEBUG
print("Lines to process:",len(lines))

# Main loop, move through data in 24 hour steps grabbing the OHLC values and appending the counting date that moves forward.
for n in range(0,len(lines)-24,24):
        H.append(max(lines[n:n+23]))
        L.append(min(lines[n:n+23]))
        O.append(lines[n])
        C.append(lines[n+23])
        D.append(date_ct)
        V.append(0) # NO VOLUME ANYMORE

        # Format the date from the regular time format to just the date, getting it into a string format.
        d = datetime.strptime(d_lines[n], '%Y-%m-%d %H:%M:%S.%f')


        day_string = d.strftime('%Y-%m-%d')
        # DEBUG print(day_string)
        # Append the final date in the format we want to the list.
        final_d_str.append(day_string)
        date_ct += 1

''' For Debug
print("------------------------------------------")
print(H)
print("------------------------------------------")
print(L)
print("------------------------------------------")
print(O)
print("------------------------------------------")
print(C)
print("------------------------------------------")
print(D)
#quit()
'''

print("Today's Date and shift of the date from 1/1/1970: ",day_string,date_ct)

# The header has to be in this format for Ichimoku.py. Can have added fields but, needs these as a minimum.
#,Close,Date,High,Low,Open

# Open a file and write all of the lists to it row by row.
filename = currency_label + '-ohcl.csv'

with open(filename, mode='w') as csv_file:
    writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    writer.writerow(['','Close','Date','High','Low','Open','HDate','Volume'])

    for x in range(0,len(D)):
            writer.writerow([D[x],C[x],D[x],H[x],L[x],O[x],final_d_str[x],V[x]])
