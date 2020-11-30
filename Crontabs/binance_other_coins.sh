#!/bin/bash
# Author: Ron Haber
# Date: 31.10.2020
# This script will run all of the different collections for other coins

cd /home/pi/CryptoCurrency/
now=$(date)
echo $now

python3 /home/pi/CryptoCurrency/Binance/collect_coin_info.py -d /media/pi/HaberServer/Crypto_Share/Binance/ -i LTC ADA XRP ADA SXP DOT