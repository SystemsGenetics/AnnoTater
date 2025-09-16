#!/bin/bash

outfile=$1

# Get the list of EC number txt files
ec_files=`ls *.ECnumbers.txt`

# Create header
echo -e "Gene_ID\tSwissProt_Accession\tSwissProt_Entry_Name\tEC_Number\tEC_Description" > $outfile

# Combine all EC files, skipping headers
for f in $ec_files; do
    tail -n +2 $f >> $outfile
done

# Remove duplicates while preserving header
head -n 1 $outfile > temp_header
tail -n +2 $outfile | sort | uniq >> temp_header
mv temp_header $outfile

exit 0