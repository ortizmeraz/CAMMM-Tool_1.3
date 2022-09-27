import csv
Path="/mnt/f/OneDrive - Concordia University - Canada/RA-CAMM/Density Calculations/Service/Tables/QuebecRawData.csv"

Data={}
ProcData={}
DisolveFiled="fclass"
ConcatField="name"
Count={}
with open(Path,encoding="utf-8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    headers = next(csv_reader, None)
    print(csv_reader)
    for idx,row in enumerate(csv_reader):
        # print(idx,row)
        Data[idx]={}
        for j,elem in enumerate(row):
            Data[idx][headers[j]]=elem

for ki in Data.keys():
    # print(ki, Data[ki])
    if Data[ki][DisolveFiled] not in ProcData.keys():
        ProcData[Data[ki][DisolveFiled]]=[] 
        Count[Data[ki][DisolveFiled]]=0
    Count[Data[ki][DisolveFiled]]+=1
    if len(ProcData[Data[ki][DisolveFiled]])<15:
        if ProcData[Data[ki][DisolveFiled]]!="":
            ProcData[Data[ki][DisolveFiled]].append(Data[ki][ConcatField])

# for ki in ProcData.keys():
#     print(ki,len(ProcData[ki]),ProcData[ki])
#     print()


import csv
exitPath="/mnt/f/OneDrive - Concordia University - Canada/RA-CAMM/Density Calculations/Service/Tables/Categories.csv"
header=["fclass","num","examples"]
WorkDict=ProcData
data_file = open(exitPath, 'w')
csv_writer = csv.writer(data_file)
csv_writer.writerow(header)
for i,x in enumerate(WorkDict.keys()):
    print(i,x)
    Example="|".join(WorkDict[x])
    Line=[x,Count[x],Example]
    csv_writer.writerow(Line)

data_file.close()
