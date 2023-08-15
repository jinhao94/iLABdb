#!/bin/bash 

function display_help() {
    echo " "
    echo "Fasta_to_sample: Converts assembly in fasta format to scaffolds-to-sample table."
    echo "Usage: Fasta2sample.sh -e fasta > my_scaffolds2bin.tsv"
    echo " "
    echo "   -i, --input_dir           Path of input dir."
    echo "   -o, --output_file         Output file. "
    echo "   -p, --prefix              Output file prefix. "
    echo " "
    echo " "
    exit 1
}


if [ $# -eq 0 ];then
  display_help
  exit 1
fi

input_dir="None"
output_file="None"
prefix="None"


while [ "$1" != "" ]; do
    case $1 in
        -i | --input_dir )      shift
                                input_dir=$1
                                ;;
        -o | --output_file )    shift
                                output_file=$1
                                ;;
        -p | --prefix )         shift
                                prefix=$1
                                ;;
        -h | --help )           display_help
                                exit
                                ;;
        * )                     display_help
                                exit 1
    esac
    shift
done



basic_txt=${input_dir}/${prefix}.bak/${prefix}.txt
rrna_loca=${input_dir}/${prefix}.bak/${prefix}.rrna.loca.tsv
ko=${input_dir}/${prefix}.ko.gene
Number_of_CAZymes=${input_dir}/${prefix}.cazy
Number_of_Pfam_genes=${input_dir}/${prefix}.pfam.gene
Number_of_ARGs_genes=${input_dir}/${prefix}.arg
Number_of_virulence_factors=${input_dir}/${prefix}.VFDB.position
Max_growth_rate=${input_dir}/${prefix}.growth.rate/${prefix}.grwoth.res


if [ $output_file == "None" ] || [ $prefix == "None" ]; then
    echo "Please input output_file and prefix."
    exit
fi

if [ ! -f $basic_txt ] ; then
    echo $basic_txt
    echo "basic_txt is missing"
    exit
fi

if [ ! -f $rrna_loca ] ; then
    echo $rrna_loca
    echo "rrna_loca is missing"
    exit
fi

if [ ! -f $ko ] ; then
    echo "ko is missing"
    exit
fi

if [ ! -f $Number_of_CAZymes ] ; then
    echo "Number_of_CAZymes is missing"
    exit
fi

if [ ! -f $Number_of_Pfam_genes ] ; then
    echo "Number_of_Pfam_genes is missing"
    exit
fi

if [ ! -f $Number_of_ARGs_genes ] ; then
    echo "Number_of_ARGs_genes is missing"
    exit
fi

if [ ! -f $Number_of_virulence_factors ] ; then
    echo "Number_of_virulence_factors is missing"
    exit
fi

if [ ! -f $Max_growth_rate ] ; then
    echo "Max_growth_rate is missing"
    exit
fi

echo -e  "Genome_ID\t${prefix}" > $output_file

# basic info
less $basic_txt | perl -e 'while(<>){chomp; if($_=~/^Length: (\d+)/){$size=$1}elsif($_=~/^Count: (\d+)/){$N_contigs=$1}elsif($_=~/^GC: (\d+)/){$GC=$1}elsif($_=~/^CDSs: (\d+)/){$CDSs=$1}elsif($_=~/^N50: (\d+)/){$N50=$1}elsif($_=~/^tRNAs: (\d+)/){$tRNAs=$1} } ; print "Genome_size\t$size\nN_contigs\t$N_contigs\nN50\t$N50\nGC_content\t$GC\nCDS\t$CDSs\nNumber_of_trna_genes\t$tRNAs\n"' >> $output_file

## 5s 16s 23s tRNA
less $rrna_loca | perl -e '$s5s=0; $s16s=0; $s23s=0; while(<>){chomp; @s=split /\t/; if(@s[5] == "5S ribosomal RNA"){$s5s++}elsif(@s[5] == "23S ribosomal RNA"){$s23s++}elsif(@s[5] == "16S ribosomal RNA"){$s16s++};}; print "Number_of_5S_genes\t$s5s\nNumber_of_16S_genes\t$s16s\nNumber_of_23S_genes\t$s23s\n" ' >> $output_file

## KO
sed '1d' $ko | wc -l | perl -lane 'print "Number_of_KOs\t$_" '  >> $output_file
## Number_of_CAZymes
sed '1d' $Number_of_CAZymes | wc -l | perl -lane 'print "Number_of_CAZymes\t$_" ' >> $output_file
## Number_of_Pfam_genes
sed '1d' $Number_of_Pfam_genes | wc -l | perl -lane 'print "Number_of_Pfam_genes\t$_" ' >> $output_file
## Number_of_ARGs_genes
sed '1d' $Number_of_ARGs_genes | wc -l | perl -lane 'print "Number_of_ARGs_genes\t$_" ' >> $output_file
## Number_of_virulence_factors
sed '1d' $Number_of_virulence_factors | wc -l | perl -lane 'print "Number_of_virulence_factors\t$_"' >> $output_file
## Max_growth_rate
less $Max_growth_rate | perl -lane 'print "Max_growth_rate\t@F[1]" if @F[0] eq "d"' >> $output_file


