from datetime import datetime
import os
from pathlib import Path
import sys
import pandas as pd
import glob
import subprocess

sys.path.append("/home/scormack/src/benchmark")
#from .mando_constants import MandoConstants
from tama_run.tama_constants import TamaConstants
from constants import R_quant
from constants.nih_paths import NIHPaths
from constants.constants import GlobalConstants, MetadataColumns
 
def run_gff_to_bed12(gtf_file, mouse_merge_dir):
    gtf_file_str = str(gtf_file)
    gtf_name = os.path.basename(gtf_file_str)
    
    unique_bed_name = f"{gtf_name}{TamaConstants.SUFFIX_TAMA_BED}"
    tama_bed = mouse_merge_dir / unique_bed_name

    gff_to_bed_run = subprocess.run(
        TamaConstants.CMD_GFF_TO_BED12.format(
            src=gtf_file,
            dest=tama_bed,
        ),
        capture_output=True,
        shell=True,
    )
    print(
        f"{datetime.now()} concat reads tama gff to bed run: {gff_to_bed_run}",
        flush=True,
    )
    
def create_bed_fofn(mouse_merge_dir, mouse_merge_fofn):    
    create_bed_fofn = subprocess.run(   
        TamaConstants.CMD_CREATE_BED_FOFN.format(
            merged_bed=mouse_merge_dir,
            bed_fofn=mouse_merge_fofn,
        ),
        capture_output=True,
        shell=True,
        cwd=mouse_merge_dir,   
    )
    print(
        f"{datetime.now()} created bed_fofn: {create_bed_fofn}",
        flush=True,
    )

def bed_fofn_concatenation(mouse_merge_fofn):
    ######### ONLY FOR INDIVIDUAL (Call & join) FOFN FILES, AS ONLY ONE FOFN CONCAT FILE IS MADE FOR ALL CONDITIONS #######################

    #directory where previously made bed fofn files are stored
    mando_tama =  NIHPaths.mando_tama
    bed_fofn_pattern = f"{mando_tama}/*{TamaConstants.SUFFIX_BED_FOFN}"
    fofn_files = []

    for file_path in glob.glob(bed_fofn_pattern):
        fofn_files.append(file_path)

    with open(mouse_merge_fofn, 'w') as output_file:
        for fofn_file in fofn_files:
            with open(fofn_file, 'r') as input_file:
                output_file.write(input_file.read())

def run_tama_merge(mouse_merge_dir, mouse_merge_fofn):
    log_file_path = f"{mouse_merge_dir}/tama_merge_log.txt"
    
    ###DEFAULT TAMA MERGE
    with open(log_file_path, 'w') as log_file:
        tama_merge_run = subprocess.run(
                TamaConstants.CMD_TAMA_MERGE.format(
                    bed_fofn=mouse_merge_fofn,
                    merged_bed=mouse_merge_dir,
                ),
                shell=True,
                cwd=mouse_merge_dir,
                stdout=log_file,
                stderr=subprocess.STDOUT,
        )

    ###TAMA MERGE DUPLICATE TRANSCRIPT GROUPS
    with open(log_file_path, 'r') as log_file:
        log_content = log_file.read()
    
    if "By default TAMA merge does not allow merging of duplicate transcript groups." in log_content:
        with open(log_file_path, 'a') as log_file:
            print(f"{datetime.now()} TAMA merge error: duplicate transcript groups present, changing to TAMA_Merge_Dup...")
            tama_merge_dup_run = subprocess.run(
                    TamaConstants.CMD_TAMA_MERGE_DUP.format(
                        bed_fofn=mouse_merge_fofn,
                        merged_bed=mouse_merge_dir,
                    ),
                    shell=True,
                    cwd=mouse_merge_dir,
                    stdout=log_file,  # Redirect standard output to the log file
                    stderr=subprocess.STDOUT,
            )
    else:
        print(
        f"{datetime.now()} TAMA merge run: {tama_merge_run}",
        flush=True,
    )

    ###BED TO GTF 
    tama_bed_to_gtf_run = subprocess.run(
            TamaConstants.CMD_CONVERT_BED_GTF.format(
                src=mouse_merge_dir / (str(mouse_merge_dir) + GlobalConstants.SUFFIX_BED),
                dest=mouse_merge_dir / (str(mouse_merge_dir) + GlobalConstants.SUFFIX_GTF),
            ),
            capture_output=True,
            shell=True,
        )
    print(
    f"{datetime.now()} tama bed to gtf run: {tama_bed_to_gtf_run}",
    flush=True,
    ) 

