# This program is used to create the analysis of the concetions between the nodes in all of their connections
# TODO
# - figure what the heck to do

import json
import csv
import ast
from itertools import pairwise
from itertools import islice

def ChckStp(stop:str,City:str="MTL")->str:

    if stop in ('9999111','9999112','9999114'):
        New='99'
    elif stop in ('9999495','9999492'):
        New='98'
    elif stop in ('9999055','9999052'):
        New='97'
    else: 
        New=stop
    return New

def CreateClusterLinks(Clusters:dict,TripData:dict,ShowProcess:bool=False)->dict:
    ### Description
    ### 
    # Variables 
    # - 
    SimpleLinks=[]
    ReverseDictionary={}
    ClusterLinks=[]
    for clust in Clusters.keys():
        L1=ast.literal_eval(Clusters[clust]["List of Stations"])
        L2=ast.literal_eval(Clusters[clust]["List of Stops"]) 
        L3=L1+L2
        for stop in L3:
            ReverseDictionary[stop]=clust
        # print(clust,Clusters[clust]["List of Stations"],Clusters[clust]["List of Stops"])
        # b=input('.................................')
    for trip in TripData.keys():
        if ShowProcess: print(trip,)
        # if ShowProcess: print("\t",type(TripData[trip]["0"]))
        # if ShowProcess: print("\t",TripData[trip]["1"])
        for a,b in pairwise(TripData[trip]["0"]):
            SimpleLinks.append([ChckStp(a[0]),ChckStp(b[0])])
        #     if ShowProcess: print(a,b)
        #     if ShowProcess: print("A",Clusters[ChckStp(a[0])]["List of Stops"])
        #     if ShowProcess: print("B",Clusters[ChckStp(b[0])]["List of Stops"])
        # if ShowProcess: b=input('.................................')
    print("SimpleLinks len:",len(SimpleLinks))
    # for link in SimpleLinks[:100]:
    #     print(link)
    #     print("->",Clusters[link[0]]["List of Stops"])
    #     print("<-",Clusters[link[1]]["List of Stops"])
    # for clust in Clusters.keys():
    #     print(clust) 
    #     L1=ast.literal_eval(Clusters[clust]["List of Stations"])
    #     L2=ast.literal_eval(Clusters[clust]["List of Stops"])
    #     Temporary=L1+L2
    #     print(Temporary,len(Temporary))
    #     for stop in Temporary:
    #         for link in SimpleLinks: 
    #             if stop in link:
    #                 print(link)
    #                 CLusterLink=[link[0]]
    #                 b=input('.................................')
    Check=[]
    for link in SimpleLinks:
        if link[0] in ReverseDictionary.keys() and link[1] in ReverseDictionary.keys():
            NewLink=[ReverseDictionary[link[0]],ReverseDictionary[link[1]]]
            if NewLink not in ClusterLinks:
                ClusterLinks.append(NewLink)
                print(NewLink)
        else:
            if link[0] not in ReverseDictionary.keys():
                if link[0] not in Check: Check.append(link[0])
            if link[1] not in ReverseDictionary.keys():
                if link[1] not in Check: Check.append(link[1])
    print("Check",Check,len(Check))
    print("Lenght of ClusterLinks:",len(ClusterLinks))
    return None



def BuildFeature(Route:str,Dir:str,Coordinates:list,ShowProcess:bool=False)->str:
    ### Description
    ### This function return a section of json file with the coordinates for each route-direction
    ### return a string
    feature='''
    {
    "type": "Feature",
    "properties": {
    "Route": "'''+Route+'''",
    "Direction": "'''+Dir+'''"
    },
    "geometry": {
    "coordinates": 
    [
    '''
    for coord in Coordinates:
        feature+='''   ['''+coord['lon']+''','''+coord['lat']+''']'''
        if coord !=Coordinates[-1]:
            feature+=''','''
    feature+='''],
        "type": "LineString"
      }
    }'''
    return feature

