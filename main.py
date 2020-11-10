from datetime import datetime
import csv

import matplotlib.pyplot as plt

from Point import Point
from DenStream import DenStream

with open("data/art_load_balancer_spikes.csv") as data_file:
    csv_file = csv.reader(data_file)
    times = []
    values = []
    points = []
    for time, value in csv_file:
        time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        value = float(value)
        times.append(time)
        values.append(value)
        points.append(Point(time, value))

ds = DenStream()

for point in points:
    if not ds.merge(point.timestamp, point):
        # Print outliers
        print(point.timestamp, point.value)


plt.plot(times, values)
plt.show()
