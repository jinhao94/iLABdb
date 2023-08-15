import snakemake
from glob import glob

workdir: config['workdir']
script_path = "/ddn/script/ilabdb_script"
db_dir = "/ddn/database"

genome_path_list = config['genome_path_list']

geneme_files = {}

with open(genome_path_list, 'r') as f:
    for line in f:
        items = line.strip().split("\t")
        if items[1] != "NA":
            geneme_files[items[1]] = items[0]
            # print(items[0])

ilabids = list(geneme_files.keys())


rule all:
    input:
        expand("0.genome.info/{ilabid}/{ilabid}.task.done", ilabid = ilabids)

rule format_check:
    input:
        lambda wildcards: geneme_files[wildcards.ilabid]
    output:
        "0.genome.info/{ilabid}/{ilabid}.fa",
        "0.genome.info/{ilabid}/{ilabid}.name",
        "0.genome.info/{ilabid}/{ilabid}.info"
    threads: 1
    shell:
        """
        python /ddn/script/ilabdb_script/ilab_legal_data_format.py -i {input} -of {output[0]} -on {output[1]} -o {output[2]} -p {wildcards.ilabid}
        """

rule run_fastANI:
    input:
        "0.genome.info/{ilabid}/{ilabid}.fa"
    threads:3
    output:
        ""
        "0.genome.info/{ilabid}/{ilabid}.ani",
        "0.genome.info/{ilabid}/{ilabid}.ANI.res"
        ""
    shell:
        """
        /ddn/conda/envs/ilabdb/bin/fastANI -q {input} --refList /ddn/script/script_sup/ilabdb.rep.genome.path --visualize -o {output[0]} -t 3  
        sh /ddn/script/ilabdb_script/iLABdb.ani.format.sh {output[0]} {output[1]}
        """
        

rule run_chromsize:
    input:
        "0.genome.info/{ilabid}/{ilabid}.fa"
    output:
        "0.genome.info/{ilabid}/{ilabid}.chromsize"
    shell:
        """
        seq_len {input} > {output}
        """

rule run_bakta:
    input:
        "0.genome.info/{ilabid}/{ilabid}.fa"  
    threads: 20
    params:
        outdir = "0.genome.info/{ilabid}/{ilabid}.bak"
    output:
        temp("0.genome.info/{ilabid}/{ilabid}.bak/{ilabid}.embl"),
        "0.genome.info/{ilabid}/{ilabid}.bak/{ilabid}.faa",
        "0.genome.info/{ilabid}/{ilabid}.bak/{ilabid}.ffn",
        temp("0.genome.info/{ilabid}/{ilabid}.bak/{ilabid}.fna"),
        "0.genome.info/{ilabid}/{ilabid}.bak/{ilabid}.gbff",
        "0.genome.info/{ilabid}/{ilabid}.bak/{ilabid}.gff3",
        temp("0.genome.info/{ilabid}/{ilabid}.bak/{ilabid}.hypotheticals.faa"),
        temp("0.genome.info/{ilabid}/{ilabid}.bak/{ilabid}.hypotheticals.tsv"),
        "0.genome.info/{ilabid}/{ilabid}.bak/{ilabid}.json",
        "0.genome.info/{ilabid}/{ilabid}.bak/{ilabid}.tsv",
        "0.genome.info/{ilabid}/{ilabid}.bak/{ilabid}.txt"
    shell:
        """
        bakta --min-contig-length 200 --db /ddn/database/bakta_db_light/db-light --locus {wildcards.ilabid} --prefix {wildcards.ilabid} --output {params.outdir} --keep-contig-headers --skip-plot --locus-tag {wildcards.ilabid} {input} --threads {threads}
        """

rule run_rrna_loca:
    input:
        "0.genome.info/{ilabid}/{ilabid}.bak/{ilabid}.tsv"
    output:
        "0.genome.info/{ilabid}/{ilabid}.rrna.loca.tsv"
    shell:
        """
        sh /ddn/script/ilabdb_script/rrna_loca.sh {input} {output}
        """

