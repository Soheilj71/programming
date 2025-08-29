# Written by Soheil Jamali
# Email: sjamali@uark.edu, soheil.jamali.dev@gmail.com
# University of Arkansas, Fayetteville, AR, USA

#Loading the libraries
import numpy as np
import matplotlib.pyplot as plt

# Load data, skipping comment lines
data = np.loadtxt('pressure.xvg', comments=['@', '#']) #You can paste any .xvg file here

# Assuming first column is x and second is y
x = data[:, 0]
y = data[:, 1]

plt.plot(x, y)
plt.xlabel('Time (ps)') #You can change it based on your xvg file (e.g., Time, Distance, RMSD, etc.)
plt.ylabel('Pressure (bar)') #You can change it based on your xvg file (e.g., Energy, RMSD, etc.)
plt.title('Pressure, NPT Equilibration') #You can change it based on your xvg file (e.g., Energy, RMSD, etc.)
plt.savefig('pressure.png') #You can change the name of the output figure
plt.show() #This will display the figure in a pop-up window

