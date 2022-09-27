import csv


def FullNum(x:int,TotalX:int)->str:
    StrTot=str(TotalX)
    Top=1
    Exit=str(x)
    for i in StrTot:
        Top*=10
    Diff=Top-x
    for i in str(Diff):
        Exit='0'+Exit
    return (Exit)


DistDict={"S":800,"N":400}
ListOfStops=[]
TypeNode={}
Capactiy={}








BasePath= r"F:\OneDrive - Concordia University - Canada\RA-CAMM\Density Calculations\SuperNodes\Transit_Nodes_Montreal.csv"
with open(BasePath,encoding="utf-8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    headers = next(csv_reader, None)
    # print(csv_reader)
    for idx,row in enumerate(csv_reader):
        # print(idx,row,len(row))
        ListOfStops.append(int(row[0]))
        TypeNode[int(row[0])]=row[6]
        Capactiy[int(row[0])]=0


# for i in ListOfStops:
#     print(i,type(i))


# for key in TypeNode.keys():
#     print(key,TypeNode[key])


for NumNode in range(1,3935):
    Num=FullNum(x=NumNode,TotalX=4000)
    Path=r"E:\GitHub\CAMMM-Tool_1.3\Results\CSV Montreal\Samp"+Num+".csv"
    print(Path,TypeNode[int(NumNode)])
    with open(Path,encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        headers = next(csv_reader, None)
        # print(headers)
        for idx,row in enumerate(csv_reader):
            # print(idx,row)
            if row[23]!="":
                Dist=row[23]
            else:
                Dist=99999
            # print(idx,DistDict[TypeNode[int(NumNode)]])

            # print("-",Dist,"¬¬")
            if float(Dist) <= DistDict[TypeNode[int(NumNode)]]:
                Capactiy[int(NumNode)]+=1
            # b=input('.................................')
    # print("Capactiy",Capactiy[int(NumNode)])







# field names 
fields = "fid, reach\n"
    
# data rows of csv file 

    
# name of csv file 
filename = "university_records.csv"
    
# writing to csv file 
csvfile= open(filename, 'w')

csvfile.write(fields)
for NumNode in range(1,3935):
    text=str(NumNode)+","+str(Capactiy[NumNode])+"\n"
    # writing the fields 
    csvfile.write(text) 

