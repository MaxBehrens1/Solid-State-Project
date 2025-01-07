import os
import pathlib
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import hbar, m_e
try:
    from ReadData import ReadData
except:
    print('Unable to import ReadData')
    exit()
    
folder = str(pathlib.Path(__file__).parent.resolve()) + r'/Data/Comparing_Drift_vel/'

file_list = os.listdir(folder)
E_vel = []
for file in file_list:
    path = folder + file
    Ratio = float(file[8:13])
    E_field = float(file[2:4])*1e6        
    time, x, y, Energy = ReadData(path, 'sommer')
    index_cutoff = round(len(x)*0.1) #To remove bit before equilibrium
    average_x = np.mean(x[index_cutoff:])
    vel = hbar * average_x / m_e
    E_vel.append([Ratio, E_field, vel])
E_vel = np.array(E_vel)

symbols = ['.', '^', 'x', 'd', '*', 'p']
colors = ['k', 'b', 'g', 'r', 'c', 'm']

pos_ratios = list(set(E_vel[:,0]))
x_val = np.linspace(min(E_vel[:,1]), max(E_vel[:,1]))
for i, val in enumerate(pos_ratios):
    cur_data = []
    for j in E_vel:
        if j[0] == val:
            cur_data.append([j[1],j[2]])
    cur_data = np.array(cur_data)
    cons = np.polyfit(cur_data[:,0], cur_data[:,1], 1)
    plt.plot(cur_data[:,0], cur_data[:,1], symbols[i], label =f'R={val}', color = colors[i], alpha = 0.6)
    plt.plot(x_val, x_val*cons[0] + cons[1], color = colors[i], alpha = 0.3)
    


plt.title('Sommerfeld Simulation \n Drift velocity agianst E-field')
plt.xlabel('$E-field (V/m)')
plt.ylabel('Drift vel (m/s)')
plt.legend()
plt.grid()
plt.show()