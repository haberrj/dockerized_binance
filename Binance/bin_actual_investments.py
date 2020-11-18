#!/usr/bin/python3

# Author: Ron Haber
# Date: 6.11.2020
# This will execute actual trades on the Binance platform

import os, sys
import os.path
import csv, json, time
import argparse
import API.api_utils as au
import Actual_Investment.coin_type as ct

parser = argparse.ArgumentParser(description="Find the ideal thresholds for any currency.")
parser.add_argument("-d", "--home", type=str, required=True, help="The directory for artifacts")
parser.add_argument("-i", "--currencies", type=str, nargs="+", required=True, help="The names of currencies")
parser.add_argument("-r", "--run", type=int, required=True, help="Whether or not to run the system")

args = parser.parse_args()
home = str(args.home)
currencies = args.currencies
run = int(args.run)
names = []
for name in currencies:
    names.append(str(name).upper())

def CheckIfFileExits(filename):
    return os.path.isfile(filename)

def GetCoinInfo(client, names, direc):
    # names is an array of strings
    coins = []
    direc = direc + "Balances/"
    for name in names:
        detailed_price = client.GetDetailedPrices(name)
        try:
            balance = float(client.GetAssetBalance(name)["free"])
        except ValueError:
            balance = 0.0
        except TypeError:
            balance = 0.0
        details = {
            "time": au.convert_timestamp_to_date(int(time.time())),
            "name": name,
            "price":float(detailed_price["price"]),
            "bid":float(detailed_price["bid"]),
            "ask":float(detailed_price["ask"]),
            "balance": balance,
            "last_cash": GetCashValue(direc, name),
            "commission": float(client.GetCommission(name)) * 0.75 # since I get a discount but it's not calculated
        }
        coins.append(details)
    actual_cash = client.GetAssetBalance("EUR")["free"] # This will need to be changed somehow for the current cash amount
    print(actual_cash)
    return coins, actual_cash

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

def ExecuteRealTime(client, data_direc, info, actual_cash):
    execs = []
    order_info_array = []
    for value in info:
        name = value["name"]
        balance = value["balance"]
        cash = value["last_cash"]
        price = value["price"]
        bid = value["bid"]
        ask = value["ask"]
        commission = value["commission"]
        print("commission: ", commission)
        print(name)
        print("balance: ", balance)
        coin = ct.Currency(name, data_direc, commission, price, cash, balance, bid, ask) 
        action, quantity, networth = coin.DetermineTradeType() # This will need to return an action as well
        print("Actions ", action, " ", quantity, " ", cash)
        # action = 2
        details = {
            "time": au.convert_timestamp_to_date(int(time.time())),
            "name": name,
            "action": action,
            "networth": networth
        }
        order_info = False
        if(action == 1):
            # Buy
            new_price = float(client.GetDetailedPrices(name)["price"]) # this way I don't accidently overestimate the quantity
            print("new_price", new_price)
            if(name == "BTC" or name == "ETH"):
                quantity = "{:0.0{}f}".format(float(cash/new_price), 5) # quantity will not match since above output deducts commission
            else:
                quantity = "{:0.0{}f}".format(float(cash/new_price), 3)
            print("quantity: ", quantity)
            order_info = client.BuyItem(name, quantity)
            order_info["price"] = new_price
            # order_info = client.TestOrder("buy", name, quantity)
            # order_info = {
            #     "time": "0",
            #     "name": name,
            #     "id": "0",
            #     "price": new_price,
            #     "status": "FILLED",
            #     "coin": quantity,
            #     "type": "BUY"
            # }
            if(order_info == False):
                print("Insufficient Funds")
        elif(action == 2):
            # Sell
            new_price = float(client.GetDetailedPrices(name)["price"]) # this way I don't accidently overestimate the quantity
            if(name == "BTC" or name == "ETH"):
                quantity = "{:0.0{}f}".format(quantity, 5)
            elif(name == "BNB"):
                quantity = "{:0.0{}f}".format((quantity-1), 3) # always keep 1 BNB leftover
            else:
                quantity = "{:0.0{}f}".format(quantity, 3)
            print("quantity: ", quantity)
            order_info = client.SellItem(name, quantity)
            order_info["price"] = new_price
            # order_info = client.TestOrder("sell", name, quantity)
            # order_info = { 
            #     "time": "0",
            #     "name": name,
            #     "id": "0",
            #     "price": new_price,
            #     "status": "FILLED",
            #     "coin": quantity,
            #     "type": "SELL"
            # }
            if(order_info == False):
                print("Error with order")
        order_info_array.append(order_info)
        execs.append(details)
    return order_info_array, execs 

