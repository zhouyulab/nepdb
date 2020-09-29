## Codes for NEPdb database

### Curation of Validated Neopeptide Dataset (VND)

- Verify the sequence and site information using match_sequencing.py

  Note: Use the tran_sort4.py script if the transcript names in the collected data are come from different databases.  

- Add short sequence of wild_peptide and the length of antigen peptide when not provided with default NA for other information that could not be inferred using antiglen_wtpep_NA.py

- Unify data format with unifydata.R

- Check sequences, antigens, and location information using Check_align.py

### Predicted Neopeptide Dataset (PND) 

- We downloaded COSMIC mutation information for genes that are important in cancer, which were then screened and sorted. These data came from 8,767 samples and 69 primary histology (cosmic_info_extract.py). We obtained 14,191 non-synonymous mutation sites from 683 genes and these sites appeared at least 3 times in all tumor samples, resulting in 516,036 short peptides. The short peptide lengths were 8, 9, 10, and 11 (cos_snp_pep_extract.py). 

- The programs for running netMHCpan4.0 and HLAthena are in their respective folders.

- Extract the protein sequence from Homo_sapiens.GRCh38.pep.all.fa files based on the transcript ID (cos_pro_fasta.py). The references of Ensembl was downloaded from: ftp://ftp.ensembl.org/pub/release-93/fasta/homo_sapiens/pep/Homo_sapiens.GRCh38.pep.all.fa.gz


