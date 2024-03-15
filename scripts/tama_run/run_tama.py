from datetime import datetime
from multiprocessing import Pool
import os
from pathlib import Path
import sys
import pandas as pd
import glob
import subprocess

sys.path.append("/home/scormack/src/benchmark")
from .tama_constants import TamaConstants
from constants.nih_paths import NIHPaths
from constants.constants import GlobalConstants, MetadataColumns

def run_gff_to_bed12(wd, gtf_file, merged_bed):
    gtf_file_str = str(gtf_file)
    gtf_name = os.path.basename(gtf_file_str)
    tama_bed = merged_bed / (gtf_name + TamaConstants.SUFFIX_TAMA_BED)

    gff_to_bed_run = subprocess.run(
        TamaConstants.CMD_GFF_TO_BED12.format(
            src=gtf_file,
            dest=tama_bed,
        ),
        capture_output=True,
        shell=True,
        cwd=wd,
    )
    print(
        f"{datetime.now()} tama gff to bed run: {gff_to_bed_run}",
        flush=True,
    )

def run_tama_merge(merged_bed, wd):
    #Creating bed fofn
    bed_fofn = merged_bed / (str(merged_bed) + TamaConstants.SUFFIX_BED_FOFN)
    create_bed_fofn = subprocess.run(   
        TamaConstants.CMD_CREATE_BED_FOFN.format(
            merged_bed=merged_bed,
            bed_fofn=bed_fofn,
        ),
        capture_output=True,
        shell=True,   
    )
    print(
        f"{datetime.now()} created bed_fofn {create_bed_fofn}",
        flush=True,
    )

    #Running tama merge
    tama_merge_run = subprocess.run(
        TamaConstants.CMD_TAMA_MERGE.format(
            bed_fofn=bed_fofn,
            merged_bed=merged_bed,
        ),
        capture_output=True,
        shell=True,
        cwd=merged_bed,
    )
    print(
        f"{datetime.now()} tama merge run: {tama_merge_run}",
        flush=True,
    )

def run_tama(condition: str):
    #Creating gtf file list, excluding  gtf files in the TAMAIsoforms directory
    glob_wd = NIHPaths.out_quant_mando / condition
    wd  = NIHPaths.mando_tama
    #wd = ("/home/scormack/data/output/quantification/mando/Test")
    print("wd", wd)

    glob_pattern = f"{glob_wd}/*/*{GlobalConstants.SUFFIX_GTF}"
    exclude_directory_name = TamaConstants.TAMA_ISOFORMS

    gtf_list = []
    for file_path in glob.glob(glob_pattern):
        directory_name = os.path.dirname(file_path)
        if exclude_directory_name not in directory_name:
            gtf_list.append(file_path)

    print(f"{datetime.now()} gtf files: {gtf_list}")

    merged_bed = wd / (condition + TamaConstants.TAMA_ISOFORMS)

    # for gtf_file in gtf_list:
    #     run_gff_to_bed12(wd, gtf_file, merged_bed)

    # #making the tama_isoforms directory

    # if not os.path.exists(merged_bed):
    #     os.makedirs(merged_bed, exist_ok=True)
    # print('created directory: \n', merged_bed )

    # #Running tama merge
    # run_tama_merge(merged_bed, wd)

    # tama_bed_to_gtf_run = subprocess.run(
    #     TamaConstants.CMD_CONVERT_BED_GTF.format(
    #         src=str(merged_bed) + GlobalConstants.SUFFIX_BED,
    #         dest=str(merged_bed) + GlobalConstants.SUFFIX_GTF,
    #     ),
    #     capture_output=True,
    #     shell=True,
    #     cwd=wd,
    # )
    # print(
    #     f"{datetime.now()} tama bed to gtf run: {tama_bed_to_gtf_run}",
    #     flush=True,
    # )

def main():
    ## runs a for loop for the run_tama function for each condition in the metadata 
    samples_metadata = NIHPaths.mouse_metadata_file
    print(samples_metadata)
    metadata_df = pd.read_table(samples_metadata, sep=" ")
    n_cores = int(os.getenv(GlobalConstants.CPUS_PER_TASK, default="10"))
    
    ## creates a tuple containing both condition and sample ID; used for accessing the gtf files in the mando directory
    ## .values is a necessary method as it converts the 
    conditions = metadata_df[MetadataColumns.CONDITION].unique().tolist()

    for cond in conditions:
        run_tama(cond)