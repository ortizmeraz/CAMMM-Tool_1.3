import csv
import os
from statistics import mean

BasePath=r"/mnt/e/GitHub/CAMMM-Tool_1.3/Results/CSV_Results_Services/Montreal"
ExitPath=r"/mnt/e/GitHub/CAMMM-Tool_1.3/Results/CSV_Results_Services/Montreal/Summary.csv"

def GetDist(text):
    exit=int(text.split(".")[0])
    # print("exit",exit)
    return exit



def ToInt(text):
    Start=text.split(".")[0]
    Start=Start.replace("Samp","")
    # print("##############################################################Start",Start)
    Start=int(Start)
    # print("")
    # print(Start,type(Start))
    # b=input('.................................')
    return Start

dir_list = os.listdir(BasePath)

f = open(ExitPath, 'w')
text="FiD,Primary_NumberServices,Primary_MaxDist,Primary_MinDist,Primary_AvDist,"
text+="Secondary_NumberServices,Secondary_MaxDist,Secondary_MinDist,Secondary_AvDist,"
text+="Tertiary_NumberServices,Tertiary_MaxDist,Tertiary_MinDist,Tertiary_AvDist\n"
f.write(text)
for fileName in dir_list:
    

    Values={"Primary":[],"Secondary":[],"Tertiary":[],"NA":[],"":[]}
    FiD=ToInt(text=fileName)
    FullPath=BasePath+"/"+fileName
    with open(FullPath,encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        headers = next(csv_reader, None)
        # print(csv_reader)
        # print(headers)
        for idx,row in enumerate(csv_reader):
            # print(idx,row)
            # print("")
            # print(idx,type(idx))
            # print(row[6],type(row[6]))
            # print(row[10],type(row[10]))
            # print("")
            if row[10] !="":
                Values[row[6]].append(GetDist(row[10]))
            # for idy,elem in enumerate(row):
            #     print(idy,elem)
            # b=input('.................................')
    if len(Values["Primary"])>0:
        MaxP=max(Values["Primary"])
        MinP=min(Values["Primary"])
        AveP=mean(Values["Primary"])
        LenP=len(Values["Primary"])
    else:
        MaxP=0
        MinP=0
        AveP=0
    if len(Values["Secondary"])>0:
        MaxS=max(Values["Secondary"])
        MinS=min(Values["Secondary"])
        AveS=mean(Values["Secondary"])
        LenS=len(Values["Secondary"])
    else:
        MaxS=0
        MinS=0
        AveS=0
    if len(Values["Tertiary"])>0:
        MaxT=max(Values["Tertiary"])
        MinT=min(Values["Tertiary"])
        AveT=mean(Values["Tertiary"])
        LenT=len(Values["Tertiary"])
    else:
        MaxT=0
        MinT=0
        AveT=0
    # print("------------------------------")
    # print("LenP",LenP)
    # print("MaxP",MaxP)
    # print("MinP",MinP)
    # print("AveP",AveP)
    # print("···")
    # print("LenS",LenS)
    # print("MaxS",MaxS)
    # print("MinS",MinS)
    # print("AveS",AveS)
    # print("···")
    # print("LenT",LenT)
    # print("MaxT",MaxT)
    # print("MinT",MinT)
    # print("AveT",AveT)

    text=str(FiD)+","+str(LenP)+","+str(MaxP)+","+str(MinP)+","+str(AveP)+","+str(LenS)+","+str(MaxS)+","+str(MinS)+","+str(AveS)+","+str(LenT)+","+str(MaxT)+","+str(MinT)+","+str(AveT)+"\n"
    f.write(text)

f.close()