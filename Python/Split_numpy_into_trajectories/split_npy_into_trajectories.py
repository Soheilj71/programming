#!/usr/bin/env python3
"""
split_npy_into_trajectories.py

Purpose:
    Load a NumPy array from a .npy file, extract one 1D trajectory from it,
    split that trajectory into many equal pieces, save each piece as its own
    .npy file, and also save all pieces together in one final stacked array.

Why this script is useful:
    Sometimes simulation or trajectory data is stored as one long array.
    This script helps convert that long array into many smaller trajectories
    that are easier to analyze, plot, or reuse later.

Example:
    python split_npy_into_trajectories.py \
        --input final_one_array.npy \
        --output-dir split_output \
        --num-trajectories 10000 \
        --save-combined final.npy
"""

import argparse  # Lets users pass options from the terminal.
import sys  # Lets us exit safely if something goes wrong.
from pathlib import Path  # Safer and cleaner file-path handling.
import numpy as np  # Main library for working with NumPy arrays.


def fail(message: str, code: int = 1) -> None:
    """
    Stop the script with a clear error message.

    Parameters
    ----------
    message : str
        The error message to show.
    code : int
        Exit code. Non-zero means something failed.
    """
    print(f"[ERROR] {message}", file=sys.stderr)
    sys.exit(code)


def load_array(path: Path) -> np.ndarray:
    """
    Load a NumPy array from a .npy file.

    Parameters
    ----------
    path : Path
        Path to the input .npy file.

    Returns
    -------
    np.ndarray
        The loaded NumPy array.
    """
    if not path.exists():
        fail(f"Input file not found: {path}")

    try:
        data = np.load(path, allow_pickle=False)
    except Exception as exc:
        fail(f"Could not load NumPy file '{path}': {exc}")

    return data


def extract_1d_data(data: np.ndarray) -> np.ndarray:
    """
    Extract a 1D array from the input data.

    This function follows the same idea as your original script:
    it takes data[0] and assumes that is the main long trajectory.

    If data[0] is not 1D, it will flatten it into 1D.

    Parameters
    ----------
    data : np.ndarray
        Loaded input array.

    Returns
    -------
    np.ndarray
        A 1D NumPy array.
    """
    if data.ndim == 0:
        fail("Input array has 0 dimensions. A trajectory array is required.")

    # In your original script, you used data[0].
    # We keep that behavior here so the output matches your intended workflow.
    extracted = data[0]

    # If the extracted piece is not already 1D, flatten it into one long vector.
    extracted = np.asarray(extracted).reshape(-1)

    return extracted


def split_into_equal_parts(data_1d: np.ndarray, num_trajectories: int) -> np.ndarray:
    """
    Split a 1D array into equal-length trajectories.

    If the data length is not perfectly divisible by num_trajectories,
    the extra values at the end are removed.

    Parameters
    ----------
    data_1d : np.ndarray
        The 1D array to split.
    num_trajectories : int
        Number of smaller trajectories to create.

    Returns
    -------
    np.ndarray
        A 2D array with shape:
        (num_trajectories, length_of_each_trajectory)
    """
    if num_trajectories <= 0:
        fail("The number of trajectories must be greater than 0.")

    total_points = data_1d.shape[0]
    length_each = total_points // num_trajectories

    if length_each == 0:
        fail(
            f"Cannot split {total_points} data points into {num_trajectories} trajectories. "
            "Each trajectory would have length 0."
        )

    usable_points = length_each * num_trajectories

    # Remove the leftover points at the end, if any.
    trimmed = data_1d[:usable_points]

    # Reshape the trimmed 1D array into a 2D array:
    # rows   = number of trajectories
    # cols   = length of each trajectory
    split_data = trimmed.reshape(num_trajectories, length_each)

    return split_data


def save_individual_arrays(split_data: np.ndarray, output_dir: Path, prefix: str) -> None:
    """
    Save each trajectory as its own .npy file.

    Parameters
    ----------
    split_data : np.ndarray
        2D array of split trajectories.
    output_dir : Path
        Folder where the files will be saved.
    prefix : str
        Prefix for output filenames.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    for i in range(split_data.shape[0]):
        output_path = output_dir / f"{prefix}_{i}.npy"
        np.save(output_path, split_data[i])
        print(f"Saved: {output_path}")


def save_combined_array(split_data: np.ndarray, output_path: Path) -> None:
    """
    Save all trajectories together into one .npy file.

    Parameters
    ----------
    split_data : np.ndarray
        2D array of split trajectories.
    output_path : Path
        File path for the combined array.
    """
    np.save(output_path, split_data)
    print(f"Saved combined array: {output_path}")


def build_parser() -> argparse.ArgumentParser:
    """
    Build the command-line argument parser.

    Returns
    -------
    argparse.ArgumentParser
        Configured argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Split one long NumPy trajectory into many equal smaller trajectories."
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to the input .npy file."
    )

    parser.add_argument(
        "--output-dir",
        default="split_output",
        help="Folder where individual trajectory files will be saved. Default: split_output"
    )

    parser.add_argument(
        "--num-trajectories",
        type=int,
        default=10000,
        help="Number of smaller trajectories to create. Default: 10000"
    )

    parser.add_argument(
        "--prefix",
        default="numpy_array",
        help="Prefix for individual output files. Default: numpy_array"
    )

    parser.add_argument(
        "--save-combined",
        default="final.npy",
        help="Filename for the combined output array. Default: final.npy"
    )

    return parser


def main() -> None:
    """
    Main function:
    1. Read arguments.
    2. Load the input array.
    3. Extract one long 1D trajectory.
    4. Split it into equal parts.
    5. Save each part separately.
    6. Save all parts together.
    """
    parser = build_parser()
    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    combined_output_path = Path(args.save_combined)

    # Load the original input data.
    data = load_array(input_path)

    # Extract the 1D trajectory we want to split.
    data_1d = extract_1d_data(data)

    print(f"Input data shape: {data.shape}")
    print(f"Extracted 1D data shape: {data_1d.shape}")

    # Split into equal trajectories.
    split_data = split_into_equal_parts(data_1d, args.num_trajectories)

    print(f"Final split data shape: {split_data.shape}")
    print(f"Number of trajectories: {split_data.shape[0]}")
    print(f"Length of each trajectory: {split_data.shape[1]}")

    # Save each smaller trajectory as its own file.
    save_individual_arrays(split_data, output_dir, args.prefix)

    # Save all trajectories together in one file.
    save_combined_array(split_data, combined_output_path)

    print("Done.")


if __name__ == "__main__":
    main()
