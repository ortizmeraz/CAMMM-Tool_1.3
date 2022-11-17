def TypeOfStop(City:str="MTL",stop:str="NA"):
    if City=="MTL":
        if int(stop)<200:
            ExitVal="Metro"
        else:
            ExitVal="Bus"
    return ExitVal



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

def GetLine(dataStop:dict,dataTrip:dict,stop:str,ShowProcess:bool=False):
    if stop in dataStop.keys():
        ExitValue=dataStop[stop]
        if ShowProcess: print("ExitValue:",ExitValue)
        b=input('.................................')
    else:
        ExitValue=""
    return ExitValue



def Main(PathNodeList,PathBuses,PathMetro,ShowProcess:bool=False):
    ExitData={}

    Buses=OpenCSV(Path=PathBuses)
    BusesData={}
    # print(len(Buses.keys()))
    for key in Buses.keys():
        # print(key,Buses[key],"----")
        BusesData[str(Buses[key]['StopCode'])]=Buses[key]

    Metro=OpenCSV(Path=PathMetro)
    MetroData={}
    for key in Metro.keys():
        stop= str(Metro[key]['StopCode'])
        MetroData[stop]=Metro[key]
    
    RailRData={}
    TramsData={}

    if ShowProcess: print(list(MetroData.keys()))
    if ShowProcess: print(list(BusesData.keys()))

    NodeDict=OpenDictionaryFile(Path=PathNodeList)


    TripData=GetTripData()
    StopTripData=GetStopiTrip()
    d=0
    # for key in StopTripData.keys():
    #     d+=1
    #     print(key,"-",type(key))
    #     if d==10: break
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




    for id,key in enumerate(NodeDict.keys()):
        Mainstop=str(key)
        print("\n\n\n#########################")
        print("MainStop",Mainstop,type)
        if ShowProcess: print(id,key)
        if ShowProcess: print(NodeDict[key])
        FiD=id+1
        Coord={'Lat':[],'Lon':[]}
        MetroStations={}
        RailRStations={}
        TramsStations={}
        BusesStations={}

        if NodeDict[key]['Type']=='Hub':
            if ShowProcess: print("Is  HUB")
            ListStopsForCoords=[]
            for stop in NodeDict[key]['Data']:

                print("Stop:",stop)
                if stop in MetroData.keys(): 
                    if ShowProcess: print("stop",stop)
                    if ShowProcess: print(MetroData[stop])
                    MetroStations[stop]=[]
                    Coord['Lat']=MetroData[stop]['stop_lat']
                    Coord['Lon']=MetroData[stop]['stop_lon']

                if stop in RailRData.keys(): 
                    if ShowProcess: print("stop",stop)
                    if ShowProcess: print(RailRData[stop])
                    RailRStations[stop]=[]
                    Coord['Lat']=RailRData[stop]['stop_lat']
                    Coord['Lon']=RailRData[stop]['stop_lon']
                if stop in TramsData.keys(): 
                    if ShowProcess: print("stop",stop)
                    if ShowProcess: print(TramsData[stop])
                    TramsStations[stop]=[]

                if stop in BusesData.keys(): 
                    if ShowProcess: print("stop",stop)
                    # if ShowProcess: print(BusesData[stop])
                    BusesStations[stop]=GetLine(dataStop=StopTripData,dataTrip=TripData,stop=stop)




        if ShowProcess: print("Coord",Coord)
        if ShowProcess: print("MetroStations",MetroStations)
        if ShowProcess: print("RailRStations",RailRStations)
        if ShowProcess: print("TramsStations",TramsStations)
        if ShowProcess: print("BusesStations",BusesStations)
        if ShowProcess: b=input('.................................')
 


if __name__=="__main__":
    PathTxtFile=r"E:\GitHub\CAMMM-Tool_1.3\SampleData\GIS_Data\NodeList.txt"
    PathToBuses=r"F:\OneDrive - Concordia University - Canada\RA-CAMMM\Gis_Data\BusesData.csv"
    PathToMetro=r"F:\OneDrive - Concordia University - Canada\RA-CAMMM\Gis_Data\MetroData.csv"
    Main(PathNodeList=PathTxtFile,PathBuses=PathToBuses,PathMetro=PathToMetro,ShowProcess=True)


    {'Data': ['65', '60290', '61654', '60292', '60807', '55639', '55650', '55641', '55640', '55890', '60293', '55901', '55945', '60289', '60288', '60295', '61798', '60383', '61323', '55829', '61819', '60296'], 'Type': 'Hub'}

    61819