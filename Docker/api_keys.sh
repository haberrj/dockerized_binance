#!/bin/bash
# Author: Ron Haber
# Will set the file for API Keys for use with Binance

public=$1
secret=$2

mkdir /bin/api_keys

cd /bin/api_keys/
touch API_Binance_public_key
touch API_Binance_secret_key

public_direc="/bin/api_keys/API_Binance_public_key"
secret_direc="/bin/api_keys/API_Binance_secret_key"

if [ -f "$public_direc" ]
then 
    echo "$public" > "$public_direc"
fi

if [ -f "$secret_direc" ]
then 
    echo "$secret" > "$secret_direc"
fi

# Will check licensing here
#
# License script or close the docker
#

# cron related setup
touch /etc/crontab /etc/cron.*/*
service cron start

while true # This is an infinite loop to keep the docker up
do
    sleep 1
done