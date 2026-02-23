# Alanine Dipeptide Backbone Dihedral Calculator

This script computes backbone dihedral angles **ϕ (phi)**, **ψ (psi)**, and **ω (omega)** for **alanine dipeptide** from a molecular dynamics trajectory using **MDAnalysis**.

It works with common topology and trajectory formats such as:

- Topology: `PDB`, `PSF`, `PRMTOP`
- Trajectory: `DCD`, `XTC`, `TRR`

The script saves results in both:
- ✅ NumPy format (`.npz`)
- ✅ CSV format (`.csv`) for Excel or plotting

---

## 📌 What This Script Does

1. Loads a molecular structure (topology)
2. Loads a trajectory (coordinates over time)
3. Identifies the alanine (ALA) residue
4. Finds neighboring residues (required for dihedrals)
5. Computes:
   - Phi (ϕ)
   - Psi (ψ)
   - Omega (ω)
6. Saves angles (in degrees) for all frames

---

## 📚 Background

In proteins and peptides:

- **Phi (ϕ)** = C(prev) – N – CA – C  
- **Psi (ψ)** = N – CA – C – N(next)  
- **Omega (ω)** = CA – C – N(next) – CA(next)

For alanine dipeptide, the system typically looks like:
ACE – ALA – NME


---

## ⚙️ Requirements

Install dependencies:

```bash
pip install numpy MDAnalysis

Python version: 3.8+
```
🚀 How to Run
Basic usage:
python dihedrals.py -t topol.pdb -x traj.xtc
Full example:

python dihedrals.py \
    -t topol.pdb \
    -x traj.xtc \
    -o backbone_dihedrals.npz \
    --csv backbone_dihedrals.csv

🧾 Command Line Arguments
Argument	Description
-t / --top	Topology file (required)
-x / --traj	Trajectory file (required)
-o / --out	Output NumPy filename (default: backbone_dihedrals.npz)
--csv	Output CSV filename (default: backbone_dihedrals.csv)
📦 Output Files
1️⃣ NumPy File (.npz)
Load in Python:
import numpy as np

data = np.load("backbone_dihedrals.npz")

time = data["time"]
phi = data["phi"]
psi = data["psi"]
omega = data["omega"]
Each array has shape:
(number_of_frames,)
2️⃣ CSV File
Columns:
time, phi_deg, psi_deg, omega_deg
You can open this directly in:
Excel
Origin
MATLAB
Python (pandas)
Any plotting software
📊 Example Use Cases
Ramachandran plots (ϕ vs ψ)
Conformational state analysis
Transition detection
Free energy surface reconstruction
Machine learning feature extraction
⚠️ Important Assumptions
The script assumes:
Exactly one ALA residue exists in the system.
Backbone atom names are:
N
CA
C
The alanine residue has neighbors on both sides (e.g., ACE–ALA–NME).
If your naming differs (CHARMM vs AMBER vs GROMACS variations), adjust the atom selection in the script.
🧠 Why This Is Useful
Backbone dihedral angles define peptide conformation.
For alanine dipeptide, ϕ and ψ are commonly used to:
Study conformational basins
Build free energy surfaces
Benchmark enhanced sampling methods
Train generative models
🛠 Troubleshooting
❌ "Expected exactly 1 ALA residue"
Your topology may contain multiple alanines. Modify selection.
❌ Atom not found
Check atom naming in your topology:
u.atoms.names

