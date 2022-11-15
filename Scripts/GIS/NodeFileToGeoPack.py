
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

def Main(PathNodeList,PathBuses,PathMetro,ShowProcess:bool=False):
    ExitData={}

    Buses=OpenCSV(Path=PathBuses)
    BusesData={}
    # print(len(Buses.keys()))
    for key in Buses.keys():
        # print(key,Buses[key],"----")
        BusesData[int(Buses[key]['StopCode'])]=Buses[key]

    Metro=OpenCSV(Path=PathMetro)
    MetroData={}
    for key in Metro.keys():
        # print(key,Buses[key],"----")
        MetroData[int(Metro[key]['StopCode'])]=Metro[key]


    NodeDict=OpenDictionaryFile(Path=PathNodeList)

    # print(Buses.keys())
    # for key in Buses.keys():
    #     print(key,type(key))

                # Lat
                # Lon
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
        if ShowProcess: print(id,key)
        if ShowProcess: print(NodeDict[key])
        if ShowProcess: b=input('.................................')
        FiD=id+1
        Coord={'Lat':[],'lon':[]}
        MetroData={}
        BusData={}
        TramData={}
        RailData={}
        if NodeDict[key]['Type']=='Hub':
            Coord[]
        if int(key) in MetroData.keys():
            Coord
        # if NodeDict[key]['Type']=="Hub":
            # print("Hub")
            # print(NodeDict[key])
            # print("Type of NodeDict[key]['Data']",type(NodeDict[key]['Data']))
            # for stop in NodeDict[key]['Data']:
            #     if int(stop) in MetroData.keys():
            #         print("stop",stop,type(stop))
            #         # print(stop,MetroData[int(stop)]['location'])
            #         print(stop,MetroData[int(stop)]['stop_lat'],MetroData[int(stop)]['stop_lon'])
            #     if int(stop) in BusesData.keys():
            #         print("stop",stop,type(stop))
            #         print(stop,BusesData[int(stop)]['stop_lat'],BusesData[int(stop)]['stop_lon'])

        # else:
        #     print("Cluster")
        #     print(NodeDict[key])



if __name__=="__main__":
    PathTxtFile=r"E:\GitHub\CAMMM-Tool_1.3\SampleData\GIS_Data\NodeList.txt"
    PathToBuses=r"F:\OneDrive - Concordia University - Canada\RA-CAMMM\Gis_Data\BusesData.csv"
    PathToMetro=r"F:\OneDrive - Concordia University - Canada\RA-CAMMM\Gis_Data\MetroData.csv"
    Main(PathNodeList=PathTxtFile,PathBuses=PathToBuses,PathMetro=PathToMetro,ShowProcess=True)