rule run_gene_loca:
    input:
         "0.genome.info/{ilabid}/{ilabid}.bak/{ilabid}.tsv"
    output:
        "0.genome.info/{ilabid}/{ilabid}.gene.loca"
    shell:
        """
        sh /ddn/script/ilabdb_script/gene_loca.sh {input} {output}
        """

rule run_eggnog:
    input:
        "0.genome.info/{ilabid}/{ilabid}.bak/{ilabid}.faa"
    threads: 20
    params:
        outprefix = "0.genome.info/{ilabid}/{ilabid}",
        temp_dir = "0.genome.info/{ilabid}/"
    output:
        "0.genome.info/{ilabid}/{ilabid}.emapper.annotations",
        temp("0.genome.info/{ilabid}/{ilabid}.emapper.hits"),
        temp("0.genome.info/{ilabid}/{ilabid}.emapper.seed_orthologs")
    shell:
        """
        emapper.py --cpu {threads} --output {params.outprefix} --itype proteins -i {input} -m diamond --evalue 1e-10 --override --sensmode  fast --temp_dir {params.temp_dir}
        """

rule run_eggnog_process:
    input:
        rules.run_eggnog.output[0]
    threads: 1
    output:
        "0.genome.info/{ilabid}/{ilabid}.ko.gene",
        "0.genome.info/{ilabid}/{ilabid}.KO",
        "0.genome.info/{ilabid}/{ilabid}.pfam.gene",
        "0.genome.info/{ilabid}/{ilabid}.pfam"
    shell:
        """
        sh {script_path}/eggnog_process.sh {input} {output[0]} {wildcards.ilabid} {output[1]} {output[2]} {output[3]}
        """

rule run_KEGG_core:
    input:
        rules.run_eggnog_process.output[1]
    threads: 1
    params:
        core_out = "0.genome.info/{ilabid}/{ilabid}.KO.core"
    output:
        "0.genome.info/{ilabid}/{ilabid}.KO.core/{ilabid}.modules"
    shell:
        """
        java -jar {script_path}/omixer-rpm-1.1.jar -d {script_path}/new_pathway.f -c 0.66 -i {input} -o {params.core_out} -t 1 
        """

rule run_KEGG_core_des:
    input:
        "0.genome.info/{ilabid}/{ilabid}.KO.core/{ilabid}.modules"
    threads: 1
    output:
        "0.genome.info/{ilabid}/{ilabid}.KO.res"
    shell:
        """
        sh {script_path}/kegg_core_des.sh {input} {output}
        """


rule run_KEGG:
    input:
        rules.run_eggnog_process.output[1]
    threads: 1
    params:
        module_out = "0.genome.info/{ilabid}/{ilabid}.module"
    output:
        "0.genome.info/{ilabid}/{ilabid}.KEGG.l1",
        "0.genome.info/{ilabid}/{ilabid}.KEGG.l2",
        "0.genome.info/{ilabid}/{ilabid}.KEGG.l3",
        "0.genome.info/{ilabid}/{ilabid}.module/KEGG_module_choosed_reaction.csv",
        "0.genome.info/{ilabid}/{ilabid}.module/KEGG_module_coverage.csv",
        "0.genome.info/{ilabid}/{ilabid}.module/KEGG_module_mean_abundance.csv",
        "0.genome.info/{ilabid}/{ilabid}.module/KEGG_module_median_abundance.csv",
        touch("0.genome.info/{ilabid}/{ilabid}.kegg.task.done")
    shell:
        """
        python /ddn/links/19_get_kegg_level1_sum.py {input} {output[0]}
        python /ddn/links/19_get_kegg_level2_sum.py {input} {output[1]}
        python /ddn/links/19_get_kegg_level3_sum.py {input} {output[2]}
        python /ddn/links/Bin_module_completeness.py -i {input} -o {params.module_out} --force
        """


