import os
import subprocess
import pandas as pd
from multiprocessing import Pool
from pathlib import Path
import logging
import sys

sys.path.append("/home/scormack/src/benchmark")
from .flair_constants import FlairConstants
from constants.nih_paths import NIHPaths
from constants.constants import GlobalConstants, MetadataColumns

# Configuring logging directories 
log_dir = "/home/scormack/src/benchmark/logs/log_flair"
log_file = "run_flair_quantify.log"
log_path = os.path.join(log_dir, log_file)

logging.basicConfig(
    level=logging.DEBUG,  # Adjust the log level as needed (INFO, DEBUG, etc.)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=log_path,  # Specify the log file path
    filemode="w",  # "w" for write, "a" for append
)

# Create a logger instance for your script
logger = logging.getLogger("run_flair_individual_samples")

def run_flair_quantify(sample: dict):
    wd = NIHPaths.output
    genome = NIHPaths.mouse_genome_file
    annotation = NIHPaths.mouse_annot_file
    out_iso_detect = NIHPaths.out_detect_flair
    out_quant = NIHPaths.out_quant_flair
    n_cores = int(os.getenv(GlobalConstants.CPUS_PER_TASK, default="4"))

    concat_reads_dir = Path(sample[MetadataColumns.CONCAT_READS_DIR])
    sample_id = sample[MetadataColumns.ID]
    condition = sample[MetadataColumns.CONDITION]

    fastq_file = concat_reads_dir / (sample_id + FlairConstants.SUFFIX_CONCAT_FASTQ)
    bam_file = concat_reads_dir / (sample_id + FlairConstants.SUFFIX_BAM)
    out_align = out_iso_detect / FlairConstants.FLAIR_ALIGN_CORRECT / condition
    bed_file = out_align / (sample_id + FlairConstants.SUFFIX_BED)
    out_collapse = out_iso_detect / FlairConstants.FLAIR_COLLAPSE / condition
    out_quant_cond = out_quant / condition
    manifest_file = out_quant / (sample_id + FlairConstants.SUFFIX_READ_MANIFEST)

    sample_manifest = {
        k: v
        for k, v in sample.items()
        if k in [MetadataColumns.ID, MetadataColumns.CONDITION, MetadataColumns.POOL]
    }
    sample_manifest["fastq"] = fastq_file
    df_manifest = pd.DataFrame([sample_manifest])

    logger.info(f"[SRC] Inputting [{fastq_file}] for manifest file [{df_manifest}]")

    df_manifest.to_csv(manifest_file, sep="\t", header=False, index=False)

    logger.info(f"[{sample_id}] Created sample manifest: {manifest_file}")
    logger.info(f"[SRC] [{sample_id}] Starting flair quantify...")

    # flair quantify
    flair_quantify_run = subprocess.run(
        FlairConstants.CMD_FLAIR_QUANTIFY.format(
            out_collapse=out_collapse,
            sample_id=sample_id,
            reads_manifest=manifest_file,
            n_cores=n_cores,
            out_quant=out_quant,
        ),
        capture_output=True,
        shell=True,
        cwd=wd,
    )
    print("flair_quantify_run:", flair_quantify_run.stdout, "\n")
    print("out_collapse_dir:", out_collapse, "\n")
    print("Sample_ID:", sample_id, "\n")
    print("Manifest file:", manifest_file, "\n")
    print("N_cores:", n_cores, "\n")
    print("out quant_dir:",  out_quant, "\n")