
import numpy as np
import copy
import json
import matplotlib.pyplot as plt
import numpy as np

FILE_NAME = './data/final_adjusted_coord.json'
with open(FILE_NAME,'r') as f:
    raw_traj = json.load(f)['raw_traj']
processed_traj = [[] for _ in range(4)]
for ind,sub in enumerate(raw_traj):
    for line in sub:
        processed_traj[ind].append(np.array(line)+ np.array([839,480])+np.array([-10,-10]))
traj_ = [[] for _ in range(4)]
for ind,i in enumerate(processed_traj):
    for j in i:
        traj = np.array(j)
        rotation_matrix = np.array([[np.cos(1.166879),-np.sin(1.166879)],[np.sin(1.166879),np.cos(1.166879)]])
        traj = rotation_matrix.dot(traj.T).T
        traj[:,0] = traj[:,0]/0.012177966 - np.array([-8600.9]) + np.array([220])
        traj[:,1] = traj[:,1]/0.023095238 -  np.array([41002.9]) + np.array([60])
        traj_[ind].append(traj)
tmp = []
for j in traj_:
    for i in j:
        tmp+=list(i)
tmp = np.array(tmp)
fig = plt.figure(figsize=(20,20))
ax = fig.add_subplot(111, title="traj")
ax.scatter(tmp[:,0],tmp[:,1], alpha=1,s = 0.1)
plt.show()
print('done')

out_put = [[] for _ in range(4)]
for ind,i in enumerate(traj_):
    for j in i:
        last = 0
        for tmp in j[::-1]:
            if tmp[0] > 1000:
                print(last)
                break
            last+=1

        out_put[ind].append(len(j)-last)

with open('timeline_cutoff.json','w') as fout:
    json.dump({'cut_off':out_put}, fout)
