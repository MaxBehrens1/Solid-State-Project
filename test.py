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

folder = str(pathlib.Path(__file__).parent.resolve()) + r'/Data/Ratio_E_sommer/'
font = {'fontname':'Times New Roman'}

Fermi_E = 10

file_list = os.listdir(folder)
r_E = []
for file in file_list:
    ratio = float(file[1:4])
    time, x, y, Energy = ReadData(folder + file, 'sommer')
    index_cutoff = round(len(Energy)*0.1)
    E_data = Energy[index_cutoff:]
    mean_E = np.mean(E_data) * Fermi_E
    r_E.append([ratio, mean_E])
r_E = np.array(r_E)

def fit_func(x, a, b):
    return a*x/(b+x)

# par, cov = curve_fit(fit_func, r_E[:,0], r_E[:,1])
# x_val = np.linspace(0, max(r_E[:,0]), 10000)
# plt.plot(x_val, fit_func(x_val, *par), label = 'Fit', alpha = 0.7, color = 'black')
plt.errorbar(r_E[:,0], r_E[:,1], linestyle='',
             label ='Data', fmt='o', ecolor='black', capsize=5, color='black')
plt.title('Sommerfeld Simulation \n Relation between temperature and R')
plt.xlabel('R (tau_e/tau_i)')
plt.ylabel('Excess Energy (eV)')
plt.legend()
plt.grid()
plt.show()

    