#!/bin/bash
#SBATCH --job-name=transcriptome_sq3
#SBATCH --qos short
#SBATCH --nodes=1
#SBATCH --cpus-per-task=16
#SBATCH --mail-type=ALL # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mem=40gb # Per processor memory
#SBATCH -t 1-00:00:00     # Walltime
#SBATCH -o /home/scormack/src/benchmark/logs/log_sqanti/flair_transcriptome_sq3-%j.out
#SBATCH -e /home/scormack/src/benchmark/logs/log_sqanti/flair_transcriptome_sq3-%j.err

module load anaconda
source activate SQANTI3.env

sqanti_path=/home/scormack/SQANTI3
cupcake_path=/home/scormack/SQANTI3/cDNA_Cupcake

export PYTHONPATH=$PYTHONPATH:$cupcake_path/
export PYTHONPATH=$PYTHONPATH:$cupcake_path/sequence/

# Input
WD="/home/scormack/data/output/isoform_detection/flair" # Working directory
split_by_chrom=$WD/flair_collapse/*/split_by_chrom/*
SQANTI_out="/home/scormack/data/output/isoform_detection/flair/sqanti_output"
genome="/storage/gge/genomes/mouse_ref_NIH/reference_genome/mm39_SIRV.fa" # Reference genome
annotation="/storage/gge/genomes/mouse_ref_NIH/reference_genome/mm39.ncbiRefSeq_SIRV.gtf" # Reference annotation
n_cores="$SLURM_CPUS_PER_TASK"
flair_transcriptomes=$WD/flair_transcriptomes.fofn

cd $WD

#Find all gtf files and place them in fofn
find $WD -type f -name '*.gtf' ! -path "$WD/flair_collapse/*/split_by_chrom/*" # and gtf files fiund in sqanti output,  > $flair_transcriptomes


# iterate over all transcriptomes
while IFS= read -r line
do
	filename=$(basename $line .gtf)

	printf "\n\n\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX Starting $filename XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n\n\n"

    python $sqanti_path/sqanti3_qc.py \
	$line \
	$annotation \
	$genome \
	-o $filename \
	-d $SQANTI_out/sq3_${filename}\
	-t $n_cores

	printf "\n\n\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX Finished $filename XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n\n\n"
done < $flair_transcriptomes


#######################################################################################################################
#Running extra sqanti QC for mouse flair ind again as it didn't contain the mixed samples 
flair_transcriptomes_recover=$WD/flair_transcriptomes_recover.fofn

mouse_flair_ind.gtf

while IFS= read -r line
do
	filename=$(basename $line .gtf)

	printf "\n\n\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX Starting $filename XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n\n\n"

    python $sqanti_path/sqanti3_qc.py \
	$line \
	$annotation \
	$genome \
	-o $filename \
	-d $SQANTI_out/sq3_${filename}\
	-t $n_cores

	printf "\n\n\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX Finished $filename XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n\n\n"
done < $flair_transcriptomes_recover
