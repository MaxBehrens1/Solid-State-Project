import os
import pathlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator
from matplotlib import cm
try:
    from ReadData import ReadData
except:
    print('Unable to import ReadData')
    exit()

folder = str(pathlib.Path(__file__).parent.resolve()) + r'/Data/Ratio_E/'
font = {'fontname':'Times New Roman'}

file_list = os.listdir(folder)
r_E = []
for file in file_list:
    tau_i = float(file[1:5])
    tau_e = float(file[7:11])
    time, x, y, Energy = ReadData(folder + file, 'sommer')
    index_cutoff = round(len(x)*0.3)
    E_data = Energy[index_cutoff:]
    mean_E = np.mean(E_data)
    r_E.append([tau_e/tau_i, mean_E])

r_E = np.array(r_E)
values_r = list(set(r_E[:,0]))

r_mean_std = []
for r in values_r:
    data_r = []
    for data in r_E:
        if data[0] == r:
            data_r.append(data[1])
    r_mean = np.mean(data_r)
    r_std = np.std(data_r)
    r_mean_std.append([r, r_mean, r_std])

r_mean_std = np.array(r_mean_std)
plt.plot(r_mean_std[:,0], r_mean_std[:,1], 'o')
plt.errorbar(r_mean_std[:,0], r_mean_std[:,1], yerr=r_mean_std[:,2], linestyle='')

plt.show()

    