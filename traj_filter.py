import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
p1 = Polygon(np.array([[103.5006,1.055653],[103.5039,1.036862],[103.5448,1.044908],[103.5448,1.055653]]))

import json
with open('filtered_traj.json') as f:
      data = json.load(f)
filtered = data['raw_traj']
tmp = []
count = 0
for line in filtered:
    for ind,po in enumerate(line):
        pointx,pointy  = po
        point_sub = Point(pointx,pointy)
        if p1.contains(point_sub) and len(line)-ind<1700:
            tmp+= line
            break
print(len(tmp)-count)
count = len(tmp)

p2 = Polygon(np.array([[103.9556,0.755353],[103.9814,0.7544839],[103.972,0.7187623],[103.9551,0.7150501]]))
p2_not = Polygon(np.array([[103.8689,0.769],[103.9180,0.780],[103.8943,0.550]]))
for line in filtered:
    boolean = False
    for ind,po in enumerate(line):
        pointx,pointy  = po
        point_sub = Point(pointx,pointy)
        if p2.contains(point_sub) and len(line)-ind<1600:
            boolean = True
        if p2_not.contains(point_sub):
            boolean = False
            break
    if boolean:
        tmp+= line
print(len(tmp)-count)
count = len(tmp)

p3 = Polygon(np.array([[104.4275,1.163419],[104.4857,1.16196],[104.4861,1.167362],[104.4481,1.171852]]))
#p2_not = Polygon(np.array([[103.8689,0.769],[103.9180,0.780],[103.8943,0.550]]))
for line in filtered:
    for ind,po in enumerate(line):
        pointx,pointy  = po
        point_sub = Point(pointx,pointy)
        if p3.contains(point_sub) and len(line)-ind<1700:
            tmp+= line
            break
print(len(tmp)-count)
count = len(tmp)
p4 = Polygon(np.array([[104.10104,1.9933],[104.10880,1.9933],[104.10773,1.9809],[104.10279,1.9788]]))
#p2_not = Polygon(np.array([[103.8689,0.769],[103.9180,0.780],[103.8943,0.550]]))
for line in filtered:
    for ind,po in enumerate(line):
        pointx,pointy  = po
        point_sub = Point(pointx,pointy)
        if p4.contains(point_sub) and len(line)-ind<1000:
            tmp+= line
            break
print(len(tmp)-count)
count = len(tmp)

tmp = np.array(tmp)

fig = plt.figure(figsize=(20,20))
ax = fig.add_subplot(111, title="traj")
ax.scatter(tmp[:,0],tmp[:,1], alpha=0.5,s = 0.1)
plt.show()
