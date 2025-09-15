#!/usr/bin/env python3
"""
This is the download script.
"""
import argparse
import json
import os
import fcntl

def get_datasets():
    """
    """
    IPR_VERSION='5.75-106.0'
    PANTHER_VERSION='14.1'
    ORTHODB_MAJOR_VERSION="v12"
    ORTHODB_VERSION='odb12v0'
    STRINGDB_VERSION='v12.0'

    return {
        "interproscan": {
            "dir": "interproscan",
            "script": [
                f"wget -c https://ftp.ebi.ac.uk/pub/software/unix/iprscan/5/{IPR_VERSION}/interproscan-{IPR_VERSION}-64-bit.tar.gz",
                f"tar -zxvf interproscan-{IPR_VERSION}-64-bit.tar.gz",
                f"rm -f interproscan-{IPR_VERSION}-64-bit.tar.gz",
            ],
        },
        "panther": {
            "dir": f"interproscan/interproscan-{IPR_VERSION}/data",
            "script": [
                f"wget -c https://ftp.ebi.ac.uk/pub/software/unix/iprscan/5/data/panther-data-{PANTHER_VERSION}.tar.gz",
                f"tar -zxvf panther-data-{PANTHER_VERSION}.tar.gz",
                f"rm -f panther-data-{PANTHER_VERSION}.tar.gz",
            ],
        },
        "nr": {
            "dir": "nr",
            "script": [
                "wget -c ftp://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nr.gz",
                "gunzip -f nr",
                "diamond makedb --threads 4 --in nr -d nr",
                "rm -f nr.gz",
            ],
        },
        "refseq_plant": {
            "dir": "refseq_plant",
            "script": [
                "wget -c -r -A '*.protein.faa.gz' ftp://ftp.ncbi.nlm.nih.gov/refseq/release/plant/",
                "gunzip -f ./ftp.ncbi.nlm.nih.gov/refseq/release/plant/*.gz",
                "cat ./ftp.ncbi.nlm.nih.gov/refseq/release/plant/*.faa > refseq_plant.protein.faa",
                "rm -rf ./ftp.ncbi.nlm.nih.gov/",
                "diamond makedb --threads 4 --in refseq_plant.protein.faa -d refseq_plant.protein",
            ],
        },
        "orthodb": {
            "dir": "orthodb",
            "script": [
                f"wget -c https://data.orthodb.org/{ORTHODB_MAJOR_VERSION}/download/{ORTHODB_VERSION}_level2species.tab.gz",
                f"gunzip -f {ORTHODB_VERSION}_level2species.tab.gz",
                f"rm -f {ORTHODB_VERSION}_level2species.tab.gz",

                f"wget -c https://data.orthodb.org/{ORTHODB_MAJOR_VERSION}/download/{ORTHODB_VERSION}_OG2genes.tab.gz",
                f"gunzip -f {ORTHODB_VERSION}_OG2genes.tab.gz",
                f"rm -f {ORTHODB_VERSION}_OG2genes.tab.gz",

                f"wget -c https://data.orthodb.org/{ORTHODB_MAJOR_VERSION}/download/{ORTHODB_VERSION}_OGs.tab.gz",
                f"gunzip -f {ORTHODB_VERSION}_OGs.tab.gz",
                f"rm -f {ORTHODB_VERSION}_OGs.tab.gz",

                f"wget -c https://data.orthodb.org/{ORTHODB_MAJOR_VERSION}/download/{ORTHODB_VERSION}_all_og_fasta.tab.gz",
                f"gunzip -f {ORTHODB_VERSION}_all_og_fasta.tab.gz",
                f"rm -f {ORTHODB_VERSION}_all_og_fasta.tab.gz",

                f"wget -c https://data.orthodb.org/{ORTHODB_MAJOR_VERSION}/download/{ORTHODB_VERSION}_OG_xrefs.tab.gz",
                f"gunzip -f {ORTHODB_VERSION}_OG_xrefs.tab.gz",
                f"rm -f {ORTHODB_VERSION}_OG_xrefs.tab.gz",

                f"wget -c https://data.orthodb.org/{ORTHODB_MAJOR_VERSION}/download/{ORTHODB_VERSION}_species.tab.gz",
                f"gunzip -f {ORTHODB_VERSION}_species.tab.gz",
                f"rm -f {ORTHODB_VERSION}_species.tab.gz",

                f"wget -c https://data.orthodb.org/{ORTHODB_MAJOR_VERSION}/download/{ORTHODB_VERSION}_gene_xrefs.tab.gz",
                f"gunzip -f {ORTHODB_VERSION}_gene_xrefs.tab.gz",
                f"rm -f {ORTHODB_VERSION}_gene_xrefs.tab.gz",

                f"python3 ./index_orthodb.py .",
                f"diamond makedb --threads 4 --in {ORTHODB_VERSION}_all_og_fasta.tab -d {ORTHODB_VERSION}_all_og",
            ],
        },
        "string-db": {
            "dir": "string-db",
            "script": [
                f"wget -c https://stringdb-downloads.org/download/protein.sequences.{STRINGDB_VERSION}.fa.gz",
                f"gunzip -f protein.sequences.{STRINGDB_VERSION}.fa.gz",
                f"rm -f protein.sequences.{STRINGDB_VERSION}.fa.gz",

                f"wget -c https://stringdb-downloads.org/download/protein.links.full.{STRINGDB_VERSION}.txt.gz",
                f"gunzip -f protein.links.full.{STRINGDB_VERSION}.txt.gz",
                f"rm -f protein.links.full.{STRINGDB_VERSION}.txt.gz",

                f"wget -c https://stringdb-downloads.org/download/protein.info.{STRINGDB_VERSION}.txt.gz",
                f"gunzip -f protein.info.{STRINGDB_VERSION}.txt.gz",
                f"rm -f protein.info.{STRINGDB_VERSION}.txt.gz",

                f"python3 ./index_string.py --links protein.links.full.{STRINGDB_VERSION}.txt --info protein.info.{STRINGDB_VERSION}.txt --out protein",
                f"diamond makedb --threads 4 --in protein.sequences.{STRINGDB_VERSION}.fa -d protein.sequences.{STRINGDB_VERSION}",
            ],
        },
        "uniprot_sprot": {
            "dir": "uniprot_sprot",
            "script": [
                "wget -c ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.fasta.gz",
                "gunzip -f uniprot_sprot.fasta.gz",
                "wget -c ftp://ftp.expasy.org/databases/enzyme/enzyme.dat",
                "diamond makedb --threads 4 --in uniprot_sprot.fasta -d uniprot_sprot",
                "rm -f uniprot_sprot.fasta.gz",
            ],
        },
        "uniprot_trembl": {
            "dir": "uniprot_trembl",
            "script": [
                "wget -c ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_trembl.fasta.gz",
                "gunzip -f uniprot_trembl.fasta.gz",
                "diamond makedb --threads 4 --in uniprot_trembl.fasta -d uniprot_trembl",
                "rm -f uniprot_trembl.fasta.gz"
            ],
        },
    }


