#Written by Soheil Jamali
#sjamali@uark.edu, soheil.jamali.dev@gmail.com
#University of Arkansas, Fayetteville, AR, USA

#Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import uniform_filter1d

# Load .xvg file such as pressure.xvg
data = np.loadtxt('pressure.xvg', comments=['@', '#'])

# First column = x, second column = y
x = data[:, 0]
y = data[:, 1]

# Apply a smoothing filter for the line (adjust size for smoothness)
y_smooth = uniform_filter1d(y, size=10)

# Plot black scatter points. you can change the size and color of the points.
plt.scatter(x, y, color='black', s=10, label='Raw data')

# Plot smooth blue line. You can change the line width and color.
plt.plot(x, y_smooth, color='blue', linewidth=1.5, label='Smoothed')

# Labels and title
plt.xlabel('Time (ps)', fontsize=14) # You can change the x-axis label
plt.ylabel('Pressure (bar)', fontsize=14) # You can change the y-axis label
plt.title('Pressure, NPT Equilibration', fontsize=16) # You can change the title

# Legend
plt.legend()

# Save & show
plt.tight_layout() # Adjust layout to prevent clipping
plt.savefig('pressure.png', dpi=300) # Save as PNG file with 300 dpi
plt.show() # Display the plot
