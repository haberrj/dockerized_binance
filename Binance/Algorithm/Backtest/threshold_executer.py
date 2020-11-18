#!/usr/bin/python3
# Author: Ron Haber
# Date: 10.10.2020
# For updating the thresholds for Bitcoin
# Later for updating the price amount

import sys
import json
import csv
import argparse
from datetime import datetime
from os.path import expanduser
import threshold_calculator as tc
import derivative_algorithm as da
import currency as ghp 

parser = argparse.ArgumentParser(description="Find the ideal thresholds for any currency.")
parser.add_argument("-d", "--home", type=str, required=True, help="The directory for artifacts")
parser.add_argument("-c", "--cash", type=float, required=True, help="The amount of starting cash")
parser.add_argument("-i", "--currency", type=str, required=True, help="The type of currency (BTC, ETH, LTC)")
parser.add_argument("-t", "--threshold_limits", type=int, nargs=4, required=True, help="The 4 threshold limits for the algorithm")
parser.add_argument("-p", "--commission", type=float, required=True, help="The commission percentage taken by the broker")
args = parser.parse_args()

def CurrencyExecution(currency_type, price_path, json_path, cash, commission, threshold_limits):
    csv_path = price_path + currency_type + "_Transactions.csv"
    price_path = price_path + currency_type + "_Realtime.csv"
    json_path = json_path + currency_type.lower() + "_thresholds.json"
    Coin = ghp.Crypto(currency_type, price_path, json_path)
    threshold_array, wallet_array = tc.CalculateThresholds(Coin, cash, commission, 
                                    threshold_limits[0], threshold_limits[1], threshold_limits[2], threshold_limits[3])
    max_threshold, max_amount = tc.GetMaxThreshold(threshold_array, wallet_array)
    print(max_amount)
    WriteInfoToJson(Coin, max_threshold, max_amount, json_path)
    return max_threshold, max_amount, json_path

def WriteInfoToJson(coin_type, threshold_data, max_amount, json_path):
    data_dict = {
        "coin_name": coin_type.name,
        "threshold": threshold_data,
        "max_amount": max_amount,
        "date": datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    }
    with open(json_path, "w") as json_file:
        json.dump(data_dict, json_file) # This way only 1 entry every time... will be easier to track
    print("JSON updated at ", json_path)

def ThresholdLog(currency_type, price_path, json_path, cash, commission, threshold, sample):
    csv_path = price_path + currency_type + "_Transactions.csv"
    price_path = price_path + currency_type + "_Realtime.csv"
    json_path = json_path + currency_type.lower() + "_thresholds.json"
    Coin = ghp.Crypto(currency_type, price_path, json_path)
    # Calculate with the new threshold
    dataset = Coin.GetCoinPriceList()
    first_deriv = da.FirstDerivative2Data(dataset, sample)
    second_deriv = da.SecondDerivative2Data(first_deriv, sample)
    transactions, final = da.TradingCurrency(dataset, first_deriv, second_deriv, cash, commission, threshold)
    WriteInfoToCSV(csv_path, transactions)

def WriteInfoToCSV(csv_name, details):
    try:
        keys = list(details[0].keys())
    except IndexError:
        return csv_name
    with open(csv_name, 'w') as new_csv:
        writer = csv.DictWriter(new_csv, keys)
        writer.writeheader()
        for row in details:
            writer.writerow(row)
    return csv_name

if __name__ == "__main__":
    home = str(args.home) #"/media/pi/HaberServer/Crypto_Share/Real_Time_Artifacts/"
    price_path = home
    json_path = home + "Json_Output_Data/"
    threshold_limits = args.threshold_limits
    cash = args.cash
    currency_type = (args.currency).upper()
    commission = args.commission
    threshold, amount, json_file = CurrencyExecution(currency_type, price_path, json_path, cash, commission, threshold_limits)
    print("The ideal thresholds are: ", threshold)
    print("That will produce a max amount of: ", "{:,.2f}".format(amount), "€")
    if(currency_type == "BTC"):
        sample = 67
    elif(currency_type == "ETH"):
        sample = 67
    elif(currency_type == "BNB"):
        sample = 2
    else: # Link
        sample = 2
    ThresholdLog(currency_type, price_path, json_path, cash, commission, threshold, sample)