import urllib
import re
from Bio import Entrez


f = open('id.txt','r')
fw = open('error.txt','w')
uni=[]
gene_id=[]
for line in f:
    list1=line.strip().split('\t')
    gene_id=list1[1]
    url = 'https://www.ebi.ac.uk/ena/browser/api/embl/' + gene_id + '?lineLimit=1000'
    try:
        print(f'Requesting {url}')
        source=urllib.request.urlopen(url).read()
        print('Requesting done.')
    except:
        fw.write(gene_id+'\n')
        print('Error Requesting url.')
        continue

    try:
        complement=re.findall('complement.*[^)]',source.decode('utf-8'))
        start = complement[0].strip().split(':')[1].split('.')[0]
        genome = complement[0].split(':')[0].split('(')[1]
        stop = complement[0].split(':')[1].split('..')[1].replace(')','')
        print(f'Fetching Genome {genome} start {start} stop: {stop}')
        handle = Entrez.efetch(db="nuccore", id=genome,rettype="fasta", retmode="text", seq_start=(int(start)-4000), seq_stop=(int(stop)+4000))
    except:
        fw.write(gene_id+'\n')
        print('Entrez fetch error.')
        continue
    
    try:
        read_efetch_gb = handle.read()
        print(read_efetch_gb)
        with open(gene_id +".fasta","w") as file:
            file.write(read_efetch_gb)
    except:
        fw.write(gene_id+'\n')
        print ('Write error.')

fw.close()