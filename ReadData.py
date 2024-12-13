import numpy as np
import matplotlib.pyplot as plt
from itertools import groupby

def ReadData(filename):
    """_summary_

    Args:
        filename: Full filepath to data

    Returns:
        data: time (ps), x (1/A), y (1/A), E (eV)
    """
    #Read in the data
    array_list = []
    with open(filename) as f_data:    
        for k, g in groupby(f_data, lambda x: x.startswith('&')):
            if not k:
                array_list.append(np.array([[float(x) for x in d.split()] for d in g if len(d.strip())]))
    array_list = np.array(array_list[:3])
    return array_list[0,:,0], array_list[1,:,1], array_list[0,:,1], array_list[2,:,1]

        



    

