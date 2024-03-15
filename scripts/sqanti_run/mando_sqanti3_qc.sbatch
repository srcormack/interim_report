#!/bin/bash
#SBATCH --job-name=transcriptome_sq3
#SBATCH --qos short
#SBATCH --nodes=1
#SBATCH --cpus-per-task=32
#SBATCH --mail-type=ALL # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mem=20gb # Per processor memory
#SBATCH -t 1-00:00:00     # Walltime
#SBATCH -o /home/scormack/src/benchmark/logs/log_sqanti/transcriptome_sq3-%j.out
#SBATCH -e /home/scormack/src/benchmark/logs/log_sqanti/transcriptome_sq3-%j.err

source activate SQANTI3.env

sqanti_path=/home/scormack/SQANTI3
cupcake_path=/home/scormack/SQANTI3/cDNA_Cupcake

export PYTHONPATH=$PYTHONPATH:$cupcake_path/
export PYTHONPATH=$PYTHONPATH:$cupcake_path/sequence/

# Input
WD="/home/scormack/data/output/quantification/mando" # Working directory
genome="/storage/gge/genomes/mouse_ref_NIH/reference_genome/mm39_SIRV.fa" # Reference genome
annotation="/storage/gge/genomes/mouse_ref_NIH/reference_genome/mm39.ncbiRefSeq_SIRV.gtf" # Reference annotation
mando_transcriptomes=${WD}/mando_transcriptomes.fofn
sqanti_output="/home/scormack/data/output/isoform_detection/sqanti_output/mando"

cd $WD

#Find all gtf files and place them in fofn
find $WD -type f -name '*.gtf' -not -path '*/tmp/*' -exec realpath {} \; > $mando_transcriptomes

mando_transcriptomes=('/home/scormack/data/output/test/merge_ind.gtf' '/home/scormack/data/output/test/merge_concat.gtf')


#while IFS= read -r line

for line in ${mando_transcriptomes[@]}; do

	filename=$(basename $line .gtf)

	printf "\n\n\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX Starting $filename XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n\n\n"

    python $sqanti_path/sqanti3_qc.py \
	$line \
	$annotation \
	$genome \
	-o $filename \
	-d  ${sqanti_output}/sq3_${filename}\
	-t 32

	printf "\n\n\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX Finished $filename XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n\n\n"
done #< $mando_transcriptomes

#File collection
#srun python /home/scormack/src/benchmark/file_collect.py "mando" "/home/scormack/NIH_report_new/data"
