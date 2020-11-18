#!/usr/bin/python3

# Author: Ron Haber
# Date: 30.10.2020
# This script will grab the required API key information and other required utilities

import os, sys
import time
import API.decrypt_api_keys as dak
from datetime import datetime
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException

def convert_timestamp_to_date(timestamp):
    time_holder = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return time_holder

class API_Client:
    def __init__(self, direc, demo_bool):
        self.home = direc
        self.api_public, self.api_secret = self.GetAPIKeys()
        self.demo = demo_bool
        self.isDemoBool()
        self.client = self.ConnectToClient()
        # self.TopUpBNB() # will add this later once this ready to be used and I have money in the account

    def ConnectToClient(self):
        client = Client(self.api_public, self.api_secret)
        if(client.get_account() == ''):
            print("Could not connect to account. Please try again")
            sys.exit()
        return client

    def GetCommission(self, name):
        ticker = name + "EUR"
        fee = self.client.get_trade_fee(symbol=ticker)["tradeFee"][0]["taker"] # maker seems to return 0
        return fee
    
    def GetCurrentPrice(self, name):
        ticker = name + "EUR"
        values = self.client.get_symbol_ticker(symbol=ticker)
        price = values["price"]
        return price
    
    def GetDetailedPrices(self, name):
        ticker = name + "EUR" # Always gets the value in Euros
        values = self.client.get_ticker(symbol=ticker)
        info = {
            "time": convert_timestamp_to_date(int(time.time())),
            "price": values["lastPrice"],
            "bid": values["bidPrice"],
            "ask": values["askPrice"]
        }
        return info

    def BuyItem(self, name, quantity):
        # Will execute the fastest possible transaction
        ticker = name + "EUR"
        try:
            buy_order_market = self.client.create_order(
                symbol=ticker,
                side='BUY',
                type='MARKET',
                quantity=quantity
            )
        except BinanceAPIException as e:
            print(e)
            print("False Call")
            return False
        except BinanceOrderException as e:
            print(e)
            print("False Call")
            return False
        order_info = {
            "time": convert_timestamp_to_date(int(time.time())),
            "name": name,
            "id": buy_order_market["orderId"],
            "price": buy_order_market["price"],
            "status": buy_order_market["status"],
            "coin": buy_order_market["executedQty"],
            "type": buy_order_market["side"]
        }
        return order_info
    
    def SellItem(self, name, quantity):
        # Will execute the fastest possible transaction
        ticker = name + "EUR"
        try:
            sell_order_market = self.client.create_order(
                symbol=ticker,
                side='SELL',
                type='MARKET',
                quantity=quantity
            )
        except BinanceAPIException as e:
            print(e)
            print("False Call")
            return False
        except BinanceOrderException as e:
            print(e)
            print("False Call")
            return False
        order_info = {
            "time": convert_timestamp_to_date(int(time.time())),
            "name": name, 
            "id": sell_order_market["orderId"],
            "price": sell_order_market["price"],
            "status": sell_order_market["status"],
            "coin": sell_order_market["executedQty"],
            "type": sell_order_market["side"]
        }
        return order_info
    
    def TestOrder(self, action, symbol, quantity):
        ticker = symbol + "EUR"
        try:
            sell_order_market = self.client.create_test_order(
                symbol=ticker,
                side=action.upper(),
                type='MARKET',
                quantity=quantity
            )
        except BinanceAPIException as e:
            print(e)
            print("False Call")
            return False
        except BinanceOrderException as e:
            print(e)
            print("False Call")
            return False
        # order_info = {
        #     "time": convert_timestamp_to_date(int(time.time())),
        #     "id": sell_order_market["orderId"],
        #     "price": sell_order_market["price"],
        #     "status": sell_order_market["status"],
        #     "coin": sell_order_market["executedQty"],
        #     "type": sell_order_market["side"]
        # }
        return sell_order_market

    def GetAccountDetails(self):
        return self.client.get_account()
    
    def GetAssetBalance(self, name):
        return self.client.get_asset_balance(asset=name)

    def GetAssetDetails(self):
        return self.client.get_asset_details()

    def TopUpBNB(self):
        # Keeps me having a BNB balance to have the commission as low as possible
        min_balance = 1 # minimum 1 BNB at all times
        top_up = 1.5
        bnb_balance = self.GetAssetBalance("BNB")
        bnb_balance = float(bnb_balance['free'])
        if (bnb_balance < min_balance):
            qty = round((top_up - bnb_balance), 2)
            order_details = self.BuyItem("BNB", qty)
            return order_details
        return

    def isDemoBool(self):
        if(self.demo):
            client.API_URL = 'https://testnet.binance.vision/api'
        return True
    
    def GetOrderDetails(self, order_num, symbol):
        ticker = symbol.upper() + "EUR"
        order_info = self.client.get_order(orderId=str(order_num), symbol=ticker)
        return order_info

    def GetAPIKeys(self):
        public_file_encrypted = self.home + 'API_Binance_public_key_encrypted'
        secret_file_encrypted = self.home + 'API_Binance_secret_key_encrypted'
        public_file = dak.GetAPIKeyFile("/home/pi/Bookshelf/api.key", public_file_encrypted, "/home/pi/Bookshelf/API_Binance_public_key")
        secret_file = dak.GetAPIKeyFile("/home/pi/Bookshelf/api.key", secret_file_encrypted, "/home/pi/Bookshelf/API_Binance_secret_key")
        with open(secret_file, 'r') as secret:
            secret_key = secret.read()
            secret_key = secret_key[:-1]
        with open(public_file, 'r') as public:
            public_key = public.read()
            public_key = public_key[:-1]
        os.remove(public_file)
        os.remove(secret_file)
        return public_key, secret_key
