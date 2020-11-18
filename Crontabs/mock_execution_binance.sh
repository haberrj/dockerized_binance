#!/bin/bash
# Author: Ron Haber
# Date: 10.10.2020
# This will execute the price collection and currency trading for Binance

cd /home/pi/CryptoCurrency/
git pull

python3 /home/pi/CryptoCurrency/Binance/bin_run_investments.py -d /media/pi/HaberServer/Crypto_Share/Binance/ -i BTC ETH LINK BNB -p 0.00075 -t 1
# Currently will only execute the price retrieval