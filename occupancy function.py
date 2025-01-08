import numpy as np
import matplotlib.pyplot as plt

x_data = np.linspace(0, 5, 1000)
mu = 1
T=0.4  # use T values from 0.1 to 3-4K for good results (this is a mock-up)
y_MB = np.exp(-(x_data-mu)/T)
y_FD = 1/(np.exp((x_data-mu)/T)+1)


ylabel = r'$\bar{n}$'

plt.plot(x_data, y_MB, label = "Maxwell-Boltzmann")
plt.plot(x_data,y_FD, label = "Fermi-Dirac")
plt.vlines(mu,0,5, ls='--', color = 'r', alpha = 0.5,)
plt.text(mu+0.2, 4, f'μ = {mu}eV', color='r', fontsize='14')
plt.xlabel("Energy \\eV")
plt.ylabel(ylabel)
plt.ylim(0,5)
plt.legend()
plt.savefig("hightempcomp.png", dpi=400)
plt.show()
plt.close()