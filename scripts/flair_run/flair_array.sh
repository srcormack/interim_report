#!/bin/bash

# Input
samples_metadata="/home/scormack/data/metadata/mouse_samples_metadata.tsv" # TSV file with sample,run,primers...
WD="/home/scormack/src/benchmark/flair_run/"

nSamples=$(wc -l < $samples_metadata) # Calculate number of samples (wc-l counts the number of lines in the file)
nSamples=$((nSamples - 1)) # Remove count of header line 

if [ $nSamples -ge 1 ]
then
sbatch --array=1-$nSamples flair_individual_samples.sbatch $samples_metadata
fi
