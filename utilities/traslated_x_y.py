import json
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
"""
FILE_NAME = 'D:/simulator/MARL/final_adjusted_coord.json'
with open(FILE_NAME,'r') as f:
    raw_traj = json.load(f)['raw_traj']
tmp = []
for i in raw_traj[0:4]:
    for j in i:
        tmp+=j[-200:]
tmp = np.array(tmp)
print(raw_traj)
fig = plt.figure(figsize=(20,20))
ax = fig.add_subplot(111, title="traj")
ax.scatter(tmp[:,0],tmp[:,1], alpha=1,s = 0.3)
plt.show()
print('done')
"""

FILE_NAME = 'D:/simulator/MARL/trail.json'
with open(FILE_NAME,'r') as f:
    raw_traj = json.load(f)['trail']
tmp = []
for j in raw_traj:
    tmp+=j
tmp = np.array(tmp)

fig = plt.figure(figsize=(20,20))
ax = fig.add_subplot(111, title="traj")
ax.scatter(tmp[:,0],tmp[:,1], alpha=1,s = 0.1)
plt.show()
print('done')
