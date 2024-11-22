from collections import OrderedDict
# Initial point take on 02/01/2021 at 1200 EDT.
#price_dict = {'BTC Price': 33578.22, 'BCH Price': 405.76, 'ETC Price': 7.523, 'ETH Price': 1316.0, 'LTC Price': 130.46, 'DAI Price': 1.00045, 'XLM Price': 0.317738, 'LINK Price': 22.29339, 'ALGO Price': 0.6327, 'ATOM Price': 8.167, 'OXT Price': 0.3455, 'ZEC Price': 87.23621556, 'BAT Price': 0.298723, 'CVC Price': 0.151437, 'GLM Price': 0.164357, 'MANA Price': 0.150457, 'LOOM Price': 0.0653, 'CGLD Price': 2.7844, 'KNC Price': 1.293, 'OMG Price': 3.4864, 'ZRX Price': 0.670885, 'FIL Price': 22.4243, 'NU Price': 0.3024}


# Revised when the CB Pro API stopped in 9/2024.
price_dict = OrderedDict()
#price_dict = {'BTC': 64396,  'ETH': 2615, 'DOGE': 0.21875, 'FET': 0.158, 'ICP': 9.32, 'LTC': 68.1, 'QNT': 74.46,'SOL': 156.2, 'GRT':0.184202}
price_dict = {'BTC': 67555.0, 'DOGE': 0.132506, 'ETH': 2610.22, 'FET': 1.37, 'ICP': 7.77, 'LTC': 72.74, 'QNT': 64.83, 'RNDR': 5.41393, 'SOL': 151.8, 'GRT': 0.164744}


# How long is the dict ?

print("Price Dict Length:",len(price_dict))

# Create a new one that will be the recipricols of price in order to create the index base value.
new_dict = {}

print("/nBase Prices/n")
# Create the index price multiplier dict
for key in price_dict:
	print(key,price_dict[key]) # Base prices

	temp_key = key.split() # Spilt to string to get the currency and price sepeerate.
	new_key = temp_key[0] # Get the currency alone.
	new_dict[new_key] = (1/(price_dict[key]*len(price_dict))) # Use the recipricol of the price, with a scaler papplied for how many coins.

# For sanity price it out
print(new_dict)

# S2nity check, recalculate the base values, should be close to the 1/ttl value below it.
print("\nTest of index values\n")
ttl,index_value = 0,0
for key in new_dict:
	print(price_dict[key]*new_dict[key])
	ttl+=1
	index_value += price_dict[key]*new_dict[key]


# Print out how many currencies counted up for a check, the is the total for the index. Then get the recipricol.
# This is the scaler that is to be applied to the index to bring it to unity.
print("/nHow Many Currencies in index and the index scaler: ",ttl,1/ttl)
print("Index Value, s/b 1 or very close to it:",index_value)

'''
2024-09-29 23:00:02.242218 Current Cryptocurrency Prices (USD): Bitcoin : 
64396 Dogecoin : 0.121875 Ethereum : 2615.89 Fetch-ai : 1.58 
Internet-computer : 9.32 Litecoin : 68.1 Quant-network : 74.46 Solana : 
156.2 The-graph : 0.184202 erick@Satellite-A135:~/python/ta$ nano linr-sk.py 
erick@Satellite-A135:~/python/ta$ python3 Python 3.4.3 (default, Nov 12 
2018, 22:20:49) [GCC 4.8.4] on linux Type "help", "copyright", "credits" or 
"license" for more information.
>>> 1/9*64396
7155.11111111111
>>> 1/(9*64396)
1.7254349821590024e-06
>>> round(1/(9*64396),5)
0.0
>>> 1/(9*2615)
4.248990864669641e-05
>>> 1/(1*1.58)
0.6329113924050632
>>> 1/(9*1.58)
0.07032348804500703
>>> 1/(9*9.32)
0.011921793037672867
>>> 1/(9*68.1)
0.0016315875346712351
>>> 1/(9*74.46)
0.0014922255051183335
>>> 1/(9*156.2)
0.0007113387395077536
>>> 1/(9*0.184202)
0.6032025228342315
'''
