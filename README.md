# Programming Utilities

A collection of reusable Bash and Python scripts for HPC automation, data processing, molecular dynamics analysis, and machine learning workflows.

---

## Structure

```
programming/
├── Bash_Script/
│   ├── Bash_utilities_pack/          # General-purpose shell utilities
│   ├── Shell-Scripts-for-HPC-and-Automation/  # HPC workflow helpers
│   ├── Slurm_Scripts_Pack/           # Slurm job management
│   ├── change_any_line.sh/           # Edit arbitrary lines in a file
│   ├── Open_images/                  # Open images from the terminal
│   ├── open_iteratively/             # Open files one by one interactively
│   ├── Run_Slurm_in_Every_Folder/    # Submit Slurm jobs across directories
│   └── search_slurm_logs/            # Parse Slurm logs to find best results
│
└── Python/
    ├── Automation/                   # Batch folder command runner
    ├── Data_Processing/              # Line removal, pattern extraction, transcript cleaning, trajectory cleaning
    ├── Docs/                         # PDF utilities (add blank pages)
    ├── Machine_Learning/             # Checkpoint finder, KL divergence tools
    ├── Molecular_Dynamics/           # Dihedral angles, FES, Müller potential, PDB standardizer
    ├── Plotting/                     # XVG file plotting (line and scatter)
    └── Structured_Record_Extractor/  # Parse structured text records to CSV
```

---

## Bash Scripts

### General Utilities (`Bash_utilities_pack/`)
| Script | Description |
|---|---|
| `backup_folder.sh` | Creates a timestamped backup of a target folder |
| `collect_file_extensions.sh` | Collects all files of a given extension into one directory |
| `find-large-files.sh` | Finds files above a size threshold |
| `rename_spaces_to_underscores.sh` | Renames files by replacing spaces with underscores |
| `run_command_in_each_subfolder.sh` | Runs a shell command inside every subfolder |

### HPC & Automation (`Shell-Scripts-for-HPC-and-Automation/`)
| Script | Description |
|---|---|
| `gather_files.sh` | Gathers specific files from a directory tree into one place |
| `lineforge.sh` | Adds, removes, or replaces arbitrary lines in text files |

### Slurm (`Slurm_Scripts_Pack/`)
| Script | Description |
|---|---|
| `check_my_queue.sh` | Displays your current Slurm queue in a readable format |
| `slurm_array_job_template.sh` | Template for Slurm array jobs |
| `submit_many_jobs.sh` | Submits multiple Slurm jobs in batch |

### Other
| Script | Description |
|---|---|
| `change_any_line.sh` | Replaces a specific line in any file by line number |
| `open_images.sh` | Opens image files from the terminal |
| `open_iteratively.sh` | Opens files one at a time, waiting for user input between each |
| `run_every_folder.sh` | Runs a Slurm script inside every subfolder |
| `find_best.sh` | Searches Slurm log files to identify the best metric result |

---

## Python Scripts

### Data Processing (`Data_Processing/`)
| Script | Description |
|---|---|
| `remove_lines.py` | Removes arbitrary lines from a file by line number or range |
| `traj_clean_slice.py` | Cleans and slices NumPy trajectory arrays |
| `txt_keyword_extractor_to_excel.py` | Extracts lines matching a pattern and writes to Excel |
| `clean_transcript.py` | Cleans raw transcript files (removes timestamps, speaker labels, etc.) |

### Machine Learning (`Machine_Learning/`)
| Script | Description |
|---|---|
| `find_best_checkpoint.py` | Scans ML checkpoint files to find the one with the best validation metric |
| `kl_2d.py` | Computes KL divergence between two 2D datasets |
| `kl_2d_bootstrap.py` | KL divergence with bootstrapped confidence intervals |

### Molecular Dynamics (`Molecular_Dynamics/`)
| Script | Description |
|---|---|
| `dihedrals.py` | Calculates dihedral angles from trajectory data |
| `fes_2d_from_points.py` | Generates a 2D free energy surface from point data |
| `kl_2d_bootstrap.py` | KL divergence bootstrapping for MD ensemble comparison |
| `muller_potential.py` | Plots and samples the 2D Müller potential energy surface |
| `pdb_standardizer.py` | Standardizes PDB files for consistent downstream processing |

### Plotting (`Plotting/`)
| Script | Description |
|---|---|
| `plotting_xvg_line_graph.py` | Plots GROMACS `.xvg` files as line graphs |
| `plot_timeseries.py` | Plots `.xvg` files as combined scatter and line graphs |

### Automation (`Automation/`)
| Script | Description |
|---|---|
| `folder_runner.py` | Runs a specified command inside each subfolder in a directory |

### Docs (`Docs/`)
| Script | Description |
|---|---|
| `Adding_Blank_Page.py` | Inserts a blank page into a PDF at a specified position |

### Other
| Script | Description |
|---|---|
| `txt_to_csv_extractor.py` | Extracts structured records from plain text files into CSV format |

---

## Tools & Libraries Used

**Bash:** standard POSIX shell utilities, Slurm (`sbatch`, `squeue`)

**Python:** `numpy`, `pandas`, `matplotlib`, `scipy`, `MDAnalysis` / `MDTraj` (MD scripts), `openpyxl` (Excel output), `pypdf` / `PyPDF2` (PDF tools)
