###### RUNN NOVEMBER 2022

#### Script 20







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
    # ExitString='\''+ExitString+"'"
    if ShowProcess: print(ExitString)
    if ShowProcess: b=input('.................................')
    return ExitString

def GetLine(dataStop:dict,dataTrip:dict,stop:str,Patch:dict,ShowProcess:bool=False):
    if ShowProcess: print("Getting the Line")
    if ShowProcess: b=input('.................................')
    def SubMainFunc(stop):
        if stop in dataStop.keys():
            if ShowProcess: print("Key in dataStop")
            ListTrips=dataStop[stop]
            for trip in ListTrips:
                if ShowProcess: print("stop",stop,"trip",trip,dataTrip[trip])
                if ShowProcess: print("ExitValue",ExitValue)
                if trip in dataTrip.keys():
                    if ShowProcess: print(".")
                    # if ShowProcess: b=input('.................................')

                    if dataTrip[trip] in ExitValue:
                        # if ShowProcess: print("The line is not on list")
                        pass
                    else:
                        if ShowProcess: print("Adding line to list")
                        ExitValue.append(str(dataTrip[trip]))
            if ShowProcess: print("ExitValue:",ExitValue)
            # if ShowProcess: b=input('.................................')    
    ExitValue=[]
    CheckInPatch=False
    for st in Patch:
        if int(stop) in Patch.keys():
            CheckInPatch=True
            TempVar=st

    if ShowProcess: print("CheckInPatch",CheckInPatch)
    if ShowProcess: b=input('.................................')
    if CheckInPatch is False:
        SubMainFunc(stop=stop)
    if CheckInPatch:
        if ShowProcess: print("stop:",stop)
        if ShowProcess: print("Patch:",Patch)
        if ShowProcess: print("TempVar:",TempVar)
        if ShowProcess: print("Patch[(stop)]:",Patch[int(stop)])
        if ShowProcess: b=input('.................................')
        for st in Patch[int(stop)]:
            if ShowProcess: print("                                     CHECK here:",st,stop)
            SubMainFunc(stop=str(st))
    if ShowProcess: print("ExitValue",ExitValue)
    if ShowProcess: b=input('.................................')
    if len(ExitValue)==0:
        ExitValue=['NA']
    return ExitValue
def ckeckStop(listOfChecker,stop):
    if stop in listOfChecker:
        return True
    else:
        return False


