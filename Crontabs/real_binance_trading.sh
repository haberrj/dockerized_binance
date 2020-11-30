#!/bin/bash
# Author: Ron Haber
# Date: 14.11.2020
# This will execute the price collection and currency trading for Binance

cd /home/pi/CryptoCurrency/
now=$(date)
echo $now
git pull

python3 /dockerized_binance/Binance/bin_actual_investments.py -d /Artifacts/ -i BTC ETH LINK BNB -r 1