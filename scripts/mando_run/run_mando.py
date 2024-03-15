import os
import subprocess
import pandas as pd
from pathlib import Path
import logging
import sys

sys.path.append("/home/scormack/src/benchmark")
from .mando_constants import MandoConstants
from constants.nih_paths import NIHPaths
from constants.constants import GlobalConstants, MetadataColumns

log_file_template = "run_mando_{}.log"

#Logging configuration
def log_config(sample_id):
    log_dir = "/home/scormack/src/benchmark/logs/log_mando"
    log_file = log_file_template.format(sample_id)
    log_path = os.path.join(log_dir, log_file)

    logging.basicConfig(
        level=logging.DEBUG,  # Adjust the log level as needed (INFO, DEBUG, etc.)
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        filename=log_path,  # Specify the log file path
        filemode="w",  # "w" for write, "a" for append
    )
    logger = logging.getLogger("run_mando_individual_samples")
    return logger

def run_mando_individual_samples(sample: dict[str, str | int]):
 # Assigning file paths for mando command inputs, using objects from NIHPaths class
    concat_reads_dir = Path(sample[MetadataColumns.CONCAT_READS_DIR])
    sample_id = sample[MetadataColumns.ID]
    condition = sample[MetadataColumns.CONDITION]

    logger = log_config(sample_id)

    try:
        out_quant_mando = NIHPaths.out_quant_mando
        wd = NIHPaths.mando_wd
        out_mando =  out_quant_mando / condition / sample_id
        genome = NIHPaths.mouse_genome_file
        annotation = NIHPaths.mouse_annot_file
        n_cores = int(os.getenv(GlobalConstants.CPUS_PER_TASK, default="32"))
    except Exception as e2:
        logger.error(f"[SRC] An error occured with mandalorion: {str(e2)}")
 
 # Assigning mando fastq file
    fastq_file = concat_reads_dir / (sample_id + MandoConstants.SUFFIX_CONCAT_FASTQ)
    logger.info(f"[SRC]: Current fastq file - {fastq_file}")

 # Making directories
    for dir in [out_quant_mando, out_mando]:
        if not os.path.exists(dir):
            os.makedirs(dir, exist_ok=True)
    logger.info(f"[{sample_id}] [SRC] Created directory: {dir}")
    logger.info(f"[{sample_id}] [SRC]: Starting Mandalorion...")
 
 # Mandalorion
    logger.info(f"[SRC] Mandalorion files: {comando}")

    try:
        Mando_run = subprocess.run(
            MandoConstants.CMD_MANDO.format(
                out_mando=out_mando,
                sample_id=sample_id,
                annotation=annotation,
                genome=genome,
                fastq_file=fastq_file,
                n_cores=n_cores,
            ),
            capture_output=True, 
            shell=True,
            cwd=wd,
        )
        # Check if the command was successful
        if Mando_run.returncode == 0:
            # The command was successful, and the output is in result.stdout
            logger.info(f"[SRC] Command output:\n, {Mando_run.stdout}")
        else:
            # The command failed, and you can check the error message in result.stderr
            logger.info(f"[SRC] Command failed with error:, {Mando_run.stderr}")
    except Exception as e3:
        logger.error(f"[SRC] An error occured with mandalorion: {str(e3)}")
        logger.info(f"[{sample_id}] [SRC]: Standard Output:\n{Mando_run.stdout.decode('utf-8')}")
        logger.info(f"[{sample_id}] [SRC]: Standard Error:\n{Mando_run.stderr.decode('utf-8')}")
    
    logger.info(f"[SRC]: Finished Mandalorion processing for sample: [{sample_id}]")
