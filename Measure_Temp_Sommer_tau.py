import os
import pathlib
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.constants import Boltzmann
try:
    from ReadData import ReadData
except:
    print('Unable to import ReadData')
    exit()

folder = str(pathlib.Path(__file__).parent.resolve()) + r'/Data/Temp_Ratio_Sommer/'
font = {'fontname':'Times New Roman'}

Fermi_E = 10

file_list = os.listdir(folder)
r_E = []
for file in file_list:
    tau_i = float(file[1:5])
    tau_e = float(file[7:11])
    time, x, y, Energy = ReadData(folder + file, 'sommer')
    index_cutoff = round(len(x)*0.3)
    E_data = Energy[index_cutoff:]
    mean_E = np.mean(E_data) * Fermi_E 
    r_E.append([round(tau_e/tau_i), mean_E])
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
def fit_func(x, a, b):
    return a*x/(b+x)

def inv_func(y, a, b):
    return b*y/(a-y)

par, cov = curve_fit(fit_func, r_mean_std[:,0], r_mean_std[:,1], sigma=r_mean_std[:,2])
x_val = np.linspace(min(r_mean_std[:,0]), max(r_mean_std[:,0]))
plt.plot(x_val, fit_func(x_val, *par), label = 'Fit', alpha = 0.7, color = 'black')
plt.errorbar(r_mean_std[:,0], r_mean_std[:,1], yerr=r_mean_std[:,2], linestyle='',
             label ='Data', fmt='o', ecolor='black', capsize=5, color='black')
plt.title('Sommerfeld Simulation \n Relation between temperature and R')
plt.xlabel('R (tau_e/tau_i)')
plt.ylabel('Excess Energy (eV)')
plt.legend()
plt.grid()
plt.show()

    