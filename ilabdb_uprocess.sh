#!/bin/bash
# Author：Jinhao 

export PATH=/ddn/conda/bin:/ddn/links:/ddn/conda/envs/ilabdb/bin:$PATH

function display_help() {
    echo ""
    echo -e "A pipeline for LAB analysis pipeline..."
    echo -e "Author jinh"
    echo "-_-!!!"
    echo "   -i, --input_genome_list    New LAB genome list, generated by get_ilabdb_id.py [*Required]"
    echo "   -o, --outdir               The absolute path of output folder (default: /ddn/userdata/iLABdb/iLABdb.user.sub.data)"
    echo "   -t, --threads              Number of threads (default: 8)"
    echo "   -h, --help                 Show this message"
    echo " "
    exit 1
}

# echo $#
if [ $# -eq 0  ];then
    echo "Please input parameters!"
    display_help
fi

## default settings.
input_genome_list="None"
threads=8
outdir="/ddn/userdata/iLABdb/iLABdb.user.sub.data"


while [ "$1" != "" ]; do
    case $1 in
        -i | --input_genome_list ) shift
                                  input_genome_list=$1
                                  ;;
        -t | --threads)           shift
                                  threads=$1
                                  ;;
        -o | --outdir)            shift
                                  outdir=$1
                                  ;;
        * )                       display_help
                                  exit 1
    esac
    shift
done

if [ "${outdir:0:1}" = "/" ]
then
    # echo "Input file path is absolute. Running program..."
    out_path=$outdir
else
    # echo "Input file path is relative, Changing the path to absolute"
    out_path=$PWD/$outdir

fi


if [ "${input_genome_list:0:1}" = "/" ]
then
    # echo "Input file path is absolute. Running program..."
    run_path=$input_genome_list
else
    # echo "Input file path is relative, Changing the path to absolute"
    run_path=$PWD/$input_genome_list

fi

# echo $run_path
source activate /ddn/conda/envs/ilabdb
echo "snakemake -s /ddn/script/ilabdb_script/ilab_snakemeke.py --default-resources \"tmpdir=\'/ddn/userdata/iLABdb/iLABdb.user.sub.data/temp\'\" ---config workdir=$out_path genome_path_list=$run_path -r -p --cores $threads -j $threads --rerun-incomplete"

# echo "              00000000000000000000000            "
# echo $PATH

snakemake -s /ddn/script/ilabdb_script/ilab_snakemeke.py --default-resources "tmpdir='/ddn/userdata/iLABdb/iLABdb.user.sub.data/temp'" --config workdir=$out_path genome_path_list=$run_path -k -r -p --cores $threads -j $threads --rerun-incomplete