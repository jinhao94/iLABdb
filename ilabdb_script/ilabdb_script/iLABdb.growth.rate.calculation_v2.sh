#!/bin/bash 

function display_help() {
    echo " "
    echo "Fasta_to_sample: Converts assembly in fasta format to scaffolds-to-sample table."
    echo "Usage: Fasta2sample.sh -e fasta > my_scaffolds2bin.tsv"
    echo " "
    echo "   -i, --input_ffn            Path of input ffn."
    echo "   -g, --input_gff3           GFF3 file."
    echo "   -o, --output_dir           Output directory. "
    echo "   -p, --prefix               Output file prefix. "
    echo "   -h, --help                 Show this message. "
    echo "   -f, --froce                Force overwrite output file. "
    echo " "
    echo " "
    exit 1
}

if [ $# -eq 0 ];then
  display_help
  exit 1
fi

input_ffn="None"
input_gff3="None"
output_dir="None"
prefix="None"
froce="F"

while [ "$1" != "" ]; do
    case $1 in
        -i | --input_ffn )      shift
                                input_ffn=$1
                                ;;
        -g | --input_gff3 )     shift
                                input_gff3=$1
                                ;;
        -o | --output_dir )     shift
                                output_dir=$1
                                ;;
        -p | --prefix )         shift
                                prefix=$1
                                ;;
        -f | --froce )          shift
                                froce="T"
                                ;;
        -h | --help )           display_help
                                exit
                                ;;
        * )                     display_help
                                exit 1
    esac
    shift
done

if [ $input_ffn == "None" ] || [ $input_gff3 == "None" ] || [ $output_dir == "None" ] || [ $prefix == "None" ]; then
    display_help
fi


if [ -d $output_dir ];then
    if [ $froce == "T"  ];then
        echo "Output folder exist, so remove..."
        rm -rf $output_dir
    else
        echo "Output folder exist, so exit. Please use -f or --force to overwrite it."
        exit
    fi  
fi

mkdir $output_dir 

gff3_filt=${output_dir}/${prefix}.gene.gff3.filt
gene_info=${output_dir}/${prefix}.gene.info
CDS_names=${output_dir}/${prefix}.CDS.names
res_file=${output_dir}/${prefix}.grwoth.res

#echo  $input_gff3 $gene_info  $CDS_names 

awk -F"\t" '$3=="CDS"' $input_gff3 | perl -a -F"\t" -lne '@F[-1]=~/ID=(.*?)\;/; $id=$1; $l1=@F[0]."_".@F[3]."_".@F[4]; $l2=$id; $l3=@F[0]; $o=(join "\t", @F[1..$#F]); print "$l1\t$l2\t$l3\t$o" ' > $gene_info
cut -f2 $gene_info > $CDS_names

source activate gRodon
/ddn/conda/envs/gRodon/bin/Rscript /ddn/script/ilabdb_script/iLABdb.growth.rate.calculation.R $input_ffn $CDS_names $gene_info $res_file
source deactivate 
