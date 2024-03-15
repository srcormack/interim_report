import os
from pathlib import Path
import pandas as pd
import sys
import glob
import subprocess
import re

sys.path.append("/home/scormack/src/benchmark")
from constants.nih_paths import NIHPaths
from constants.constants import MetadataColumns, GlobalConstants

#NIHPaths.out_detect = output / "isoform_detection"
#NIHPaths.out_quant = output / "quantification"

#base directories
assembler = sys.argv[1] # "mando" or "flair"
dest = Path("/home/scormack/NIH/NIH_report/data/")

#metadata
samples_metadata = NIHPaths.mouse_metadata_file
metadata_df = pd.read_table(samples_metadata, sep=" ")
sample_ids = metadata_df[MetadataColumns.ID].tolist()
conditions = metadata_df[MetadataColumns.CONDITION].tolist()

#reference data
ref_annotation = NIHPaths.mouse_annot_file
ref_genome = NIHPaths.mouse_genome_file

#directories
nih_data = dest / assembler  # where NIH report data is stored 
isoform_detection_dir = NIHPaths.out_detect / "sqanti_output" #isoform detection directory
sqanti_out_dir = isoform_detection_dir / assembler #sqanti output directory
quant_dir = NIHPaths.out_quant / assembler  #quant file output directory
merge_dir = quant_dir / (assembler + "_merge")

#suffixes
classification_suffix = "_classification.txt"
junction_suffix = "_junctions.txt"

#FILE COLLECT SCRIPT
#####################################

# ##### MERGED FILES
# #finding _counts.tsv files:
# counts_files = glob.glob(f'{merge_dir}/*/_counts.tsv')
# #finding .gtf merged files
# gtf_merged_files = glob.glob(f'{merge_dir}/*.gtf')
# #sqanti outputs:
# sqanti_out_merged_files = glob.glob(f'{sqanti_out_dir}/*merge_*/{classification_suffix}')
# #######


#Collects 'call and join' and 'join and call' junction and classification files, as well as each individual sample's.
#Creates fofns and places them in "NIH_report/data" directories depending on the transcriptome assembly algorithm

def file_collect(metadata_df, sqanti_out_dir, junction_suffix, classification_suffix, nih_data):
 #Collecting call and join and join and call files
 for condition in metadata_df[MetadataColumns.CONDITION].unique():
    all_junctions = []
    all_classifications = []

    junction_pattern = f'{sqanti_out_dir}/*{condition}*/*{junction_suffix}*'
    classification_pattern = f'{sqanti_out_dir}/*{condition}*/*{classification_suffix}*'

    junction_list = glob.glob(junction_pattern)
    classification_list = glob.glob(classification_pattern)

    all_junctions += junction_list
    all_classifications += classification_list

    #Collecting individual sample files for each condition
    for sample_id in metadata_df[MetadataColumns.ID].unique():
        sample_condition = metadata_df.loc[metadata_df[MetadataColumns.ID] == sample_id, MetadataColumns.CONDITION].values[0] #Matches sample ID to associated condition; if true, passes condition value to sample_condition   

        if condition == sample_condition:
            junction_pattern_ID = f'{sqanti_out_dir}/*{sample_id}*/*{junction_suffix}*'
            classification_pattern_ID = f'{sqanti_out_dir}/*{sample_id}*/*{classification_suffix}*'

            junction_list_ID = glob.glob(junction_pattern_ID)
            classification_list_ID = glob.glob(classification_pattern_ID)

            #APPENDS JUNCTIONS AND CLASSIFICATIONS TO LIST IF THEY DON'T ALREADY EXIST
            [all_junctions.append(junction) for junction in junction_list_ID if junction not in all_junctions]
            [all_classifications.append(classification) for classification in classification_list_ID if classification not in all_classifications]

    #Creating fofn for all junction and classification files for each condition 
    junction_fofn = nih_data / (str(condition) + junction_suffix + ".fofn_test")
    classification_fofn = nih_data / (str(condition) + classification_suffix + ".fofn_test")

    fofn_files = [junction_fofn, classification_fofn]
    lists = [all_junctions, all_classifications]

    for fofn, item in zip(fofn_files, lists):
        with open(fofn, 'w') as file:
            for line in item:
                file.write(f"{line}\n")

file_collect(metadata_df, sqanti_out_dir, junction_suffix, classification_suffix, nih_data)


############################################################
#### NEED TO FIND A WAY OF COPYING THE REST OF THE DOCUMENT PATH FILES TO THE NIH_DATA FOLDER

#class and junctions of individual merged files 
# quant_ind <- file.path(src_dir, "mouse_flair_ind.counts.tsv")
# quant_concat <- file.path(src_dir, "mouse_flair_ConcatReads_tama.counts.tsv")

# class and junctions of concat merged files
# class_ind <- file.path(src_dir, "mouse_flair_ind_classification.txt")
# class_concat <- file.path(src_dir, "mouse_flair_ConcatReads_classification.txt")

# ref_genome <- file.path(src_dir, "mm39_SIRV.fa")

# annot_ind_quantification <- file.path(src_dir, "mouse_flair_ind.gtf")
# annot_concat_quantification <- file.path(src_dir, "mouse_flair_ConcatReads_tama.gtf")

# class_ind_quantification <- file.path(src_dir, "mouse_flair_ind_classification.txt")
# class_concat_quantification <- file.path(src_dir, "mouse_flair_ConcatReads_tama_classification.txt")

