"""
File to compare the speeds and temp of sommer and Drude model
"""
import numpy as np
from scipy.constants import m_e, k

try:
    from ReadData import ReadData
except:
    print('Unable to import ReadData')
    exit()

#filename = "C:/Users/User/OneDrive - The University of Manchester/Year 3/Estado Sólido/sss/Solid-State-Project/Data/mean_sq_dev_vel_for_t_5e-1ps.txt"
filename = r'/Users/maxbehrens/OneDrive - UAM/Solid State/Solid-State-Project/Data/Confirm_Drude_temperature_distb/mean_sq_dev_vel_for_t_5e-1ps.txt'

def DrudeTemp(x_data, y_data):
    x_avg = np.mean(x_data)
    y_avg = np.mean(y_data)

    T = (x_avg+y_avg)*(10**8)*(m_e)/(2*k)
    print(f"T = {T:.4f}K")

times, x_data, y_data, E_field = ReadData(filename, 'drude')

averages = [np.mean(i) for i in (times, x_data, y_data, E_field)]
for i, avg in enumerate(averages):
    print(f"Average for data[{i}] is {avg:.4f}")

DrudeTemp(x_data, y_data)

