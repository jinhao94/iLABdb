## 路径
## /ddn/userdata/iLABdb/test
ls $PWD/test.genome/*fa
get_ilabdb_id.py -i test.in -o test.in.confir

## /ddn/userdata/iLABdb


snakemake -s /ddn/script/ilabdb_script/ilab_snakemeke.py --default-resources "tmpdir='/ddn/userdata/iLABdb/temp'" --config workdir=/ddn/userdata/iLABdb/test_run genome_path_list=/ddn/userdata/iLABdb/test/test.in.confir -r -p --cores 32 -j 32 --rerun-incomplete
