import sys
from mando_run import run_mando
from constants.constants import MetadataColumns

# Set the working directory to the parent directory of 'Mandalorion'

if __name__ == "__main__":
    sample = {
        MetadataColumns.ID: sys.argv[1],
        MetadataColumns.CONDITION: sys.argv[2],
        MetadataColumns.CONCAT_READS_DIR: sys.argv[3],
    }
    sample = {
        
    }
    run_mando.run_mando_individual_samples(sample)

    # Makes dictionary, so when any of these metadatacolumns
    # are called, they correspond to the sys argument
    # which will be from the associated fastq file