def list_datasets():
    """
    Prints list of all possible download datasets that can be done to the user to
    standard output.
    """
    datasets = get_datasets()

    print("The following datasets are available:")
    for name in datasets:
        print(f" - {name}")


def write_session(session, outdir):
    """
    Writes the session to a file. Uses file locking to prevent clobbering.
    """

    session_file = f"{outdir}/session.json"

    with open(session_file, "w") as file:

        # Acquire exclusive lock on the file
        fcntl.flock(file.fileno(), fcntl.LOCK_EX)

        # Write the session
        file.write(json.dumps(session, indent=4) + "\n")

        # Release the lock
        fcntl.flock(file.fileno(), fcntl.LOCK_UN)

def load_session(outdir):
    """
    Loads the global session state from the session JSON file if it exists, else
    it loads a new default session state. Resets any task from the given command
    line argument string.
    """
    session_file = f"{outdir}/session.json"
    session = {}

    datasets = get_datasets()

    # Open and load the session file
    if os.path.isfile(session_file):
        with open(session_file, "r") as file:
            session = json.loads(file.read())

    # Make sure every task has an entry in the
    # session file.
    for name in datasets:
        if name not in session:
            reset_task(name, session, outdir)

    return session


def reset_task(name, session, outdir):
    """
    Resets the session for this task by setting the step back to 0 and removing the log file.
    """
    datasets = get_datasets()

    # Set the step to 0
    session[name] = 0

    # Remove any existing log file.
    dirPath = datasets[name]["dir"]
    working_dir = f"{outdir}/{dirPath}"
    log_file = f"{working_dir}/log.txt"
    if os.path.exists(log_file):
        os.remove(log_file)


