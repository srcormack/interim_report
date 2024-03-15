#!/bin/bash

# Input
samples_metadata="/home/scormack/data/metadata/mando_recover.tsv" # TSV file with sample,run,primers...
WD="/home/scormack/src/benchmark/mando_run/"

nSamples=$(wc -l < $samples_metadata) # Calculate number of samples (wc-l counts the number of lines in the file)
nSamples=$((nSamples - 1)) # Remove count of header line 
echo "n samples" $nSamples

#TEST
# if [ $nSamples -ge 1 ]
# then
# bash "$WD"mando_individual_samples.sbatch $samples_metadata
# fi

if [ $nSamples -ge 1 ]
then
sbatch --array=1-$nSamples "$WD"mando_individual_samples.sbatch $samples_metadata
fi