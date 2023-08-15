#!/ddn/conda/envs/ilabdb/bin/python
import os, sys
import argparse
import fcntl
import time
from collections import defaultdict
import textwrap
from Bio import SeqIO


parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=textwrap.dedent('''\
This program is used to determine whether the input file conforms to the fasta format and calculate the bacterial genome characteristics (that is Genome_size, N_contigs, GC_content, Assembly_level, N50_length).
nucleotide sequences for LAB genome, must meet the following format
>SequenceName1
ATCGATCGATCG...
>SequenceName2
CTAGCTAGCTA...'''))

parser.add_argument('--input', '-i', required=True, help='input absolute path of LAB genomes')
parser.add_argument('--outinfo', '-o', required=True, help='output file, tsv format')

args = parser.parse_args()
filename = args.input
outfile = args.outinfo


ilab_id_file = '/ddn/script/ilabdb_script/ilabdb.id'

def is_fasta_file(file_path):
    Allbase = ""
    for record in SeqIO.parse(open(file_path), "fasta"):
        Allbase += record.seq.upper()
    if not set(Allbase).issubset({"A", "T", "C", "G", "N"}):
        return False
    else:
        return True

file_check_res = defaultdict(list)

while True:
    try:
        # fcntl.flock(file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        with open(ilab_id_file, "r") as file:
            fcntl.flock(file.fileno(), fcntl.LOCK_EX)
            ilab_id = int(file.readline().strip())
        break
    except IOError:
        time.sleep(15)
        pass
with open(outfile, "w") as of:
    with open(filename, "r") as f:
        for line in f:
            genome_path = line.strip()
            if not os.path.exists(genome_path):
                out = genome_path + "\t" + "NA" + "\t" + "Illegal format"
                of.write(out + "\n")
                # print(genome_path, "NA", "Illegal format")
            else:
                res = is_fasta_file(genome_path)
                if res == True:
                    ilab_id += 1
                    ilab_name = "iLABdb.g" + str(ilab_id)
                    # print(genome_path, ilab_name, "Legal format")
                    # of.write(genome_path, "\t", ilab_name, "\t", "Legal format")
                    out = genome_path + "\t" + ilab_name + "\t" + "Legal format"
                    of.write(out + "\n")
                else:
                    # print(genome_path, "NA", "Illegal format")
                    out = genome_path + "\t" + "NA" + "\t" + "Illegal format"
                    of.write(out + "\n")

with open(ilab_id_file, "w") as file:
    fcntl.flock(file.fileno(), fcntl.LOCK_UN)
    file.write(str(ilab_id))
    

    
