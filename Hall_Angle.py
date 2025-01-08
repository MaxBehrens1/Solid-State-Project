import os
import pathlib
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import m_e, e
try:
    from ReadData import ReadData
except:
    print('Unable to import ReadData')
    exit()

folder = str(pathlib.Path(__file__).parent.resolve()) + r'/Data/Hall_angle/'

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
angle_d = []
angle_s = []
for file in file_list:
    path = folder + file
    Btau = float(file[1:5])*1e-12 #From psT to sT
    if file[0] == 's':
        time, x, y, Energy = ReadData(path, 'sommer')
        R_val = float(file[8:14])
        average_x = np.mean(x)
        average_y = np.mean(y)
        angle = np.arctan(average_y/average_x)
        angle_s.append([Btau,angle,R_val])
    else:
        times, _, y_data, x_data = ReadData(path, 'drude')
        average_x = np.mean(x_data)
        average_y = np.mean(y_data)
        angle = np.arctan(average_y/average_x)
        angle_d.append([Btau,angle])
angle_d = np.array(angle_d)
angle_s = np.array(angle_s)

def arctangent(x):
    return np.arctan(x*e / m_e)
x_val = np.linspace(0, 20e-12, 1000)
symbols = ['.', '^', 'x', 'd', '*', 'p']
colors = ['k', 'b', 'g', 'r', 'c', 'm']

R_list = list(set(angle_s[:,2]))
for i, val in enumerate(R_list):
    cur_data = []
    for j in angle_s:
        if j[2] == val:
            cur_data.append([j[0],j[1]])
    cur_data = np.array(cur_data)
    plt.errorbar(cur_data[:,0], cur_data[:,1], linestyle='',
             label =f'R={val:.2e}', fmt=symbols[i], ecolor=colors[i], capsize=2, markeredgecolor=colors[i],
                 markerfacecolor=colors[i], alpha = 0.5)



plt.plot(x_val, arctangent(x_val), label = 'Theory')
plt.plot(angle_d[:,0], angle_d[:,1], 'x', label = 'Drude')

plt.legend()
plt.title('Hall Angle')
plt.xlabel('B tau')
plt.ylabel('Hall Angle')
plt.grid()
plt.show()