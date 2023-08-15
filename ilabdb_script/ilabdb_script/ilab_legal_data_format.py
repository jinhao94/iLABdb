import os, sys
import argparse
import textwrap
from Bio import SeqIO

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=textwrap.dedent('''\
This program is used to determine whether the input file conforms to the fasta format and calculate the bacterial genome characteristics (that is Genome_size, N_contigs, GC_content, Assembly_level, N50_length).
nucleotide sequences for LAB genome, must meet the following format
>SequenceName1
ATCGATCGATCG...
>SequenceName2
CTAGCTAGCTA...'''))

parser.add_argument('--input', '-i', required=True, help='nucleotide sequences for LAB genome, must meet the following format')
parser.add_argument('--prefix', '-p', required=True, help='output name list, tsv format')
parser.add_argument('--outinfo', '-o', required=True, help='output file, tsv format')
parser.add_argument('--outfasta', '-of', required=True, help='output fasta file')
parser.add_argument('--outname', '-on', required=True, help='output name list, tsv format')


args = parser.parse_args()
filename = args.input
outfasta = args.outfasta
outname = args.outname
outinfo = args.outinfo
new_ilabid = args.prefix


def is_fasta_file(Allbase):
    if not set(Allbase).issubset({"A", "T", "C", "G", "N"}):
        return False
    else:
        return True

def cacul_n50(Length_list, Genome_size):
    ValueSum = 0.0
    Length_list.sort(reverse = True)
    N50_position = Genome_size/2.0
    for value in Length_list:
        ValueSum += value
        if N50_position <= ValueSum:
            N50_length = value
            break
    return N50_length

def load_fasta_file(filename):
    
    ## 设置变量
    Length_list, Allbase = [], ""
    ## 开始流程
    for record in SeqIO.parse(open(filename), "fasta"):
        Length_list.append(len(record.seq))
        Allbase += record.seq.upper()
    ## 判断是否满足fasta格式文件
    if is_fasta_file(Allbase):
        
        ## 计算基因组大小, contig/scaffold数
        Genome_size = len(Allbase)
        N_contigs = len(Length_list)        
        ## 计算GC含量
        N_G = Allbase.count('G')
        N_C = Allbase.count('C')
        N_N = Allbase.count('N')
        GC_content = round(float(N_G + N_C)/Genome_size * 100, 2) ## percent GC
        
        ## 查看 assembly level
        """
        如果 N_N >= 1 -- scaffold level
        否则 -- contig level
        """
        if (N_N >= 1):
            Assembly_level = "Scaffold"
        else:
            Assembly_level = "Contig"
        
        ## 计算 N50
        N50_length = cacul_n50(Length_list, Genome_size)
    else:
        return False
    return Genome_size, N_contigs, GC_content, Assembly_level, N50_length


if load_fasta_file(filename):
    outlist = ["Genome_size", "N_contigs", "GC_content", "Assembly_level", "N50_length"]
    # Genome_size, N_contigs, GC_content, Assembly_level, N50_length = load_fasta_file(filename)
    with open(outinfo, "w") as outfile:
        cto = 0
        for info in load_fasta_file(filename):
            outfile.write(outlist[cto] + "\t" + str(info) + "\n")
            cto += 1
else:
    print(f"{filename} is not a valid FASTA file.")
    raise SystemExit(1)

# 设置ilab id
count = 1
with open(outfasta, 'w') as seqfile:
    with open(outname, 'w') as namefile:
        for record in SeqIO.parse(open(filename), "fasta"):
            # new_seq_name =  "iLABdb.g" + str(new_ilabid) + "_" + str(count)
            new_seq_name =  str(new_ilabid) + "_" + str(count)
            seqfile.write(">" + new_seq_name + "\n")
            seqfile.write(str(record.seq) + "\n")
            namefile.write(record.description + "\t" + new_seq_name +  "\n")
            count += 1