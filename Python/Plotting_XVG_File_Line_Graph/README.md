# 📈 Pressure Plot from GROMACS .xvg File

This repository contains a simple Python script to read and visualize pressure data from a GROMACS output file (such as pressure.xvg).
The script uses NumPy for data handling and Matplotlib for plotting.


## 📌 Features
-  Loads .xvg file while ignoring GROMACS comment lines (@, #).
-  Extracts time (ps) and pressure (bar) columns.
-  Creates a line plot of pressure vs. time.
-  Saves the plot as pressure.png.

## 📂 File Structure

```
├── pressure.xvg      # Input data file from GROMACS
├── plot_pressure.py  # Python script for plotting
└── README.md         # Documentation
```

## ⚙️ Requirements

Make sure you have Python 3.x installed and the following packages:
```bash
pip install numpy matplotlib
```
## 🚀 Usage
1. Place your pressure.xvg file in the same directory as the script.
2. Run the script:
```pythin
python plot_pressure.py
```

The plot will be:
-  Displayed on screen.
-  Saved as pressure.png in the current directory.

# 🖼 Example Output

Pressure vs. Time Plot

The output will look similar to this:
```
X-axis: Time (ps)
Y-axis: Pressure (bar)
Title: Pressure, NPT Equilibration

```

<img width="480" height="720" alt="pressure" src="https://github.com/user-attachments/assets/46fd63a5-bbeb-4631-a308-bb97cec79723" />

## 🧪 Notes
This script assumes:
-  First column = time (ps)
-  Second column = pressure (bar)
-   you can easily adapt it to plot other .xvg data types by changing labels and titles.
-   .xvg files are typically generated during GROMACS simulations using:
 gmx energy -f npt.edr -o pressure.xvg
 
