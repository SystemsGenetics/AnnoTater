#!/usr/bin/env python3
"""
Clean FASTA sequences by removing non-IUPAC characters
"""

import argparse
import re

def clean_sequence(sequence, seq_type='pep'):
    """
    Remove non-IUPAC characters from sequence

    Args:
        sequence: Input sequence string
        seq_type: 'pep' for protein, 'nuc' for nucleotide

    Returns:
        Cleaned sequence string
    """
    if seq_type == 'pep':
        # Keep only standard amino acids (IUPAC single letter codes)
        # Remove asterisks (*), X's, and other non-standard characters
        cleaned = re.sub(r'[^ACDEFGHIKLMNPQRSTVWY]', '', sequence.upper())
    else:  # nucleotide
        # Keep only standard nucleotides (IUPAC codes including ambiguous)
        cleaned = re.sub(r'[^ACGTRYSWKMBDHVN]', '', sequence.upper())

    return cleaned

def parse_fasta(filename):
    """
    Simple FASTA parser that yields (header, sequence) tuples
    """
    with open(filename, 'r') as f:
        header = None
        sequence = []

        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if header is not None:
                    yield header, ''.join(sequence)
                header = line[1:]  # Remove the '>' character
                sequence = []
            else:
                sequence.append(line)

        # Don't forget the last sequence
        if header is not None:
            yield header, ''.join(sequence)

def main():
    parser = argparse.ArgumentParser(description='Clean FASTA sequences by removing non-IUPAC characters')
    parser.add_argument('--input', required=True, help='Input FASTA file')
    parser.add_argument('--output', required=True, help='Output cleaned FASTA file')
    parser.add_argument('--seq_type', choices=['pep', 'nuc'], default='pep',
                       help='Sequence type: pep for protein, nuc for nucleotide')

    args = parser.parse_args()

    cleaned_count = 0

    with open(args.output, 'w') as out_handle:
        for header, sequence in parse_fasta(args.input):
            # Clean the sequence
            cleaned_seq = clean_sequence(sequence, args.seq_type)

            # Skip sequences that become empty after cleaning
            if len(cleaned_seq) == 0:
                print(f"Warning: Sequence {header.split()[0]} became empty after cleaning, skipping")
                continue

            # Write cleaned sequence in FASTA format
            out_handle.write(f">{header}\n")

            # Write sequence in 80-character lines (standard FASTA format)
            for i in range(0, len(cleaned_seq), 80):
                out_handle.write(cleaned_seq[i:i+80] + '\n')

            cleaned_count += 1

    print(f"Cleaned {cleaned_count} sequences")

if __name__ == '__main__':
    main()