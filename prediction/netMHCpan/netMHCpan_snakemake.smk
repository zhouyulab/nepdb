"""Commit to run multiple netMHCpan4  """

nfiles = 1000

rule run_MHC_predict:
    input:
        pep = "data/new_pep.{indx}.txt",
        hla = "data/HLA_type.txt"
    output:
        os.path.join("result", "{indx}_results.txt")
    shell:
        r"""
set +u
source ~/.bashrc
conda activate py27
if [[ -e result/annres.{wildcards.indx}.tmp.txt ]]; then
    rm result/annres.{wildcards.indx}.tmp.txt
fi

for pep in $(cat {input.pep}); do
    echo ">{wildcards.indx}" > result/test.{wildcards.indx}.fa
    echo "${{pep}}" >> result/test.{wildcards.indx}.fa
    for hla in $(cat {input.hla}); do
        python2 mhc_i/src/predict_binding.py netmhcpan HLA-${{hla}} ${{#pep}} result/test.{wildcards.indx}.fa >> result/annres.{wildcards.indx}.tmp.txt
    done
    rm result/test.{wildcards.indx}.fa
done
awk '{{if(NR%2==0){{print $0}}}}' result/annres.{wildcards.indx}.tmp.txt > {output}
rm result/annres.{wildcards.indx}.tmp.txt
        """

rule all:
    input:
        expand(rules.run_MHC_predict.output, indx=range(nfiles))
