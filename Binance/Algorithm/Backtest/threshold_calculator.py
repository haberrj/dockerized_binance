#!/usr/bin/python3
# Author: Ron Haber
# Date: 10.10.2020
# This script is meant for the purposes of finding out the best thresholds for the currency in question 
# trading algorithm.

import os
import csv
import json
import time, sys
import currency as ghp 
import derivative_algorithm as da 

def CalculateThresholds(currency_obj, cash, commission, fb_max, sb_max, fs_max, ss_max):
    # currency_obj is the class Crypto
    # need to include currency differentiation
    name = currency_obj.name
    if(name == "BTC"):
        multiplier = 1
        sample = 2
    elif(name == "ETH"):
        multiplier = 8
        sample = 2
    elif(name == "BNB"):
        multiplier = 80
        sample = 2
    else:
        multiplier = 800 # value could potentially change
        sample = 2
    dataset = currency_obj.GetCoinPriceList()
    first_deriv = da.FirstDerivative2Data(dataset, sample)
    second_deriv = da.SecondDerivative2Data(first_deriv, sample)
    wallet = []
    thr = [] # an array to hold all the threshold data
    thresh_holder = [0,0,0,0]
    current_iterations = 0.0
    total_iterations = (fb_max * sb_max * fs_max * ss_max) * 16
    for sb in range(-1* sb_max, sb_max, 1): 
        thresh_holder[1] = sb/float(multiplier)
        for fs in range(-1 *fs_max, fs_max, 1): 
            thresh_holder[2] = fs/float(multiplier)
            for fb in range(-1*fb_max, fb_max, 1): 
                thresh_holder[0] = fb/float(multiplier)
                for ss in range(-1*ss_max, ss_max, 1): 
                    thresh_holder[3] = ss/float(multiplier)
                    transactions, final = da.TradingCurrency(dataset, first_deriv, second_deriv, cash, commission, thresh_holder)
                    wallet.append(final)
                    new_thresh = [fb/float(multiplier), sb/float(multiplier), fs/float(multiplier), ss/float(multiplier)]
                    thr.append(new_thresh)
                    current_iterations = current_iterations + 1.0
                    UpdateProgress(current_iterations/total_iterations)
    return thr, wallet
    
def GetMaxThreshold(threshold_array, wallet_array):
    ideal_index = wallet_array.index(max(wallet_array))
    return threshold_array[ideal_index], wallet_array[ideal_index]

def UpdateProgress(progress):
    bar_length = 25
    status = ""
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(bar_length*progress))
    text = "\rPercent Complete: [{0}] {1}% {2}".format( "#"*block + "-"*(bar_length-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()