def Main(PathNodeList,PathBuses,PathMetro,Patch,ShowProcess:bool=False):
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
        # if ShowProcess: print("key",key,type(key))
        stop= str(Metro[key]['StopCode'])
        
        # if ShowProcess: print(Patch)
        for st in Patch:
            if ShowProcess: print(st)
            if int(stop) in Patch[st]:
                stop=str(st)
                MetroData[stop]=Metro[key]
                MetroData[stop]['StopCode']=stop
                MetroData[stop]['stop_id']=stop
                # if ShowProcess: print("stop",stop,type(stop))
                # if ShowProcess: print("MetroData",MetroData[stop])
                # if ShowProcess: b=input('.................................')
        if stop not in MetroData.keys():
            MetroData[stop]=Metro[key]
    
    RailRData={}
    TramsData={}

    if ShowProcess: print("\n"*5,"#########################\nMetro Keys")
    if ShowProcess: print(list(MetroData.keys()))
    # if ShowProcess: print(list(BusesData.keys()))
    if ShowProcess: b=input('.................................')
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

    ListOfNodeKeys=list(NodeDict.keys())

    if ShowProcess: print("\n"*10)
    if ShowProcess: print("List Of Node Keys")
    if ShowProcess: print(ListOfNodeKeys)
    if ShowProcess: b=input('.................................')

    for id,key in enumerate(NodeDict.keys()):
        Mainstop=str(key)
        if ShowProcess: print("\n\n\n#########################\n#########################\n#########################\n#########################")
        print("MainStop",Mainstop,type)

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
        AccesibilityIndex={"Buses":[],"Tram":[],"Metro":[],"Train":[]}

        if NodeDict[key]['Type']=='Hub':
            if ShowProcess: print("Is  HUB")
        ListStopsForCoords=[]
        for stop in NodeDict[key]['Data']:

            print("Stop:",stop)
            

            if stop in TramsData.keys(): 
                ListName.append(TramsData[stop]['stop_name'])
                if ShowProcess: print("stop",stop)
                if ShowProcess: print(TramsData[stop])

                TramsStations[stop]=GetLine(dataStop=StopTripData,dataTrip=TripData,stop=stop,ShowProcess=False,Patch=Patch)
                ListStopsForCoords.append([TramsData[stop]['stop_lat'],TramsData[stop]['stop_lon']])
                ListName.append(TramsData[stop]['stop_name'])

            if stop in BusesData.keys(): 
                ListName.append(BusesData[stop]['stop_name'])
                if ShowProcess: print("BUS - stop",stop)
                if ShowProcess: print(BusesData[stop])
                BusesStations[stop]=GetLine(dataStop=StopTripData,dataTrip=TripData,stop=stop,ShowProcess=False,Patch=Patch)
                ListStopsForCoords.append([BusesData[stop]['stop_lat'],BusesData[stop]['stop_lon']])
                ListName.append(BusesData[stop]['stop_name'])
                AccesibilityIndex["Buses"].append(BusesData[stop]['wheelchair_boarding'])
                if ShowProcess: print()
            
            if stop in MetroData.keys(): 
                if ShowProcess: print("Metro Station",stop)
                if ShowProcess: print(MetroData[stop])
                # ckeckStop(listOfChecker=["91","92","93"],stop=stop)
                MetroStations[stop]=GetLine(dataStop=StopTripData,dataTrip=TripData,stop=stop,ShowProcess=False,Patch=Patch)
                Name=MetroData[stop]['stop_name']
                Coord['Lat']=MetroData[stop]['stop_lat']
                Coord['Lon']=MetroData[stop]['stop_lon']
                print("Name:",MetroData[stop]['stop_name'],Name)
                AccesibilityIndex["Metro"].append(MetroData[stop]['wheelchair_boarding'])
                # if ShowProcess: b=input('End of Metro calculations.................................')

            if stop in RailRData.keys(): 
                if ShowProcess: print("Train Station",stop)
                if ShowProcess: print(RailRData[stop])
                RailRStations[stop]=GetLine(dataStop=StopTripData,dataTrip=TripData,stop=stop,ShowProcess=False,Patch=Patch)
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
        if ShowProcess: print("Key",key)
        if ShowProcess: print("Name",Name)
        if ShowProcess: print("Coord",Coord)
        if ShowProcess: print("MetroStations",MetroStations)
        if ShowProcess: print("RailRStations",RailRStations)
        if ShowProcess: print("TramsStations",TramsStations)
        if ShowProcess: print("BusesStations",str(BusesStations))
        if ShowProcess: print("AccesibilityIndex",AccesibilityIndex)
        ExitLine=str(key)+",\'"+Name+"\',\'"+NodeDict[key]['Type']+"\',"+str(Coord['Lat'])+","+str(Coord['Lon'])+","
        ExitLine+=DictToString(Dict=MetroStations,ShowProcess=False)+","
        ExitLine+=DictToString(Dict=RailRStations,ShowProcess=False)+","
        ExitLine+=DictToString(Dict=TramsStations,ShowProcess=False)+","
        ExitLine+=DictToString(Dict=BusesStations,ShowProcess=False)+","
        ExitLine+=DictToString(Dict=AccesibilityIndex,ShowProcess=False)+","
        ExitLine+="\'"+URL+"\'\n"
        # if "'" in ExitLine:
        #     print("ERRROR")
        #     print(ExitLine)
        #     b=input('.................................')
        ExitData+=ExitLine
        if ShowProcess: print("\n"*5)
        if ShowProcess: print(ExitLine)


        Jason="{"
        Jason+="\"type\": \"Feature\","
        Jason+="\"properties\": {"
        Jason+="\"Id\": \""+str(key)+"\","
        Jason+="\"Name\": \""+Name+"\","
        Jason+="\"Type\": \""+NodeDict[key]['Type']+"\","
        Jason+="\"MetroData\": "+DictToString(Dict=MetroStations,ShowProcess=False)+","
        Jason+="\"RailData\": "+DictToString(Dict=RailRStations,ShowProcess=False)+","
        Jason+="\"TramData\": "+DictToString(Dict=TramsStations,ShowProcess=False)+","
        Jason+="\"BusData\": "+DictToString(Dict=BusesStations,ShowProcess=False)+","
        Jason+="\"AccesibilityIndex\": "+DictToString(Dict=AccesibilityIndex,ShowProcess=False)+","

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
    f = open(Path, 'w',encoding='utf8')
    f.write(Data)
    f.close()

if __name__=="__main__":
    PathTxtFile=r'F:\OneDrive - Concordia University - Canada\RA-CAMMM\Gis_Data\NodeList.txt'
    PathToBuses=r"F:\OneDrive - Concordia University - Canada\RA-CAMMM\Gis_Data\BusesData.csv"
    PathToMetro=r"F:\OneDrive - Concordia University - Canada\RA-CAMMM\Gis_Data\MetroData.csv"
    PatchMTL={91:[9999111,9999112,9999114],92:[9999052,9999055],93:[9999492,9999495]}
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
    Data=Main(PathNodeList=PathTxtFile,PathBuses=PathToBuses,PathMetro=PathToMetro,ShowProcess=False,Patch=PatchMTL)
    WriteToFile(Path="Salida2.json",Data=Data)
    # print(Data)


