import os
import pathlib
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import m_e, e
from scipy.optimize import curve_fit
try:
    from ReadData import ReadData
except:
    print('Unable to import ReadData')
    exit()

folder = str(pathlib.Path(__file__).parent.resolve()) + r'/Data/Hall_angle/'

def mean_std(data_x, data_y):
    interval = len(data_x)//5
    angles = []
    for ind in range(5):
        if ind != 4:
            mean_x = np.mean(data_x[ind*interval:(ind+1)*interval])
            mean_y = np.mean(data_y[ind*interval:(ind+1)*interval])
            cur_angle = np.arctan(mean_y/mean_x)
        else:
            mean_x = np.mean(data_x[ind*interval:])
            mean_y = np.mean(data_y[ind*interval:])
            cur_angle = np.arctan(mean_y/mean_x)
        angles.append(cur_angle)
    return np.mean(angles), np.std(angles)

def fit_function(Btau, alpha):
    return np.arctan(alpha * Btau * e / m_e)

file_list = os.listdir(folder)
angle_d = []
angle_s = []
for file in file_list:
    path = folder + file
    Btau = float(file[1:5])*1e-12 #From psT to sT
    if file[0] == 's':
        time, x, y, Energy = ReadData(path, 'sommer')
        R_val = float(file[8:14])
        average_angle, error_angle = mean_std(x, y)
        angle_s.append([Btau,average_angle,R_val, error_angle])
    else:
        times, _, y_data, x_data = ReadData(path, 'drude')
        average_angle, error_angle = mean_std(x_data, y_data)
        angle_d.append([Btau,average_angle, error_angle])
angle_d = np.array(angle_d)
angle_s = np.array(angle_s)

def arctangent(x):
    return np.arctan(x*e / m_e)

x_val = np.linspace(0, 20e-12, 1000)
symbols = ['.', '^', 'x', 'd', '*', 'p']
colors = ['k', 'b', 'g', 'r', 'c', 'm']
fig = plt.figure()
ax = fig.add_subplot(111)


ax.grid('on')
ax.spines['right'].set_color((.6, .6, .6))
ax.spines['top'].set_color((.6, .6, .6))
ax.spines['left'].set_color((0, 0, 0))
ax.spines['bottom'].set_color((0, 0, 0))

R_list = list(set(angle_s[:,2]))
fit_params = {}
x_fit = np.linspace(0, 2e-11, 1000)
sommer_fits = {}
for i, val in enumerate(R_list):
    cur_data = []
    for j in angle_s:
        if j[2] == val:
            cur_data.append([j[0],j[1], j[3]])
    cur_data = np.array(cur_data)
    
    Btau_vals = cur_data[:, 0]
    angles = cur_data[:, 1]
    angle_errs = cur_data[:, 2]
    
    # Perform curve fitting
    popt, pcov = curve_fit(fit_function, Btau_vals, angles, sigma=angle_errs, absolute_sigma=True)
    alpha = popt[0]
    alpha_err = np.sqrt(np.diag(pcov))[0]
    fit_params[val] = (alpha, alpha_err)
    sommer_fits[val] = fit_function(x_fit, alpha)
    
# Curve fit for Drude data
popt, pcov = curve_fit(fit_function, angle_d[:, 0], angle_d[:, 1], sigma=angle_d[:, 2], absolute_sigma=True)
alpha_drude = popt[0]
alpha_drude_err = np.sqrt(np.diag(pcov))[0]
drude_fit = fit_function(x_fit, alpha_drude)

# Print results
print("Sommer model fit parameters:")
for R_val, (alpha, alpha_err) in fit_params.items():
    print(f"R={R_val:.2e}: alpha={alpha:.4e} ± {alpha_err:.4e}")
print("\nDrude model fit parameters:")
print(f"alpha={alpha_drude:.4e} ± {alpha_drude_err:.4e}")


for i, val in enumerate(R_list):
    cur_data = []
    for j in angle_s:
        if j[2] == val:
            cur_data.append([j[0], j[1], j[3]])
    cur_data = np.array(cur_data)
    ax.errorbar(cur_data[:, 0], cur_data[:, 1], cur_data[:, 2], linestyle='', 
                label=r'R$_{\tau}$' + f'={val:.0e}', fmt=symbols[i], ecolor=colors[i], capsize=2, 
                markeredgecolor=colors[i], markerfacecolor=colors[i], alpha=0.5)
    
    # Add fitted curve for this R value
    ax.plot(x_fit, sommer_fits[val], linestyle='--', color=colors[i])


ax.plot(x_val, arctangent(x_val), label = 'Theory')
ax.plot(x_fit, drude_fit, linestyle='--', color='m')
ax.errorbar(angle_d[:,0], angle_d[:,1], angle_d[:,2], linestyle='',
             label ='Drude', fmt=symbols[-1], ecolor=colors[-1], capsize=2, markeredgecolor=colors[-1],
                 markerfacecolor=colors[-1], alpha = 0.5)

#Put legend labels in nice order
handles, labels = plt.gca().get_legend_handles_labels()
order = [0,4,3,1,2]
ax.legend([handles[idx] for idx in order],[labels[idx] for idx in order])

ax.set_title('Variation of Hall Angle with Magnetic Field Strength')
ax.set_xlabel(r'B$\tau$ (T$\cdot$s)')
ax.set_ylabel('Hall Angle (rad)')
plt.savefig("Graphs/Hall_angle.png",dpi=400)
plt.show()