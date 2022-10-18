import csv
import ast
from turtle import Turtle
from unicodedata import category
import utm


def RemoveParethesis(String:str):
    AddLetter=True
    ExitString=""
    for stri in String:
        if stri =="(":
            AddLetter=False
        elif AddLetter:
            # print("String:",stri)
            ExitString+=stri
        elif stri ==")":
            AddLetter=True
    return ExitString


def WriteToFile(Data:dict,Path:str):
    FirstKey=list(Data.keys())[0]
    Header=list(Data[FirstKey].keys())
    print(Header,type(Header))
    # writer = csv.writer(Path)
    with open(Path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(Header)
        for key in Data.keys():
            Text=[]
            for h in Header:
                Text.append(Data[key][h])
            writer.writerow(Text)
    file.close()
    # writer.close()
    # f = open(Path, 'w')

    # for t in List:
    #     text=t
    #     f.write(text)
    # f.close()

def GetStopName(Lite:list,ShowResult=False):
    Name=""
    nameLength=0
    ListOhNames={}
    for element in Lite:
        if "(" in element:
            element=RemoveParethesis(String=element)
        Streets=element.split(' / ')
        if ShowResult: print(element)
        # if ShowResult: print(Streets)
        for st in Streets:
            st=st.rstrip(" ")
            if st in ListOhNames.keys():
                ListOhNames[st]+=1
            else:
                ListOhNames[st]=1
    if ShowResult: print(ListOhNames)
    MaxRepetetion=0
    for key in ListOhNames.keys():
        if ListOhNames[key]> MaxRepetetion:
            MaxRepetetion=ListOhNames[key]
    
    if ShowResult: print("MaxRepetetion:",MaxRepetetion)
    for i in range(MaxRepetetion,0,-1):
        if ShowResult: print("i:",i)
        for key in ListOhNames.keys():
            if int(i)==int(ListOhNames[key]):
                if ShowResult: print(key,ListOhNames[key])
                if nameLength==0:
                    Name=key
                    nameLength+=1
                elif nameLength<4:
                    nameLength+=1
                    Name=Name+" - "+key
    if ShowResult: print("Name",Name)
    if ShowResult: b=input('.................................')
    return Name



def Convert2UTM(XCoord:float,YCoord:float,Zone=18,Region='U',ShowResult=False):
    LatLon=utm.to_latlon(XCoord,YCoord,Zone,Region)
    if ShowResult: print(LatLon)
    return LatLon

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



def Process(Data:dict,CatHubs:dict,CatBuses:dict,BusData:dict,MetroData:dict,CheckPrint=False):
    ExitDict={}
    for key in Data.keys():
        NumStations=0
        NumBusStops=0
        ListName=[]
        NeedToRename=True
        XCoord=[]
        YCoord=[]
        ListOfStations=[]
        ListOfStops=[]
        if CheckPrint: print()
        if CheckPrint: print("-------------------------------------------------------------------")
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
                # if CheckPrint: print(" ",StCode,MetroData[StCode])
                Coord=TurnStr2Coord(string=MetroData[StCode]['location'])
                XCoord.append(Coord[0])
                YCoord.append(Coord[1])
                NumStations+=1
                ListOfStations.append(StCode)
                Name=MetroData[StCode]['stop_name']
                NeedToRename=False
            else:
                if CheckPrint: print(StCode,BusData[StCode]['location'])
                # if CheckPrint: print(StCode,"------",BusData[StCode])
                Coord=TurnStr2Coord(string=BusData[StCode]['location'])
                XCoord.append(Coord[0])
                YCoord.append(Coord[1])
                NumBusStops+=1
                ListOfStops.append(StCode)
                ListName.append(BusData[StCode]['stop_name'])
        if NeedToRename:
            Name=GetStopName(Lite=ListName,ShowResult=False)

        if CheckPrint: print("XCoord",XCoord)
        if CheckPrint: print("YCoord",YCoord)
        AvgXcoord=(sum(XCoord))/len(XCoord)
        AvgYcoord=(sum(YCoord))/len(YCoord)
        if CheckPrint: print("Coord X:",AvgXcoord)
        if CheckPrint: print("Coord y:",AvgYcoord)
        LatLon=Convert2UTM(XCoord=AvgXcoord,YCoord=AvgYcoord)
        if CheckPrint: print("Lat Lon:",LatLon)
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
        if CheckPrint: print("Name:",Name)
        # if CheckPrint: b=input('.................................')
        ExitDict[key]={"Id":key,
        "Lat":LatLon[0],"Lon":LatLon[1],
        "Magnitud":len(Data[key]['Data']),"Number of Stops":NumBusStops,"Number of Stations":NumStations,
        "List of Stations":ListOfStations,"List of Stops":ListOfStops,
        "Type":Data[key]['Type'],"Category":Category,
        "Name":Name,
        "URL":"http://maps.google.com/maps?q=&layer=c&cbll="+str(LatLon[0])+","+str(LatLon[1])
        }
    return ExitDict
    # Id, x, y,magnitud, number of stops, number of stations, type, category, name of node,StreetViewUrl

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
    CategoriesClusters={"Small":range(0,4),"Medium":range(4,7),"Large":range(7,99)}
    Data=ReadDict(Path=ListPath,ShowData=False)
    BusData=ReadCSVgeoFile(Path=CsvPathBus,IndexVal=2,ShowData=False)
    MetroData=ReadCSVgeoFile(Path=CsvPathMetro,IndexVal=2,ShowData=False)
    NodeData=Process(Data=Data,CatHubs=CategoriesHUbs,CatBuses=CategoriesClusters,BusData=BusData,MetroData=MetroData,CheckPrint=False)
    WriteToFile(Data=NodeData,Path="NodesV2.csv")

    # for key in NodeData.keys():
    #     print(key,NodeData[key])


# Id, x, y, number of stops, number of stations, type, category, name of node,StreetViewUrl
# 1 ,10,10,         6      ,     1             ,  hub, medium  , Station Guy , URL


# 45.503197,-73.569732


# http://maps.google.com/maps?q=&layer=c&cbll=31.33519,-89.28720

# http://maps.google.com/maps?q=&layer=c&cbll=45.537949,-73.578240
