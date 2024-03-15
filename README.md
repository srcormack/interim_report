## Overview   

Directories included within this branch:

- Mandalorion/ 

- Flair/

Both directories contain plots acquired from NIH_report.Rmd, which is found in */home/scormack/NIH/NIH_report*. Final html reports will be added as soon as they are completed.

Condition IDs:

```
- B100K0: Brain
- B0K100: Kidney
- BK8020: 80% Brain, 20% Kidney
- BK2080: 20% Brain, 80% Kidney
```

- scripts/

Contains all essential scripts involved in isoform identification and quantification strategies for Mandalorion and Flair.

## Garnatxa File Trees

- File trees which depict directory structure in Garnatxa, starting from */home/scormack/*.

#### Scripts
```
src/
┣ benchmark/
┃ ┣ constants/
┃ ┃ ┣ R_quant.py
┃ ┃ ┣ constants.py
┃ ┃ ┗ nih_paths.py
┃ ┃
┃ ┣ flair_run/
┃ ┃ ┣ concat_reads/
┃ ┃ ┃ ┣ BK8020.test.fa
┃ ┃ ┃ ┣ BK8020.test.gtf
┃ ┃ ┃ ┣ array_flair_ConcatReads_quant.sh
┃ ┃ ┃ ┣ run_flair_ConcatReads_quant.sbatch
┃ ┃ ┃ ┗ test.sh
┃ ┃ ┣ merge_expression/
┃ ┃ ┃ ┣ merge_flair_quatification_files_after_tama_merge.R
┃ ┃ ┃ ┣ run_flair_merge_expression_files.sbatch
┃ ┃ ┣ flair_array.sh
┃ ┃ ┣ flair_constants.py
┃ ┃ ┣ flair_individual_samples.sbatch
┃ ┃ ┣ flair_quantify.py
┃ ┃ ┗ run_flair.py
┃ ┃
┃ ┣ logs/
┃ ┃ ┣ log_flair/
┃ ┃ ┣ log_mando/
┃ ┃ ┣ log_sqanti/
┃ ┃ ┗ log_tama/
┃ ┃
┃ ┣ mando_run/
┃ ┃ ┣ RECOVER_MANDO.sbatch
┃ ┃ ┣ apboa.messages
┃ ┃ ┣ mando_array.sh
┃ ┃ ┣ mando_constants.py
┃ ┃ ┣ mando_individual_samples.sbatch
┃ ┃ ┣ mando_merge_expression.R
┃ ┃ ┣ mando_merge_expression.py
┃ ┃ ┗ run_mando.py
┃ ┃
┃ ┣ sqanti_run/
┃ ┃ ┣ flair_sqanti3_qc.sbatch
┃ ┃ ┣ just_sqanti.sbatch
┃ ┃ ┗ mando_sqanti3_qc.sbatch
┃ ┃
┃ ┣ tama_run/
┃ ┃ ┣ jorge_script/
┃ ┃ ┣ run_tama.py
┃ ┃ ┣ tama_constants.py
┃ ┃ ┗ tama_run.sbatch
┃ ┃
┃ ┣ execute_flair.py
┃ ┣ execute_mando.py
┃ ┣ execute_merge.py
┃ ┣ execute_tama.py
┃ ┣ merge_expression.sbatch
┃ ┗ merge_sqanti.py
┗ 
```

#### Data

```
data/
┣ metadata/
┃ ┣ mando_recover.tsv
┃ ┣ mouse_individual_metadata.tsv
┃ ┣ mouse_mixed_metadata.tsv
┃ ┣ mouse_pooled_metadata.tsv
┃ ┗ mouse_samples_metadata.tsv
┃
┣ output/
┃ ┣ isoform_detection/
┃ ┃ ┣ flair/
┃ ┃ ┃ ┣ flair_align_correct/
┃ ┃ ┃ ┣ flair_collapse/
┃ ┃ ┃ ┣ concat_chrom.sh
┃ ┃ ┃ ┣ flair_concat_reads.sbatch
┃ ┃ ┃ ┣ flair_transcriptomes.fofn
┃ ┃ ┗ sqanti_output/
┃ ┃   ┣ flair/
┃ ┃   ┗ mando/
┃ ┣ quantification/
┃ ┃ ┣ flair/
┃ ┃ ┃ ┣ B0K100/
┃ ┃ ┃ ┣ B100K0/
┃ ┃ ┃ ┣ BK2080/
┃ ┃ ┃ ┣ BK8020/
┃ ┃ ┃ ┣ ConcatReads/
┃ ┃ ┃ ┣ mouse_flair_ConcatReads_quant.fofn
┃ ┃ ┃ ┣ mouse_flair_ConcatReads_tama.counts.tsv
┃ ┃ ┃ ┣ mouse_flair_ind.counts_OLD.tsv
┃ ┃ ┃ ┣ mouse_flair_ind.counts_new.tsv
┃ ┃ ┃ ┗ mouse_flair_quant.fofn
┃ ┃ ┗ mando/
┃ ┃   ┣ B0K100/
┃ ┃   ┣ B100K0/
┃ ┃   ┣ BK2080/
┃ ┃   ┣ BK8020/
┃ ┃   ┣ Pooled/
┃ ┃   ┣ TAMAIsoforms/
┃ ┃   ┣ Test/
┃ ┃   ┣ mando_transcriptomes
┃ ┃   ┗ mando_transcriptomes.fofn
┃ ┃
┗ pooled_reads/
  ┣ B0K100_pooled.concat.fastq
  ┣ B100K0_pooled.concat.fastq
  ┣ BK2080_pooled.concat.fastq
  ┗ BK8020_pooled.concat.fastq
```
