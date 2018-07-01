import requests
import os
from os import environ

tortmapjsonURL = os.environ["TORTMAPURL"]

import urllib2

data = urllib2.urlopen(tortmapjsonURL).read(20000)
data = data.split("\n")
data = str(data)

#for line in data:
jsonmap = open("app/tort2devicemap.json", "a", 1)
jsonmap.write(data)
jsonmap.close()
