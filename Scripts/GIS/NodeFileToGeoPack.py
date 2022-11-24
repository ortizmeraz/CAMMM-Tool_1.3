###### RUNN NOVEMBER 2022

#### Script 20



# def TypeOfStop(City:str="MTL",stop:str="NA"):
#     if City=="MTL":
#         if int(stop)<200 and :
#             ExitVal="Metro"
#         else:
#             ExitVal="Bus"
#     return ExitVal



def OpenDictionaryFile(Path):
    Dict=""
    with open(Path) as f:
        Lines = f.readlines()
        for i,line in enumerate(Lines):
            # print(i)
            Dict=line
    f.close()
    DictionaryData=eval(Dict)
    return DictionaryData

def OpenCSV(Path,ShowProcess:bool =False):
    import csv
    Data={}
    with open(Path,encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        headers = next(csv_reader, None)
        if ShowProcess: print(csv_reader)
        for idx,row in enumerate(csv_reader):

            if ShowProcess: print(idx,row)
            Data[idx]={}
            for i,elem in enumerate(row):
                Data[idx][headers[i]]=elem

    return Data


def GetTripData(ShowProcess:bool=False):
    ExtDict={}
    SourcePath=r"E:\GitHub\CAMMM-Tool_1.3\Operational\trips.txt"
    import csv
    with open(SourcePath,encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        headers = next(csv_reader, None)

        if ShowProcess: print(headers)
        # b=input('.................................')
        for idx,row in enumerate(csv_reader):
            if ShowProcess: print(idx,row)
            # b=input('.................................')
            ExtDict[row[2]]=row[0]
    if ShowProcess:
        for key in ExtDict.keys():
            print(key,ExtDict[key])
    return ExtDict
            

def GetStopiTrip(ShowProcess:bool=False):
    ExitDict={}
    SourcePath=r"E:\GitHub\CAMMM-Tool_1.3\Operational\stop_times.txt"
    import csv
    with open(SourcePath,encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        headers = next(csv_reader, None)
        if ShowProcess: print(headers)
        for idx,row in enumerate(csv_reader):
            Stop=str(row[3])
            Trip=str(row[0])
            if ShowProcess: print(idx,row)
            if Stop not in ExitDict.keys():
                ExitDict[Stop]=[]
            ExitDict[Stop].append(Trip)
            # b=input('.................................')
    if ShowProcess:
        for key in ExitDict.keys():
            print(key,ExitDict[key])
    return ExitDict

def GetAvCoords(ListCoords:list,ShowProcess:bool=False):
    Lat=[]
    Lon=[]
    for pairs in ListCoords:
        if ShowProcess: print(pairs)
        Lat.append(float(pairs[0]))
        Lon.append(float(pairs[1]))
    ExitLat=(sum(Lat)/len(Lat))
    ExitLon=(sum(Lon)/len(Lon))
    ExitVal={'Lat':str(round(ExitLat,6)),'Lon':str(round(ExitLon,6))}
    return ExitVal
    
def GetName(ListName:list,ShowProcess:bool=False):
    UniqueNames=[]
    for names in ListName:
        singlenames=names.split(" / ")
        for na in singlenames:
            if ShowProcess: print(na)
            if na not in UniqueNames:
                UniqueNames.append(na)

    Exit = "-".join([str(item) for item in UniqueNames])            
    return Exit

def DictToString(Dict:dict,ShowProcess:bool=False):
    if ShowProcess: print("Dictionary to string tool")
    if ShowProcess: print(Dict)
    DictString=str(Dict)
    ExitString=""
    for char in DictString:
        if char !="'":
            ExitString+=char
        else:
            ExitString+='"'
    ExitString='\''+ExitString+"'"
    if ShowProcess: print(ExitString)
    if ShowProcess: b=input('.................................')
    return ExitString

def GetLine(dataStop:dict,dataTrip:dict,stop:str,ShowProcess:bool=False):
    ExitValue=[]
    if stop in dataStop.keys():
        ListTrips=dataStop[stop]
        for trip in ListTrips:
            if ShowProcess: print("stop",stop,"trip",trip,dataTrip[trip])
            if ShowProcess: print("ExitValue",ExitValue)
            if trip in dataTrip.keys():
                if ShowProcess: b=input('.................................')

                if dataTrip[trip] in ExitValue:
                    if ShowProcess: print("The line is not on list")
                else:
                    if ShowProcess: print("Adding line to list")
                    ExitValue.append(str(dataTrip[trip]))
        if ShowProcess: print("ExitValue:",ExitValue)
        if ShowProcess: b=input('.................................')

    if len(ExitValue)==0:
        ExitValue=['NA']
    return ExitValue



def Main(PathNodeList,PathBuses,PathMetro,ShowProcess:bool=False):
    ExitData="Id,Name,Type,Lat,Lon,"
    ExitData+="MetroStations,RailRStations,TramsStations,BusesStations,URL\n"

    ExitJSONtext="{\n  \"features\": [\n"

    Buses=OpenCSV(Path=PathBuses)
    BusesData={}
    # print(len(Buses.keys()))
    for key in Buses.keys():
        # print(key,Buses[key],"----")
        BusesData[str(Buses[key]['StopCode'])]=Buses[key]
    #     print(BusesData[str(Buses[key]['StopCode'])])
    # b=input('.................................')
    Metro=OpenCSV(Path=PathMetro)
    MetroData={}
    for key in Metro.keys():
# 9999111,9999112,9999114
# Key 14 Station Berri-UQAM 1
# Key 14 9999111
# Key 43 Station Berri-UQAM 2
# Key 43 9999112
# Key 59 Station Berri-UQAM 4
# Key 59 9999114


# Key 49 Station Jean-Talon 2
# Key 49 9999052
# Key 68 Station Jean-Talon 5
# Key 68 9999055


# Key 33 Station Snowdon 2
# Key 33 9999492
# Key 60 Station Snowdon 5
# Key 60 9999495



#         if int(Metro[key]['StopCode'])>100:
#             if ShowProcess: print("Key",key,Metro[key]['stop_name'])
#             if ShowProcess: print("Key",key,Metro[key]['StopCode'])
#             b=input('.................................')
#             stop= "99"
#         else:
        stop= str(Metro[key]['StopCode'])
        MetroData[stop]=Metro[key]
    
    RailRData={}
    TramsData={}

    if ShowProcess: print("\n"*5,"#########################\nMetro Keys")
    if ShowProcess: print(list(MetroData.keys()))
    if ShowProcess: print(list(BusesData.keys()))

    NodeDict=OpenDictionaryFile(Path=PathNodeList)


    TripData=GetTripData()
    print("TripData",type(TripData))
    # d=0
    # for key in TripData.keys():
    #     d+=1
    #     print(key,TripData[key])
    #     if d==10: break
    # b=input('.................................')
    StopTripData=GetStopiTrip()
    # for key in StopTripData.keys():
    #     print(key,"-",type(key))
    # if ShowProcess: print("------------------------------------")
    # if ShowProcess: print(StopTripData.keys())

    # b=input('.................................')
    # print(Buses.keys())
    # for key in Buses.keys():
    #     print(key,type(key))
                # Lat :
                # Lon :

                # "fid": "1644",
                # "Id": "54735",
                # "Type": "Cluster",
                # "Category": "Small",
                # "MetroData": "{}",
                # "BusData": "{'54737':['24','101'],'54735':['102']}",
                # "TramData": "{}",
                # "RailData": "{}",
                # "Name": "De La V�rendrye - Rondeau",
                # "URL": "http://maps.google.com/maps?q=&layer=c&cbll=45.613755500424006,-73.54609349974568",

    # ListOfNodeKeys=list(NodeDict.keys())
    # if ShowProcess: print("ListOfNodeKeys")
    # if ShowProcess: print(NodeDict["9999111"])
    # if ShowProcess: print(NodeDict["9999492"])
    # if ShowProcess: print(NodeDict["9999112"])
    # if ShowProcess: print(NodeDict["9999052"])
    # if ShowProcess: print(NodeDict["9999114"])
    # if ShowProcess: print(NodeDict["9999495"])
    # if ShowProcess: print(NodeDict["9999055"])
    # # if ShowProcess: print(NodeDict[""])
    # if ShowProcess: print("\n"*10)
    # if ShowProcess: print(ListOfNodeKeys)
    # if ShowProcess: b=input('.................................')
    for key in NodeDict.keys():
        if int(key)>9999000:
            if ShowProcess: print("HEY HEY")
            if ShowProcess: b=input('.................................')

    for id,key in enumerate(NodeDict.keys()):
        Mainstop=str(key)
        if ShowProcess: print("\n\n\n#########################\n#########################\n#########################\n#########################")
        print("MainStop",Mainstop,type)
        if key=="99":
            if ShowProcess: b=input('.................................')
        if ShowProcess: print(id,key)
        if ShowProcess: print(NodeDict[key])
        FiD=id+1
        Name=""
        ListName=[]
        Coord={'Lat':0,'Lon':0}
        MetroStations={}
        RailRStations={}
        TramsStations={}
        BusesStations={}

        if NodeDict[key]['Type']=='Hub':
            if ShowProcess: print("Is  HUB")
        ListStopsForCoords=[]
        for stop in NodeDict[key]['Data']:

            print("Stop:",stop)

            if stop in TramsData.keys(): 
                ListName.append(TramsData[stop]['stop_name'])
                if ShowProcess: print("stop",stop)
                if ShowProcess: print(TramsData[stop])
                TramsStations[stop]=GetLine(dataStop=StopTripData,dataTrip=TripData,stop=stop,ShowProcess=False)
                ListStopsForCoords.append([TramsData[stop]['stop_lat'],TramsData[stop]['stop_lon']])
                ListName.append(TramsData[stop]['stop_name'])

            if stop in BusesData.keys(): 
                ListName.append(BusesData[stop]['stop_name'])
                if ShowProcess: print("BUS - stop",stop)
                if ShowProcess: print(BusesData[stop])
                BusesStations[stop]=GetLine(dataStop=StopTripData,dataTrip=TripData,stop=stop,ShowProcess=False)
                ListStopsForCoords.append([BusesData[stop]['stop_lat'],BusesData[stop]['stop_lon']])
                ListName.append(BusesData[stop]['stop_name'])
                if ShowProcess: print()

            if stop in MetroData.keys(): 
                if ShowProcess: print("stop",stop)
                if ShowProcess: print(MetroData[stop])
                MetroStations[stop]=GetLine(dataStop=StopTripData,dataTrip=TripData,stop=stop,ShowProcess=False)
                Name=MetroData[stop]['stop_name']
                Coord['Lat']=MetroData[stop]['stop_lat']
                Coord['Lon']=MetroData[stop]['stop_lon']
                print("Name:",MetroData[stop]['stop_name'],Name)

            if stop in RailRData.keys(): 
                if ShowProcess: print("stop",stop)
                if ShowProcess: print(RailRData[stop])
                RailRStations[stop]=GetLine(dataStop=StopTripData,dataTrip=TripData,stop=stop,ShowProcess=False)
                Name=RailRData[stop]['stop_name']+" - "+Name
                Coord['Lat']=RailRData[stop]['stop_lat']
                Coord['Lon']=RailRData[stop]['stop_lon']

        if Coord=={'Lat':0,'Lon':0}:
            Coord=GetAvCoords(ListCoords=ListStopsForCoords,ShowProcess=False)
        if Name=="":
            if ShowProcess: print(ListName)
            Name=GetName(ListName=ListName,ShowProcess=False)
        URL="http://maps.google.com/maps?q=&layer=c&cbll="+str(Coord['Lat'])+","+str(Coord['Lon'])

        if ShowProcess: print("\n"*3)
        if ShowProcess: print("Name",Name)
        if ShowProcess: print("Coord",Coord)
        if ShowProcess: print("MetroStations",MetroStations)
        if ShowProcess: print("RailRStations",RailRStations)
        if ShowProcess: print("TramsStations",TramsStations)
        if ShowProcess: print("BusesStations",str(BusesStations))
        ExitLine=str(key)+",\'"+Name+"\',\'"+NodeDict[key]['Type']+"\',"+str(Coord['Lat'])+","+str(Coord['Lon'])+","
        ExitLine+=DictToString(Dict=MetroStations,ShowProcess=False)+","
        ExitLine+=DictToString(Dict=RailRStations,ShowProcess=False)+","
        ExitLine+=DictToString(Dict=TramsStations,ShowProcess=False)+","
        ExitLine+=DictToString(Dict=BusesStations,ShowProcess=False)+","
        ExitLine+="\'"+URL+"\'\n"
        # if "'" in ExitLine:
        #     print("ERRROR")
        #     print(ExitLine)
        #     b=input('.................................')
        ExitData+=ExitLine
        if ShowProcess: print(ExitLine)


        Jason="{"
        Jason+="\"type\": \"Feature\","
        Jason+="\"properties\": {"
        Jason+="\"Id\": \""+str(key)+"\","
        Jason+="\"Name\": \""+Name+"\","
        Jason+="\"Type\": \""+NodeDict[key]['Type']+"\","
        Jason+="\"MetroData\": \""+DictToString(Dict=MetroStations,ShowProcess=False)+"\","
        Jason+="\"RailData\": \""+DictToString(Dict=RailRStations,ShowProcess=False)+"\","
        Jason+="\"TramData\": \""+DictToString(Dict=TramsStations,ShowProcess=False)+"\","
        Jason+="\"BusData\": \""+DictToString(Dict=BusesStations,ShowProcess=False)+"\","

        Jason+="\"URL\": \""+URL+"\""
        Jason+="},"
        Jason+="\"geometry\": {"
        Jason+="\"coordinates\": ["
        if ShowProcess: print("Coord['Lon']",Coord['Lon'],type(Coord['Lon']))
        Jason+=Coord['Lon']+","
        Jason+=str(Coord['Lat'])
        Jason+="],"
        Jason+="\"type\": \"Point\""
        Jason+="},"
        Jason+="\"id\": \""+str(id)+"\""
        Jason+="},"
        ExitJSONtext+=Jason
        if ShowProcess: print(Jason)

        if ShowProcess: b=input('.................................')
    ExitJSONtext+="]}"
    return ExitJSONtext



def WriteToFile(Path,Data):
    f = open(Path, 'w')
    f.write(Data)
    f.close()

if __name__=="__main__":
    PathTxtFile=r'F:\OneDrive - Concordia University - Canada\RA-CAMMM\Gis_Data\NodeList.txt'
    PathToBuses=r"F:\OneDrive - Concordia University - Canada\RA-CAMMM\Gis_Data\BusesData.csv"
    PathToMetro=r"F:\OneDrive - Concordia University - Canada\RA-CAMMM\Gis_Data\MetroData.csv"
    Data=Main(PathNodeList=PathTxtFile,PathBuses=PathToBuses,PathMetro=PathToMetro,ShowProcess=False)
    WriteToFile(Path="Salida2.json",Data=Data)
    # print(Data)


