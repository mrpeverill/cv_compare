#!/bin/env python3

import urllib.request
import sys
import re
import pandas as pd

def file_get_contents(path):
    try:
        page = urllib.request.urlopen(path)
        data = page.read().decode(page.headers.get_content_charset())
        return data
    except:
        with open(path) as file:
            data = file.read()
            return data

regex=re.compile(r'10.\d{4,9}/[-._;()/:A-Z0-9]+',flags=re.I)
preprintRegexes = ['10\.1101',  #bioRxiv
                   '10\.31234'] #psyarxiv
preprintCombinedRegex = "(" + ")|(".join(preprintRegexes) + ")"
def preprint_search(x):
    if re.match(preprintCombinedRegex,x):
        return "preprint"
    else:
        return ""

dois = []
for i in range(1,len(sys.argv)):
    print(sys.argv[i])
    data = file_get_contents(sys.argv[i])
    doitmp=[j.rstrip(".") for j in re.findall(regex,data)]
    datadoi=pd.DataFrame(doitmp,columns=['DOIs'])
    datadoi['preprint'] = [preprint_search(j) for j in datadoi['DOIs']]
    print("Found %s DOI codes" % datadoi.shape[0])
    print("Found %s preprints" % datadoi[datadoi['preprint']=='preprint'].shape[0])
    dois.append(datadoi)
    print("___________________")

#Make lists
A=dois[0]
B=dois[1]
Aex=A[~A['DOIs'].isin(B['DOIs'])]
Bex=B[~B['DOIs'].isin(A['DOIs'])].add_suffix("B")

print("Duplicate Detection:")
Adup=A[A.duplicated()]
print("%s duplicates in A" % len(Adup.index))
print(Adup['DOIs'])
Bdup=B[B.duplicated()]
print("%s duplicates in B" % len(Bdup.index))
print(Bdup['DOIs'])
print("___________________")


print("Unique Items:")

exclusivejoin=pd.concat([Aex,Bex])

print(exclusivejoin.fillna(''))

       



