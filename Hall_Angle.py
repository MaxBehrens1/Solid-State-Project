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

def mean_std(data_x, data_y):
    interval = len(data_x)//5
    angles = []
    for ind in range(5):
        if ind != 4:
            mean_x = np.mean(data_x[ind*interval:(ind+1)*interval])
            mean_y = np.mean(data_y[ind*interval:(ind+1)*interval])
            cur_angle = np.arctan(mean_y/mean_x)
        else:
            mean_x = np.mean(data_x[ind*interval:])
            mean_y = np.mean(data_y[ind*interval:])
            cur_angle = np.arctan(mean_y/mean_x)
        angles.append(cur_angle)
    return np.mean(angles), np.std(angles)

file_list = os.listdir(folder)
angle_d = []
angle_s = []
for file in file_list:
    path = folder + file
    Btau = float(file[1:5])*1e-12 #From psT to sT
    if file[0] == 's':
        time, x, y, Energy = ReadData(path, 'sommer')
        R_val = float(file[8:14])
        average_angle, error_angle = mean_std(x, y)
        angle_s.append([Btau,average_angle,R_val, error_angle])
    else:
        times, _, y_data, x_data = ReadData(path, 'drude')
        average_angle, error_angle = mean_std(x_data, y_data)
        angle_d.append([Btau,average_angle, error_angle])
angle_d = np.array(angle_d)
angle_s = np.array(angle_s)

def arctangent(x):
    return np.arctan(x*e / m_e)
x_val = np.linspace(0, 20e-12, 1000)
symbols = ['.', '^', 'x', 'd', '*', 'p']
colors = ['k', 'b', 'g', 'r', 'c', 'm']
fig = plt.figure()
ax = fig.add_subplot(111)


ax.grid('on')
ax.spines['right'].set_color((.6, .6, .6))
ax.spines['top'].set_color((.6, .6, .6))
ax.spines['left'].set_color((0, 0, 0))
ax.spines['bottom'].set_color((0, 0, 0))

R_list = list(set(angle_s[:,2]))
for i, val in enumerate(R_list):
    cur_data = []
    for j in angle_s:
        if j[2] == val:
            cur_data.append([j[0],j[1], j[3]])
    cur_data = np.array(cur_data)
    ax.errorbar(cur_data[:,0], cur_data[:,1], cur_data[:,2], linestyle='',
             label =f'R={val:.2e}', fmt=symbols[i], ecolor=colors[i], capsize=2, markeredgecolor=colors[i],
                 markerfacecolor=colors[i], alpha = 0.5)


ax.plot(x_val, arctangent(x_val), label = 'Theory')
ax.errorbar(angle_d[:,0], angle_d[:,1], angle_d[:,2], linestyle='',
             label =f'R={val:.2e}', fmt=symbols[-1], ecolor=colors[-1], capsize=2, markeredgecolor=colors[-1],
                 markerfacecolor=colors[-1], alpha = 0.5)

ax.legend()
ax.set_title('Hall Angle')
ax.set_xlabel('B tau')
ax.set_ylabel('Hall Angle')
plt.show()