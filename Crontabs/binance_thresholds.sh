#!/bin/bash
# Author: Ron Haber
# Date: 31.10.2020
# This script will run all of the different threshold executions for the
# different currencies.
# The inputs will be the thresholds themselves.

cd /home/pi/CryptoCurrency/
now=$(date)
echo $now
git pull

python3 /home/pi/CryptoCurrency/Binance/Algorithm/Backtest/threshold_executer.py -d /media/pi/HaberServer/Crypto_Share/Binance/ -c 1000.00 -i BTC -t 30 15 15 15 -p 0.00075 &
P1=$!
python3 /home/pi/CryptoCurrency/Binance/Algorithm/Backtest/threshold_executer.py -d /media/pi/HaberServer/Crypto_Share/Binance/ -c 1000.00 -i ETH -t 15 15 15 15 -p 0.00075 &
P2=$!
python3 /home/pi/CryptoCurrency/Binance/Algorithm/Backtest/threshold_executer.py -d /media/pi/HaberServer/Crypto_Share/Binance/ -c 1000.00 -i LINK -t 15 15 15 15 -p 0.00075 &
P3=$!
python3 /home/pi/CryptoCurrency/Binance/Algorithm/Backtest/threshold_executer.py -d /media/pi/HaberServer/Crypto_Share/Binance/ -c 1000.00 -i BNB -t 15 15 15 15 -p 0.00075 &
P4=$!
wait $P1 $P2 $P3 $P4