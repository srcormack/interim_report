#!/bin/bash
#SBATCH --job-name=flair_merge_expression_matrices
#SBATCH --qos short
#SBATCH --nodes=1
#SBATCH --cpus-per-task=4
#SBATCH --mail-type=ALL # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mem=20gb # Per processor memory
#SBATCH -t 1-00:00:00     # Walltime
#SBATCH -o /home/scormack/src/benchmark/logs/log_flair/flair_merge_expression_matrices.out

module load anaconda
source activate TAMAENV

#########################
#IND samples

# Input
WD="/home/scormack/data/output/isoform_detection/flair/flair_collapse"

bed_fofn=$WD/mouse_flair_ind.isoforms.bed.fofn
merged_bed=$WD/mouse_flair_ind

quant_dir="/home/scormack/data/output/quantification"
quant_fofn=$quant_dir/flair/mouse_flair_quant.fofn
out_quant_mat="${quant_dir}/flair/mouse_flair_ind.counts.tsv"

n_cores="$SLU#RM_CPUS_PER_TASK"

# Change working directory
cd $WD

# GTF to BED12
#grep -v  "\.join" excludes Concat samples
#Only all individual samples from all conditions
ls $WD/B*/*.gtf | grep -v "\.join" | while IFS= read -r line; do
	tama_bed="${line%.gtf}.tama.bed"
	echo "$line $tama_bed"
	python /home/scormack/tama/tama_go/format_converter/tama_format_gff_to_bed12_cupcake.py \
		$line \
		$tama_bed
done

ls ${WD}/B*/*.tama.bed | awk -F/ '{split($NF, a, "."); gsub(".gtf", "", a[1]); print $0 "\tno_cap\t1,1,1\t" a[1]}' > $bed_fofn

# Run TAMA merge
echo "merged bed:" $merged_bed
/home/scormack/tama/tama_merge.py \
	-f $bed_fofn \
	-p $merged_bed \
	-a 50 \
	-z 50 \
	-m 0

# BED to GTF
python /home/scormack/tama/tama_go/format_converter/tama_convert_bed_gtf_ensembl_no_cds.py \
	$merged_bed.bed \
	$merged_bed.gtf > tama_ind.log

# Generate transcript expression matrix
ls /home/scormack/data/output/quantification/flair/B*/*.counts.tsv > $quant_fofn

#Replace SQANTI environment with module load R - as the R script may not receive the installed packages
#conda activate SQANTI-SIM.env
module load R

Rscript /home/scormack/src/benchmark/flair_run/merge_expression/merge_flair_quatification_files_after_tama_merge.R \
	$quant_fofn \
	"$merged_bed"_merge.txt \
	$out_quant_mat

# ############################################################################################################################################################
# ConcatReads

source activate TAMAENV

# Input
bed_fofn="/home/scormack/data/output/isoform_detection/flair/flair_collapse/ConcatReads/mouse_flair_ConcatReads.isoforms.bed.fofn"
merged_bed="/home/scormack/data/output/isoform_detection/flair/flair_collapse/ConcatReads/mouse_flair_ConcatReads_tama_new"

quant_fofn="/home/scormack/data/output/quantification/flair/ConcatReads/mouse_flair_ConcatReads_quant.fofn"
out_quant_mat="/home/scormack/data/output/quantification/flair/ConcatReads/mouse_flair_ConcatReads_tama.counts_new.tsv"
n_cores="$SLURM_CPUS_PER_TASK"

cd $WD

ls ${WD}/ConcatReads/*.gtf | while IFS= read -r line; do
        tama_bed="${line%.gtf}.tama.bed"
        echo "$line $tama_bed"
        python /home/scormack/tama/tama_go/format_converter/tama_format_gff_to_bed12_cupcake.py \
                $line \
                $tama_bed
done

ls ${WD}/ConcatReads/*.tama.bed | awk -F/ '{split($NF, a, "."); gsub(".gtf", "", a[1]); print $0 "\tno_cap\t1,1,1\t" a[1]}' > $bed_fofn

# Run TAMA merge
echo "merged bed Concat READS:" $merged_bed
/home/scormack/tama/tama_merge.py \
        -f $bed_fofn \
        -p $merged_bed \
        -a 50 \
        -z 50 \
        -m 0 > tama_ConcatReads.log

# BED to GTF
python /home/scormack/tama/tama_go/format_converter/tama_convert_bed_gtf_ensembl_no_cds.py \
        ${merged_bed}.bed \
        ${merged_bed}.gtf

# Generate transcript expression matrix
ls ${quant_dir}/flair/ConcatReads/*.counts.tsv | grep -v "/mouse_flair" > $quant_fofn

#conda activate SQANTI-SIM.env
module load R

Rscript /home/scormack/src/benchmark/flair_run/merge_expression/merge_flair_quatification_files_after_tama_merge.R \
        $quant_fofn \
        "$merged_bed"_merge.txt \
        $out_quant_mat

