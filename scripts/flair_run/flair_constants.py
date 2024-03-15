class FlairConstants:
    SUFFIX_CONCAT_FASTQ = ".concat.fastq"
    SUFFIX_BAM = ".aln.sorted.bam"
    SUFFIX_BED = ".aln.bed"
    SUFFIX_CORRECTED_BED = "_all_corrected.bed"
    SUFFIX_READ_MANIFEST = ".read_manifest.tsv"
    SUFFIX_ISOFORMS_FA = ".isoforms.fa"
    SUFFIX_ISOFORMS_BED = ".isoforms.bed"

    FLAIR_ALIGN_CORRECT = "flair_align_correct"
    FLAIR_COLLAPSE = "flair_collapse"

    CMD_BAM2BED12 = 'bam2Bed12 -i "{bam_file}" > "{bed_file}"'
    CMD_FLAIR_CORRECT = f'flair correct \
        -q "{{out_align}}/{{sample_id}}{SUFFIX_BED}" \
        -f "{{annotation}}" \
        -g "{{genome}}" \
        --output "{{out_align}}/{{sample_id}}" \
        --threads "{{n_cores}}"'
    CMD_FLAIR_COLLAPSE = f'flair collapse \
        -g "{{genome}}" \
        --gtf "{{annotation}}" \
        -q "{{out_align}}/{{sample_id}}{SUFFIX_CORRECTED_BED}" \
        -r "{{fastq_file}}" \
        --output "{{out_collapse}}/{{sample_id}}" \
        --check_splice \
        --threads "{{n_cores}}"'
    CMD_FLAIR_QUANTIFY = f'flair quantify \
        -i "{{out_collapse}}/{{sample_id}}"{SUFFIX_ISOFORMS_FA} \
        --reads_manifest "{{reads_manifest}}" \
        --threads "{{n_cores}}" \
        --output "{{out_quant}}/{{sample_id}}" \
        --tpm \
        --check_splice \
        --isoform_bed "{{out_collapse}}/{{sample_id}}{SUFFIX_ISOFORMS_BED}"'