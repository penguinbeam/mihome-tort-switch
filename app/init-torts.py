import requests
import os
from os import environ

tortmapjsonURL = os.environ["TORTMAPURL"]

from urllib.request import urlopen

data = urlopen(tortmapjsonURL).read(20000).decode('utf-8')
data = data.split("\n")
data = str(data)

#for line in data:
jsonmap = open("tort2devicemap.json", "a", 1)
jsonmap.write(data)
jsonmap.close()