def create_quant_fofn(mouse_merge_dir, mouse_merge_counts, script_path, quant_wd):
    quant_fofn_file = mouse_merge_dir /  (str(mouse_merge_dir) + "_quant.fofn")
    #{MandoConstants.SUFFIX_QUANT}
    quant_pattern = f"{quant_wd}/*/*.quant" 
    quant_fofn_list = []

    for file_path in glob.glob(quant_pattern):
        quant_fofn_list.append(file_path)
    print("quant files per condition: \n", quant_fofn_list)


def run_ind(script_path):
    samples_metadata = NIHPaths.mouse_metadata_file
    metadata_df = pd.read_table(samples_metadata, sep=" ")  
    conditions = metadata_df[MetadataColumns.CONDITION].unique().tolist()

    mouse_ind_dir = NIHPaths.out_test / "merge_ind" 
    mouse_ind_fofn = mouse_ind_dir / "mouse_ind.fofn"
    mouse_ind_counts = mouse_ind_dir / "mouse_ind_counts.tsv"

    if not os.path.exists(mouse_ind_dir):
        os.makedirs(mouse_ind_dir, exist_ok=True) 
        print('created directory: \n', mouse_ind_dir)

    files = [mouse_ind_fofn, mouse_ind_counts]

    for file in files:
        if not file.exists():
            file.touch()

    #individual functions 
    bed_fofn_concatenation(mouse_ind_fofn)
    run_tama_merge(mouse_ind_dir, mouse_ind_fofn)
    for cond in conditions:
        wd_ind = NIHPaths.out_quant_mando / cond
        quant_fofn_file = create_quant_fofn(mouse_ind_dir, mouse_ind_counts, script_path, wd_ind) 
        
    with open(quant_fofn_file, 'r') as f:
        lines = f.readlines()
        lines.sort()
    return mouse_ind_dir, mouse_ind_counts, quant_fofn_file

def run_concat(script_path: str):  
    wd_concat = NIHPaths.out_quant_mando / "Pooled"
    mouse_concat_dir = NIHPaths.out_test / "merge_concat" 
    #mouse_concat_dir = NIHPaths.mando_merge / "merge_concat"  #to be used once debugging is complete
    mouse_concat_fofn = mouse_concat_dir / "mouse_concat.fofn"
    mouse_concat_counts = mouse_concat_dir / "mouse_concat_counts.tsv"

    files = [mouse_concat_fofn, mouse_concat_counts]

    if not os.path.exists(mouse_concat_dir):
        os.makedirs(mouse_concat_dir, exist_ok=True) 
        print('created directory: \n', mouse_concat_dir)

    for file in files:
        if not file.exists():
            file.touch()

    gtf_pattern = f"{wd_concat}/*/*{GlobalConstants.SUFFIX_GTF}"
    gtf_list = []

    for file_path in glob.glob(gtf_pattern):
            gtf_list.append(file_path)
    
    #Concat functions
    for gtf_file in gtf_list:
       run_gff_to_bed12(gtf_file, mouse_concat_dir)
    
    create_bed_fofn(mouse_concat_dir, mouse_concat_fofn)
    run_tama_merge(mouse_concat_dir, mouse_concat_fofn)
    quant_fofn_file = create_quant_fofn(mouse_concat_dir, mouse_concat_counts, script_path, wd_concat) 
    
    return mouse_concat_dir, mouse_concat_counts, quant_fofn_file

def main(script_path: str):
    #Individual
    mouse_ind_dir, mouse_ind_counts, quant_fofn_file = run_ind(script_path)
    R_quant.quant_run(mouse_ind_dir, mouse_ind_counts, script_path, quant_fofn_file)
    
    #Concat
    #mouse_concat_dir, mouse_concat_counts, quant_fofn_file = run_concat(script_path)
    #R_quant.quant_run(mouse_concat_dir, mouse_concat_counts, script_path, quant_fofn_file)
