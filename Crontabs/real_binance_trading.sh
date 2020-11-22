#!/bin/bash
# Author: Ron Haber
# Date: 14.11.2020
# This will execute the price collection and currency trading for Binance

cd /home/pi/CryptoCurrency/
now=$(date)
echo $now
git pull

python3 /home/pi/CryptoCurrency/Binance/bin_actual_investments.py -d /media/pi/HaberServer/Crypto_Share/Binance/ -i BTC ETH LINK BNB -r 1