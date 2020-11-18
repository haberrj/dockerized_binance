#!/bin/bash
# Author: Ron Haber
# Date: 10.10.2020
# This will call the API periodically to get each type of currency's
# price data.

cd /home/pi/CryptoCurrency/
git pull

# Get price info from the ticker
python3 /home/pi/CryptoCurrency/API_Utils/krakenapi.py Ticker pair=xbteur
python3 /home/pi/CryptoCurrency/API_Utils/krakenapi.py Ticker pair=etheur
python3 /home/pi/CryptoCurrency/API_Utils/krakenapi.py Ticker pair=ltceur

python3 /home/pi/CryptoCurrency/Kraken/Real_Time/run_investments.py -d /media/pi/HaberServer/Crypto_Share/Real_Time_Artifacts/ -i BTC -p 0.0026
python3 /home/pi/CryptoCurrency/Kraken/Real_Time/run_investments.py -d /media/pi/HaberServer/Crypto_Share/Real_Time_Artifacts/ -i ETH -p 0.0026
python3 /home/pi/CryptoCurrency/Kraken/Real_Time/run_investments.py -d /media/pi/HaberServer/Crypto_Share/Real_Time_Artifacts/ -i LTC -p 0.0026