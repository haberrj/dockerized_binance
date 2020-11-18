#!/usr/bin/python3

# Author: Ron Haber
# Date 2.11.2020
# Used to decrypt the api keys so they arent saved in plain text

import os, sys
import API.key_operations as ko

def ReadEncryptedAPIKey(api_key):
    with open(api_key, "rb") as api:
        api_value = api.read().strip()
    return api_value

def DecryptAPIKey(key_file, api):
    key = ko.LoadKey(key_file)
    decoded_api = ko.Decode(key, api)
    return decoded_api

def GetAPIKeyFile(key_file, api_file, new_file_name):
    api = ReadEncryptedAPIKey(api_file)
    decoded_api = DecryptAPIKey(key_file, api)
    file_name = WriteDecodedFile(decoded_api, new_file_name, key_file)
    return file_name

def WriteEncodedFile(new_file_name, old_file_name, key_file):
    key = LoadKey(key_file)
    with open(old_file_name, "r") as old_file:
        plain_api = old_file.read()
    e_api = Encode(key, plain_api)
    with open(new_file_name, "wb") as new_file:
        new_file.write(e_api)
    return new_file_name

def WriteDecodedFile(api_key, new_file_name, key_file):
    with open(new_file_name, "w") as new_file:
        new_file.write(api_key)
    return new_file_name