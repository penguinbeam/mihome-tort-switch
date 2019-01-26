import os
from os import environ

tortdatajsonURL = os.environ["TORTDATAURL"]

import urllib.request, json, time
with urllib.request.urlopen(tortdatajsonURL) as url:
    data = json.loads(url.read().decode())

from datetime import datetime, timedelta
#eg = "2019-01-22 00:00:00.000000"
time_format = "%Y-%m-%d %H:%M:%S.%f"

now = datetime.now()
few_days_ago = datetime.today() - timedelta(days=2)

# Create empty object
results_object={}

final_entry = sorted(data.items())[-1]

# Use the final entry to loop through and fetch sensor IDs
for x in range(len(final_entry[1])):
  sensor_id = final_entry[1][x][0]
  # Create a nested object for each sensor
  results_object[sensor_id]={}
  # Create an empty list for x and y values
  results_object[sensor_id]["x-axis"]=[]
  results_object[sensor_id]["y-axis"]=[]

# For each entry in json
for attr, value in sorted(data.items()):
  # Check if within date range
  if few_days_ago <= datetime.strptime(attr, time_format) <= now:
    # Then loop through results of the sensors for that entry
    for x in range(len(value)):
      # Loop through each sensor ID
      for key in results_object:
        # Save x and y values if matches sensor
        if value[x][0] == key:
          results_object[key]["x-axis"].append(datetime.strptime(value[x][1], "%H:%M:%S %d/%m/%y"))
          results_object[key]["y-axis"].append(value[x][2])

          
# Data fetched, now draw a graph

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
import numpy as np

fig = plt.figure(figsize=(15, 10), dpi=150)

colour_array = ['blue', 'green', 'red', 'orange', 'magenta', 'yellow', 'black']
colour_int = len(colour_array)
legend_array = []

for key in results_object:
  colour_int -= 1
  colour = colour_array[colour_int]
  if colour_int < 0:
    colour_int = len(colour_array)
  
  x = results_object[key]["x-axis"]
  y = results_object[key]["y-axis"]
  #Convert text temps to floats
  y = np.array(y, dtype=np.float32)
  plt.plot_date(x, y, linestyle='solid', marker='None', markersize = 1, color=colour )
  
  #Add sensor ID to legend
  legend_array.append(key)

plt.legend(legend_array, loc='upper left')

days = DayLocator()   # every year
hours = HourLocator()  # every month
dayFmt = DateFormatter('%Y-%m-%d')
hourFmt = DateFormatter('%H')

plt.gca().xaxis.set_major_locator(days)
plt.gca().xaxis.set_major_formatter(dayFmt)
plt.gca().xaxis.set_minor_locator(hours)
plt.gca().xaxis.set_minor_formatter(hourFmt)
plt.gca().tick_params(axis='x', which='major', pad=15)
plt.gca().xaxis.set_tick_params(labelcolor='green')
plt.ylim(0.0, 40.0)

plt.grid(True,which='both', axis='both')
plt.xlabel('Time')
plt.ylabel('Temperature (°C)')
plt.title('Tortoise Temperatures')

fig.savefig('plot.png')