rule run_KEGG_module_des:
    input:
        "0.genome.info/{ilabid}/{ilabid}.module/KEGG_module_coverage.csv"
    threads: 1
    output:
        "0.genome.info/{ilabid}/{ilabid}.module/KEGG_module_coverage.des.tsv",
    shell:
        """
        sh {script_path}/kegg_module_des.sh {input} {output}
        """


rule run_gutsmash:
    input:
        "0.genome.info/{ilabid}/{ilabid}.fa"
    threads: 3
    params:
        outdir = "0.genome.info/{ilabid}/{ilabid}.MGC"
    output:
        "0.genome.info/{ilabid}/{ilabid}.MGC/{ilabid}.zip",
        "0.genome.info/{ilabid}/{ilabid}.MGC/index.html"
    shell:
        """
        run_gutsmash.py -c {threads} --genefinding-tool prodigal --cb-knownclusters --enable-genefunctions {input} --output-dir {params.outdir} 
        """

rule run_gutsmash_process:
    input:
        "0.genome.info/{ilabid}/{ilabid}.MGC/index.html"
    threads: 1
    output:
        "0.genome.info/{ilabid}/{ilabid}.MGC.summary"
    shell:
        """
        sh {script_path}/Bin_gutsmash_ilab.sh {input} > {output}
        """

rule run_phispy:
    input:
        "0.genome.info/{ilabid}/{ilabid}.bak/{ilabid}.gbff"
    threads: 3
    params:
        outdir = "0.genome.info/{ilabid}/{ilabid}.pro"
    output:
        "0.genome.info/{ilabid}/{ilabid}.pro/{ilabid}_phage.fasta",
        "0.genome.info/{ilabid}/{ilabid}.pro/{ilabid}_phage.gbk",
        "0.genome.info/{ilabid}/{ilabid}.pro/{ilabid}_phispy.log",
        "0.genome.info/{ilabid}/{ilabid}.pro/{ilabid}_prophage_coordinates.tsv",
        "0.genome.info/{ilabid}/{ilabid}.pro/{ilabid}_prophage.gff3",
        "0.genome.info/{ilabid}/{ilabid}.pro/{ilabid}_prophage_information.tsv",
        "0.genome.info/{ilabid}/{ilabid}.pro/{ilabid}_prophage.tbl",
        "0.genome.info/{ilabid}/{ilabid}.pro/{ilabid}_prophage.tsv",
        "0.genome.info/{ilabid}/{ilabid}_prophage.tsv",
        temp("0.genome.info/{ilabid}/{ilabid}.pro/{ilabid}_bacteria.fasta"),
        temp("0.genome.info/{ilabid}/{ilabid}.pro/{ilabid}_bacteria.gbk"),
        temp("0.genome.info/{ilabid}/{ilabid}.pro/{ilabid}_{ilabid}.gbff"),
        temp("0.genome.info/{ilabid}/{ilabid}.pro/{ilabid}_test_data.tsv"),
        touch("0.genome.info/{ilabid}/{ilabid}.prophage.done")
    shell:
        """
        PhiSpy.py --phmms {db_dir}/pVOGdb/pVOGs.hmm --threads {threads} -o {params.outdir} --file_prefix {wildcards.ilabid} --color --output_choice 255 {input}
        cp {output[7]} {output[8]}
        """


rule run_growthrate:
    input:
        "0.genome.info/{ilabid}/{ilabid}.bak/{ilabid}.ffn",
        "0.genome.info/{ilabid}/{ilabid}.bak/{ilabid}.gff3"
    threads: 3
    params:
        outdir = "0.genome.info/{ilabid}/{ilabid}.growth.rate"
    output:
        temp("0.genome.info/{ilabid}/{ilabid}.growth.rate/{ilabid}.CDS.names"),
        temp("0.genome.info/{ilabid}/{ilabid}.growth.rate/{ilabid}.gene.info"),
        "0.genome.info/{ilabid}/{ilabid}.growth.rate/{ilabid}.grwoth.res"
    shell:
        """
        sh {script_path}/iLABdb.growth.rate.calculation_v2.sh -i {input[0]} -g {input[1]} -o {params.outdir} -p {wildcards.ilabid} -f
        """

