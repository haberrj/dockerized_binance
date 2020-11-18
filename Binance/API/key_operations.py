#!/usr/bin/python3

# Author: Ron Haber
# Date 2.11.2020
# This will create a key for encrypting documents

import os, sys
from cryptography.fernet import Fernet

def GenerateEncryptionKey(direc):
    key = Fernet.generate_key()
    key_file = direc + "api.key"
    with open(key_file, "wb") as keyname:
        keyname.write(key)
    return key_file

def LoadKey(key_file):
    key = open(key_file, "rb").read()
    return key

def Encode(key, message):
    message = message.encode()
    f = Fernet(key)
    e_message = f.encrypt(message)
    return e_message

def Decode(key, e_message):
    f = Fernet(key)
    d_message = f.decrypt(e_message)
    return d_message.decode("utf-8")