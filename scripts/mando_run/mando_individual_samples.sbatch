#!/bin/bash
#SBATCH --job-name=mando_recover
#SBATCH --qos medium
#SBATCH --nodes=1
#SBATCH --cpus-per-task=32
#SBATCH --mail-type=ALL # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mem=100gb # Per processor memory
#SBATCH -t 3-00:00:00     # Walltime
#SBATCH -o /home/scormack/src/benchmark/logs/log_mando/mando_recover-%j.out
#SBATCH -e /home/scormack/src/benchmark/logs/log_mando/mando_recover-%j.out

echo "Starting Mando python script..."

samples_metadata=$1 ### Choose Pooled or Individual metadata
line_number_metadata=$((SLURM_ARRAY_TASK_ID + 1))

read -r sample_id cond pool run_start run_end barcode concat_reads_dir <<< "$(head -n $line_number_metadata $samples_metadata | tail -n 1)"
#reads the line number given by the variable $line_number_metadata.

echo line number from metadata table $line_number_metadata 
cat $sample_id $cond $concat_reads_dir 

cd "/home/scormack/src/benchmark"

echo "Running Mandalorion for"  $sample_id $cond $concat_reads_dir

python execute_mando.py $sample_id $cond $concat_reads_dir

echo "Finished"
