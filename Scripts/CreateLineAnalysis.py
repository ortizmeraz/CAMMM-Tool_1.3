# This program is used to create the analysis of the concetions between the nodes in all of their connections


import json
import csv
from itertools import pairwise


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
        if ShowProcess: b=input('.................................')
    return NodeData


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
        if ShowProcess: b=input('.................................')
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
        if ShowProcess: b=input('.................................')
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





    print("GetRoute2TripData")
    # TripsByRoute={}
    RoutesWithTrips={}
    with open(Path,encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        headers = next(csv_reader, None)
        print(headers)
        if ShowProcess: b=input('.................................')
        for idx,row in enumerate(csv_reader):
            # if ShowProcess: print(idx,row)
            # if row[0] not in TripsByRoute.keys():
                # TripsByRoute[row[0]]=[]
            if row[0] not in RoutesWithTrips.keys():
                RouteTemp=RouteClass(Id=row[0])
                RoutesWithTrips[row[0]]=RouteTemp
            
            # TripsByRoute[row[0]].append({'trip_id':row[2],'trip_headsign':row[3],'direction_id':row[4]})
            RoutesWithTrips[row[0]].TripList.append(row[2])
            RoutesWithTrips[row[0]].Heading[row[2]]={'trip_headsign':row[3],'direction_id':row[4]}
            # if int(row[0])>6:
            #     if ShowProcess: print(headers)
            #     if ShowProcess: print(row)
            #     if ShowProcess: print(TripsByRoute[row[0]])
            #     if ShowProcess: print(row[0])
                # if ShowProcess: b=input('.................................')
            #if ShowProcess: b=input('.................................')
        if ShowProcess:
            for route in RoutesWithTrips:
                # print(route,RoutesWithTrips[route].TripList)
                print(route,RoutesWithTrips[route].Heading[RoutesWithTrips[route].TripList[-1]])
                print(route,RoutesWithTrips[route].Heading[RoutesWithTrips[route].TripList[-2]])
                b=input('.................................')
    return RoutesWithTrips

if __name__=="__main__":
    class RouteClass:
        def __init__(self, Id="", TripList=[],Heading={}):
            self.Id = Id
            self.TripList = TripList
            self.Heading=Heading

    csvPath=r"E:\Github\CAMMM-Web-Tool\Data\general.geojson"
    stopTimesPath=r"E:\Github\CAMMM-Tool_1.3\SampleData\GTFS DATA\gtfs_stm-220822-231022\stop_times.txt"
    routePath=r"E:\Github\CAMMM-Tool_1.3\SampleData\GTFS DATA\gtfs_stm-220822-231022\routes.txt"
    tripDataPath=r"E:\Github\CAMMM-Tool_1.3\SampleData\GTFS DATA\gtfs_stm-220822-231022\trips.txt"

    NodeData=GetNodeData(Path=csvPath)
    TripSeq=GetStopSequence(Path=stopTimesPath,ShowProcess=False)
    RouteSata=GetRouteData(Path=routePath,ShowProcess=False)
    TripRputeData=GetRoute2TripData(Path=tripDataPath,ShowProcess=False)