rule run_VFDB:
    input:
        "0.genome.info/{ilabid}/{ilabid}.bak/{ilabid}.faa"
    threads:3
    output:
        "0.genome.info/{ilabid}/{ilabid}.vfdb.ant",
        "0.genome.info/{ilabid}/{ilabid}.vfdb"
    shell:
        """
        diamond blastp -q {input} -d /ddn/database/VFDB/VFDB_setB_pro.fas --threads {threads} --out {output[0]} --evalue 1e-10 --outfmt 6
        sh {script_path}/vfdb_process.sh {output[0]} {output[1]}
        """


rule get_vfdb_pos:
    input:
        "0.genome.info/{ilabid}/{ilabid}.vfdb",
        "0.genome.info/{ilabid}/{ilabid}.gene.loca"
    threads:1
    output:
        "0.genome.info/{ilabid}/{ilabid}.VFDB.position"
    shell:
        """
        sh {script_path}/ilabdb.get_vfdb_pos.sh {input} {output}
        """


rule run_CAZY:
    input:
        "0.genome.info/{ilabid}/{ilabid}.bak/{ilabid}.faa"
    threads:3
    output:
        "0.genome.info/{ilabid}/{ilabid}.cazy.ant",
        "0.genome.info/{ilabid}/{ilabid}.cazy"
    shell:
        """
        diamond blastp -q {input} -d {db_dir}/CAZY/CAZyDB.09242021.dmnd --threads {threads} --out {output[0]} --evalue 1e-10 --outfmt 6
        sh {script_path}/cazy_process.sh {output[0]} {output[1]}
        """


# 注意可能有空值！！！
rule run_ARG:
    input:
        "0.genome.info/{ilabid}/{ilabid}.fa"
    threads:3
    output:
        "0.genome.info/{ilabid}/{ilabid}.arg"
    shell:
        """
        abricate --db ncbi {input} --threads {threads} > {output}
        """

rule task_done:
    input:
        rules.run_bakta.output,
        "0.genome.info/{ilabid}/{ilabid}.ANI.res",
        "0.genome.info/{ilabid}/{ilabid}.cazy",
        "0.genome.info/{ilabid}/{ilabid}.vfdb",
        "0.genome.info/{ilabid}/{ilabid}.arg",
        "0.genome.info/{ilabid}/{ilabid}.growth.rate/{ilabid}.grwoth.res",
        "0.genome.info/{ilabid}/{ilabid}.prophage.done",
        "0.genome.info/{ilabid}/{ilabid}.MGC.summary",
        rules.run_eggnog_process.output,
        "0.genome.info/{ilabid}/{ilabid}.rrna.loca.tsv",
        "0.genome.info/{ilabid}/{ilabid}.gene.loca",
        "0.genome.info/{ilabid}/{ilabid}.VFDB.position",
        "0.genome.info/{ilabid}/{ilabid}.KEGG.l1",
        "0.genome.info/{ilabid}/{ilabid}.KEGG.l2",
        "0.genome.info/{ilabid}/{ilabid}.KEGG.l3",
        "0.genome.info/{ilabid}/{ilabid}.module/KEGG_module_coverage.des.tsv",
        "0.genome.info/{ilabid}/{ilabid}.KO.core/{ilabid}.modules",
        "0.genome.info/{ilabid}/{ilabid}.KO.res",
        "0.genome.info/{ilabid}/{ilabid}.chromsize"

    output:
        touch("0.genome.info/{ilabid}/{ilabid}.task.done"),
        "0.genome.info/{ilabid}/{ilabid}.res.zip"
    shell:
        """
        echo "------"
        zip -r {output[1]} {input}
        """

