## Scripts Overview

- Constants/

Python classes used for storing global constants which include: directories, functions and suffixes specific to different transcriptome assemnly algorithms.

- flair_run/

Python and Bash scripts to run flair modules for individual and pooled (join and call) samples.

- mando_run/

Python scripts to run Mandalorion for individual and pooled (join and call) samples.

- sqanti_run/ 

Bash scripts to run SQANTI3 for individual and pooled samples from either Mandalorion or Flair.

- tama_run/

Python and Bash scripts to run TAMA Merge for individual samples from each condition (call and join).

- *Execute_*.py scripts

Top level code that calls an associated function when executed as the main script.

## Scripts File Tree

```
scripts/
┣ constants/
┃ ┣ R_quant.py
┃ ┣ __init__.py
┃ ┣ constants.py
┃ ┗ nih_paths.py
┣ flair_run/
┃ ┣ concat_reads/
┃ ┃ ┣ array_flair_ConcatReads_quant.sh
┃ ┃ ┗ run_flair_ConcatReads_quant.sbatch
┃ ┣ merge_expression/
┃ ┃ ┣ merge_flair_quatification_files_after_tama_merge.R
┃ ┃ ┗ run_flair_merge_expression_files.sbatch
┃ ┣ __init__.py
┃ ┣ flair_array.sh
┃ ┣ flair_constants.py
┃ ┣ flair_individual_samples.sbatch
┃ ┣ flair_quantify.py
┃ ┗ run_flair.py
┣ mando_run/
┃ ┣ merge_expression/
┃ ┃ ┣ mando_merge_expression.R
┃ ┃ ┗ mando_merge_expression.py
┃ ┣ __init__.py
┃ ┣ mando_array.sh
┃ ┣ mando_constants.py
┃ ┣ mando_individual_samples.sbatch
┃ ┗ run_mando.py
┣ sqanti_run/
┃ ┣ flair_sqanti3_qc.sbatch
┃ ┣ mando_sqanti3_qc.sbatch
┃ ┗ merge_sqanti.py
┣ tama_run/
┃ ┣ __init__.py
┃ ┣ run_tama.py
┃ ┣ tama_constants.py
┃ ┗ tama_run.sbatch
┣ README.md
┣ __init__.py
┣ execute_flair.py
┣ execute_mando.py
┣ execute_merge.py
┗ execute_tama.py
```

