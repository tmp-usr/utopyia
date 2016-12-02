from Bio import Entrez
Entrez.email = "my@email.com"
ids = ["148908191", "297793721", "48525513", "507118461"]
search_results = Entrez.read(Entrez.epost("protein", id=','.join(ids)))
webenv = search_results["WebEnv"]
query_key = search_results["QueryKey"]
result= Entrez.read(Entrez.elink(webenv=webenv,
                         query_key=query_key,
                         dbfrom="protein",
                         db="taxonomy"))

print result[0]['IdList']
taxa=[e['Id'] for e in result[0]['LinkSetDb'][0]['Link']]
print taxa
#print "-------"

a= """for i in ids:
    search_results = Entrez.read(Entrez.epost("protein", id=i))
    webenv = search_results["WebEnv"]
    query_key = search_results["QueryKey"]
    print Entrez.read(Entrez.elink(webenv=webenv,
                         query_key=query_key,
                         dbfrom="protein",
                         db="taxonomy"))
"""

