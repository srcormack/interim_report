class TamaConstants:
    PYTHON_EXECUTABLE = "python"

    SUFFIX_BED_FOFN = ".bed.fofn"
    SUFFIX_TAMA_BED = ".tama.bed"
    SUFFIX_GENEPRED = ".genePred"
    TAMA_ISOFORMS = "_TAMAIsoforms"
    GFF_CONVERTED = "_Converted"

    TAMA_PATH = "/home/scormack/tama"
    FORMAT_CONVERTER_PATH = "tama_go/format_converter"
    TAMA_RUN_PATH = "/home/scormack/src/benchmark/tama_run"

    CMD_GFF_TO_BED12 = f"python2 {TAMA_PATH}/{FORMAT_CONVERTER_PATH}/tama_format_gff_to_bed12_cupcake.py {{src}} {{dest}}"
    CMD_CREATE_BED_FOFN = f"ls {{merged_bed}}/*{SUFFIX_TAMA_BED} | awk -F/ '{{{{split($NF, a, \".\"); gsub(\".gtf\", \"\", a[1]); print $0 \"\\tno_cap\\t1,1,1\\t\" a[1]}}}}' > {{bed_fofn}}"

    #####DEFAULT PARAMETERS########
    CMD_TAMA_MERGE = f"source activate TAMAENV && \
    python {TAMA_PATH}/tama_merge.py \
        -f {{bed_fofn}} \
        -p {{merged_bed}} \
        -a 50 \
        -z 50 \
        -m 0" 

    CMD_TAMA_MERGE_DUP = f"source activate TAMAENV && \
    python {TAMA_PATH}/tama_merge.py \
        -f {{bed_fofn}} \
        -p {{merged_bed}} \
        -a 50 \
        -z 50 \
        -d merge_dup\
        -m 0" #-d flag merges duplicate transcript groups - current issue with concat Mando samples 


    CMD_CONVERT_BED_GTF = f"python2 {TAMA_PATH}/{FORMAT_CONVERTER_PATH}/tama_convert_bed_gtf_ensembl_no_cds.py {{src}} {{dest}}"
    #Original CMD_CREATE_BED_FOFN = f'ls {{merged_bed}}/*{SUFFIX_TAMA_BED} | awk -F/ \'{{split($NF, a, "."); gsub(".gtf", "", a[1]); print $0 "\tno_cap\t1,1,1\t" a[1]}}\' > {{bed_fofn}}'
 