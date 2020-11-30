#!/usr/bin/python3

# Author: Ron Haber
# Date: 30.10.2020
# This will create a class for the currency to hold relevant data

import os, sys
import os.path
import json
import csv
from datetime import datetime
import time
import ast

def convert_timestamp_to_date(timestamp):
    time_holder = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return time_holder

def BuyPercentageCurrency(cash, price, commission):
    percent_currency = cash/price
    w_commission = percent_currency * (1.0 - commission)
    paid = (percent_currency * price) - (w_commission * price)
    return w_commission, paid

def SellPercentageCurrency(currency, price, commission):
    amount = price*currency
    new_amount = amount * (1.0 - commission)
    paid = amount - new_amount
    return new_amount, paid

def CheckIfFileExits(filename):
    return os.path.isfile(filename)

class Currency:
    # will add more data as things come up
    def __init__(self, name, data_direc, commission, current_price, cash_allowance, balance, bid, ask):
        self.name = name
        self.direc = data_direc
        self.current_price = current_price
        self.current_bid = bid
        self.current_ask = ask
        self.last_three_prices = [] # ltp[0] is current price required to determine 2 first_deriv values
        self.last_three_bid = []
        self.last_three_ask = []
        self.coin = balance
        self.cash = cash_allowance
        self.commission = commission

        self.thresholds = self.GetThresholds()
        self.GetPrices()
        self.current_holding_price, self.last_transaction_type = self.GetCurrentHoldingPrice() # needs to get the last price that it was bought for
        self.sample = self.SetSampleSize()
        self.first_deriv = self.FirstDerivative() # required to determine the second derivative (first_deriv[0] is the important one here)
        self.second_deriv = self.SecondDerivative(self.first_deriv)
    
    def SetSampleSize(self):
        if(self.name == "BTC"):
            sample = 2
        elif(self.name == "ETH"):
            sample = 2
        else: # BNB and LINK for now since short term
            sample = 2
        return sample

    def GetCurrentHoldingPrice(self):
        transactions = self.ReadPreviousTransactions()
        try:
            price = float(transactions[0]["price"])
        except ValueError:
            price = 0
        try:
            last_transaction_type = str(transactions[0]["type"]).upper()
        except ValueError:
            last_transaction_type = "SELL"
        return price, last_transaction_type

    def ReadPreviousTransactions(self):
        csv_name = self.direc + "Actual/CSV_Transactions/" + self.name + "_transactions.csv"
        if(CheckIfFileExits(csv_name)):
            with open(csv_name, "r") as transaction_data:
                history_values = csv.DictReader(transaction_data)
                holder = []
                for value in history_values: 
                    holder.append(value)
            transactions = list(reversed(holder))
        else:
            print("Invalid Name")
            sys.exit()
        return transactions

    def GetThresholds(self):
        thresholds = []
        json_name = self.direc + "Json_Output_Data/" + self.name.lower() + "_thresholds.json"
        if(CheckIfFileExits(json_name)):
            with open(json_name, "r") as json_file:
                data = json.load(json_file)
            thresholds = data["threshold"]
        else:
            print("File does not exist")
            sys.exit()
        return thresholds
    
    def GetPrices(self):
        prices = []
        csv_name = self.direc + self.name + "_Realtime.csv"
        if(CheckIfFileExits(csv_name)):
            with open(csv_name, "r") as price_data:
                history_values = csv.DictReader(price_data)
                holder = []
                for value in history_values: 
                    holder.append(value)
            prices = list(reversed(holder))
            for i in range(0,300):
                if(prices[i]["price"] != ""):
                    self.last_three_prices.append(float(prices[i]["price"]))
                else:
                    self.last_three_prices.append(0.0)
                if(prices[i]["bid"] != ""):
                    self.last_three_ask.append(float(prices[i]["bid"]))
                else:
                    self.last_three_ask.append(0.0)
                if(prices[i]["ask"] != ""):
                    self.last_three_bid.append(float(prices[i]["ask"]))
                else:
                    self.last_three_bid.append(0.0)
        else:
            print("File does not exist")
            sys.exit()
        self.current_ask = self.last_three_ask[0]
        self.current_bid = self.last_three_bid[0]
        return self.current_price
        
    def GetBalance(self):
        coin_value = self.coin * self.current_price
        balance = self.cash + coin_value
        return balance

    def FirstDerivative(self):
        sample = self.sample
        deriv_array = []
        price_holder = self.last_three_prices
        try:
            for i in range(0, sample + 1):
                deriv_holder = (price_holder[i] - price_holder[i+sample])/float(sample) # captures the price over the last sample points
                deriv_array.append(deriv_holder)
        except IndexError:
            size = len(price_holder)
            for i in range(0, size):
                deriv_holder = (price_holder[i] - price_holder[i+((size-1)/2)])/float(size/2) # captures the price over the last sample points
                deriv_array.append(deriv_holder)
        return deriv_array

    def SecondDerivative(self, first_deriv):
        sample = self.sample
        try:
            second_deriv = (first_deriv[0] - first_deriv[sample])/float(sample)
        except IndexError:
            size = len(first_deriv)
            second_deriv = (first_deriv[0] - first_deriv[size-1])/float(size)
        return second_deriv

    def DetermineTradeType(self):
        # Will return trade action as 0 (leave), 1 (buy), 2 (sell)
        first_val = self.FirstDerivative()
        second_val = self.SecondDerivative(first_val)
        self.thresholds = self.GetThresholds()
        print("Current holding price: ", self.current_holding_price)
        print("Last transaction type: ", self.last_transaction_type)
        print("Current bid price: ", self.current_bid)
        print("Thresholds: ", self.thresholds)
        print("First deriv: ", first_val[0])
        print("Second deriv: ", second_val)
        action = 0
        quantity = self.coin
        if((self.name == "LINK")):
            sell_off = 0.95 # to prevent loss due to volatility
        else:
            sell_off = 0.95
        if(self.last_transaction_type == "SELL"): # Buy
            if(first_val[0] < self.thresholds[0] and second_val > self.thresholds[1]):
                self.coin, paid = BuyPercentageCurrency(self.cash, self.current_ask, self.commission)
                self.cash = 0
                networth = self.GetBalance()
                detailed = {
                    "time":convert_timestamp_to_date(int(time.time())),
                    "transaction": "bought",
                    "price":self.current_ask,
                    "cash":self.cash,
                    "coin":self.coin,
                    "networth":networth,
                    "commission": paid
                }
                self.WriteSaleDataToCSV(detailed)
                self.WriteLastTransactionJson(detailed)
                self.current_holding_price = self.current_price
                action = 1
                quantity = self.coin
        elif(self.last_transaction_type == "BUY"):
            if((self.current_bid < (self.current_holding_price*sell_off)) or (first_val[0] > self.thresholds[2] and second_val < self.thresholds[3])):
                # the addition of the holding price becoming too low will auto cause a sale of the asset itself
                # this will prevent severe loss in the case of the underlying losing value
                if((self.isProfitable(self.current_holding_price, self.current_bid, self.commission)) or (self.current_bid < (self.current_holding_price*sell_off))):
                    # This will only sell if the current holding is profitable or if there is a 0.5% drop in price
                    self.cash, paid = SellPercentageCurrency(self.coin, self.current_bid, self.commission)
                    self.coin = 0
                    networth = self.GetBalance()
                    detailed = {
                        "time":convert_timestamp_to_date(int(time.time())),
                        "transaction": "sold",
                        "price":self.current_bid,
                        "cash":self.cash,
                        "coin":self.coin,
                        "networth":networth,
                        "commission": paid
                    }
                    self.WriteSaleDataToCSV(detailed)
                    self.WriteLastTransactionJson(detailed)
                    action = 2
        # Write the info to a csv somewhere
        networth = self.GetBalance()
        return action, quantity, networth

    def WriteSaleDataToCSV(self, details):
        csv_name = self.direc + "Actual/Predicted_Data/" + self.name + "_Transactions.csv"
        if(CheckIfFileExits(csv_name)):
            with open(csv_name,'a') as old_csv:
                writer = csv.writer(old_csv)
                writer.writerow([details["time"], details["transaction"], details["price"], details["cash"], details["coin"], details["networth"]])
        else:
            keys = list(details.keys())
            with open(csv_name, 'w') as new_csv:
                writer = csv.DictWriter(new_csv, keys)
                writer.writeheader()
                writer.writerow(details)
        return csv_name
    
    def WriteLastTransactionJson(self, details):
        json_name = self.direc + "Actual/Json_Transaction_Data/" + self.name + "_Last_Transaction.json"
        with open(json_name, "w") as new_json:
            json.dump(details, new_json)
        return json_name

    def isProfitable(self, last_price, current_price, commission):
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