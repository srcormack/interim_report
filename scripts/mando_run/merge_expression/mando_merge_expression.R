# Packages
# options(repos = c(CRAN = "https://ftp.cixug.es/CRAN/"))
# install.packages("tidyverse", dependencies=TRUE)
# install.packages("stringr", dependencies=TRUE)

library(tidyverse)
library(stringr)

# Input
# args <- commandArgs(trailingOnly = TRUE)
# quantification_fofn <- args[1]
# old_2_new_id_tama <- args[2]
# out_file <- args[3]

quantification_fofn <- "/home/scormack/data/output/test/merge_ind_quant.fofn"
old_2_new_id_tama <- "/home/scormack/data/output/test/merge_concat_merge.txt"
out_file <- "/home/scormack/data/output/test/mouse_concat_counts.tsv"

# ##### Log file
# output_directory <- "/home/scormack/data/output/test/"
# log_name <- basename(out_file)
# log_file <- sprintf("%s%s.log", output_directory, log_name)
# #####


quantification_fofn <- readLines(quantification_fofn)
old_2_new_id_tama <- read.table(old_2_new_id_tama, header = F, sep = "\t")

old_2_new_id_tama <- old_2_new_id_tama[, 4] #selects 4th column from bed file

pattern <- "([A-Za-z0-9.]+);([A-Za-z0-9_]+)" #regex pattern to highlight G1.2;+ the rest of the 4th column
result <- stringr::str_match(old_2_new_id_tama, pattern)
print(result)
sample_and_old <- result[, 3] #extracts the 3rd field from the result matrix, which is the rest of the column that needs to be separated
sample_id <- sub("_Isoforms.*", "", sample_and_old) #everything before _Isoforms is selected, and _Isoforms is replaced with  ""
old_id <- sub(".*Isoforms_", "", sample_and_old) #Everything after Isoforms_ is kept, and Isoforms_ is replaced with "" 

old_2_new_id_tama <- data.frame(
  new_id = result[, 2],  # G1.2
  sample_id = sample_id,   # BK8020
  old_id = old_id #Isoform3_264
)

write.table(old_2_new_id_tama, file = "/home/scormack/TAMA_TEST_file.txt", sep = " ", col.names = TRUE, row.names = FALSE, quote = FALSE)


# Quant file Change old transcript id to merged transcript id 
quant_mat_list <- list()

#sink(log_file, append = FALSE, split = FALSE)

for (i in 1:length(quantification_fofn)) {
  print(paste("################################### Processing file: ", quantification_fofn[i]))

  quant_file <- read.table(quantification_fofn[i], header = TRUE, fill = TRUE)  
  cat("initial quant file \n")
  print(head(quant_file))

  second_column <- names(quant_file[2]) #selects 2nd column of the header from the quant file 
  print(second_column)
  pattern <- "\\.([^\\.]+)\\.concat\\.fastq" #regex pattern that selects "'sample_id'.concat.fastq"
  result <- stringr::str_match(second_column, pattern) #creates matrix of two  columns - "'sample_id'.concat.fastq" "sample_id"
  sample_id <- result[, 2] #creates the second column as a vector

  print(sample_id)

  #naming columns of quant file  
  print(head(old_2_new_id_tama))
  
  match_ids <- match(quant_file$Isoform, old_2_new_id_tama$old_id)

  num_nas <- sum(is.na(match_ids))
  cat("number of NA matches: ", num_nas, "\n")

  #adds the new_ids (G1.1 etc) to a new transcript ID column, according to the matching of the old_ids in the tama bed file (which themselves are also the transcript IDs) with the Isoforms from the quant file
  quant_file$transcript_id <- old_2_new_id_tama$new_id[match_ids]
  cat("quant file with transcript ID:\n")
  print(head(quant_file, 10))

  quant_file <- subset(quant_file, select = -c(Isoform))
  cat("subsetted quant file: \n")
  print(head(quant_file, 10))
  write.table(quant_file, file = "/home/scormack/quant_file.txt", sep = "\t", col.names = TRUE, row.names = FALSE, quote = FALSE)

  quant_file <- quant_file %>%
    pivot_longer(-transcript_id, names_to = "sample", values_to = "count") %>%
    group_by(transcript_id, sample) %>%
    summarise(tot_count = sum(count)) %>%
    pivot_wider(names_from = "sample", values_from = "tot_count")

  quant_mat_list[[i]] <- as.data.frame(quant_file)
 print(paste('################################### Finished Processing: ', quantification_fofn[i]))
}

# Merge quantification matrices
quant_merged_matrix <- quant_mat_list %>%
  reduce(full_join, by = "transcript_id") %>%
  replace(is.na(.), 0) %>% 
  relocate(transcript_id)

# Write output
write.table(quant_merged_matrix, file = out_file,
            sep = "\t", col.names = T, row.names = F, quote = F)

