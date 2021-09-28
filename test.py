import json
import numpy as np
import utm
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import matplotlib.pyplot as plt
FILE_NAME = 'D:/simulator/MARL/precessed_radar_departure.json'
with open(FILE_NAME,'r') as f:
    raw_traj = json.load(f)
tmp = []
for i in raw_traj:
    for j in i:
        tmp.append(j)
tmp = np.array(tmp)
fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111, title="traj")
ax.scatter(tmp[:,0],tmp[:,1], alpha=0.5,s = 0.1)
plt.show()