import os
import pathlib
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
try:
    from ReadData import ReadData
except:
    print('Unable to import ReadData')
    exit()

folder = str(pathlib.Path(__file__).parent.resolve()) + r'/Data/DeltaE_dependance_sommer/'

Fermi_E = 10
file_list = os.listdir(folder)
dE_E = []
for file in file_list:
    if file[5] != '_':
        continue
    deltaE = float(file[1:5])
    time, x, y, Energy = ReadData(folder + file, 'sommer')
    index_cutoff = round(len(Energy)*0.1)
    E_data = Energy[index_cutoff:]
    mean_E = np.mean(E_data) * Fermi_E
    dE_E.append([deltaE, mean_E])
dE_E = np.array(dE_E)
values_r = list(set(dE_E[:,0]))

E_mean = []
errors = []
for r in values_r:
    data_r = []
    for data in dE_E:
        if data[0] == r:
            data_r.append(data[1])
    r_mean = np.mean(data_r)
    r_error = [abs(r_mean - min(data_r)),abs(r_mean - max(data_r))]
    E_mean.append([r, r_mean])
    errors.append(r_error)

E_mean = np.array(E_mean)

def fit_func(x, a, b, c, d):
    return a/x + b*np.exp(c*x) + d

fig = plt.figure()
ax = fig.add_subplot(111)

ax.grid('on')
ax.spines['right'].set_color((.6, .6, .6))
ax.spines['top'].set_color((.6, .6, .6))
ax.spines['left'].set_color((0, 0, 0))
ax.spines['bottom'].set_color((0, 0, 0))

de = r'$\Delta E$'

x_val = np.linspace(0.05, max(E_mean[:,0]), 1000)
par, cov = curve_fit(fit_func, E_mean[:,0], E_mean[:,1], sigma=[np.mean(i) for i in errors])
ax.plot(x_val, fit_func(x_val, *par), alpha = 0.5, label = 'Fit', color='black')
ax.errorbar(E_mean[:,0], E_mean[:,1], yerr=np.transpose(errors), linestyle='',
             label ='Data', fmt='o', ecolor='black', capsize=5, markeredgecolor='black',
                 markerfacecolor='white', alpha = 0.9)
ax.set_title('Sommerfeld Simulation \n Relation between ' + de + ' and ' + r'$\langle$E$\rangle$')
ax.set_xlabel(de + '(eV)')
ax.set_ylabel('Excess Energy (eV)')
ax.legend()
plt.savefig("Graphs/Relation_between_dE_E.png", dpi=400)
plt.show()


    