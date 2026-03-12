# Clean NumPy Trajectories

A simple Python script for cleaning and preparing NumPy trajectory or point-array files saved as `.npy`.

This tool is useful when your dataset contains invalid values such as `NaN` or `inf`, and you want to:

- remove bad rows
- keep only part of the dataset
- slice trajectory steps
- randomly subsample the data
- save the cleaned result as a new `.npy` file

It is designed to be easy to run from the terminal and practical for preprocessing simulation or trajectory data.

---

## What this script does

The script loads a NumPy array from a `.npy` file and applies the following optional processing steps:

1. **Load the array**
   - Reads a `.npy` file from disk.

2. **Remove non-finite values**
   - Deletes rows along axis 0 if they contain invalid numbers such as:
     - `NaN`
     - `+inf`
     - `-inf`

3. **Slice the array**
   - Optionally keeps only the first `N` items along axis 0.
   - Optionally slices along axis 1, which is often the time-step dimension in trajectory data.

4. **Subsample the array**
   - Optionally keeps only a random fraction of rows/items along axis 0.

5. **Save the cleaned result**
   - Writes the processed array back to a new `.npy` file.

---

## Typical input shapes

This script can be useful for arrays such as:

- `(N, 2)` for 2D points
- `(N, 3)` for 3D points
- `(n_traj, n_steps, dim)` for trajectory datasets
- `(n_samples, n_features)` for general numerical arrays

---

## Requirements

- Python 3.8 or newer
- NumPy

Install NumPy if needed:

```bash
pip install numpy
```

# File structure
Suggested GitHub folder structure:

```bash
clean-numpy-trajectories/
├── traj_clean_slice.py
└── README.md
```

# Usage
Basic command:
```bash
python traj_clean_slice.py --in input.npy --out cleaned.npy
```

# Command-line arguments
## Required arguments
`--in`
Path to the input `.npy` file.

`--out`
Path to the output `.npy` file.

## Optional arguments
`--max_items`
Keep only the first `N` items along axis 0.
Default:
```bash
0
```

Meaning:
*   `0` = keep everything

Example:
```bash
--max_items 100
```

This keeps only the first 100 rows, trajectories, or items.

`--step_start`
Start index for slicing along axis 1.

Default:
```bash
0
```

Example:
```bash
--step_start 10
```

This starts from step 10.

```--step_stop```
Stop index for slicing along axis 1.

Default:
```bash
-1
```

Meaning:
*   `-1` is treated as “go to the end”

Example:
```bash
--step_stop 500
```

This stops before step 500.

`--step_stride`

Stride for slicing along axis 1.
Default:
```bash
1
```
Example:
```bash
--step_stride 5
```

This keeps every 5th step along axis 1.

`--keep_every`
Randomly keep about `1 / keep_every` of items along axis 0.
Default:
```bash
1
```

Meaning:
*   `1` = no subsampling
Example:
```bash
--keep_every 4
```

This keeps about one quarter of the rows/items.
`--seed`
Random seed for reproducible subsampling.
Default:
```bash
0
```

Example:
```bash
--seed 42
```

Using the same seed gives the same random selection each time.

# Examples
## 1. Clean a file by removing bad rows only
```bash
python traj_clean_slice.py --in raw.npy --out cleaned.npy
```

This will:
*   load `raw.npy`
*   remove rows with `NaN` or `inf`
*   save the result to `cleaned.npy`

## 2. Keep only the first 100 trajectories
```bash
python traj_clean_slice.py --in raw.npy --out cleaned.npy --max_items 100
```

## 3. Slice time steps from a trajectory array
```bash
python traj_clean_slice.py --in raw.npy --out cleaned.npy --step_start 0 --step_stop 1000 --step_stride 10
```

This keeps:
*   steps from 0 to 999
*   every 10th step

## 4. Randomly subsample the dataset
```bash
python traj_clean_slice.py --in raw.npy --out cleaned.npy --keep_every 5 --seed 123
```

This keeps about 20% of the items along axis 0.

## 5. Combine cleaning, slicing, and subsampling
```bash
python traj_clean_slice.py \
  --in raw.npy \
  --out cleaned.npy \
  --max_items 200 \
  --step_start 100 \
  --step_stop 1000 \
  --step_stride 2 \
  --keep_every 4 \
  --seed 42
```

This will:
*   remove invalid rows
*   keep the first 200 items
*   slice steps 100 to 999 with stride 2
*   randomly keep about 25% of the remaining items

# Example workflow
Suppose you have a trajectory array with shape:
```python
(n_traj, n_steps, dim)
```

For example:
```python 
(500, 2000, 2)
```

You may want to:
*   remove bad trajectories
*   keep only the first 100 trajectories
*   keep every 5th step
*   reduce the total number of trajectories for faster testing

You can do that with:
```bash
python traj_clean_slice.py \
  --in trajectories.npy \
  --out trajectories_cleaned.npy \
  --max_items 100 \
  --step_stride 5 \
  --keep_every 2 \
  --seed 0
```

# Output

The script saves a new `.npy` file containing the cleaned array.

It also prints progress information in the terminal, such as:
*   input file name
*   original shape
*   shape after removing invalid rows
*   shape after slicing
*   shape after subsampling
*   output file path

Example terminal output:
```bash
Loaded: raw.npy
Original shape: (500, 2000, 2), dtype: float64
After removing non-finite rows: shape (480, 2000, 2)
After slicing: shape (100, 200, 2)
After subsampling: shape (50, 200, 2)
Saved cleaned array to: cleaned.npy
```

# Notes
## 1. How invalid rows are removed
The script checks for finite values using NumPy.

Finite values are normal numeric values, not:
*   `NaN`
*   `+inf`
*   `-inf`

If a row/item along axis 0 contains any non-finite value, that row/item is removed.

## 2. How slicing works
If the array has at least 2 dimensions, the script slices along axis 1:
arr[:, start:stop:stride, ...]

This is useful when axis 1 represents time steps.

If the array has fewer than 2 dimensions, slicing along axis 1 is skipped.

## 3. How subsampling works
Subsampling is applied along axis 0.
That means:
*   for `(N, 2)` arrays, it keeps a random subset of rows
*   for `(n_traj, n_steps, dim)` arrays, it keeps a random subset of trajectories

If you want to reduce time steps instead of rows/trajectories, use:
```bash
--step_stride
```

instead of `--keep_every`.

## 4. Important detail about randomness
Subsampling is random, but reproducible if you use the same `--seed`.

# Limitations
*   The script assumes that removing invalid data along axis 0 is the correct behavior.
*   It does not interpolate missing values.
*   It does not validate whether axis 1 is truly a time dimension; it simply slices axis 1 when possible.
*   It only works with NumPy `.npy` files.

# When this script is useful
This script is useful for:
*   molecular dynamics preprocessing
*   machine learning dataset cleanup
*   trajectory preparation
*   removing broken simulation entries
*   reducing dataset size for debugging or faster experiments

