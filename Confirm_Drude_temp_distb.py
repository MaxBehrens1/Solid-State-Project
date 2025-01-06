"""
File to compare the speeds and temp of sommer and Drude model
"""
import numpy as np
from scipy.constants import m_e, k
import os
import csv
from pathlib import Path # this makes iterating easier
COLLATE_DATA = True 

# Set the folder where you keep things
data_folder = Path("C:/Users/arceu/OneDrive - The University of Manchester/Year 3/Estado Sólido/sss/Solid-State-Project/Data/Drude_current/")
file_name = "tau_1ps_T_5K_vel.txt" # you only need the name 
filename = data_folder / file_name 

def DrudeTemp(x_data, y_data):
    
    x_avg = np.mean(x_data)
    y_avg = np.mean(y_data)

    T = (x_avg+y_avg)*(10**8)*(m_e)/(2*k)
    print(f"T = {T:.4f}K")
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
    
    temp = filename.relative_to(data_folder)
    name = str(temp)
    # DrudeTemp(abs(x_data), abs(y_data))
    
    #This is for the Drude current comparison:
    return [name, abs(averages[1]), std[1]]
    
    
    
# Define the folder and output file
output_name = input("Name the output file (xyz.csv) (CHECK EXISTING FILES SO AS TO NOT OVERWRITE): ")
output_file = Path(output_name)

Analysis(filename)

# %% COLLATE DATA 

if COLLATE_DATA:
    # Collect results for each file
    results = []
    for file in data_folder.iterdir():
        temp = file.relative_to(data_folder)
        print(str(temp))
        if file.is_file() and file.suffix == '.txt':  # Filter for text files
            result = Analysis(file)
            if result:  # If valid result, add to list
                results.append(result)
    
    # Write results to a CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["file_name", "average_x_data", "std_x_data"])  # header
        writer.writerows(results)
    
    print(f"Results compiled into {output_file}")
    
