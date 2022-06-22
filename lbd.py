import requests
import difflib
import socket
import json
import time
import sys

domain = input("Domain: ")
port = input("Port: ")

print()
print("*** Checking for DNS-Loadbalancing ***")
addrs = socket.getaddrinfo(domain, int(port))
for addr in addrs:
    print(addr[4][0])

print()
print("*** Checking for HTTP-Server ***")
res = requests.head('http://'+domain +':'+port)
data = res.headers
print("Server:",data["Server"])

print()
print("*** Checking for Date-Loadbalancing ***")
for i in range(10):
    res = requests.head('http://'+domain+':'+port)
    data = res.headers
    print(data["Date"])

print()
print("*** Cheking for Session-Based-Loadbalancing ***")
res = requests.head('http://'+domain+':'+port)
if 'Location' in res.headers:
    res = requests.head(res.headers['Location'])

data = res.headers

if 'Date' in data:
    sess1_1 = data['Date']

if 'Set-Cookie' in data:
    sess1_2 = data['Set-Cookie']

time.sleep(1)

res = requests.head('http://'+domain+':'+port)
if 'Location' in res.headers:
    res = requests.head(res.headers['Location'])

data = res.headers

if 'Date' in data:
    sess2_1 = data['Date']

if 'Set-Cookie' in data:
    sess2_2 = data['Set-Cookie']

if sess1_1 != sess2_1:
    print("Found")
    print("<",sess1_1)
    print(">",sess2_1)
    sys.exit(0)

print("Not Found")
