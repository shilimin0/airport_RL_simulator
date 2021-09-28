import json
import numpy as np
import utm
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import matplotlib.pyplot as plt

FILE_NAME = 'D:/simulator/MARL/utilities/departure_raw_traj.json'
with open(FILE_NAME,'r') as f:
    raw_traj = json.load(f)

tmp = []
for j in raw_traj:
    tmp+=list(j[:1500])
tmp = np.array(tmp)
traj = []

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111, title="traj")

def rotate(dx,dy):
    vector_1 = np.array([1, 0])
    vector_2 = np.array([dx, dy])
    cosTh = np.dot(vector_1,vector_2)
    sinTh = np.cross(vector_1,vector_2)
    res = np.arctan2(sinTh,cosTh)
    return res
angle =  -rotate(387670-386962,152481-150821)
rotation_matrix = np.array([[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]])
origin = np.array([292583,-296768])
for sub in raw_traj:
    sub = np.array(sub)
    lat = sub[:,1]
    lon = sub[:,0]
    x,y,_,_ = utm.from_latlon(lat,lon)
    sub[:,0]= x
    sub[:,1]= y
    sub = rotation_matrix.dot(sub.T).T
    traj.append(sub[:len(sub)-200]-origin)
    #ax.scatter(sub[:len(sub)-200,0],sub[:len(sub)-200,1], alpha=1,s = 0.1)
#plt.show()

dy = -296775 - (-296971)
dx = 3.733*dy
scale_x = 300/dx
scale_y = (1050-855)/dy

new_traj = []
for i in traj:
    d = np.sum(i**2,axis = 1)
    index = np.argmin(d)
    i[index:,0] = i[index:,0]*scale_x
    i[index:,1] = i[index:,1]*scale_y
    new_traj.append(list(map(list,i[index:])))
    #ax.scatter(i[index:,0],i[index:,1], alpha=1,s = 0.1)


#plt.show()

#with open('precessed_runway_departure.json','w') as f:
    #json.dump(new_traj,f)

#finished runway proecess
####################################
dx = 842 - 839
dy = 480 - 473

lat=np.array([1.3555541629319738,1.3761181131876685])
lon=np.array([103.98020429181963,103.98891938905349])
x,y,_,_ = utm.from_latlon(lat,lon)
real_x = (x-x[0])[1]
real_y = (y-y[0])[1]
scale_x = dx/real_x
scale_y = dy/real_y

FILE_NAME = 'D:/simulator/MARL/utilities/departure_raw_traj.json'
with open(FILE_NAME,'r') as f:
    raw_traj = json.load(f)
traj = []
for sub in raw_traj:
    sub = np.array(sub)
    lat = sub[:,1]
    lon = sub[:,0]
    x,y,_,_ = utm.from_latlon(lat,lon)
    sub[:,0]= x*scale_x
    sub[:,1]= y*scale_y
    traj.append(list(map(list,(sub[:len(sub)-200]-np.array([1198.65,470.5114])))))
    ax.scatter(sub[:len(sub)-200,0],sub[:len(sub)-200,1], alpha=1,s = 0.1)
plt.show()
new_traj=  []
p = Polygon(np.array([[-0.40,-0.0538],[0.09,-0.0598],[-0.04,-0.0169]]))
for i in traj:
    for ind,j in enumerate(i):
        if p.contains(Point(j)):
            new_traj.append(i[ind::])
            break
with open('precessed_radar_departure.json','w') as f:
    json.dump(new_traj,f)
