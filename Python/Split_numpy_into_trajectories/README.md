# Split NumPy Array into Equal Trajectories

This script takes a long NumPy trajectory stored in a `.npy` file, splits it into many equal smaller trajectories, saves each smaller trajectory as its own `.npy` file, and also saves all trajectories together in one final combined `.npy` file.

It is useful when you have one long simulation output and want to divide it into many smaller pieces for analysis, machine learning, or visualization.

---

## What this script does

The script:

1. Loads a NumPy array from an input `.npy` file
2. Extracts the first main array using `data[0]`
3. Converts that extracted data into a 1D array
4. Splits the 1D array into a user-defined number of equal trajectories
5. Saves each trajectory separately
6. Saves all trajectories together in one final file

---

## Input assumption

This script follows the logic of the original workflow and uses:

```python
data[0]
```

from the loaded NumPy array.

That means your input file should contain an array where the first element represents the long trajectory you want to split.

If `data[0]` is not already 1D, the script flattens it into one long 1D array.


# Requirements
*   Python 3.8 or newer
*   NumPy

Install NumPy with:
```bash
pip install numpy
```

# File structure example
```
project_folder/
├── split_npy_into_trajectories.py
├── README.md
└── final_one_array.npy
```

# Usage
Basic example:
```bash
python split_npy_into_trajectories.py \
    --input final_one_array.npy \
    --output-dir split_output \
    --num-trajectories 10000 \
    --save-combined final.npy
```

# Arguments
*   **`--input`**

Path to the input `.npy` file.

Example:
```bash
--input final_one_array.npy
```

*   **`--output-dir`**

Folder where individual trajectory files will be saved.
Default:
```bash
split_output
```

*   **`--num-trajectories`**

Number of smaller trajectories to create.

Default:
```bash
10000
```

*   **`--prefix`**

Prefix used for naming the individual output files.
Default:
```bash
numpy_array
```

Example output files:
```
numpy_array_0.npy
numpy_array_1.npy
numpy_array_2.npy
...
```

*   **`--save-combined`**

Filename for the final combined NumPy array.
Default:
```bash
final.npy
```

# Output
After running the script, you will get:

**1. Many individual `.npy` files**
For example:
```
split_output/
├── numpy_array_0.npy
├── numpy_array_1.npy
├── numpy_array_2.npy
└── ...
```

Each file contains one smaller trajectory.

**2. One combined `.npy` file**
For example:
```
final.npy
```
This file contains all trajectories stacked together as one 2D NumPy array.
Its shape will be:
(num_trajectories, length_of_each_trajectory)
Example
Suppose your extracted 1D data has length:
1000000
and you choose:
--num-trajectories 10000
Then each trajectory will have length:
1000000 // 10000 = 100
So the final combined array will have shape:
(10000, 100)
Important note about leftover values
If the total number of data points is not exactly divisible by the number of trajectories, the script removes the extra points at the end.
Example:
Total points = 100003
Number of trajectories = 1000
Length of each trajectory = 100
Usable points = 100000
The final 3 points are ignored.
This is done to make sure all trajectories have the same length.
Why this version is better than the original script
Compared to the original code, this version:
is easier to read
is safer for general use
includes error handling
uses command-line arguments
avoids reloading thousands of temporary files
is more suitable for GitHub
is documented for beginner users
Example command
python split_npy_into_trajectories.py \
    --input final_one_array.npy \
    --output-dir my_split_arrays \
    --num-trajectories 5000 \
    --prefix traj \
    --save-combined all_trajectories.npy
This will create:
individual files such as traj_0.npy, traj_1.npy, ...
a combined file called all_trajectories.npy

