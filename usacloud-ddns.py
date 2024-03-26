#
#   Replace IP address in JSON file
#     for usacloud dynamic dns
#

import os
import sys
import urllib.request
import json

def getIPv4():
    try:
        with urllib.request.urlopen('http://v4.ident.me') as response:
            return response.read().decode()
    except urllib.error.URLError as e:
        print(e.reason)

def getIPv6():
    try:
        with urllib.request.urlopen('http://v6.ident.me') as response:
            return response.read().decode()
    except urllib.error.URLError as e:
        print(e.reason)

temp1 = 'temp1.json'
temp2 = 'temp2.json'

# Command Argument
args = sys.argv
if len(args) < 2:
    print('Usage: python3 usacloud-ddns.py HOST [HOST2] ...')
    exit()

# Get IP Address
IPv4 = getIPv4()
IPv6 = getIPv6()

# Read JSON file
with open(temp1) as jf:
    json_records = json.load(jf)

# Replace IP Address
changed = False
for i in range(1, len(args)):
    host = args[i]
    for rec in json_records:
        if rec['Name'] == host and rec['Type'] == 'A' and rec['RData'] != IPv4:
            changed = True
            print(host + "\t" + rec['Type'] + "\t" + rec['RData'] + ' -> ' + IPv4)
            rec['RData'] = IPv4
        if rec['Name'] == host and rec['Type'] == 'AAAA' and rec['RData'] != IPv6:
            changed = True
            print(host+ "\t" + rec['Type'] + "\t" + rec['RData'] + ' -> ' + IPv6)
            rec['RData'] = IPv6

if changed:
    # Convert JSON to string
    js = json.dumps(json_records)
    js = js.replace(" ","")
    jz = '{"Records":' + js + '}'

    # for Windows
    if os.name == "nt":
        jz = '{\\"Records\\":' + js.replace('"', '\\"') + '}'

    # Write JSON file
    with open(temp2, "w") as jf:
        jf.write(jz)
        jf.close()
