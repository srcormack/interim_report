#!/bin/bash

# Input
WD="/home/scormack/data/output/isoform_detection/flair" # Working directory
genome="/storage/gge/genomes/mouse_ref_NIH/reference_genome/mm39_SIRV.fa" # Reference genome
annotation="/storage/gge/genomes/mouse_ref_NIH/reference_genome/mm39.ncbiRefSeq_SIRV.gtf" # Reference annotation
samples_metadata="/home/scormack/data/metadata/mouse_samples_metadata.tsv" # TSV file with sample,run,primers...
out_iso_detect="/home/scormack/data/output/isoform_detection/flair"
out_quant="/home/scormack/data/output/quantification/flair"

# Create array to store condition factors
declare -a unique_conds

# Read the metadata file line by line
while IFS= read -r line; do
	if [[ "$line" == \#* ]]; then
		continue  # Skip lines that start with #
	fi

	# Split like into variables
	read -r sample_id cond pool run_start run_end barcode concat_reads_dir <<< "$line"

	# Add cond to array
	if [[ ! " ${unique_conds[*]} " =~ " ${cond} " ]]; then
		unique_conds+=("$cond")
	fi
	
done < "$samples_metadata"

# Run for each condition
for cond in "${unique_conds[@]}"; do
	echo "[SRC] Running $cond"
	sbatch run_flair_ConcatReads_quant.sbatch $WD $genome $annotation $samples_metadata $out_iso_detect $out_quant $cond
done

echo "[SRC] End"
