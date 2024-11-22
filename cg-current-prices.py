import requests
import csv
import json
from datetime import datetime
from collections import OrderedDict
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import time

ticker_filename = "/home/erick/python/ta/hourly-prices.csv"
max_retries = 10
delay = 1 # 1 second

def live_dict_read():
    ''' Reads in a dictionary of live values plus debug keys and values if present.
        This dictionary will be used to impute values if there is a failure to get
        in a price or volume. RTNS the live dict. '''
        
    live_dict = {}
    # If the file exists read it in, if not just create it on the first pass through.
    try:
            with open("live_dict.json") as f_obj:
                    live_dict = json.load(f_obj)
    except:
            #with open(filename, 'w') as f_obj:
            #        json.dump(ichimoku_state,f_obj)
            print("Missing FIle for live dict. Need to create a live dict. Will create of first run through.")        

    return live_dict    


def live_dict_write(live_dict):
        ''' Takes in the live dict and does a json dump to file to save for use next round. '''
        with open("live_dict.json", 'w') as f_obj:
                json.dump(live_dict,f_obj)

def output_price_csv(out_list):
        with open(ticker_filename, mode='a') as outfile:
                output_writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                output_writer.writerow(out_list)


def get_crypto_prices(coin_ids):


    # ONLY USE IF WE GET FAILS TOO OFTEN.
    # Live value dict. This is used to impute a value in case of a comm failure.
    #live_dict = {}

    # Pull in the live dict in case values need imputing.
    #live_dict = live_dict_read()


    #url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(coin_ids)}&vs_currencies=usd"

    base_url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ",".join(coin_ids),
        "vs_currencies": "usd"
    }

    for attempt in range(max_retries):
    
            try:
                print("Attempt:",attempt)
                #response = requests.get(url)
                response = requests.get(base_url, params=params)

                response.raise_for_status()  # Raises an HTTPError for bad responses
                data = response.json()
        
                #prices = {}
                prices = OrderedDict()

                for coin in coin_ids:
                    if coin in data and 'usd' in data[coin]:
                        prices[coin] = data[coin]['usd']
                    else:
                        prices[coin] = "Price not available"
        
                return prices
    
            #except requests.exceptions.RequestException as e:
            except (ConnectionError, Timeout, TooManyRedirects) as e:
                    print("Connection error on attempt",(attempt + 1),":",e)
                    if attempt < max_retries - 1:
                        time.sleep(delay * (2 ** attempt))  # Exponential backoff
                    else:
                        print("Max retries reached. Unable to fetch data.")
                        return None




#-------------------------------------- main. -----------------------------------

# THe out list is what is built up by appending to it and will get saved as a CSV file.
out_list = []


# List of cryptocurrency IDs
#coins = ["bitcoin", "ethereum", "dogecoin"]

# The ones that we care about sorted by alpha for starters.
coins = ["bitcoin", "dogecoin", "ethereum", "fetch-ai", "internet-computer", "litecoin", "quant-network", "render-token", "solana", "the-graph"]

print(datetime.now())
out_list.append(datetime.now())


# Fetch prices
prices = get_crypto_prices(coins)

if prices:
    print("\nCurrent Cryptocurrency Prices (USD):")
    for coin, price in prices.items():
        print(coin.capitalize(),":",price)
        out_list.append(price)
else:
    print("Failed to fetch cryptocurrency prices.")
    exit()


output_price_csv(out_list)
