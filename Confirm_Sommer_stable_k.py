""" 
Confirming whether the equilibrium of the fermi sphere is consistent with model when only elastic collisions are present
Run for ~ tau_e*200
tau_i = 1e20
0.1 ps <= tau <= 10ps
We know that the E-field works as expected. So we will keep that constant at 1e6eV. 
dk/tau = -e E/hbar
"""
import os
import pathlib
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import hbar
try:
    from ReadData import ReadData
except:
    print('Unable to import ReadData')
    exit()

folder = str(pathlib.Path(__file__).parent.resolve()) + r'/Data/Confirm_sommerfeld_stable_k/'
font = {'fontname':'Times New Roman'}

file_list = os.listdir(folder)
tau = np.array([])
stable_k = np.array([])
stable_k_std = np.array([])
for file in file_list:
    path = folder + file
    current_tau = float(file[-10:-6])*1e-12 #Getting E-field from file name
    time, x, y, Energy = ReadData(path, 'sommer')
    index_cutoff = round(len(x)*0.1) #Assume that it takes tau*20 to reach equilibrium (actually its around tau*10)
    average_x = np.mean(x[index_cutoff:])
    std_x = np.std(x[index_cutoff:])
    tau = np.append(tau, current_tau)
    stable_k = np.append(stable_k, average_x)
    stable_k_std = np.append(stable_k_std, std_x)

gradient, c = np.polyfit(tau, stable_k, deg = 1)
excpected_grad = -1.6e-19 * 1e6 /hbar
error_grad = (gradient - excpected_grad)/gradient *100
print('Calculated -eE/hbar =', gradient, '. Error against expected =', error_grad)
plt.plot(tau, gradient*tau + c, label = 'Fit', alpha = 0.7, color = 'black')
plt.plot(tau, stable_k, 'o', label ='Data', color = 'black')
plt.title('Sommerfeld Simulation \n Confirming Fermi Sphere Stabalises at expected <k>')
plt.xlabel('$tau_e$ (s)')
plt.ylabel('<$k_x$> (1/m)')
plt.legend()
plt.grid()
plt.show()

    

