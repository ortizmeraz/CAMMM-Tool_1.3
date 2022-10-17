import csv
import ast
from turtle import Turtle


def IsStation(Code:str,ShowResult=False):
    if int(Code)<100:
        Exit=True
    else:
        Exit=False
    if ShowResult: print(Exit,end="| ")
    return Exit

def TurnStr2Coord(string:str,ShowData=False):
    if ShowData: print()
    LocList=ast.literal_eval(string)
    Exit=[0,0]
    if ShowData: print("LocList",LocList,type(LocList))
    Exit[0]=float(LocList[0])
    Exit[1]=float(LocList[1])
    if ShowData: print("Exit ",Exit,type(Exit))
    if ShowData: 
        for i in Exit:
            print("\t",i,type(i))
    if ShowData: print()
    return Exit



def Process(Data:dict,CatHubs:dict,CatBuses:dict,BusData:dict,MetroData:dict):
    CheckPrint=True
    for key in Data.keys():
        XCoord=[]
        YCoord=[]
        if CheckPrint: print()
        if CheckPrint: print(key,"\t",Data[key])
        if CheckPrint: print("Length:",len(Data[key]['Data']))
        if CheckPrint: print("Type  :",Data[key]['Type'])
        Hub=False
        for StCode in Data[key]['Data']:
            if IsStation(Code=StCode,ShowResult=CheckPrint):
                Hub=True
                break

        for StCode in Data[key]['Data']:
            if CheckPrint: print(StCode,end=" , ")
            if IsStation(Code=StCode,ShowResult=CheckPrint):
                if CheckPrint: print(" ",StCode,MetroData[StCode]['location'])
                Coord=TurnStr2Coord(string=MetroData[StCode]['location'])
                XCoord.append(Coord[0])
                YCoord.append(Coord[1])
            else:
                if CheckPrint: print(StCode,BusData[StCode]['location'])
                Coord=TurnStr2Coord(string=BusData[StCode]['location'])
                XCoord.append(Coord[0])
                YCoord.append(Coord[1])
        if CheckPrint: print("XCoord",XCoord)
        if CheckPrint: print("YCoord",YCoord)
        AvgXcoord=(sum(XCoord))/len(XCoord)
        AvgYcoord=(sum(YCoord))/len(YCoord)
        if CheckPrint: print("Coord X:",AvgXcoord)
        if CheckPrint: print("Coord y:",AvgYcoord)
        if Data[key]['Type']=="Hub":
            for cat in CatHubs.keys():
                if len(Data[key]['Data']) in CatHubs[cat]:
                    Category=cat
        else:
            for cat in CatBuses.keys():
                if len(Data[key]['Data']) in CatBuses[cat]:
                    Category=cat
        if CheckPrint: print("Type    :",Data[key]['Type'])
        if CheckPrint: print("Category:",Category)
        if CheckPrint: b=input('.................................')
    


def ReadDict(Path:dict,ShowData=False):
    with open(Path) as f:
        Lines = f.readlines()
        # for line in Lines:
        #     print(line)
    f.close()
    ExitData=ast.literal_eval(Lines[0])
    if ShowData: print(ExitData,type(ExitData))
    return ExitData


def ReadCSVgeoFile(Path:str,IndexVal:int,ShowData=False):
    ExitData={}
    with open(Path,encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        headers = next(csv_reader, None)
        if ShowData: print(headers)
        if ShowData: print(csv_reader)
        for idx,row in enumerate(csv_reader):
            if ShowData: print(row)
            ExitData[row[IndexVal]]={}
            for idy,element in enumerate(row):
                if ShowData: print(idy,headers[idy],":",element)
                ExitData[row[IndexVal]][headers[idy]]=element
            # if ShowData: print(headers[idx],':',row)
            if ShowData: print("ExitData:",ExitData)
            if ShowData: b=input('.................................')
        if ShowData: print()
    return ExitData


if __name__=="__main__":
    ListPath=r"SampleData\GIS_Data\NodeList2.txt"
    CsvPathBus=r"SampleData\GIS_Data\Montreal_Bus_Data.csv"
    CsvPathMetro=r"SampleData\GIS_Data\Montreal_Metro_Data.csv"
    CategoriesHUbs={"Small":range(0,5),"Medium":range(5,99)}
    CategoriesClusters={"Samll":range(0,4),"Medium":range(4,7),"Large":range(7,99)}
    Data=ReadDict(Path=ListPath,ShowData=False)
    BusData=ReadCSVgeoFile(Path=CsvPathBus,IndexVal=2,ShowData=False)
    MetroData=ReadCSVgeoFile(Path=CsvPathMetro,IndexVal=2,ShowData=False)
    Process(Data=Data,CatHubs=CategoriesHUbs,CatBuses=CategoriesClusters,BusData=BusData,MetroData=MetroData)
    # for key in MetroData.keys():
    #     print(key,MetroData[key])
    #     print()
