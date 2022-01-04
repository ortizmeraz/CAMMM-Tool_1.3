Path=r"D:\GitHub\CAMMM-Tool_1.3\YELP\POIS_Quebec.csv"
ListType=[]
import csv

FullData={}
with open(Path, 'r',encoding='utf8') as file:
    reader = csv.reader(file)
    Header=next(reader)
    print(Header)
    print("-----------------------")
    cont=1
    for idx,row in enumerate(reader):
        cont+=1
        # print(row)
        FullData[row[0]]={}
        ListType.append(row[2])
        for i in range(1,7):
            # print(i)
            FullData[row[0]][Header[i]]=row[i]

# print(set(ListType))


ListOfCatInterest=['nightclub','restaurant','pub']
ListPOIS=[]
for Record in FullData.keys():
    if FullData[Record]['fclass'] in ListOfCatInterest:
        ListPOIS.append(Record)

print(len(ListPOIS))

import numpy as np
Count=np.unique(ListType, return_counts=True)

# print(Count)