def log_message(log, message):
    """
    Logs a message for the task.
    """
    print(message)
    log.write(f"{message}\n")
    log.flush()

def process_task(name, session, outdir):
    """
    Processes the task with the given key in the datasets, using
    the global session state to determine where to start in the task. Any task
    that is complete is ignored and this does nothing.

    Parameters
    ----------
    name : string
        Key name of the task that is processed.
    """
    state = session[name]
    datasets = get_datasets()
    dirPath = datasets[name]["dir"]
    steps = datasets[name]["script"]

    # Make sure the working directory exists
    working_dir = f"{outdir}/{dirPath}"
    if not os.path.isdir(working_dir):
        os.makedirs(working_dir)

    # Open the log file
    log_file = f"{working_dir}/log.txt"
    log = open(log_file, "a")

    # Change to the required working directory
    os.chdir(working_dir)

    # Perform the next task in the state.
    for i in range(len(steps)):
        if i < state:
            log_message(log, "Previously completed step %i of %i for %s" % (i + 1, len(steps), name))
        else:
            step = steps[i]
            log_message(log, f"  {step}")
            if os.system(step):
                log_message(log, "FAILURE: step %i of %i for %s: %s" % (i + 1, len(steps), name, step))
                log.close()
                return False
            log_message(log, "Successfully completed step %i of %i for %s" % (i + 1, len(steps), name))
            state += 1
            session[name] = state

    log_message(log, f"Successfully completed task {name}")
    log.close()
    return True


def main():
    """
    The main function
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", dest='outdir', required=True, help="The directory path where the downloaded files will be stored")
    parser.add_argument("--list", action='store_true', help="Print the list of available datasets for download")
    parser.add_argument("--reset", action='store_true', help="By deafult, if the file exists it won't be redownloaded. Use this to force a redownload for any datasets.")
    parser.add_argument("--datasets", dest="requests", nargs="?", default=None, help="Perform one or more datasets. Provide a comma-separted list of task names.")
    args = parser.parse_args()

    # Load the session information.
    session = load_session(args.outdir)

    # Print the list of available datasets.
    if args.list is True:
        list_datasets()
        return

    datasets = get_datasets()
    # Run the steps for each specified task.
    if args.requests is not None:
        requests = set((s.strip() for s in args.requests.split(",") if s))
        try:
            for name in requests:

                # If the requested dataset doesn't exist then print an error and return
                if name not in datasets.keys():
                    print(f"ERROR: Uknown dataset: \"{name}\". Use the --list argument to see a list of valid datasets. ")
                    return

                # If the user wants to reset the session for this dataset do so.
                if args.reset is True:
                    reset_task(name, session, args.outdir)

                # Process the dataset
                print(f"Processing dataset: \"{name}\"")
                process_task(name, session, args.outdir)

                # Update the session for this dataset.
                write_session(session, args.outdir)

        except Exception as error:
            print("ERROR:", error)

        finally:
            write_session(session, args.outdir)
            return

    parser.print_help()

if __name__ == "__main__":
    main()
