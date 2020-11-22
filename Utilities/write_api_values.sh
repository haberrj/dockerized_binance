#!/bin/bash
# Author: Ron Haber
# This script will write the environmental variables into proper representative files

# First arg is the public key
# Second arg is the secret key

touch /bin/API_Binance_public_key
touch /bin/API_Binance_secret_key

var="text to append"
public_direc=/bin/API_Binance_public_key
secret_direc=/bin/API_Binance_private_key

if [ -f "$public_direc" ]
then 
    echo "$1" > "$public_direc"
fi

if [ -f "$secret_direc" ]
then 
    echo "$2" > "$secret_direc"
fi