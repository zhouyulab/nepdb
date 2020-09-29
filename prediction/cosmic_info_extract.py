"""Extract the information we need to build the database"""

COMIC_FILE = "../data/CosmicMutantExportCensus.tsv"  # input COSMOC download files
OUTPUT = "../data/comic_snp.txt"
ENST_FILE = "../data/enst_id.txt"  # output ENST ID

enst_set = set()
with open(COMIC_FILE) as file, open(OUTPUT, "w") as output, open(ENST_FILE, "w") as ens_file:
    next(file)
    for line in file:
        line = line.strip("\n").split("\t")
        gene_name = line[0]
        enst = line[1]
        sample_name = line[4]
        primary_site = line[7]
        primary_histology = line[11]
        gene_cos_mut_id = line[16]
        legacy_mut = line[17]
        mutation_cds = line[19]
        mutation_aa = line[20]
        Mutation_Description = line[21]
        nutation_gene_position = line[25]
        strand = line[26]
        pub_id = line[32]

        if Mutation_Description == "Substitution - Missense" and "delins" not in mutation_aa:
            if enst not in enst_set:
                enst_set.add(enst)
                ens_file.write(enst+"\n")
            output.write("\t".join(
                [gene_name, enst, mutation_aa, mutation_cds, sample_name, primary_site,
                    primary_histology, gene_cos_mut_id, legacy_mut, strand, pub_id]
            )+"\n")

# new format
# Gene name	Accession Number	Sample name		Primary site	Primary histology	GENOMIC_MUTATION_ID	LEGACY_MUTATION_ID	Mutation CDS	Mutation AA		Mutation genome position	Mutation strand	SNP	Resistance Mutation	FATHMM prediction	FATHMM score	Mutation somatic status	Pubmed_PMID	ID_STUDY	Sample Type	Tumour origin	Age	Tier
# wild_aa,position,mut_aa,sequence,gene_name,enst_id,mutation_protein,mutation_cds,sample_name,primary_sit,primary_histology,gene_cos_mut_id,legacy_mut,strand,pub_id
