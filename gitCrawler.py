import requests
from bs4 import BeautifulSoup
import urllib2
import re

#regular expressions
# Except anything with secret, cred, credentials, key, token, password, and pass
r = re.compile(r'^.*secret.*$ | ^.*cred.*$ | ^.*credentials.*$ | ^.*key.*$ | ^.*token.*$ | ^.*password.*$ | ^.*pass.*$, ^.*user.*$', flags=re.I | re.X)

def endsWith(f):
    return f.split(".")[1]

std = "https://raw.githubusercontent.com"
url = "https://github.com/bradosev03/SentimentAnalysis"
ignore = ["zip","md","pickle","pkl"]

creds = ["secret","cred","credentials","key"]

contents = url.replace("https://github.com/",'')
req = requests.get(url)
data = req.text
soup = BeautifulSoup(data,"lxml")

files = []

for link in soup.find_all('a'):
    if contents in link.get('href') and "." in link.get("href"):
        files.append(link.get('href'))

files = filter(lambda f: endsWith(f) not in ignore ,files)

for f in files:
    count = 0
    f = f.replace("/blob","")
    req = requests.get(std + f)
    data = req.content
    data = data.split("\n")
    for line in data:
        count = count + 1
        for word in line.split(" "):
            if r.findall(word):
                print "[+] Found in file: %s %s [Line %s]" % (f, line.split("="), count)