def WriteJSON(Routes,Coords,WritePath:str,ShowProcess:bool=False)->None:
    ### Description
    ### 
    # Variables 
    # - 
    ListRoutes=list(Routes.keys())
    Text='''
    {
    "features": ['''
    for route in ListRoutes:
        if ShowProcess: print("Route:",route)
        for dir in Routes[route].keys():
            Seq=Routes[route][dir]
            if ShowProcess: print("Dir",dir,"|",end="")
            if len(Seq)>0:
                ListStops=[]
                for stop in Seq:
                    if ShowProcess: print("-",stop[0],"-",end="\t")
                    if ShowProcess: print(Coords[stop[0]],end="\t")
                    ListStops.append(Coords[stop[0]])
            else:
                print("NA",end="\t")
            Feature=BuildFeature(Route=route,Dir=dir,Coordinates=ListStops)
            Text+=Feature
            if dir=="0":
                Text+=''','''
            if ShowProcess: print(Feature)
            if ShowProcess: print()
        if route !=ListRoutes[-1]:
            Text+=''','''
        if ShowProcess: print("\n-------------------\n")
    Text+='''
    ],
    "type": "FeatureCollection"
    }'''
    print(Text)
    f = open(WritePath, 'w')
    f.write(Text)
    f.close()
    return None

