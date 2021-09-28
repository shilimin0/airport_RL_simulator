
import numpy as np
import utm
import json
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


FILE_NAME = 'D:/simulator/MARL/utilities/final_filted_raw_traj.json'
with open(FILE_NAME,'r') as f:
    raw_traj = json.load(f)['raw_traj']

dx = 842 - 839
dy = 480 - 473

lat=np.array([1.3555541629319738,1.3761181131876685])
lon=np.array([103.98020429181963,103.98891938905349])
x,y,_,_ = utm.from_latlon(lat,lon)
real_x = (x-x[0])[1]
real_y = (y-y[0])[1]
scale_x = dx/real_x
scale_y = dy/real_y

transformed_traj = [[] for _ in range(4)]
for ind,sub in enumerate(raw_traj):
    for line in sub:
        line = np.array(line)
        x,y,_,_ = utm.from_latlon(line[:,1],line[:,0])

        line[:,0] = x*scale_x
        line[:,1] = -y*scale_y
        #line -= line[-1]
        line = list(map(list,line))
        transformed_traj[ind].append(list(line))

import matplotlib.pyplot as plt
tmp = []
for i in transformed_traj[0:4]:
    for j in i:
        tmp+=list(j[-200:])
tmp = np.array(tmp)

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111, title="traj")
ax.scatter(tmp[:,0],tmp[:,1], alpha=0.5,s = 0.1)
plt.show()



p = Polygon(np.array([[1195.76,-463.39],[1194.942,-461.40],[1194.994,-460.10],[1196.265,-463.14]]))
final_transformed_traj = [[] for _ in range(4)]
for inds,sub in enumerate(transformed_traj):
    for line in sub:
        for ind,ps in enumerate(line):
            point = Point(ps[0],ps[1])
            if p.contains(point):
                line = np.array(line[:ind]) - np.array([1195.081,-462.18])
                final_transformed_traj[inds].append(list(map(list,line)))
                break



remove_discontinuous = [[] for _ in range(4)]
for ind,sub in enumerate(final_transformed_traj):
    for line in sub:
        line1 = np.array(line)
        line1 = line1[1:]-line1[0:-1]
        dis = np.sum(line1**2,axis = 1)

        aver = np.mean(dis,axis = 0)
        if np.sum(dis>5*aver):
            print('remove')
            continue
        remove_discontinuous[ind].append(list(map(list,line)))



import matplotlib.pyplot as plt
tmp = []
for i in final_transformed_traj[0:4]:
    for j in i:

        tmp = np.array(j)
        fig = plt.figure(figsize=(10,10))
        ax = fig.add_subplot(111, title="traj")
        ax.scatter(tmp[:,0],tmp[:,1], alpha=0.5,s = 0.1)
        plt.show()




with open('final_adjusted_coord.json','w') as fout:
    json.dump({'raw_traj':remove_discontinuous}, fout)
