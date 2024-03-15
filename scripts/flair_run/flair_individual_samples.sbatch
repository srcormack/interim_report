#!/bin/bash
#SBATCH --job-name=flair_ind_mix
#SBATCH --qos medium
#SBATCH --nodes=1
#SBATCH --cpus-per-task=8
#SBATCH --mail-type=ALL # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mem=30gb # Per processor memory
#SBATCH -t 2-00:00:00     # Walltime
#SBATCH -o /home/scormack/src/benchmark/logs/log_flair/flair_ind_mix-%j.out
#SBATCH -e /home/scormack/src/benchmark/logs/log_flair/flair_ind_mix-%j.out

# echo "Starting Flair python script..."
source activate flair

samples_metadata="$1"
line_number_metadata=$((SLURM_ARRAY_TASK_ID + 1)) # Add 1 because of header

# Get sample metadata
read -r sample_id cond pool run_start run_end barcode concat_reads_dir <<< "$(head -n $line_number_metadata $samples_metadata | tail -n 1)"

#reads the line number given by the variable $line_number_metadata.

cd "/home/scormack/src/benchmark"

srun python execute_flair.py $sample_id $cond $concat_reads_dir $pool

echo "Finished Flair for $sample_id, $cond"
