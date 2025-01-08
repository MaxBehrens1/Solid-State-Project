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

folder = str(pathlib.Path(__file__).parent.resolve()) + r'/Data/High_temp_noise/'

file_list = os.listdir(folder)
std_v_s = []
std_v_d = []
for file in file_list:
    path = folder + file
    if file[0] == 's':
        time, x, y, Energy = ReadData(path, 'sommer')
        print(np.mean(Energy)*10)
        total_k = np.sqrt(x**2 + y**2)
        vel = total_k * hbar / m_e
        std_v_s.append(np.std(vel))
    else:
        times, _, y_data, x_data = ReadData(path, 'drude')
        total_v = np.sqrt((x_data*1e4)**2 + (y_data*1e4)**2)
        std_v_d.append(np.std(total_v))
        

# print(np.mean(std_v_s))
# print(np.std(std_v_s))
# print(std_v_s)

# print(np.mean(std_v_d))
# print(np.std(std_v_d))
# print(std_v_d)