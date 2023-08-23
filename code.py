import Bio
import urllib
import re
import os 
from Bio import Entrez, SeqIO


f = open('id.txt','r')
fw = open('error.txt','w')
uni=[]
gene_id=[]
for line in f:
    list1=line.strip().split('\t')
    gene_id=list1[1]
    url = 'https://www.ebi.ac.uk/ena/browser/api/embl/' + gene_id + '?lineLimit=1000'
    try:
        source=urllib.request.urlopen(url).read()
        complement=re.findall('complement.*[^)]',source.decode('utf-8'))
        start = complement[0].strip().split(':')[1].split('.')[0]
        print (type(start))
        print (int(start)-4000)
        genome = complement[0].split(':')[0].split('(')[1]
        stop = complement[0].split(':')[1].split('..')[1].replace(')','')
        handle = Entrez.efetch(db="nuccore", id=genome,rettype="fasta", retmode="text", seq_start=(int(start)-4000), seq_stop=(int(stop)+4000))
        print (handle.read())
        parse_efetch_gb = SeqIO.parse(handle, "fasta")
        read_efetch_gb = handle.read()
        with open(gene_id +".fasta","w") as file:
            file.write(read_efetch_gb)
    except:
        fw.write(gene_id+'\n')
       # print ('except')
