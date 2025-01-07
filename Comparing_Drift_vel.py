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

expected_grad = -1.60217663e-19 * 1e-12 / m_e

def mean_std(data):
    interval = len(data)//5
    means = []
    for ind in range(5):
        if ind != 4:
            mean_val = np.mean(data[ind*interval:(ind+1)*interval])
        else:
            mean_val = np.mean(data[ind*interval:])
        means.append(mean_val)
    return np.mean(means), np.std(means)

file_list = os.listdir(folder)
R_E_vel_err_s = []
R_E_vel_err_d = []
for file in file_list:
    path = folder + file
    if file[0] == 's':
        Ratio = 1/float(file[8:13])
        E_field = float(file[2:4])*1e6        
        time, x, y, Energy = ReadData(path, 'sommer')
        index_cutoff = round(len(x)*0.1) #To remove bit before equilibrium
        data_x = x[index_cutoff:] * hbar / m_e
        average_x, error_x = mean_std(data_x)
        R_E_vel_err_s.append([Ratio, E_field, average_x, error_x])
    else:
        E_field = float(file[2:4])*1e6
        times, _, y_data, x_data = ReadData(path, 'drude')
        index_cutoff = round(len(x_data)*0.01) #To remove bit before equilibrium
        x_data = x_data[index_cutoff:]*1e4
        average_x, error_x = mean_std(x_data)
        R_E_vel_err_d.append([E_field, average_x, error_x])
R_E_vel_err_s = np.array(R_E_vel_err_s)
R_E_vel_err_d = np.array(R_E_vel_err_d)


x_val = np.linspace(min(R_E_vel_err_s[:,1]), max(R_E_vel_err_s[:,1]))
symbols = ['.', '^', 'x', 'd', '*', 'p']
colors = ['k', 'b', 'g', 'r', 'c', 'm']

pos_ratios = list(set(R_E_vel_err_s[:,0]))
for i, val in enumerate(pos_ratios):
    cur_data = []
    for j in R_E_vel_err_s:
        if j[0] == val:
            cur_data.append([j[1],j[2], j[3]])
    cur_data = np.array(cur_data)
    cons = np.polyfit(cur_data[:,0], cur_data[:,1], 1, w=1/cur_data[:,2])
    plt.errorbar(cur_data[:,0], cur_data[:,1], cur_data[:,2], linestyle='',
             label =f'R={val:.2e}', fmt=symbols[i], ecolor=colors[i], capsize=2, markeredgecolor=colors[i],
                 markerfacecolor=colors[i], alpha = 0.5)
    plt.plot(x_val, x_val*cons[0] + cons[1], color = colors[i], alpha = 0.7)

#Plotting drude
cons = np.polyfit(R_E_vel_err_d[:,0], R_E_vel_err_d[:,1], 1, w=1/R_E_vel_err_d[:,2])
plt.errorbar(R_E_vel_err_d[:,0], R_E_vel_err_d[:,1], R_E_vel_err_d[:,2], linestyle='',
             label ='Drude', fmt='X', ecolor='y', capsize=2, markeredgecolor='y',
                 markerfacecolor='y', alpha = 0.5)
plt.plot(x_val, x_val*cons[0] + cons[1], color = 'y', alpha = 0.9)

#Plotting expected gradient 
plt.plot(x_val, x_val * expected_grad, linestyle='dashed', color = 'orange', label = 'Theory')

print(abs((expected_grad-cons[0])/cons[0]) * 100, '%')

#Put legend labels in nice order
handles, labels = plt.gca().get_legend_handles_labels()
order = [5,1,2,3,4,6,7,0]
plt.legend([handles[idx] for idx in order],[labels[idx] for idx in order])

plt.title('Sommerfeld Simulation \n Drift velocity agianst E-field')
plt.xlabel('E-field (V/m)')
plt.ylabel('Drift vel (m/s)')
plt.grid()
plt.show()