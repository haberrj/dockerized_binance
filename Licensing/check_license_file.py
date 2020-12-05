#!/usr/bin/python3

# Author: Ron Haber
# Date: 30.11.2020
# This script will check whether a license is valid

import os, sys


def GetLicenseInfo():
    license_file = "/Licenses/license"
    with open(license_file, 'r') as secret:
        license_val = secret.read()
        license_key = license_val[:-1]
    return license_key

# Need to write code to read the license file
