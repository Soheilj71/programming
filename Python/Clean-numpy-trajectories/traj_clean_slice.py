#!/usr/bin/env python3
# This script is meant to be run from the terminal with Python 3.

# traj_clean_slice.py
# Goal:
#   - Load a .npy file (numpy array) that represents points or trajectories
#   - Remove rows with NaN/inf values (bad numbers)
#   - Optionally slice the trajectory (choose steps, choose number of trajectories)
#   - Optionally subsample points to reduce size
#   - Save the cleaned result as a new .npy file

import argparse  # Lets users pass options like --in and --out from terminal.
import sys  # Lets us exit safely with error codes.
from pathlib import Path  # Safe file path handling.
import numpy as np  # Numpy is the standard library for numeric arrays.


def fail(message: str, code: int = 1) -> None:
    # Print an error message and stop the program.
    print(f"[ERROR] {message}", file=sys.stderr)
    sys.exit(code)


def load_array(path: Path) -> np.ndarray:
    # Check that the file exists.
    if not path.exists():
        fail(f"Input file not found: {path}")

    # Load the numpy array from disk.
    # .npy is a binary format that stores numpy arrays efficiently.
    arr = np.load(str(path))

    # Ensure we have a numpy array (not a list).
    arr = np.asarray(arr)

    return arr


def remove_nonfinite(arr: np.ndarray) -> np.ndarray:
    # "Finite" means not NaN and not +/- infinity.
    # Many computations break if NaN or inf exists.
    mask = np.isfinite(arr)

    # If arr is multi-dimensional, mask has the same shape.
    # We want to remove "rows" (or "frames") that contain any non-finite number.
    # So we collapse mask across the last dimension(s) depending on interpretation.
    #
    # For general safety, we treat each element as important and require all finite.
    all_finite = mask.reshape(mask.shape[0], -1).all(axis=1) if arr.ndim >= 1 else mask

    # Keep only rows where everything is finite.
    cleaned = arr[all_finite]

    return cleaned


def maybe_slice(arr: np.ndarray, max_items: int, step_start: int, step_stop: int, step_stride: int) -> np.ndarray:
    # This function tries to slice in a meaningful way if the array looks like trajectories.
    #
    # Common shapes:
    #   (n_traj, n_steps, dim)
    #   (n_particles, n_steps, dim)
    #
    # If arr.ndim < 2, there is no "time" axis to slice.
    if arr.ndim < 2:
        return arr

    # If user requests "keep only first max_items" along axis 0, apply it.
    if max_items > 0:
        arr = arr[:max_items]

    # If user requests slicing along axis 1 (often time steps), apply it.
    # Python slicing: arr[:, start:stop:stride, ...]
    if arr.ndim >= 2:
        arr = arr[:, step_start:step_stop:step_stride, ...]

    return arr


def maybe_subsample_rows(arr: np.ndarray, keep_every: int, seed: int) -> np.ndarray:
    # If keep_every <= 1, user does not want subsampling.
    if keep_every <= 1:
        return arr

    # For generality, we subsample along the first axis (rows/items).
    # This works for:
    #   (N,2) points -> keep every k points
    #   (n_traj, n_steps, dim) -> keep every k trajectories (not time steps)
    #
    # If you want time-step subsampling, use --step_stride instead.
    rng = np.random.default_rng(seed)

    # We choose indices such that we keep approximately 1/keep_every fraction.
    n = arr.shape[0]
    k = max(1, n // keep_every)

    # Randomly pick k indices without replacement.
    idx = rng.choice(n, size=k, replace=False)

    # Sort indices so output order is stable and readable.
    idx = np.sort(idx)

    return arr[idx]


def main() -> None:
    # Create argument parser so the script is easy to use from terminal.
    parser = argparse.ArgumentParser(
        description="Clean and slice a .npy trajectory/points array (remove NaN/inf, slice, subsample, save)."
    )

    # Required input and output files.
    parser.add_argument("--in", dest="infile", required=True, help="Input .npy file path.")
    parser.add_argument("--out", dest="outfile", required=True, help="Output .npy file path.")

    # Optional: keep only first N items along axis 0.
    parser.add_argument("--max_items", type=int, default=0, help="Keep only the first N items along axis 0 (0 = keep all).")

    # Optional: slice along axis 1 (often time steps).
    parser.add_argument("--step_start", type=int, default=0, help="Start index for slicing along axis 1 (default: 0).")
    parser.add_argument("--step_stop", type=int, default=-1, help="Stop index for slicing along axis 1 (default: -1 = end).")
    parser.add_argument("--step_stride", type=int, default=1, help="Stride for slicing along axis 1 (default: 1).")

    # Optional: subsample along axis 0.
    parser.add_argument("--keep_every", type=int, default=1, help="Randomly keep about 1/keep_every of axis-0 items (default: 1 = no subsample).")
    parser.add_argument("--seed", type=int, default=0, help="Random seed for subsampling (default: 0).")

    args = parser.parse_args()

    # Convert string paths to Path objects (safer).
    infile = Path(args.infile)
    outfile = Path(args.outfile)

    # Load the numpy array.
    arr = load_array(infile)

    # Print a quick summary so user knows what was loaded.
    print(f"Loaded: {infile}")
    print(f"Original shape: {arr.shape}, dtype: {arr.dtype}")

    # Remove NaN/inf by dropping bad rows along axis 0.
    arr2 = remove_nonfinite(arr)
    print(f"After removing non-finite rows: shape {arr2.shape}")

    # Slice the array (if it looks like it has a time axis).
    # We handle step_stop = -1 to mean "end" (Python slicing supports -1 but it excludes last element,
    # so we convert -1 to None for convenience).
    step_stop = None if args.step_stop == -1 else args.step_stop
    arr3 = maybe_slice(
        arr2,
        max_items=args.max_items,
        step_start=args.step_start,
        step_stop=step_stop,
        step_stride=args.step_stride,
    )
    print(f"After slicing: shape {arr3.shape}")

    # Subsample along axis 0 if requested.
    arr4 = maybe_subsample_rows(arr3, keep_every=args.keep_every, seed=args.seed)
    print(f"After subsampling: shape {arr4.shape}")

    # Make sure output folder exists.
    outfile.parent.mkdir(parents=True, exist_ok=True)

    # Save the cleaned array.
    np.save(str(outfile), arr4)

    # Confirm output.
    print(f"Saved cleaned array to: {outfile}")


if __name__ == "__main__":
    main()
