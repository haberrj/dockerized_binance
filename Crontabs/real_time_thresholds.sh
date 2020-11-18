#!/bin/bash
# Author: Ron Haber
# Date: 10.10.2020
# This script will run all of the different threshold executions for the
# different currencies.
# The inputs will be the thresholds themselves.

cd /home/pi/CryptoCurrency/
git pull

python3 /home/pi/CryptoCurrency/Kraken/Test_Thresholds/threshold_executer.py -d /media/pi/HaberServer/Crypto_Share/Real_Time_Artifacts/ -c 1000.00 -i BTC -t 15 15 15 15 -p 0.0026 &
P1=$!
python3 /home/pi/CryptoCurrency/Kraken/Test_Thresholds/threshold_executer.py -d /media/pi/HaberServer/Crypto_Share/Real_Time_Artifacts/ -c 1000.00 -i LTC -t 15 15 15 15 -p 0.0026 &
P2=$!
python3 /home/pi/CryptoCurrency/Kraken/Test_Thresholds/threshold_executer.py -d /media/pi/HaberServer/Crypto_Share/Real_Time_Artifacts/ -c 1000.00 -i ETH -t 15 15 15 15 -p 0.0026 &
P3=$!
wait $P1 $P2 $P3