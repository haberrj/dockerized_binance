#!/usr/bin/python3

# Author: Ron Haber
# Date: 10.10.2020
# This version will be used for real-time pricing
# It works incredibly well in the back test
# I need to determine how often I want to collect prices

import os
import csv
import currency as ghp

def FirstDerivative2Data(dataset, sample):
    #sample = 67 # will sample the deriv from the past 3 prices and divide accordingly
    # Will take from a dataset from every hour and compare points
    first_derivative = []
    data_size = len(dataset)
    for i in range(sample, data_size):
        deriv_holder = (dataset[i]["price"] - dataset[i-sample]["price"])/float(sample) # sampling method
        sub_dict = {
            "time":dataset[i]["time"],
            "price_deriv":deriv_holder
        }
        first_derivative.append(sub_dict) # may not require a list since this will be an ongoing number
    return first_derivative

def SecondDerivative2Data(first_deriv, sample):
    # Will execute for every first derivative
    #sample = 67
    second_derivative = []
    data_size = len(first_deriv)
    for i in range(sample, data_size):
        deriv_holder = (first_deriv[i]["price_deriv"] - first_deriv[i-sample]["price_deriv"])/float(sample) # similar sampling method the above
        sub_dict = {
            "time":first_deriv[i]["time"],
            "price_deriv":deriv_holder
        }
        second_derivative.append(sub_dict)
    return second_derivative

def BuyPercentageCurrency(amount, price, commission):
    # This will call the api to buy this asset
    percent_currency = amount/price
    w_commission = percent_currency * (1.0 - commission)
    paid = (percent_currency * price) - (w_commission * price)
    return w_commission, paid

def SellPercentageCurrency(currency, price, commission):
    # This will call the api to sell this asset
    amount = price*currency
    new_amount = amount * (1.0 - commission)
    paid = amount - new_amount
    return new_amount, paid

def TradingCurrency(price_data, first_deriv, second_deriv, current_amount, commission, thresholds):
    # Thresholds are the thresholds for buying and selling
    #thresholds
    first_buy_thresh = thresholds[0]
    first_sell_thresh = thresholds[1]
    second_buy_thresh = thresholds[2]
    second_sell_thresh = thresholds[3]
    
    last_buy_price = 0.0
    cash = current_amount
    wallet = 0 # number of coins in possession
    transaction_data = []
    data_len = len(second_deriv)

    for i in range(0, data_len):
        time = price_data[i+2]["time"]
        price = price_data[i+2]["price"]
        first_val = first_deriv[i+1]["price_deriv"]
        second_val = second_deriv[i]["price_deriv"]
        # Buy 
        if(cash > 0): # >0 since I have no idea if I'll be negative
            if(first_val < first_buy_thresh and second_val > second_buy_thresh):
                # This part will change to send a buy command to the api
                wallet, paid = BuyPercentageCurrency(cash, price, commission)
                # Below will be taken from the api and be filled that way
                cash = 0
                detailed = {
                    "time":time,
                    "transaction": "bought",
                    "price":price,
                    "cash":cash,
                    "coin":wallet,
                    "networth":SellPercentageCurrency(wallet, price, commission)[0],
                    "commission":paid
                }
                last_buy_price = price
                transaction_data.append(detailed)
        if(wallet > 0):
            if((first_val > first_sell_thresh and second_val < second_sell_thresh) or (price < 0.95*last_buy_price)):
                # This part will change to send a sell command to the api 
                if((CheckProfitability(last_buy_price, price, commission)) or (price < 0.95*last_buy_price)):
                # removed the profitability since I want just the buy indices
                    cash, paid = SellPercentageCurrency(wallet, price, commission)
                    # This part will change to send a sell command to the api
                    wallet = 0
                    detailed = {
                        "time":time,
                        "transaction": "sold",
                        "price":price,
                        "cash":cash,
                        "coin":wallet,
                        "networth": cash,
                        "commission":paid
                    }
                    transaction_data.append(detailed)
    try:
        final = transaction_data[-1]["networth"]
    except IndexError:
        final = current_amount
    return transaction_data, final

def CheckProfitability(last_price, current_price, commission):
    previous_commission = commission * last_price
    current_commission = current_price * commission
    total_comm = previous_commission + current_commission
    revenue = current_price - last_price
    profit = revenue - total_comm
    if(profit >= commission):
        # This will make the system only choose profitable transactions
        return True
    else:
        return False
