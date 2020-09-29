#!/usr/bin/env Rscript

df <- read.table("../test/20180621data.csv", header=TRUE, sep=",")
nrow(df)
ncol(df)
df[df == 'N/A'] <- 'null'
df[df == 'null'] <- NA

table(df$response, useNA="always")

df$sampleid[df$sampleid == "From 2014 OI"] <- NA
df$sampleid[df$sampleid == "ID no.9"] <- "no.9"
df$sampleid <- gsub('^Patient ', 'patient', ignore.case=TRUE, df$sampleid)
df$sampleid <- gsub('^Patient', 'patient', df$sampleid)
df$sampleid <- gsub('^TIL ', 'TIL', df$sampleid)
table(df$sampleid, useNA="always")

df$tumor_type <- gsub('Cancer$', 'cancer', df$tumor_type)
table(df$tumor_type, useNA="always")

length(table(df$genesymbol))

table(df$fpkm)
table(df$mut_dna)
str(df$transcript_id)
str(df$mut_aa_pos)
length(unique(df$wt_peptide))

df$antigen_type <- gsub('minigenem RNA', 'minigene mRNA', df$antigen_type)
df$antigen_type <- gsub('peptides', 'peptide', df$antigen_type)
df$antigen_type <- gsub('RNA TMGs', 'TMG RNA', df$antigen_type)
df$antigen_type <- gsub('TMG RNAs', 'TMG RNA', df$antigen_type)
df$antigen_type <- gsub('TMGs', 'TMG RNA', df$antigen_type)
df$antigen_type <- gsub('Tetramer', 'tetramer', df$antigen_type)
table(df$antigen_type, useNA="always")

df$Tcell_source <- gsub('TIL$', 'TILs', df$Tcell_source)
df$Tcell_source <- gsub('PBMC$', 'PBMCs', df$Tcell_source)
table(df$Tcell_source, useNA="always")

df$APC_type <- gsub('Autologous', 'autologous', df$APC_type)
df$APC_type <- gsub('COS7 cell$', 'COS7', df$APC_type)
df$APC_type <- gsub('COS7 cells$', 'COS7', df$APC_type)
df$APC_type <- gsub('B cell$', 'B cells', df$APC_type)
df$APC_type[grepl('^T', df$APC_type)] <- 'T2'
table(df$APC_type, useNA="always")

df$assay <- gsub('CD137$', 'ELISPOT assay', df$assay)
df$assay <- gsub('^IFNg$', 'IFNg ELISPOT assay', df$assay)
df$assay[grepl('^IFNg ELISPOT assay and ', df$assay)] <- 'IFNg ELISPOT assay'
table(df$assay, useNA="always")

df$checkpoint_blockade <- gsub('Ipilimumab', 'ipilimumab', df$checkpoint_blockade)
df$checkpoint_blockade[df$checkpoint_blockade == 'N'] <- NA
table(df$checkpoint_blockade, useNA="always")

table(df$ACT, useNA="always")

table(df$vaccination, useNA="always")

df$curative_effect[df$curative_effect == 'NT'] <- NA
table(df$curative_effect, useNA="always")

table(df$PMID, useNA="always")
length(unique(df$PMID))
length(unique(df$ref_title))

df$journal <- gsub('\\.$', '', df$journal)
table(df$journal, useNA="always")
length(unique(df$journal))

table(df$HLA_A1, useNA="always")
table(df$HLA_A2, useNA="always")
table(df$HLA_B1, useNA="always")
table(df$HLA_B2, useNA="always")
table(df$HLA_C1, useNA="always")
table(df$HLA_C2, useNA="always")

sum(!is.na(df[, c("HLA_A1", "HLA_A2")]))
sum(!is.na(df[, c("HLA_B1", "HLA_B2")]))
sum(!is.na(df[, c("HLA_C1", "HLA_C2")]))
sum(!is.na(df[, c("HLA_A1", "HLA_A2", "HLA_B1", "HLA_B2", "HLA_C1", "HLA_C2")]))

write.table(df, "../test/20180626data.csv", col.names=TRUE, row.names=FALSE, sep=',', quote=FALSE)
