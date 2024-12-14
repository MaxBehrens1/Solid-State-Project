""" 
Script to confirm whether the E-field in sommerfeld simulation acts as expected
Plot dk/dt against E-field
Gradient is expected to be -e/hbar
0.1e6 <= E_x < 10e6 in jumps of 0.9
E_fermi = 10eV (arbitrary)
A = 50 Amstrongs (arbitary)
Both tau_i and tau_e = 1e20
Run all simulations on speed 1 for ~ 50 ps
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import hbar
try:
    from ReadData import ReadData
except:
    print('Unable to import ReadData')

folder = r'/Users/maxbehrens/OneDrive - UAM/Solid State/Solid-State-Project/Data/Confirm_sommerfeld_moving_k/'
file_list = os.listdir(folder)
E_val = np.array([])
gradients = np.array([])
for file in file_list:
    path = folder + file
    E_field = float(file[-7:-4])*1e6 #Getting E-field from file name
    time, x, y, Energy = ReadData(path, 'sommer')
    time, x, y = time*1e-12, x*1e10, y*1e10 #Converting to SI units
    grad, c = np.polyfit(time, x, deg = 1)
    E_val = np.append(E_val, E_field)
    gradients = np.append(gradients, grad)
    plt.plot(time, x)
    plt.show()

gradient, c = np.polyfit(E_val, gradients, deg = 1)
excpected_grad = -1.6e-19/hbar
error_grad = (gradient - excpected_grad)/gradient *100
print('Calculated -e/hbar =', gradient, '. Error against expected =', error_grad)
plt.plot(E_val, gradient*E_val + c, label = 'Fit', alpha = 0.7, color = 'black')
plt.plot(E_val, gradients, 'o', label ='Data', color = 'black')
plt.legend()
plt.show()
    
    

    


    
