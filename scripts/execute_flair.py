import sys
from flair_run import flair_quantify
from constants.constants import MetadataColumns

# Set the working directory to the parent directory of 'Mandalorion'

if __name__ == "__main__":
    sample = {
        MetadataColumns.ID: sys.argv[1],
        MetadataColumns.CONDITION: sys.argv[2],
        MetadataColumns.CONCAT_READS_DIR: sys.argv[3],
        MetadataColumns.POOL: sys.argv[4]
    }
    flair_quantify.run_flair_quantify(sample)

    # Makes dictionary, so when any of these metadatacolumns
    # are called, they correspond to the sys argument
    # which will be from the associated fastq file

# runs the function run_flair_pool from the file run_flair_individual_samples


#################################################################


# if __name__ == "__main__":
#     sample = {
#         MetadataColumns.ID: sys.argv[1],
#         MetadataColumns.CONDITION: sys.argv[2],
#         MetadataColumns.CONCAT_READS_DIR: sys.argv[3],
#         MetadataColumns.POOL: sys.argv[4]
#     }
#     run_flair_test.run_flair_quantify_test(sample)

#     # Makes dictionary, so when any of these metadatacolumns
#     # are called, they correspond to the sys argument
#     # which will be from the associated fastq file
# # runs the function run_flair_pool from the file run_flair_individual_samples
