# This program is used to create the analysis of the concetions between the nodes in all of their connections


import json
import csv
from itertools import pairwise
from itertools import islice



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
    ### 
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
    ### 
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

    NodeData=GetNodeData(Path=csvPath)
    TripSeq=GetStopSequence(Path=stopTimesPath,ShowProcess=False)
    RouteData=GetRouteData(Path=routePath,ShowProcess=False)
    TripRouteData=GetRoute2TripData(Path=tripDataPath,ShowProcess=False)
    
    CleanTripData=CleanTrips(RouteData=RouteData,TripSeq=TripSeq,TripRouteData=TripRouteData,ShowProcess=False)
    SelectedRoutes=SelectionOfTrips(CleanTrips=CleanTripData,Criteria="Longest",ShowProcess=True)

    for route in SelectedRoutes.keys():
        print("Route:",route)
        for dir in SelectedRoutes[route]:
            print("\t:",dir,"\t",SelectedRoutes[route][dir])
        print()
             


