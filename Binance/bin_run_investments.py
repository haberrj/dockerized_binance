#!/usr/bin/python3

# Author: Ron Haber
# Date: 30.10.2020
# This script will track prices and save them to a csv similar to the Kraken scripts
# Will also 

import os, sys
import os.path
import csv
import json
import time
import argparse
import API.api_utils as au
import Algorithm.coin_type as ct

parser = argparse.ArgumentParser(description="Find the ideal thresholds for any currency.")
parser.add_argument("-d", "--home", type=str, required=True, help="The directory for artifacts")
parser.add_argument("-i", "--currencies", type=str, nargs="+", required=True, help="The names of currencies")
parser.add_argument("-p", "--commission", type=float, required=True, help="The commission percentage taken by the broker")
parser.add_argument("-t", "--test", type=int, required=True, help="Should the program run a demo on the prices, 1 to execute, 0 for just prices")

args = parser.parse_args()
home = str(args.home)
currencies = args.currencies
commission = float(args.commission)
test = bool(args.test)
names = []
for name in currencies:
    names.append(str(name).upper())

def CheckIfFileExits(filename):
    return os.path.isfile(filename)

def GetCoinInfo(client, names):
    # names is an array of strings
    coins = []
    for name in names:
        detailed_pricing = client.GetDetailedPrices(name)
        details = {
            "time": au.convert_timestamp_to_date(int(time.time())),
            "name": name,
            "price":float(detailed_pricing["price"]),
            "bid":float(detailed_pricing["bid"]), # price paid when selling
            "ask":float(detailed_pricing["ask"]) # price paid when buying
        }
        detailed_price = client.GetDetailedPrices(name)
        details = {
            "time": au.convert_timestamp_to_date(int(time.time())),
            "name": name,
            "price":float(detailed_price["price"]),
            "bid":float(detailed_price["bid"]),
            "ask":float(detailed_price["ask"])
        detailed_price = client.GetDetailedPrices(name)
        details = {
            "time": au.convert_timestamp_to_date(int(time.time())),
            "name": name,
            "price":float(detailed_price["price"]),
            "bid":float(detailed_price["bid"]),
            "ask":float(detailed_price["ask"])
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
            keys = coin.keys()
            with open(filename, 'w') as new_csv:
                writer = csv.DictWriter(new_csv, keys)
                writer.writeheader()
                writer.writerow(coin)
        files.append(filename)
    return files

def ExecuteRealTimeDemo(names, data_direc, commission):
    execs = []
    for name in names:
        coin = ct.Currency(name, data_direc, commission)
        networth = coin.DetermineTradeType()
        details = {
            "name": name,
            "networth": networth
        }
        execs.append(details)
    return execs

if __name__ == "__main__":
    API_key_direc = "/media/pi/HaberServer/Crypto_Share/API_Utils/Binance/"
    client = au.API_Client(API_key_direc, False)
    info = GetCoinInfo(client, names)
    files = WriteHistoryCSV(home, client, info)
    if(test):
        executions = ExecuteRealTimeDemo(names, home, commission)
        print(executions)