# Packages
options(repos = c(CRAN = "https://ftp.cixug.es/CRAN/"))
install.packages("tidyverse", dependencies=TRUE)
install.packages("stringr", dependencies=TRUE)
library(tidyverse)
library(stringr)

#Input
args <- commandArgs(trailingOnly = TRUE)
quantification_fofn <- args[1]
old_2_new_id_tama <- args[2]
out_file <- args[3]

################################################################################
#TEST

# quant_dir <- "/home/scormack/data/output/quantification/flair"
# WD <- "/home/scormack/data/output/isoform_detection/flair/flair_collapse/"
# quantification_fofn <- file.path(quant_dir, "mouse_flair_quant.fofn")
# out_file <- file.path(quant_dir, "mouse_flair_ind.counts_new.tsv")
# old_2_new_id_tama <- file.path(WD, "mouse_flair_ind_merge.txt")

################################################################################

quantification_fofn <- readLines(quantification_fofn)
old_2_new_id_tama <- read.table(old_2_new_id_tama, header = F, sep = "\t")

# Format TAMA merge dataframe
old_2_new_id_tama <- as.data.frame(
  stringr::str_split_fixed(old_2_new_id_tama[, 4], pattern = ";|_", 3)
)
colnames(old_2_new_id_tama) <- c("new_id", "sample_id", "old_id")

# Quant file Change old transcript id to merged transcript id 
quant_mat_list <- list()
for (i in 1:length(quantification_fofn)) {
  print(paste("Processing file:", quantification_fofn[i]))
  
  quant_file <- read.table(quantification_fofn[i], header = TRUE, sep = "\t")

  quant_file[,c("trans_id", "gene_id")] <- stringr::str_split_fixed(quant_file$ids, pattern = "_\\s*(?=[^_]+$)|_(?=chr)", 2)
  
  cat("Post-processed quant file:\n")
  print(head(quant_file, 10))
  
  #Extracts the sample_id from the header of the 2nd column - it uses _ to index this and takes the second index as the sample ID 
  if (ncol(quant_file) > 4){
    sample_id <- strsplit(colnames(quant_file)[2], "_")[[1]][2]
  } else {
    sample_id <- strsplit(colnames(quant_file)[2], "_")[[1]][1]
  }
  
  tama_name_by_sample <- old_2_new_id_tama[old_2_new_id_tama$sample_id == sample_id,]
  
  match_ids <- match(quant_file$trans_id, tama_name_by_sample$old_id)

  cat("Match IDs:")
  print(head(match_ids, 20))
  cat("tama name by sample :")
  print(head(tama_name_by_sample$old_id[match_ids], 20))
  cat("isoform name in quant file:")
  print(head(quant_file$trans_id, 20)) 

  quant_file$transcript_id <- tama_name_by_sample$new_id[match_ids]
  cat("quant file with transcript ID:\n")
  print(head(quant_file, 10))

  quant_file <- subset(quant_file, select = -c(ids, trans_id, gene_id))
  cat("subsetted quant file: \n")
  print(head(quant_file, 10))
  write.table(quant_file, file = "/home/scormack/quant_file_jorge.txt", sep = "\t", col.names = TRUE, row.names = FALSE, quote = FALSE)

  quant_file <- quant_file %>%
    pivot_longer(-transcript_id, names_to = "sample", values_to = "count") %>%
    group_by(transcript_id, sample) %>%
    summarise(tot_count = sum(count)) %>%
    pivot_wider(names_from = "sample", values_from = "tot_count")
  
  quant_mat_list[[i]] <- as.data.frame(quant_file)
  
}

#print(quant_mat_list)

# Merge quantification matrices
quant_merged_matrix <- quant_mat_list %>%
  reduce(full_join, by = "transcript_id") %>%
  replace(is.na(.), 0) %>% 
  relocate(transcript_id)

# Write output
write.table(quant_merged_matrix, file = out_file,
            sep = "\t", col.names = T, row.names = F, quote = F)