def GetCoordinates(Path:str,Routes:dict,ShowProcess:bool=False)->dict:
    ### Description
    ### Get the coordinates of the stops
    # Variables 
    # - 
    Coords={}
    if ShowProcess: print(GetCoordinates)
    with open(Path,encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        headers = next(csv_reader, None)
        if ShowProcess: print(headers)
        # if ShowProcess: b=input('.................................')
        for idx,row in enumerate(csv_reader):
            # print(idx,row)
            if row[0]==row[1]:
                if ShowProcess: print("Same")
                Stop=row[1]
                Latt=row[3]
                Lonn=row[4]
                Coords[Stop]={"lat":Latt,"lon":Lonn}
                if ShowProcess: print(Stop,Coords[Stop])
                # if ShowProcess: print(headers[1],row[1],end="\t")
                # if ShowProcess: print(headers[3],row[3],end="\t")
                # if ShowProcess: print(headers[4],row[4],end="\n")
            else:
                if ShowProcess: print("Different",row[0],row[1])
                if ShowProcess: print(row[0].isdigit())
                if row[0].isdigit():
                    Stop=row[0]
                    Latt=row[3]
                    Lonn=row[4]
                    Coords[Stop]={"lat":Latt,"lon":Lonn}
                    if ShowProcess: print(Stop,Coords[Stop])
                    # if ShowProcess: b=input('.................................')

    return Coords

def GetNodeData(Path:str,ShowProcess:bool=False)->dict:
    ### Description
    ### This function simplifies the JSON file to only contain the Id, Name, Metro, RAil, Tram, Bus data
    ### Returns a dictionary
    # Variables 
    # - Path is a string with the JSON File
    NodeData={}
    file=open(Path,"r")
    FileText=""
    for line in file.readlines():
        FileText+=line
    if ShowProcess: print(type(FileText))
    NodeDataRaw=json.loads(FileText)
    NodeDataRaw=NodeDataRaw['features']
    for node in NodeDataRaw:
        # if ShowProcess: print(node,"/n")
        # node['properties'][]
        NodeData[node['properties']['Id']]={'Name':node['properties']['Name'],'MetroData':node['properties']['MetroData'],'RailData':node['properties']['RailData'], 'TramData':node['properties'][ 'TramData'],'BusData':node['properties']['BusData']}
        # for elem in node:
        #     if ShowProcess: print(elem,node[elem])
        if ShowProcess: print(node['properties']['Id'],NodeData[node['properties']['Id']])
        if ShowProcess: b=input('GetNodeData .................................')
    return NodeData

def GetClusterData(Path,ShowProcess:bool=False)->dict:
    ### Description
    ### This reads the file containing the clusters and the hubs 
    # Variables 
    # - var contains the exit data for the cluster data 
    Exitdata={}
    with open(Path,encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        headers = next(csv_reader, None)
        if ShowProcess: print(headers)
        if ShowProcess: b=input('.................................')
        for idx,row in enumerate(csv_reader):
            if ShowProcess: print(idx,row)
            Exitdata[row[0]]={}
            for idx,element in enumerate(row):
                Exitdata[row[0]][headers[idx]]=element
                if ShowProcess: print(idx,headers[idx],element)
    return Exitdata

def GetStopSequence(Path:str,ShowProcess:bool=False):
    ### Description
    ### This extracts the sequence of trips frpm GTFS
    # Variables 
    # - Path for the stop_times.txt
    TripDataSeq={}
    with open(Path,encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        headers = next(csv_reader, None)
        if ShowProcess: print(headers)
        if ShowProcess: b=input('GetStopSequence .................................')
        for idx,row in enumerate(csv_reader):
            if row[0] not in TripDataSeq.keys():
                TripDataSeq[row[0]]=[]
                if row[-1]=='1':
                    TripDataSeq[row[0]].append([])
            TripDataSeq[row[0]][-1].append([row[-2],row[-1]])
    if ShowProcess:
        for id in TripDataSeq:
            print(id,len(TripDataSeq[id]))
            #if len(TripDataSeq[id]) > 1:
            print("\t",TripDataSeq[id])
            print("\n")
                #b=input('.................................')
            
        #     print(idx,row)
    return TripDataSeq

def GetRouteData(Path:str,ShowProcess:bool=False)->dict:
    ### Description
    ### Extract the Route data from GTFS 
    # Variables 
    # - Path for the stop_times.txt
    print(GetRouteData)
    RouteData={}
    with open(Path,encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        headers = next(csv_reader, None)
        print(headers)
        if ShowProcess: b=input('GetRouteData .................................')
        for idx,row in enumerate(csv_reader):
            if ShowProcess: print(idx,row)
            #if ShowProcess: b=input('.................................')
            RouteData[row[0]]={'route_short_name':row[2],'name':row[3],'route_type':row[4],'route_color':row[6]}
        if ShowProcess:
            for route in RouteData:
                print(route,RouteData[route])
    return RouteData

def GetRoute2TripData(Path:str,ShowProcess:bool=False)->dict:
    ### Description
    ### Extract the Route data from GTFS 
    # Variables 
    # - Path for the trips.txt
    if ShowProcess: print("####################################################")
    print("\tGetRoute2TripData")
    if ShowProcess: print("####################################################")
    # TripsByRoute={}
    RoutesWithTrips={}
    with open(Path,encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        headers = next(csv_reader, None)
        print(headers)
        if ShowProcess: b=input('GetRoute2TripData -1-.................................')
        for idx,row in enumerate(csv_reader):
            # if ShowProcess: print(idx,row)
            # if ShowProcess: b=input('.................................')
            route=row[0]
            tripp=row[2]
            Namee=row[3]
            Direc=row[4]
            if route not in RoutesWithTrips.keys():
                RoutesWithTrips[route]={"Id":route,"TripList":{"0":[],"1":[]},"Heading":Direc}
            RoutesWithTrips[route]["TripList"][Direc].append(tripp)

    return RoutesWithTrips

def ReturnLongest(List,ShowProcess:bool=False)->dict:
    ### Description
    ### 
    # Variables 
    # - 
    ExitList=[]
    for element in List:
        if len(element[0])>len(ExitList):ExitList=element[0]
    return ExitList

def CleanTrips(RouteData:dict,TripSeq:dict,TripRouteData:dict,ShowProcess:bool=False)->dict:
    ### Description
    ### This function checks the total of trip sequences and then retuerns the unique ones per direction per route 
    # Variables 
    # - RouteData dictionary from GetRouteData
    # - TripSeq dictionary from GetStopSequence
    # - TripRouteData dictionary from GetRoute2TripData

    CleanTripData={}
    for route in RouteData:
        CleanTripData[route]={"0":[],"1":[]}
        if ShowProcess: print("Route:",route)
        # if ShowProcess: print("\t",TripRouteData[route].TripList)
        # if ShowProcess: print("\t")
        for dir in ["0","1"]:
            for trip in TripRouteData[route]["TripList"][dir]:
                if ShowProcess: print("Direccion",dir)
                if ShowProcess: print("Trip",trip)
                if ShowProcess: print(TripSeq[trip])
                # if ShowProcess: b=input('.................................')
                if TripSeq[trip] not in CleanTripData[route][dir]:
                    CleanTripData[route][dir].append(TripSeq[trip])
    return CleanTripData

def SelectionOfTrips(CleanTrips,Criteria,ShowProcess:bool=False)->dict:
    ### Description
    ### In case of multiple trip sequences per direction, this function returns the sequence that fits the desired condiotions
    ### so far only the longest sequence has coding
    # Variables 
    # - 
    ExportRoutes={}
    if Criteria=="Longest":
        print("Longest")
        for route in CleanTrips:
            if ShowProcess: print("\n\nRoute",route)
            ExportRoutes[route]={"0":[],"1":[]}
            for dir in ["0","1"]:
                if ShowProcess: print("\tDireccion:",dir)
                if ShowProcess: print("\t\t",len(CleanTripData[route][dir]))
                if len(CleanTripData[route][dir])>1:
                    ExportRoutes[route][dir]=ReturnLongest(List=CleanTripData[route][dir])
                else:
                    if ShowProcess: print("#######################")
                    if ShowProcess: print(CleanTripData[route][dir])
                    if ShowProcess: print(len(CleanTripData[route][dir]))
                    if len(CleanTripData[route][dir])!=0:
                        ExportRoutes[route][dir]=CleanTripData[route][dir][0][0]
                    else:
                        ExportRoutes[route][dir]=[]
                # ReturnLongest(List=CleanTripData[route][dir])
                for trip in CleanTripData[route][dir]:
                    # if ShowProcess: print("\t-\tTrip",trip)
                    if ShowProcess: print("Trip Lenght",len(trip[0]))
                if ShowProcess: print(ExportRoutes[route][dir])
                if ShowProcess: print("ExportRoutes",len(ExportRoutes[route][dir]))
            # if ShowProcess: b=input('.................................')
    return ExportRoutes


if __name__=="__main__":

    csvPath=r"E:\Github\CAMMM-Web-Tool\Data\general.geojson"
    stopTimesPath=r"E:\Github\CAMMM-Tool_1.3\SampleData\GTFS DATA\gtfs_stm-220822-231022\stop_times.txt"
    routePath=r"E:\Github\CAMMM-Tool_1.3\SampleData\GTFS DATA\gtfs_stm-220822-231022\routes.txt"
    tripDataPath=r"E:\Github\CAMMM-Tool_1.3\SampleData\GTFS DATA\gtfs_stm-220822-231022\trips.txt"
    stopDataPath=r"E:\Github\CAMMM-Tool_1.3\SampleData\GTFS DATA\gtfs_stm-220822-231022\stops.txt"
    clusterPath=r"E:\Github\CAMMM-Tool_1.3\NodesV2.csv"

    ExitPathSImple=r"E:\Github\CAMMM-Tool_1.3\Output\Lines.geojson"

    NodeData=GetNodeData(Path=csvPath)
    TripSeq=GetStopSequence(Path=stopTimesPath,ShowProcess=False)
    RouteData=GetRouteData(Path=routePath,ShowProcess=False)
    TripRouteData=GetRoute2TripData(Path=tripDataPath,ShowProcess=False)
    CleanTripData=CleanTrips(RouteData=RouteData,TripSeq=TripSeq,TripRouteData=TripRouteData,ShowProcess=False)
    SelectedRoutes=SelectionOfTrips(CleanTrips=CleanTripData,Criteria="Longest",ShowProcess=False)
    Coordinates=GetCoordinates(Path=stopDataPath,Routes=SelectedRoutes,ShowProcess=False)


    ClusterData=GetClusterData(Path=clusterPath)

    CreateClusterLinks(Clusters=ClusterData,TripData=SelectedRoutes,ShowProcess=True)


    # WriteJSON(Routes=SelectedRoutes,Coords=Coordinates,WritePath=ExitPathSImple,ShowProcess=True)


             


