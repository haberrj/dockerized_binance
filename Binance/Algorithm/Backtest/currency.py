#!/usr/bin/python3

# Author: Ron Haber
# Date: 12.10.2020
# The purpose of this script to pull historical data for the following crypto-currencies:
# This will test how the algorithm works for real time data
# Bitcoin (BTC), Ethereum (ETH), Litecoin (LTC) relative to EUR
# The eventual trajectory of this script will pull fiat currencies too (i.e. USD/EU, CAD/USD, etc.)
import os
import csv
import matplotlib.pyplot as plt
from datetime import datetime

def convert_timestamp_to_date(timestamp):
    time_holder = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    return time_holder

class Crypto:
    # This class reads a CSV input and creates a list of dictionaries with the respective price and timestamp
    # There is also a CSV file saved to a desire directory
    def __init__(self, name, history_data, json_data):
        self.name = name
        self.history_file = history_data
        self.json_data = json_data
        # init methods
        self.dict_values = self.decode_csv()
        self.relevant_info = self.format_dict_values()
        
    def decode_csv(self):
        holder = []
        new_holder = []
        with open(self.history_file) as csvfile:
            history_values = csv.DictReader(csvfile)
            for value in history_values: 
                holder.append(value)
            size = len(holder)
            if(size > 10000): # Amount of data points to check
                for i in range(size-10000, size): # doing this to above gives problems due to DictReader
                    new_holder.append(holder[i]) # more relevant data this way
            else:
                new_holder = holder
        return new_holder

    def print_dataset_size(self):
        print(len(self.relevant_info))

    def print_1_value(self, index):
        print(self.relevant_info[index])

    def print_all_values(self):
        for row in self.relevant_info:
            print(row)

    def format_dict_values(self):
        holder = []
        for row in self.dict_values:
            sub_dict = { #this will cut the useless info I don't care about
                "time": 0,
                "price": 0
            }
            sub_dict["time"] = row['time']
            sub_dict["price"] = float(row["price"]) 
            holder.append(sub_dict)
        oldest_to_newest = holder # removed the reversed since the self generated version is already oldest to newest
        return oldest_to_newest

    def GetCoinPriceList(self):
        return self.relevant_info

    def CreatePriceGraph(self):
        # Beware system requirements may limit this since it is a lot of data to plot
        # set up x & y (timestamp, price)
        x_axis = []
        y_axis = []
        for row in self.relevant_info:
            time_holder = self.convert_timestamp_to_date(row['timestamp'])
            x_axis.append(time_holder)
            y_axis.append(row['price'])
        plt.plot(x_axis, y_axis)
        plt.xlabel('Time/Date')
        plt.ylabel('Price (€)')
        plt.title(self.name)
        plt.show()