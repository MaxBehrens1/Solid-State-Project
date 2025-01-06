"""
File to compare the speeds and temp of sommer and Drude model
"""
import numpy as np
from scipy.constants import m_e, k
import os

from pathlib import Path

data_folder = Path("C:/Users/arceu/OneDrive - The University of Manchester/Year 3/Estado Sólido/sss/Solid-State-Project/Data/Drude_current/")

def DrudeTemp(x_data, y_data):
    x_avg = np.mean(x_data)
    y_avg = np.mean(y_data)

    T = (x_avg+y_avg)*(10**8)*(m_e)/(2*k)
    print(f"T = {T:.4f}K")
def Analysis():
    try:
        from ReadData import ReadData
    except:
        print('Unable to import ReadData')
        exit()
    
    #filename = "C:/Users/arceu/OneDrive - The University of Manchester/Year 3/Estado Sólido/sss/Solid-State-Project/Data/Drude_current/tau_1ps_T_5K_vel.txt"
    #filename = r'/Users/maxbehrens/OneDrive - UAM/Solid State/Solid-State-Project/Data/Confirm_Drude_temperature_distb/mean_sq_dev_vel_for_t_5e-1ps.txt'
    file_name = "tau_1ps_T_5K_vel.txt"
    filename = data_folder / file_name
    

    
    times, E_field, y_data, x_data,  = ReadData(filename, 'drude')
    
    averages = [np.mean(i) for i in (times, x_data, y_data, E_field)]
    for i, avg in enumerate(averages):
        print(f"Average for data[{i}] is {avg:.4f}")
    print("Data: ", file_name)
    
    #This is for the Drude current comparison:
    dataset = [file_name, averages[1],averages[2]]
    
    DrudeTemp(abs(x_data), abs(y_data))