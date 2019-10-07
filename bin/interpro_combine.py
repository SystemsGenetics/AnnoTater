#!/usr/bin/env python3


"""
A Python script for extracting IPR terms and GO terms from the output of
InterProScan  and combining all the InterProScan output files into a single file

This script extracts the different IPR terms and GO terms assigned to a gene by
InterProScan and creates IPR_mappings and GO_mappings files with this information.
Also it combines all the information in different .tsv files produced by
InterProScan into a single .tsv file.

.. module:: Annotater
    :platform: UNIX, Linux
    :synopsis: add synopsis.

"""

import glob
import pandas as pd
import numpy as np
import re

def write_IPR(ipr_file, tsv_file):
    """"
    Retrieves the IPR terms from a TSV file and writes them to a mapping file.

    :param ipr_file: the file handle to the IPR_Mapping.txt file.
    :param tsv_file: the TSV file from InterProScan.

    """
    # The IPR results do not have a consistent number of columns. Here we creaqte
    # an array that gets used in the read_table function below that forces
    # the function to include 15 columns.
    cols = np.arange(15)

    # Import partial IPR results for this file and set the column anames,
    # drop rows that has NaN in IPR column, and remove duplicates.
    ipr_terms = pd.read_csv(tsv_file, sep='\t', header=None, names=cols, usecols=[0,11,12])
    ipr_terms.columns = ["Gene", "IPR", "Description"]
    ipr_terms = ipr_terms.dropna(subset=["IPR"])
    ipr_terms = ipr_terms.drop_duplicates(keep='first')

    # Removes the trailing ID number that InterProScan adds to the sequence
    ipr_terms["Gene"] = ipr_terms["Gene"].str.replace(r'^(.*?)_\d+', r'\1')
    ipr_terms.to_csv(ipr_file, sep="\t", mode='a', header=False, index=False)


def write_GO(go_file, tsv_file):
    """"
    Retrieves the GO terms from a TSV file and writes them to a mapping file.

    :param go_file: the file handle to the GO_Mapping.txt file.
    :param tsv_file: the TSV file from InterProScan.
    """

    # The IPR results do not have a consistent number of columns. Here we create
    # an array that gets used in the read_csv function below that forces
    # the function to include 15 columns.
    cols = np.arange(15)

    # Import partial GO results for this file and set the column names,
    # drop rows that has NaN in IPR column, and remove duplicates.
    go_terms = pd.read_csv(tsv_file,sep='\t',header=None,names=cols,usecols=[0,13])
    go_terms.columns = ["Gene", "GO"]
    go_terms = go_terms.dropna(subset=["GO"])
    go_terms = go_terms.drop_duplicates(keep='first')

    # Removes the trailing ID number that InterProScan adds to the sequence
    go_terms["Gene"] = go_terms["Gene"].str.replace(r'^(.*?)_\d+', r'\1')

    # split the GO column containing the different GO terms associated with Gene
    # create a MultiIndex matching the Gene with its associated GO terms
    # copy all the Gene and GO terms into data frame to write it to GO_mappings file
    go_terms["GO"] = go_terms["GO"].str.split("|")
    go_annotations = pd.MultiIndex.from_product([np.array(go_terms["Gene"]),np.array(go_terms["GO"])[0]])
    go_terms = go_annotations.to_frame(index=False)
    go_terms.to_csv(go_file, sep="\t", mode='a', header=False, index=False)



if __name__ == "__main__":

    # Get a list of all TSV files.
    tsv_filenames = sorted(glob.glob('*.tsv'))

    # Open the IPR_mappintgs.txt file where the final IPR mappings will be stored.
    ipr_file = open('IPR_mappings.txt','w')
    go_file = open('GO_mappings.txt','w')

    # Set the header names for the IPR_mappings.txt file
    ipr_headers = ["Gene", "IPR", "Description"]
    ipr_file.write("\t".join(ipr_headers))
    ipr_file.write("\n")

    # Set the header names for the GO_mappings.txt file
    go_headers = ["Gene", "GO"]
    go_file.write("\t".join(go_headers))
    go_file.write("\n")

    # Iterate through each of the TSV files and pull out the IPR and GO mappings
    for tsv_file in tsv_filenames:
       write_IPR(ipr_file, tsv_file)
       write_GO(go_file, tsv_file)


    ipr_file.close()
    go_file.close()
    