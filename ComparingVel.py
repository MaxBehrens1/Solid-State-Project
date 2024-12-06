"""
File to compare the speeds and temp of sommer and Drude model
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.constants import hbar, m_e, k

try:
    from ReadData import ReadData
except:
    print('Unable to import ReadData')
    
def rms(data):
    sqaured_sum = 0
    for i in data:
        sqaured_sum += i*i
    final_rms = np.sqrt(sqaured_sum/len(data))
    return final_rms

sommer_file = r'/Users/maxbehrens/OneDrive - UAM/Solid State/Solid-State-Project/Data/sommer_basic.txt'
sommer_datatime, sommer_datax, sommer_datay, sommer_dataE = ReadData(filename=sommer_file, sim_type='sommer')
min_index = round(len(sommer_datax)*0.25)
sommer_datax, sommer_datay = sommer_datax[min_index:], sommer_datay[min_index:]

sommer_totalk = []
for j in range(len(sommer_datax)):
    sommer_totalk.append(np.sqrt(sommer_datax[j]**2 + sommer_datay[j]**2))
    
sommmer_average_v = hbar*rms(sommer_totalk)/m_e
print('Average vel:', sommmer_average_v)
sommer_temp = (m_e*sommmer_average_v**2) / (3*k)
print('Temp:', sommer_temp)

