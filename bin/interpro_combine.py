#!/usr/bin/env python3

"""
A Python script for extracting IPR terms and GO terms from the output of
InterProScan and combining all the InterProScan output files into a single file

This script:
1. Automatically finds all *.tsv files in the current directory
2. Extracts IPR terms and GO terms from each file
3. Creates mapping files: {prefix}.IPR_mappings.txt and {prefix}.GO_mappings.txt
4. Combines all TSV data into: {prefix}.tsv

Usage: interpro_combine.py <output_prefix>
Example: interpro_combine.py all.5.pep

.. module:: Annotater
    :platform: UNIX, Linux
    :synopsis: Combine InterProScan outputs and extract functional annotations

"""

import argparse
import glob
import pandas as pd
import numpy as np
import re
import sys


def write_IPR(ipr_file, ipr_terms):
    """ "
    Retrieves the IPR terms and writes them to a mapping file.

    :param ipr_file: the file handle to the IPR mappings text file.
    :param ipr_terms: the pandas object with IPR terms information

    """

    # Replace InterProScan's '-' missing values with NaN, then drop rows with missing IPR terms
    ipr_terms = ipr_terms.replace('-', np.nan)
    ipr_terms = ipr_terms.dropna(subset=["IPR"])
    ipr_terms = ipr_terms.drop_duplicates(keep="first")

    # Removes the trailing ID number that InterProScan adds to the sequence
    # ipr_terms["Gene"] = ipr_terms["Gene"].str.replace(r'^(.*?)_\d+', r'\1')
    ipr_terms.to_csv(ipr_file, sep="\t", mode="a", header=False, index=False)


def write_GO(go_file, go_terms):
    """ "
    Retrieves the GO terms and writes them to a mapping file.

    :param go_file: the file handle to the GO mappings text file.
    :param go_terms: the pandas object with GO terms information.
    """

    # Replace InterProScan's '-' missing values with NaN, then drop rows with missing GO terms
    go_terms = go_terms.replace('-', np.nan)
    go_terms = go_terms.dropna(subset=["GO"])
    go_terms = go_terms.drop_duplicates(keep="first")

    # Removes the trailing ID number that InterProScan adds to the sequence
    # go_terms["Gene"] = go_terms["Gene"].str.replace(r'^(.*?)_\d+', r'\1')

    # split the GO column containing the different GO terms associated with Gene
    if go_terms["GO"].size > 0:
        go_terms["GO"] = go_terms["GO"].str.split("|")

        # Create a new empty data frame. Loop over the go_terms dataframe and append
        # gene names and each individual GO term associated with the gene to the new
        # data frame. Write this new data frame to GO_mappings file
        go_annotations_list = []
        for index, data in go_terms.iterrows():
            for terms in data["GO"]:
                # Remove database source annotation if present (backwards compatible)
                # Handles formats like "GO:0005507", "GO:0005507(InterPro)", "GO:0005507(Pfam)", etc.
                clean_go_term = re.sub(r'\([^)]*\)', '', terms)
                go_annotations_list.append({"Gene": data["Gene"], "GO": clean_go_term})

        go_annotations = pd.DataFrame(go_annotations_list)
        go_annotations = go_annotations.drop_duplicates(keep="first")
        go_annotations.to_csv(go_file, sep="\t", mode="a", header=False, index=False)


def main():

    # Specifies the arguments for this script
    parser = argparse.ArgumentParser(description="Combine InterProScan TSV files and extract IPR/GO mappings")
    parser.add_argument("output_prefix",
                       help="Prefix for output files (e.g., 'all.5.pep' creates 'all.5.pep.GO_mappings.txt')")

    # Read in the input arguments
    args = parser.parse_args()

    # Setting the prefix for output file names
    file_name_prefix = args.output_prefix

    # Setting the file names for the output files
    tsv_combine_name = file_name_prefix + ".tsv"
    ipr_file_name = file_name_prefix + ".IPR_mappings.txt"
    go_file_name = file_name_prefix + ".GO_mappings.txt"

    # Open the files to write the IPR mappings, GO mappings and combined TSV data
    ipr_file = open(ipr_file_name, "w")
    go_file = open(go_file_name, "w")
    combined_tsv_file = open(tsv_combine_name, "w")

    # Set the header names for the IPR mappings text file
    ipr_headers = ["Gene", "IPR", "Description"]
    ipr_file.write("\t".join(ipr_headers))
    ipr_file.write("\n")

    # Set the header names for the GO mappings text file
    go_headers = ["Gene", "GO"]
    go_file.write("\t".join(go_headers))
    go_file.write("\n")

    # The IPR results do not have a consistent number of columns. Here we create
    # an array that gets used in the read_csv function below that forces
    # the function to include 15 columns.
    cols = np.arange(15)

    # Get a list of all TSV file names
    tsv_filenames = sorted(glob.glob("*.tsv"))

    # Iterate through each of the TSV files and pull out the IPR and GO mappings
    for tsv_file in tsv_filenames:

        # Exclude the file we're creating.
        if tsv_file == tsv_combine_name:
            continue

        try:
            # Import the data from each file and extract partial GO results and
            # partial IPR results and pass the panda objects with this information
            # to the corresponding functions
            print("Reading file: '{}'".format(tsv_file), file=sys.stderr)

            tsv_data = pd.read_csv(tsv_file, sep="\t", header=None, names=cols)
            go_terms = tsv_data.loc[:, [0, 13]]
            go_terms.columns = go_headers
            ipr_terms = tsv_data.loc[:, [0, 11, 12]]
            ipr_terms.columns = ipr_headers
            write_IPR(ipr_file, ipr_terms)
            write_GO(go_file, go_terms)

            # writing the contents of each tsv_file into the combined_tsv_file
            tsv_data.to_csv(combined_tsv_file, sep="\t", mode="a", header=False, index=False)
        except:
            print("Problem reading '{}'. Skipping.".format(tsv_file), file=sys.stderr)

    ipr_file.close()
    go_file.close()
    combined_tsv_file.close()


if __name__ == "__main__":
    main()
