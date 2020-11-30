#!/usr/bin/python3

# Author: Ron Haber
# Date: 29.11.2020
# This script will capture crypto that I am not currently trading

import os, sys
import os.path
import csv, json
import argparse
import time
import API.api_utils as au

parser = argparse.ArgumentParser(description="Find the ideal thresholds for any currency.")
parser.add_argument("-d", "--home", type=str, required=True, help="The directory for artifacts")
parser.add_argument("-i", "--currencies", type=str, nargs="+", required=True, help="The names of currencies")

args = parser.parse_args()
home = str(args.home)
currencies = args.currencies
names = []
for name in currencies:
    names.append(str(name).upper())

def CheckIfFileExits(filename):
    return os.path.isfile(filename)

def GetCoinInfo(client, names):
    # names is an array of strings
    coins = []
    for name in names:
        detailed_price = client.GetDetailedPrices(name)
        details = {
            "time": au.convert_timestamp_to_date(int(time.time())),
            "name": name,
            "price":float(detailed_price["price"]),
            "bid":float(detailed_price["bid"]),
            "ask":float(detailed_price["ask"]),
        }
        coins.append(details)
    return coins

def WriteHistoryCSV(direc, client, coins):
    files = []
    for coin in coins:
        time = coin["time"]
        name = coin["name"]
        price = coin["price"]
        bid = coin["bid"]
        ask = coin["ask"]
        filename = direc + name + "_Realtime.csv"
        # If file exists append it
        if(CheckIfFileExits(filename)):
            with open(filename,'a') as old_csv:
                writer = csv.writer(old_csv)
                writer.writerow([time, name, price, bid, ask])
        else:
            keys = list(coin.keys())
            with open(filename, 'w') as new_csv:
                writer = csv.DictWriter(new_csv, keys)
                writer.writeheader()
                writer.writerow(coin)
        files.append(filename)
    return files

if __name__ == "__main__":
    API_key_direc = "/media/pi/HaberServer/Crypto_Share/API_Utils/Binance/"
    client = au.API_Client(API_key_direc, False)
    info = GetCoinInfo(client, names) # Gets the price of the asset
    # Write a history file for the orders. Putting it here to make sure everything gets logged
    files = WriteHistoryCSV(home, client, info)
    print(info)
    