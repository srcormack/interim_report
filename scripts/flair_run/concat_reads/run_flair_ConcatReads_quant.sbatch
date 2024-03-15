#!/bin/bash
#SBATCH --job-name=flair_join_quant
#SBATCH --qos short
#SBATCH --nodes=1
#SBATCH --cpus-per-task=4
#SBATCH --mail-type=ALL # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mem=20gb # Per processor memory
#SBATCH -t 1-00:00:00     # Walltime
#SBATCH -o /home/scormack/src/benchmark/logs/log_flair/flair_join_quant_%A.out

source activate flair

WD="$1"
genome="$2"
annotation="$3"
samples_metadata="$4"
out_iso_detect="$5"
out_quant="$6"
cond="$7"
n_cores="$SLURM_CPUS_PER_TASK"

original_cond=$cond
isoform_dir="$out_iso_detect/flair_collapse/$cond"

gtf_suffix="*.gtf"
fasta_suffix="*.fa"
bed_suffix="*.bed"

isoforms_gtf_dir="$isoform_dir/split_by_chrom/$gtf_suffix"
isoforms_fa_dir="$isoform_dir/split_by_chrom/$fasta_suffix"
isoforms_bed_dir="$isoform_dir/split_by_chrom/$bed_suffix"

isoforms_gtf="$isoform_dir/$cond.join.isoforms.gtf"
isoforms_fa="$isoform_dir/$cond.join.isoforms.fa"
isoforms_bed="$isoform_dir/$cond.join.isoforms.bed"

cat $(ls $isoforms_gtf_dir) > $isoforms_gtf
cat $(ls $isoforms_fa_dir) > $isoforms_fa
cat $(ls $isoforms_bed_dir) > $isoforms_bed

echo "isoform gtf directory $isoforms_gtf"
echo "isoform fasta directory $isoforms_fa"
echo "isoform bed directory $isoforms_bed"
echo "[SRC] Original condition name:" $cond \

read_manifest="${out_quant}/${cond}.read_manifest.tsv"
echo $read_manifest
echo -n "" > $read_manifest

head $read_manifest

condition_mapping=("B0K100:B0K100" "B100K0:B100K0" "BK2080:B20K80" "BK8020:B80K20")

while IFS= read -r line; do
    if [[ "$line" == \#* ]]; then
        continue  # Skip lines that start with #
    fi

    # Split line into variables
    read -r sample_id curr_cond pool run_start run_end barcode concat_reads_dir <<< "$line"

    if [ "$cond" = "$curr_cond" ]; then
        for mapping in "${condition_mapping[@]}"; do
            IFS=':' read -ra mapping_parts <<< "$mapping"
            if [[ "${mapping_parts[0]}" == "$cond" ]]; then
                mapped_cond="${mapping_parts[1]}"
                break
            fi
        done
        fastq_directory="/storage/gge/nih/PacBio_IsoSeq/merged_reads/mouse_${mapped_cond}"
        fastq_file="${fastq_directory}/${sample_id}.concat.fastq"
        echo "NIH directory condition: $cond" \
        
        printf "%s\t%s\t%s\t%s\n" $sample_id $original_cond $pool $fastq_file >> $read_manifest
    fi

done < "$samples_metadata"

echo "fastq directory: $fastq_directory"
echo "fastq file $fastq_file"
echo "read_manifest file: $read_manifest"
cat $read_manifest
\

# Run FLAIR quantification
flair quantify \
	-i $isoforms_fa \
	--reads_manifest $read_manifest \
	--threads $n_cores \
	--output "${out_quant}/${cond}_ConcatReads" \
	--tpm \
	--check_splice \
	--isoform_bed $isoforms_bed

echo "[SRC] End"

echo "-----------------------------------"






