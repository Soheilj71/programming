#!/usr/bin/env python3
"""
Compute backbone dihedral angles (phi, psi, omega)
for alanine dipeptide using MDAnalysis.

This script:
1. Loads a topology file (structure information)
2. Loads a trajectory file (coordinates over time)
3. Identifies the alanine residue
4. Computes backbone dihedral angles for each frame
5. Saves the results as:
      - A NumPy (.npz) file
      - A CSV file

Author: Soheil Jamali
"""

# ---------------------------------------------------------
# Import required libraries
# ---------------------------------------------------------

import argparse          # For reading command-line arguments
import numpy as np       # For numerical operations
import MDAnalysis as mda # For reading molecular simulations
from MDAnalysis.analysis.dihedrals import Dihedral


# ---------------------------------------------------------
# Helper function: convert radians to degrees
# ---------------------------------------------------------

def radians_to_degrees(angle_array):
    """
    Convert angles from radians to degrees.
    MDAnalysis returns angles in radians by default.
    """
    return np.rad2deg(angle_array)


# ---------------------------------------------------------
# Main function
# ---------------------------------------------------------

def main():
    """
    Main execution function.
    This is where the program starts running.
    """

    # -----------------------------------------------------
    # Step 1: Read command-line arguments
    # -----------------------------------------------------

    parser = argparse.ArgumentParser(
        description="Compute backbone dihedral angles (phi, psi, omega) for alanine dipeptide."
    )

    parser.add_argument(
        "-t", "--top",
        required=True,
        help="Topology file (e.g., PDB, PSF, PRMTOP)"
    )

    parser.add_argument(
        "-x", "--traj",
        required=True,
        help="Trajectory file (e.g., DCD, XTC, TRR)"
    )

    parser.add_argument(
        "-o", "--out",
        default="backbone_dihedrals.npz",
        help="Output NumPy (.npz) filename"
    )

    parser.add_argument(
        "--csv",
        default="backbone_dihedrals.csv",
        help="Output CSV filename"
    )

    args = parser.parse_args()

    # -----------------------------------------------------
    # Step 2: Load the molecular system
    # -----------------------------------------------------

    # Universe = topology + trajectory together
    u = mda.Universe(args.top, args.traj)

    # -----------------------------------------------------
    # Step 3: Find the alanine residue
    # -----------------------------------------------------

    # We assume the system contains exactly one alanine (ALA)
    ala_atoms = u.select_atoms("resname ALA")

    if len(ala_atoms.residues) != 1:
        raise RuntimeError(
            f"Expected exactly 1 ALA residue, but found {len(ala_atoms.residues)}."
        )

    # Store the alanine residue
    alanine = ala_atoms.residues[0]

    # -----------------------------------------------------
    # Step 4: Identify neighboring residues
    # -----------------------------------------------------

    # Dihedral angles require neighboring residues.
    # For alanine dipeptide, this is typically:
    # ACE - ALA - NME

    residue_list = list(u.residues)
    index = residue_list.index(alanine)

    if index == 0 or index == len(residue_list) - 1:
        raise RuntimeError("ALA has no neighbor on one side. Cannot compute dihedrals.")

    previous_residue = residue_list[index - 1]
    next_residue = residue_list[index + 1]

    # -----------------------------------------------------
    # Step 5: Helper function to safely select one atom
    # -----------------------------------------------------

    def get_atom(residue, atom_name):
        """
        Retrieve exactly one atom from a residue.
        If not found or multiple found, raise error.
        """
        atom = residue.atoms.select_atoms(f"name {atom_name}")
        if len(atom) != 1:
            raise RuntimeError(
                f"Atom '{atom_name}' not found uniquely in residue {residue.resname}{residue.resid}."
            )
        return atom[0]

    # -----------------------------------------------------
    # Step 6: Define backbone dihedral atoms
    # -----------------------------------------------------

    # Phi (ϕ): C(prev) - N - CA - C
    phi_atoms = [
        get_atom(previous_residue, "C"),
        get_atom(alanine, "N"),
        get_atom(alanine, "CA"),
        get_atom(alanine, "C"),
    ]

    # Psi (ψ): N - CA - C - N(next)
    psi_atoms = [
        get_atom(alanine, "N"),
        get_atom(alanine, "CA"),
        get_atom(alanine, "C"),
        get_atom(next_residue, "N"),
    ]

    # Omega (ω): CA - C - N(next) - CA(next)
    omega_atoms = [
        get_atom(alanine, "CA"),
        get_atom(alanine, "C"),
        get_atom(next_residue, "N"),
        get_atom(next_residue, "CA"),
    ]

    # -----------------------------------------------------
    # Step 7: Compute dihedral angles over all frames
    # -----------------------------------------------------

    # This calculates angles for every frame in trajectory
    dihedral_analysis = Dihedral([phi_atoms, psi_atoms, omega_atoms]).run()

    # Angles are returned in radians (shape: n_frames × 3)
    angles_in_radians = dihedral_analysis.angles

    # Convert to degrees
    angles_in_degrees = radians_to_degrees(angles_in_radians)

    # Separate each angle
    phi = angles_in_degrees[:, 0]
    psi = angles_in_degrees[:, 1]
    omega = angles_in_degrees[:, 2]

    # -----------------------------------------------------
    # Step 8: Extract simulation time for each frame
    # -----------------------------------------------------

    times = np.array([ts.time for ts in u.trajectory], dtype=float)

    # -----------------------------------------------------
    # Step 9: Save results
    # -----------------------------------------------------

    # Save as NumPy archive
    np.savez(
        args.out,
        time=times,
        phi=phi,
        psi=psi,
        omega=omega
    )

    # Save as CSV for easy visualization in Excel
    data = np.column_stack([times, phi, psi, omega])
    header = "time,phi_deg,psi_deg,omega_deg"

    np.savetxt(
        args.csv,
        data,
        delimiter=",",
        header=header,
        comments=""
    )

    # -----------------------------------------------------
    # Step 10: Print summary
    # -----------------------------------------------------

    print("--------------------------------------------------")
    print("Backbone dihedral calculation completed successfully.")
    print(f"Number of frames processed: {len(times)}")
    print(f"Saved NumPy file: {args.out}")
    print(f"Saved CSV file: {args.csv}")
    print("--------------------------------------------------")


# ---------------------------------------------------------
# Run the script
# ---------------------------------------------------------

if __name__ == "__main__":
    main()
