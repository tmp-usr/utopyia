from Bio import Entrez
Entrez.email = "A.N.Other@example.com"
pmid = "157170775"

record = Entrez.read(Entrez.elink(dbfrom="nucleotide", db="taxonomy", id=pmid))

linksetdb = record[0]["LinkSetDb"][0]
print linksetdb["Link"][0]["Id"]


