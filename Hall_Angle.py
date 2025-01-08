import os
import pathlib
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import m_e
try:
    from ReadData import ReadData
except:
    print('Unable to import ReadData')
    exit()

folder = str(pathlib.Path(__file__).parent.resolve()) + r'/Data/Hall_angle/'

file_list = os.listdir(folder)
angle_d = []
for file in file_list:
    path = folder + file
    Btau = float(file[1:5])*1e-12 #From psT to sT
    if file[0] == 's':
        time, x, y, Energy = ReadData(path, 'sommer')
    else:
        try:
            times, _, y_data, x_data = ReadData(path, 'drude')
        except:
            print('Failed:', file)
            continue
        average_x = np.mean(x_data)
        average_y = np.mean(y_data)
        angle = np.arctan(average_y/average_x)
        angle_d.append([Btau,angle])
angle_d = np.array(angle_d)

def arctangent(x):
    return np.arctan(x*1.6e-19 / m_e)

x_val = np.linspace(0, 20e-12, 1000)
plt.plot(x_val, arctangent(x_val))
plt.plot(angle_d[:,0], angle_d[:,1], 'x')
plt.show()