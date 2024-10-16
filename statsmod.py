''' https://www.mathsisfun.com/data/standard-deviation-formulas.html '''

def stddev(list):
    ''' Calculate the standard deviation for a list using the last period of values.
        Typical usage is to take the stddev of the last period items in a price list'''
    variance = 0

    mean = average(list) # Mean avg

    # Calculate the variance aas a summation across the list of the difference of the value from the mean.
    # Sqaured.          
    for n in range(0,len(list),1):
        variance += pow((list[n] - mean),2)
        #print(n,list[n],variance)
    # The stddev is the average variance squared.
    return pow(variance/len(list),0.5)

def average(list):
    ''' Calculate the mean average take in a list and returns the result. '''
    
    # Return the mean average of the prices.    
    return sum(list)/len(list)


def raw_return_ratio(list):
    ''' Calculate the return ratio of the index for a time period denoted by PERIOD.
        Takes in the price list of dictionaries for all prices and parses out a list of
        prices for a currency, then does the return ratio math and returns the result. '''

    # Return is the price now divided by the first price.
    rtn = list[-1]/list[0]

    #print('stddev',stddev(currency_price_list))      

    return rtn/stddev(list) # Return the return ratio


def normed_return_ratio(list):
    ''' Calculate the return ratio of the index for a time period denoted by PERIOD.
        Takes in the price list of dictionaries for all prices and parses out a list of
        prices for a currency, then does the return ratio math and returns the result. '''

    # Return is the price now divided by the first price.
    # Normalize by using the average of the returns.    
    rtn = list[-1]/list[0]

    #print('stddev',stddev(currency_price_list))    

    # Normalize the prices by multiplying by the average price.
    return average(list)*(rtn/stddev(list)) # Return the return ratio

