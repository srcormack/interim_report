class GlobalConstants:
    CPUS_PER_TASK = "SLURM_CPUS_PER_TASK"
    SUFFIX_BAM = ".aln.sorted.bam"
    SUFFIX_GTF = ".gtf"
    SUFFIX_BED = ".bed"

    CMD_RSCRIPT_QUANT = f"module load R && Rscript \
    {{script_path}} \
	{{quant_fofn}} \
	{{merged_bed}}_merge.txt \
	{{out_quant_mat}}"

    # cupcake_path=/home/scormack/SQANTI3/cDNA_Cupcake && \
    # export PYTHONPATH=$PYTHONPATH:$cupcake_path/ && \
    # export PYTHONPATH=$PYTHONPATH:$cupcake_path/sequence/ && \
    # export PYTHONPATH=$PYTHONPATH:$cupcake_path/ && \
    # export PYTHONPATH=$PYTHONPATH:$cupcake_path/sequence/ && \

    CUPCAKE_PATH = "/home/scormack/SQANTI3/cDNA_Cupcake"

    CMD_SQANTI3 = f"export PYTHONPATH=$PYTHONPATH:{CUPCAKE_PATH} && \
    export PYTHONPATH=$PYTHONPATH:{CUPCAKE_PATH}/sequence && \
    source activate SQANTI3.env && \
    python /home/scormack/SQANTI3/sqanti3_qc.py \
    {{gtf_file}} \
    {{annotation}} \
    {{genome}} \
    -o {{filename}}\
    -d {{sqanti_output}}/{{filename}}\
    -t32"

class MetadataColumns:
    ID = "#ID"
    CONDITION = "Condition"
    POOL = "Pool"
    RUN_START = "RUN_start"
    RUN_END = "RUN_end"
    BARCODE = "Barcode"
    CONCAT_READS_DIR = "ConcatReadsDir"
