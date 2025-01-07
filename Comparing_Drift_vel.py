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
    index_cutoff = round(len(x)*0.1) #To remove 
    average_x = np.mean(x[index_cutoff:])*1e10
    vel = hbar * average_x / m_e
    E_vel.append([Ratio, E_field, vel])
E_vel = np.array(E_vel)

plt.plot(E_vel[:,1], E_vel[:,2], 'o', label ='Data', color = 'black')
plt.title('Sommerfeld Simulation \n Drift velocity agianst E-field')
plt.xlabel('$E-field (V/m)')
plt.ylabel('Drift vel (m/s)')
plt.legend()
plt.grid()
plt.show()