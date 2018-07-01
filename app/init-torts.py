import requests
import os
from os import environ

tortmapjsonURL = os.environ["TORTMAPURL"]

from urllib.request import urlopen

data = urlopen(tortmapjsonURL).read(20000)
data = data.split("\n")
data = str(data)

#for line in data:
jsonmap = open("app/tort2devicemap.json", "w", 1)
jsonmap.write(data)
jsonmap.close()
