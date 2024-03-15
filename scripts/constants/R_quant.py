from datetime import datetime
import os
from pathlib import Path
import sys
import glob
import subprocess

sys.path.append("/home/scormack/src/benchmark")
from constants.constants import GlobalConstants

def quant_run(mouse_merge_dir, mouse_merge_counts, script_path, quant_fofn_file):
    print("QUANT_RUN_INPUTS: \n", mouse_merge_dir, mouse_merge_counts, script_path, quant_fofn_file)
    
    quant_run = subprocess.run(
        GlobalConstants.CMD_RSCRIPT_QUANT.format(
            script_path=script_path,
            quant_fofn=quant_fofn_file,
            merged_bed=mouse_merge_dir,
            out_quant_mat=mouse_merge_counts,
        ),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        shell=True,
        cwd=mouse_merge_dir,
    )

