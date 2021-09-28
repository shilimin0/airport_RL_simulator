import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import json
import matplotlib.pyplot as plt

FILE_NAME = './data/final_adjusted_coord.json'
with open(FILE_NAME,'r') as f:
    raw_traj = json.load(f)['raw_traj']


tmp = []
for i in raw_traj:
    for j in i:
        tmp+=j
tmp = np.array(tmp)
rotation_matrix = np.array([[np.cos(1.166879),-np.sin(1.166879)],[np.sin(1.166879),np.cos(1.166879)]])
tmp = rotation_matrix.dot(tmp.T).T
fig = plt.figure(figsize=(20,20))
ax = fig.add_subplot(111, title="traj")
ax.scatter(tmp[:,0],tmp[:,1], alpha=1,s = 0.3)
plt.show()
print('done')

holding_point = [[] for _ in range(4)]
for ind,i in enumerate(raw_traj[0:4]):
    for index,j in enumerate(i):
        if ind == 0:
            p = Polygon(np.array([[-163.77,110.11],[-162.33,98.69],[-155.11,106.06]]))
            for p_index,point in  enumerate(j):
                point = Point(point)
                if p.contains(point):
                    holding_point[ind].append(p_index)
                    break
        if ind == 1:
            p = Polygon(np.array([[-14.39,213.47],[4.02,216.55],[-3.16,194.68]]))
            for p_index,point in  enumerate(j):
                point = Point(point)
                if p.contains(point):
                    holding_point[ind].append(p_index)
                    break
        if ind == 2:
            p = Polygon(np.array([[161.60,69.97],[163.64,60.69],[157.31,64.67]]))
            for p_index,point in  enumerate(j):
                point = Point(point)
                if p.contains(point):
                    holding_point[ind].append(p_index)
                    break
        if ind == 3:
            p = Polygon(np.array([[41.029,-212.25],[44.188,-213.72],[42.699,-201.52]]))
            for p_index,point in  enumerate(j):
                point = Point(point)
                if p.contains(point):
                    holding_point[ind].append(p_index)
                    break

def rotate(dx,dy):
    vector_1 = np.array([1, 0])
    vector_2 = np.array([dx, dy])
    cosTh = np.dot(vector_1,vector_2)
    sinTh = np.cross(vector_1,vector_2)
    res = np.rad2deg(np.arctan2(sinTh,cosTh))
    return res
#with open('./data/holding_point.json','w') as fout:
    #json.dump({'holding_point':holding_point}, fout)
raw_traj_with_holding = [[] for _ in range(4)]
for ind,i in enumerate(raw_traj[0:4]):
    for index,j in enumerate(i[2:3]):
        j = np.array(j)
        speed = np.sqrt(np.sum((j[holding_point[ind][index]] -j[holding_point[ind][index]-2])**2))
        radius = speed*120/(4*np.pi)
        direction = j[holding_point[ind][index]] -j[holding_point[ind][index]-4]
        unit = (direction/np.linalg.norm(direction, axis=0))*radius
        center= np.empty_like(direction)
        center[0] = -unit[1]
        center[1] = unit[0]
        center = center + j[holding_point[ind][index]]
        angle = rotate(center[0],center[1])
        theta = np.linspace(angle, 2*np.pi+angle, int(120))
        # the radius of the circle
        r = radius
        # compute x1 and x2
        x1 = -r*np.cos(theta)+center[0]
        x2 = -r*np.sin(theta)+center[1]
        circle = np.stack((x1,x2),axis = 1)     # create the figure
        final_traj = np.vstack((j[:holding_point[ind][index]+1],circle,j[holding_point[ind][index]+1::]))

        fig = plt.figure(figsize=(20,20))
        ax = fig.add_subplot(111, title="traj")
        ax.scatter(final_traj[:,0],final_traj[:,1], alpha=1,s = 0.6)
        ax.scatter(j[holding_point[ind][index]][0],j[holding_point[ind][index]][1],c = '#9467bd', alpha=1)
        ax.scatter(center[0],center[1],c = '#9467bd', alpha=1)
        ax.scatter(x1,x2,c = '#9467bd', alpha=1,s = 0.6)
        plt.show()
        print('done')
        break
