#!/bin/bash
#SBATCH --job-name=mando_TAMAIsoforms_B0K100
#SBATCH --qos short
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mail-type=ALL # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mem=20gb # Per processor memory
#SBATCH -t 1-00:00:00     # Walltime
#SBATCH -o /home/scormack/src/benchmark/logs/log_tama/mando_TAMAIsoforms.out


srun python /home/scormack/src/benchmark/execute_tama.py