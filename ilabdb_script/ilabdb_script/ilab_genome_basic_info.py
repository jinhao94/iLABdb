import os, sys
import argparse

from Bio import SeqIO

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description = 'This program is used to re')

parser.add_argument('--input', '-i', required=True, help='fasta format genome')
parser.add_argument('--outfasta', '-of', required=True, help='output fasta file')
parser.add_argument('--outname', '-on', required=True, help='output name list, tsv format')

args = parser.parse_args()

filename = args.input
outfasta = args.outfasta
outname = args.outname

ilab_genome_id = "/ddnstor/imau_sunzhihong/mnt1/ilabdb_script/ilabdb.genome.id"

with open(ilab_genome_id, "r") as f: 
    ilabid = int(f.readline().strip())
    new_ilabid = ilabid + 1

count = 1
with open(outfasta, 'w') as seqfile:
    with open(outname, 'w') as namefile:
        for record in SeqIO.parse(open(filename), "fasta"):
            new_seq_name =  "iLABdb.g" + str(new_ilabid) + "_" + str(count)
            seqfile.write(">" + new_seq_name + "\n")
            seqfile.write(str(record.seq) + "\n")
            namefile.write(record.description + "\t" + new_seq_name +  "\n")
            count += 1

with open(ilab_genome_id, 'w') as id_file:
    id_file.write(str(new_ilabid))