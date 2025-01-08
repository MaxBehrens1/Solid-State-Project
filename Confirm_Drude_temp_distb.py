"""
File to compare the speeds and temp of sommer and Drude model
"""
import numpy as np
from scipy.constants import m_e, k
import os
import csv
from pathlib import Path # this makes iterating easier
import matplotlib.pyplot as plt
import seaborn as sns
COLLATE_DATA = False

# Set the folder where you keep things
data_folder = Path("C:/Users/arceu/OneDrive - The University of Manchester/Year 3/Estado Sólido/sss/Solid-State-Project/Data/Drude_current/")
file_name = "tau_1ps_T_5K_vel.txt" # you only need the name 
filename = data_folder / file_name 

def DrudeTemp(x_data, y_data):
    
    x_avg = np.mean(x_data)
    y_avg = np.mean(y_data)

    T = (x_avg+y_avg)*(10**8)*(m_e)/(2*k)
    print(f"T = {T:.4f}K")
def weighted_average(y_data, y_errs):
    weights = 1 / (y_errs**2)
    weighted_avg = np.sum(y_data * weights) / np.sum(weights)
    weighted_avg_err = np.sqrt(1 / np.sum(weights))
    
    return weighted_avg, weighted_avg_err
def Analysis(filename):
    try:
        from ReadData import ReadData
    except:
        print('Unable to import ReadData')
        exit()
    
    # calling main analysis function
    times, E_field, y_data, x_data,  = ReadData(filename, 'drude')
    
    averages = [np.mean(i) for i in (times, x_data, y_data, E_field)]
    std = [np.std(i) for i in (times, x_data, y_data, E_field)]
    #for i in range(4):
    #    print(f"(Average,std) for data[{i}] is ({averages[i]:.4f}, {std[i]:.4f}).")
    #print("Data: ", file_name)
    
    parts = str(filename).split("_")
    for part in parts:
        if part.endswith("K"):
            temperature = int(part[:-1])  # Remove the 'K' and convert to int
            print(f"Temperature: {temperature} K")
            break
    # DrudeTemp(abs(x_data), abs(y_data))
    
    #This is for the Drude current comparison:
    return [temperature, abs(averages[1]), std[1]]
    
    
    
# Define the folder and output file


Analysis(filename)

# %% COLLATE DATA 

if COLLATE_DATA:
    output_name = input("Name the output file (xyz.csv) (CHECK EXISTING FILES SO AS TO NOT OVERWRITE): ")
    output_file = Path(output_name)
    # Collect results for each file
    results = []
    for file in data_folder.iterdir():
        temp = file.relative_to(data_folder)
        print(str(temp))
        if file.is_file() and str(file).endswith('vel.txt'):  # Filter for text files
            result = Analysis(file)
            if result:  # If valid result, add to list
                results.append(result)
    
    # Write results to a CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["file_name", "average_x_data", "std_x_data"])  # header
        writer.writerows(results)
    
    print(f"Results compiled into {output_file}")
    
data = np.genfromtxt("Drude_Current.csv", delimiter=',', skip_header=1)
temps = data[:,0]
vel = data[:,1] * 10000
vel_errs =  data[:,2] * 10000


fig = plt.figure()
axes = fig.add_subplot(111)


axes.grid('on')
axes.spines['right'].set_color((.6, .6, .6))
axes.spines['top'].set_color((.6, .6, .6))
axes.spines['left'].set_color((0, 0, 0))
axes.spines['bottom'].set_color((0, 0, 0))

axes.errorbar(temps, vel, vel_errs, ls = 'none', fmt = 'o', 
             label = r'$\tau$ = 1ps', capsize=2, color = 'black')
axes.set_title(r'Variation of Drift Velocity with $T_D$')
axes.set_xlabel(r'Temperature $T_D$ (K)')
axes.set_ylabel(r'Drift vel (ms$^{-1}$)')
axes.legend()
plt.savefig("Drude_fixed_Tau_varying_T_drift_vel.png", dpi=400)
plt.show()