def GetCashValue(direc, name):
    # Will read a .csv file for the coin in question
    csv_file = direc + name + "_Balance.csv"
    if(CheckIfFileExits(csv_file)):
        with open(csv_file, 'r') as cash_file:
            cash_values = csv.DictReader(cash_file)
            cash = list(cash_values)
        amount = float(cash[-1]["cash"])
    else:
        print("No file found")
        return
    return amount

def CheckOrderStatuses(client, direc, orders):
    data_direc = direc + "Actual/CSV_Transactions/"
    transaction_files = []
    cash_files = []
    for order in orders:
        if(order == False):
            continue
        print(order["name"])
        print(order["status"])
        if(order["type"] == "SELL"):
            name = order["name"]
            id_num = order["id"]
            price = order["price"]
            try:
                new_info = client.GetOrderDetails(id_num, name)
                quantity = new_info["executedQty"]
                cash = float(new_info["cummulativeQuoteQty"])
            except:
                quantity = order["coin"]
                cash = float(price) * float(quantity)
            balance_direc = direc + "Actual/Balances/"
            if(cash < 0):
                cash = float(price) * float(quantity)
            cash = "{:0.0{}f}".format(cash, 2)
            print(cash)
            cash_files.append(WriteNewCashAmount(balance_direc, name, cash))
        transaction_files.append(WriteTransactionInfo(data_direc, order["name"], order))
    return transaction_files, cash_files

def WriteNewCashAmount(data_direc, name, cash):
    filename = data_direc + name + "_Balance.csv"
    time_value = au.convert_timestamp_to_date(int(time.time()))
    if(CheckIfFileExits(filename)):
        with open(filename,'a') as old_csv:
            writer = csv.writer(old_csv)
            writer.writerow([time_value, name, cash])
    else:
        details = {
            "time": time_value,
            "name": name,
            "cash": cash
        }
        keys = list(details.keys())
        with open(filename, 'w') as new_csv:
            writer = csv.DictWriter(new_csv, keys)
            writer.writeheader()
            writer.writerow(details)
    return filename

def WriteTransactionInfo(direc, name, order):
    filename = direc + order["name"] + "_transactions.csv"
    keys = list(order.keys())
    if(CheckIfFileExits(filename)):
        with open(filename,'a') as old_csv:
            writer = csv.writer(old_csv)
            writer.writerow([order["time"], order["name"], order["id"], order["price"], order["status"], order["coin"], order["type"]])
    else:
        with open(filename, 'w') as new_csv:
            writer = csv.DictWriter(new_csv, keys)
            writer.writeheader()
            writer.writerow(order)
    return filename
    
if __name__ == "__main__":
    API_key_direc = "/media/pi/HaberServer/Crypto_Share/API_Utils/Binance/"
    actual_home = home + "Actual/"
    client = au.API_Client(API_key_direc, False)
    info, actual_cash = GetCoinInfo(client, names, actual_home) # Gets the price of the asset
    # Write a history file for the orders. Putting it here to make sure everything gets logged
    files = WriteHistoryCSV(home, client, info)
    print(files)
    if(run == 1):
        orders, executions = ExecuteRealTime(client, home, info, actual_cash)
        # Any writing to documents should be done at the end
        transaction_files, cash_files = CheckOrderStatuses(client, home, orders)
        print(transaction_files)
        print(cash_files)