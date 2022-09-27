import os
import networkx as nx
import numpy as np
import pandas
# import pylab
from colour import Color
import shapefile
from pyproj import Proj, transform
import jenkspy
from epsg_ident import EpsgIdent
import pyproj
import zipfile

from FeatureOperations import AgregateTransitNetwork
from FeatureOperations import CalculateVecinityBusStops

from GuiSecondary import select_file
from GuiSecondary import select_folder

import tkinter
from tkinter import ttk 
from tkinter.filedialog import asksaveasfile 

from datetime import datetime


from Databases import UpdatePath
from Databases import RearPaths
from Tools import ProgressBarColor
from Tools import ReadGeoJson

import matplotlib.pyplot as plt

import Calculations



def ConvertToUTM(lat,lon):
    import warnings
    warnings.filterwarnings("ignore")
    Zone=int((float(lon)/6)+31)
    Val_EPSG="epsg:326"+str(Zone)
    proj_wgs84 = pyproj.Proj(init="epsg:4326")
    proj_utm = pyproj.Proj(init=str(Val_EPSG))
    x, y = pyproj.transform(proj_wgs84, proj_utm, lon, lat)
    return x,y

def NetworkLineAgregator(DataStops,DataTrips,DataRoutes,DataSequence,CityId):
    # print("DataStops:",type(DataStops),len(DataStops))
    # print("EdgeData:",type(EdgeData),len(EdgeData))
    # b=input()
    Error=0
    G = nx.DiGraph()
    List_Nodes_Key=list(DataStops.keys())

    SationsByRoutes={}
    LKdataRoutes=list(DataRoutes.keys())

    # print("DataSequence",type(DataSequence))
    for i,route in enumerate(DataRoutes.keys()):
        ProgressBarColor(current=i+1,total=len(DataRoutes.keys()),title=" Route Analysis")
        # print("#######################################")
        # print(route)
        SationsByRoutes[route]=[]
        RouteTrips=list(DataTrips[route].keys())
        for trips in RouteTrips:
            if trips in DataSequence:
                TempStops=[]
                for Sequence in DataSequence[trips].keys():
                    # print(Sequence, DataSequence[trips][Sequence])
                    TempStops.append(DataSequence[trips][Sequence]['stop_id'])
            # print("*****************************************************************",route)
            if len(TempStops)>len(SationsByRoutes[route]):
                SationsByRoutes[route]=TempStops
                # print("CHANGE!!!!!")
            # for i,x in enumerate(SationsByRoutes[route]):
            #     print(i,x)
            # b=input('.................................')
    
    PathToFolder=select_folder(Title=CityId)
    # print("·······························")
    # print(PathToFolder)
    # print("·······························")

    ListFiles = os.listdir(PathToFolder)
    TransitSystems={}
    ExitHeaderse=[]
    NotUsedStops=[]
    HeaderPrint=['stop','route']
    for file in ListFiles:
        # print(PathToFolder,file)
        Path=PathToFolder+'/'+file
        Type=list(list(file.split("_"))[1].split("."))[0]
        print(Type)
        # b=input('.................................')
        N=ReadGeoJson(gjPath=Path)
        for nn in N:
            N[nn]['Type']=Type
            for k in N[nn].keys():
                if k not in ExitHeaderse: ExitHeaderse.append(k) 
        TransitSystems.update(N)
    HeaderPrint+=ExitHeaderse
    for route in SationsByRoutes.keys():
        for stop in SationsByRoutes[route]:
            StoreList=[stop,route] 
            for key in ExitHeaderse:
                if stop in TransitSystems.keys():
                    if key in TransitSystems[stop]: 
                        if key not in ['stop','route']:   
                            StoreList.append(TransitSystems[stop][key])
                    else:
                        StoreList.append("NA")
                else:
                    Error+=1
                    NotUsedStops.append(str(stop)+"-"+str(route))
                    # b=input('...............ERRRORRRR..................')

    #         print(StoreList)
    # print(HeaderPrint)
    print(NotUsedStops)
    NotUsedStops2=list(set(NotUsedStops))
    print(NotUsedStops2,len(NotUsedStops2))
    print("Error",Error)
    b=input('.................................')







    # for i,x in enumerate(SationsByRoutes.keys()):
    #     print(i,x)
    #     for y in SationsByRoutes[x]:
    #         print("\t",y)








def GtfsToWeightedNetwork(DataStops=dict,DataSequence=dict):
       
    # print("DataStops:",type(DataStops),len(DataStops))
    # print("EdgeData:",type(EdgeData),len(EdgeData))
    # b=input()
    G = nx.DiGraph()
    List_Nodes_Key=list(DataStops.keys())

    SationsByRoutes={}
    LKdataRoutes=list(DataRoutes.keys())

    # print("DataSequence",type(DataSequence))
    for route in DataRoutes.keys():
        # print("#######################################")
        # print(route)
        SationsByRoutes[route]=[]
        RouteTrips=list(DataTrips[route].keys())
        for trips in RouteTrips:
            if trips in DataSequence:
                TempStops=[]
                for Sequence in DataSequence[trips].keys():
                    # print(Sequence, DataSequence[trips][Sequence])
                    # Stops.append(DataSequence[trips][Sequence]['stop_id'])
                    TempStops.append(DataSequence[trips][Sequence]['stop_id'])
            # print("*****************************************************************",route)
            if len(TempStops)>len(SationsByRoutes[route]):
                SationsByRoutes[route]=TempStops
                print("CHANGE!!!!!")
            for i,x in enumerate(SationsByRoutes[route]):
                print(i,x)
            # b=input('.................................')

    List_Nodes=[]
    EdgeList=[]
    NodePrintProp={'Pos':{}}
    for LineKey in EdgeData.keys():
        # print("LineKey",LineKey)
        for edge in EdgeData[LineKey]['0']:
            if edge[0] not in List_Nodes: List_Nodes.append(edge[0])
            if edge[1] not in List_Nodes: List_Nodes.append(edge[1])
            EdgeList.append(edge)
        for edge in EdgeData[LineKey]['1']:
            if edge[0] not in List_Nodes: List_Nodes.append(edge[0])
            if edge[1] not in List_Nodes: List_Nodes.append(edge[1])
            EdgeList.append(edge)
            # print("Edge",edge,)
        # print("\n")
    G.add_edges_from(EdgeList)

    # print("List_Nodes",len(List_Nodes),List_Nodes)
    # print(type(DataStops),DataStops.keys(),"DataStops")
    # if '53051' in List_Nodes:
    #     print("Hello-----------------------")
    for node in List_Nodes:
        # print(node,DataStops[node].keys())
        # b=input('Press Enter ...')
        x,y=ConvertToUTM(lat=float(DataStops[node]['stop_lat']),lon=float(DataStops[node]['stop_lon']))
        if "stop_id" in DataStops[node].keys():
            stop_id=DataStops[node]['stop_id']
        else: 
            stop_id=""
        if "stop_code" in DataStops[node].keys():
            stop_code=DataStops[node]['stop_code']
        else: 
            stop_code=""
        if "stop_name" in DataStops[node].keys():
            stop_name=DataStops[node]['stop_name']
        else: 
            stop_name=""
        if "stop_desc" in DataStops[node].keys():
            stop_desc=DataStops[node]['stop_desc']
        else: 
            stop_desc=""
        if "stop_lat" in DataStops[node].keys():
            stop_lat=DataStops[node]['stop_lat']
        else: 
            stop_lat=""
        if "stop_lon" in DataStops[node].keys():
            stop_lon=DataStops[node]['stop_lon']
        else: 
            stop_id=""
        if "zone_id" in DataStops[node].keys():
            zone_id=DataStops[node]['zone_id']
        else: 
            zone_id=""
        if "stop_url" in DataStops[node].keys():
            stop_url=DataStops[node]['stop_url']
        else: 
            stop_url=""
        if "location_type" in DataStops[node].keys():
            location_type=DataStops[node]['location_type']
        else: 
            location_type=""
        if "parent_station" in DataStops[node].keys():
            parent_station=DataStops[node]['parent_station']
        else: 
            parent_station=""
        if "stop_timezone" in DataStops[node].keys():
            stop_timezone=DataStops[node]['stop_timezone']
        else: 
            stop_timezone=""
        if "wheelchair_boarding" in DataStops[node].keys():
            wheelchair_boarding=DataStops[node]['wheelchair_boarding']
        else: 
            wheelchair_boarding=""
        if "level_id" in DataStops[node].keys():
            level_id=DataStops[node]['level_id']
        else: 
            level_id=""
        if "platform_code" in DataStops[node].keys():
            platform_code=DataStops[node]['platform_code']
        else: 
            platform_code=""
        # G.add_node(node,location=(x,y),pos=(float(DataStops[node]['stop_lat']),float(DataStops[node]['stop_lon'])),stop_id =DataStops[node]['stop_id'],stop_name =DataStops[node]['stop_name'],stop_code =DataStops[node]['stop_code'],location_type =DataStops[node]['location_type'],parent_station =DataStops[node]['parent_station'],wheelchair_boarding =DataStops[node]['wheelchair_boarding'],stop_direction =DataStops[node]['stop_direction'])
        G.add_node(node,location=(x,y),pos=(float(DataStops[node]['stop_lat']),float(DataStops[node]['stop_lon'])),stop_id =stop_id,stop_name =stop_name,stop_code =stop_code,stop_desc=stop_desc,stop_lat=stop_lat,stop_lon=stop_lon,zone_id=zone_id,stop_url=stop_url,location_type=location_type,parent_station=parent_station,stop_timezone=stop_timezone,wheelchair_boarding=wheelchair_boarding,level_id=level_id,platform_code=platform_code)
        NodePrintProp['Pos'][node]=(x,y)
    # print("List_Nodes_Key",len(List_Nodes_Key))
    # print("List_Nodes",len(List_Nodes))
    # NetWorkToGeoJson(G=G,NetworkIndex=NetworkIndex)
    # b=input()
    # nx.draw_networkx_nodes(G,pos=NodePrintProp['Pos'],node_size=50)
    # nx.draw_networkx_edges(G,pos=NodePrintProp['Pos'])
    # nx.draw(G)
    # plt.show()
    NodeList=[]
    # for i in list(G.nodes):
    #     print(i)
    #     if i not in NodeList:
    #         NodeList.append(i)
    #     else:
    #         print("#################################################################################################\n"*10)
    # print("Number of Stops in the network ",len(list(G.nodes)))
    # return len(list(G.nodes))
    return G



def GtfsToNetwork(EdgeData,DataStops,DataRoutes,DataSequence,DataTrips,NetworkIndex):
    # print("DataStops:",type(DataStops),len(DataStops))
    # print("EdgeData:",type(EdgeData),len(EdgeData))
    # b=input()
    G = nx.DiGraph()
    List_Nodes_Key=list(DataStops.keys())

    SationsByRoutes={}
    # LKdataRoutes=list(DataRoutes.keys())   #### 

    print("DataSequence",type(DataSequence))
    for route in DataRoutes.keys():
        print("#######################################")
        print(route)
        SationsByRoutes[route]=[]
        RouteTrips=list(DataTrips[route].keys())
        for trips in RouteTrips:
            if trips in DataSequence:
                TempStops=[]
                for Sequence in DataSequence[trips].keys():
                    print(Sequence, DataSequence[trips][Sequence])
                    # Stops.append(DataSequence[trips][Sequence]['stop_id'])
                    TempStops.append(DataSequence[trips][Sequence]['stop_id'])
                    print("'arrival_time'",DataSequence[trips][Sequence]['arrival_time'],type(DataSequence[trips][Sequence]['arrival_time']))
                    print("'departure_time'",DataSequence[trips][Sequence]['departure_time'])
                    # StrTimeDelts(str1=DataSequence[trips][Sequence]['arrival_time']),str2)
                    print()
            print("*****************************************************************",route)
            if len(TempStops)>len(SationsByRoutes[route]):
                SationsByRoutes[route]=TempStops
                print("CHANGE!!!!!")
            for i,x in enumerate(SationsByRoutes[route]):
                print(i,x)
            b=input('............DataSequence.....................')

    List_Nodes=[]
    EdgeList=[]
    NodePrintProp={'Pos':{}}
    for LineKey in EdgeData.keys():
        # print("LineKey",LineKey)
        for edge in EdgeData[LineKey]['0']:
            if edge[0] not in List_Nodes: List_Nodes.append(edge[0])
            if edge[1] not in List_Nodes: List_Nodes.append(edge[1])
            EdgeList.append(edge)
        for edge in EdgeData[LineKey]['1']:
            if edge[0] not in List_Nodes: List_Nodes.append(edge[0])
            if edge[1] not in List_Nodes: List_Nodes.append(edge[1])
            EdgeList.append(edge)
            # print("Edge",edge,)
        # print("\n")
    G.add_edges_from(EdgeList)

    # print("List_Nodes",len(List_Nodes),List_Nodes)
    # print(type(DataStops),DataStops.keys(),"DataStops")
    # if '53051' in List_Nodes:
    #     print("Hello-----------------------")
    for node in List_Nodes:
        # print(node,DataStops[node].keys())
        # b=input('Press Enter ...')
        x,y=ConvertToUTM(lat=float(DataStops[node]['stop_lat']),lon=float(DataStops[node]['stop_lon']))
        if "stop_id" in DataStops[node].keys():
            stop_id=DataStops[node]['stop_id']
        else: 
            stop_id=""
        if "stop_code" in DataStops[node].keys():
            stop_code=DataStops[node]['stop_code']
        else: 
            stop_code=""
        if "stop_name" in DataStops[node].keys():
            stop_name=DataStops[node]['stop_name']
        else: 
            stop_name=""
        if "stop_desc" in DataStops[node].keys():
            stop_desc=DataStops[node]['stop_desc']
        else: 
            stop_desc=""
        if "stop_lat" in DataStops[node].keys():
            stop_lat=DataStops[node]['stop_lat']
        else: 
            stop_lat=""
        if "stop_lon" in DataStops[node].keys():
            stop_lon=DataStops[node]['stop_lon']
        else: 
            stop_id=""
        if "zone_id" in DataStops[node].keys():
            zone_id=DataStops[node]['zone_id']
        else: 
            zone_id=""
        if "stop_url" in DataStops[node].keys():
            stop_url=DataStops[node]['stop_url']
        else: 
            stop_url=""
        if "location_type" in DataStops[node].keys():
            location_type=DataStops[node]['location_type']
        else: 
            location_type=""
        if "parent_station" in DataStops[node].keys():
            parent_station=DataStops[node]['parent_station']
        else: 
            parent_station=""
        if "stop_timezone" in DataStops[node].keys():
            stop_timezone=DataStops[node]['stop_timezone']
        else: 
            stop_timezone=""
        if "wheelchair_boarding" in DataStops[node].keys():
            wheelchair_boarding=DataStops[node]['wheelchair_boarding']
        else: 
            wheelchair_boarding=""
        if "level_id" in DataStops[node].keys():
            level_id=DataStops[node]['level_id']
        else: 
            level_id=""
        if "platform_code" in DataStops[node].keys():
            platform_code=DataStops[node]['platform_code']
        else: 
            platform_code=""
        # G.add_node(node,location=(x,y),pos=(float(DataStops[node]['stop_lat']),float(DataStops[node]['stop_lon'])),stop_id =DataStops[node]['stop_id'],stop_name =DataStops[node]['stop_name'],stop_code =DataStops[node]['stop_code'],location_type =DataStops[node]['location_type'],parent_station =DataStops[node]['parent_station'],wheelchair_boarding =DataStops[node]['wheelchair_boarding'],stop_direction =DataStops[node]['stop_direction'])
        G.add_node(node,location=(x,y),pos=(float(DataStops[node]['stop_lat']),float(DataStops[node]['stop_lon'])),stop_id =stop_id,stop_name =stop_name,stop_code =stop_code,stop_desc=stop_desc,stop_lat=stop_lat,stop_lon=stop_lon,zone_id=zone_id,stop_url=stop_url,location_type=location_type,parent_station=parent_station,stop_timezone=stop_timezone,wheelchair_boarding=wheelchair_boarding,level_id=level_id,platform_code=platform_code)
        NodePrintProp['Pos'][node]=(x,y)
    # print("List_Nodes_Key",len(List_Nodes_Key))
    # print("List_Nodes",len(List_Nodes))
    # NetWorkToGeoJson(G=G,NetworkIndex=NetworkIndex)
    # b=input()
    # nx.draw_networkx_nodes(G,pos=NodePrintProp['Pos'],node_size=50)
    # nx.draw_networkx_edges(G,pos=NodePrintProp['Pos'])
    # nx.draw(G)
    # plt.show()
    NodeList=[]
    # for i in list(G.nodes):
    #     print(i)
    #     if i not in NodeList:
    #         NodeList.append(i)
    #     else:
    #         print("#################################################################################################\n"*10)
    # print("Number of Stops in the network ",len(list(G.nodes)))
    # return len(list(G.nodes))
    return G




def readShpNetWork(Shapefile,Fileds):

    LineElements={}
    EdgeCollection=[]
    NodeCollection=[]
    EdgeNames={}
    EdgeLine={}
    NodeProperties={}
    EdgeProperties={}
    NameDict={}
    NodeLine={}
    NodePos={}

    PL1=Shapefile.split("/")
    # if len(PL1)==1:PL1=Shapefile.split("\\")
    # print(PL1)
    FileName=PL1[-1].split(".")[0]
    # print(FileName)
    # b=input()
    sf = shapefile.Reader(Shapefile)
    Shapes=sf.shapes()
    Features=sf.shapeRecords()
    Records = sf.records()
    NameFields = sf.fields
    print("Fileds",Fileds)
    # b=input()
    # for i,f in enumerate(NameFields):
    #     print(i,f)
    for feat in Features:
        record=list(feat.record)
        # print("record",record,type(record))
        # for i,r in enumerate(record):
            # print(r)
        # b=input()

        # for idx,key in enumerate(Fileds.keys()):
        #     FieldIndex=Fileds[key][1]
        #     print(idx,"RecordIndex",FieldIndex, Fileds[key][0],record[FieldIndex])
        LineElements['StartCode']=record[Fileds['StartCode'][1]]
        LineElements['EndCode']=record[Fileds['EndCode'][1]]
        LineElements['Line']=record[Fileds['Line'][1]]
        LineElements['StartName']=record[Fileds['StartName'][1]]
        LineElements['EndName']=record[Fileds['EndName'][1]]
            # print("FieldIndex",FieldIndex)
            # LineElements[key]=record[FieldIndex]
            # print("\t",key, LineElements[key] )


        # print("record[Fileds['StartCode'][1]]",Fileds['StartCode'][1],record[Fileds['StartCode'][1]])
        # print("record[Fileds['EndCode'][1]]",Fileds['EndCode'][1],record[Fileds['EndCode'][1]])
        # print("record[Fileds['Line'][1]]",Fileds['Line'][1],record[Fileds['Line'][1]])
        # print("record[Fileds['StartCode'][1]]",Fileds['StartCode'][1],record[Fileds['StartCode'][1]])
        # print("record[Fileds['StartCode'][1]]",Fileds['StartCode'][1],record[Fileds['StartCode'][1]])

        # print("\n"*3)




        # print('StartCode',LineElements['StartCode'],'EndCode',LineElements['EndCode'],'Line',LineElements['Line'],'StartName',LineElements['StartName'],'EndName',LineElements['EndName'])
        # b=input()
        # Section that read the Nodes
        ################################################################################################
        # if LineElements['StartCode'] ==0 or LineElements['EndCode']==0:
            # print("ODD",LineElements['StartCode'],LineElements['EndCode'] )
            # b=input()

        if LineElements['StartCode'] not in NodeCollection:
            NodeCollection.append(LineElements['StartCode'])

        if LineElements['EndCode'] not in NodeCollection:
            NodeCollection.append(LineElements['EndCode'])
        # Section that read the attribtes for the Nodes
        #########################################################
        if LineElements['StartCode'] not in NameDict.keys():
            NameDict[LineElements['StartCode']]=LineElements['StartName']
        if LineElements['EndCode'] not in NameDict.keys():
            NameDict[LineElements['EndCode']]=LineElements['EndName']
        # print(NameDict.keys())

        if LineElements['StartCode'] not in NodePos.keys():
            NodePos[LineElements['StartCode']]=feat.shape.points[0]
        if LineElements['EndCode'] not in NodePos.keys():
            # print("new key")
            NodePos[LineElements['EndCode']]=feat.shape.points[-1]
        # print(NodePos.keys())

        if LineElements['StartCode'] not in NodeLine.keys():
            NodeLine[LineElements['StartCode']]=[]
            NodeLine[LineElements['StartCode']].append(LineElements['Line'])
        else:
            if LineElements['Line'] not in NodeLine[LineElements['StartCode']]:
                NodeLine[LineElements['StartCode']].append(LineElements['Line'])

        if LineElements['EndCode'] not in NodeLine.keys():
            NodeLine[LineElements['EndCode']]=[]
            NodeLine[LineElements['EndCode']].append(LineElements['Line'])
        else:
            if LineElements['Line'] not in NodeLine[LineElements['EndCode']]:
                NodeLine[LineElements['EndCode']].append(LineElements['Line'])

        # Section that reads the Edges
        ################################################################################################
        Edge=(LineElements['StartCode'],LineElements['EndCode'])
        EdgeCollection.append(Edge)

        # Section that read the attributes of the edges
        #########################################################
        EdgeLine[Edge]=LineElements['Line']
    ################################################################################################
    # for Edge in EdgeCollection:
    #     print(Edge)

    # print("###################################################\n"*2)
    # print("NodeCollection",len(NodeCollection))
    # print("EdgeCollection",len(EdgeCollection))
    # print("NameDict",len(NameDict.keys()))

    EdgeProperties={'Line':EdgeLine}
    NodeProperties={'Line':NodeLine,'Name':NameDict,'Pos':NodePos,'FileName':FileName}

    # for Node in NodeCollection:
    #     print("Node",Node)
    #     print("\t",NameDict[Node])
    #     print("\t",NodePos[Node])
    #     print("\t",NodeLine[Node])
    #     print("\t",NodeProperties['Name'][Node])
    #     print("\t",NodeProperties['Line'][Node])
    #     print("\t",NodeProperties['Pos'][Node])

    return EdgeCollection,EdgeProperties,NodeCollection,NodeProperties


def readShpNetWorkForSimplification(Shapefile,Fileds):

    LineElements={}
    EdgeCollection=[]
    NodeCollection=[]
    EdgeNames={}
    EdgeLine={}
    NodeProperties={}
    EdgeProperties={}
    NameDict={}
    NodeLine={}
    NodePos={}
    DictionaryComplementingNode={}

    PL1=Shapefile.split("/")
    if len(PL1)==1:PL1=Shapefile.split("\\")
    # print(PL1)
    FileName=PL1[-1].split(".")[0]
    # print(FileName)
    # b=input()
    sf = shapefile.Reader(Shapefile)
    Shapes=sf.shapes()
    Features=sf.shapeRecords()
    Records = sf.records()
    NameFields = sf.fields
    # print(Fileds)
    # for i,f in enumerate(NameFields):
    #     print(i,f)
    # b=input()
    for feat in Features:
        record=list(feat.record)
        # print("record",record,type(record),len(record))
        # for i,r in enumerate(record):
        #     print(i,r)
        for key in Fileds.keys():
            # print("key",key)
            FieldIndex=Fileds[key][1]
            # print("FieldIndex",FieldIndex)
            LineElements[key]=record[FieldIndex]
            # print("\t",key, LineElements[key] )

        # Section that reads the Edges
        ################################################################################################
        Edge=(LineElements['StartCode'],LineElements['EndCode'])
        # print("Edge",Edge)
        # b=input()
        EdgeCollection.append(Edge)

        # Section that read the attributes of the edges
        #########################################################
        EdgeLine[Edge]=LineElements['Line']
    ################################################################################################
    # for Edge in EdgeCollection:
    #     print(Edge,EdgeLine[Edge])
    #     b=input()
    EdgeProperties={'Line':EdgeLine,'FileName':FileName}
    return EdgeCollection,EdgeProperties



def readSample(Path):
    f=open(Path)
    EdgeCollection=[]
    NodeCollection=[]
    EdgeNames={}
    EdgeLine={}
    NodeProperties={}
    EdgeProperties={}
    NameDict={}
    NodeLine={}
    NodePos={}

    for Line in f.readlines()[1:]:
        LineElements=Line.rstrip().split(",")
        # print(LineElements,LineElements[2],len(LineElements))
        # print(LineElements[10],LineElements[12])
        #  0  1   2   3   4   5   6   7           8         9        10         11    12     13      14
        # FID,Id,Line,CX1,CY1,CX2,CY2,CoordsSta,CoordsEnd,StartName,StartCode,EndName,EndCode,Stop_1,Name_1
        # print(LineElements[1])
        # print("Line",LineElements[2])

        # print("CoordX1",LineElements[3])
        # print("CoordY1",LineElements[4])
        # print("Start name",LineElements[9])
        # print("Start Code",LineElements[10])

        # print("CoordX2",LineElements[5])
        # print("CoordX2",LineElements[6])
        # print("End name",LineElements[11])
        # print("End Code",LineElements[12])
        # Section that reads the data for the Nodes
        ################################################################################################
        if LineElements[10] in NodeCollection:
            pass
        else:
            NodeCollection.append(LineElements[10])

        if LineElements[12] in NodeCollection:
            pass
        else:
            NodeCollection.append(LineElements[12])
        # Section that read the attribtes for the Nodes
        #########################################################
        if LineElements[10] not in NameDict.keys():
            # print("new key")
            NameDict[LineElements[10]]=LineElements[9]
        if LineElements[12] not in NameDict.keys():
            # print("new key")
            NameDict[LineElements[12]]=LineElements[11]
        # print(NameDict.keys())

        if LineElements[10] not in NodePos.keys():
            # print("new key")
            NodePos[LineElements[10]]=(float(LineElements[3]),float(LineElements[4]))
        if LineElements[12] not in NodePos.keys():
            # print("new key")
            NodePos[LineElements[12]]=(float(LineElements[5]),float(LineElements[6]))
        # print(NodePos.keys())

        if LineElements[10] not in NodeLine.keys():
            NodeLine[LineElements[10]]=[]
            NodeLine[LineElements[10]].append(LineElements[2])
        else:
            # print("NodeLine",NodeLine)
            if LineElements[2] not in NodeLine[LineElements[10]]:
                NodeLine[LineElements[10]].append(LineElements[2])

        if LineElements[12] not in NodeLine.keys():
            NodeLine[LineElements[12]]=[]
            NodeLine[LineElements[12]].append(LineElements[2])
        else:
            # print("NodeLine",NodeLine)
            if LineElements[2] not in NodeLine[LineElements[12]]:
                NodeLine[LineElements[12]].append(LineElements[2])

        # Section that reads the Edges
        ################################################################################################
        Edge=(LineElements[10],LineElements[12])
        EdgeCollection.append(Edge)

        # Section that read the attributes of the edges
        #########################################################
        EdgeLine[Edge]=LineElements[2]
    ################################################################################################
    # for Edge in EdgeCollection:
    #     print(Edge)

    # print("###################################################\n"*2)
    # print("NodeCollection",len(NodeCollection))
    # print("EdgeCollection",len(EdgeCollection))
    # print("NameDict",len(NameDict.keys()))

    # for Node in NodeCollection:
    #     print("Node",Node)
    #     print("\t",NameDict[Node])
    #     print("\t",NodePos[Node])
    #     print("\t",NodeLine[Node])
        # print("\t",NodeProperties['Name'][Node])
        # print("\t",NodeProperties['Line'][Node])
        # print("\t",NodeProperties['Pos'][Node])
    EdgeProperties={'Line':EdgeLine}
    NodeProperties={'Line':NodeLine,'Name':NameDict,'Pos':NodePos}
    return EdgeCollection,EdgeProperties,NodeCollection,NodeProperties

def GetLineColorsNodes(Dict):
    List_lines=[]
    Color_Guide_Dict={}
    ColorList=[]
    for key in Dict.keys():
        # print(key,Dict[key])
        if Dict[key] not in List_lines: List_lines.append(Dict[key])
    # print(List_lines,len(List_lines))
    red = Color("blue")
    colors = list(red.range_to(Color("green"),len(List_lines)))
    # print(colors,len(colors),type(colors))
    for idx, Line in enumerate(List_lines):
        # print(Line,type(Line))
        # print(colors[idx],type(colors[idx]))
        Color_Guide_Dict["".join([str(item) for item in Line ])]=colors[idx]
        # Color_Guide_Dict["".join(Line)]=colors[idx]
    # print("################################################")
    for key in Dict.keys():
        co=str(Color_Guide_Dict["".join([str(item) for item in Dict[key] ])])
        # co=str(Color_Guide_Dict["".join(Dict[key])])
        ColorList.append(co)
        # print(co,type(co),str(co))
        # b=input()
    # print(ColorList)
    return ColorList

def GetLineColorsEdges(List_edges,Dict_Lines):
    List_Lines=[]
    Color_Guide_Dict={}
    ColorList=[]
    for key in Dict_Lines.keys():
        if Dict_Lines[key] not in List_Lines: List_Lines.append(Dict_Lines[key])
    # print(List_Lines)
    # ColorList=[]

    InitialColor = Color("#3333CC")
    colors = list(InitialColor.range_to(Color("#FF0066"),len(List_Lines)))
    # print(colors)
    for idx, co in enumerate(List_Lines):
        # print(List_Lines[idx],"-",str(colors[idx]))
        Color_Guide_Dict[List_Lines[idx]]=str(colors[idx])

    for edge in List_edges:
        # print(Dict_Lines[edge],Color_Guide_Dict[Dict_Lines[edge]])
        ColorList.append(Color_Guide_Dict[Dict_Lines[edge]])

    return ColorList

def CreateNetwork(List_Edges,Edge_Properties,List_Nodes,Node_Properties):
    G = nx.DiGraph()
    G.add_nodes_from(List_Nodes)
    G.add_edges_from(List_Edges)

    Node_Color=GetLineColorsNodes(Dict=Node_Properties['Line'])
    Edge_Color=GetLineColorsEdges(List_edges=List_Edges,Dict_Lines=Edge_Properties['Line'])

    nx.set_node_attributes(G, values=Node_Properties['Line'], name="Line")
    nx.set_node_attributes(G, values=Node_Properties['Name'], name="Name")
    nx.set_node_attributes(G, values=Node_Properties['Pos'], name="Pos")

    nx.set_edge_attributes(G,values=Edge_Properties['Line'],name="Line")

    # nx.set_node_attributes(G, 'Name', EdgeNames)
    # nx.set_node_attributes(G, values=EdgeNames, name="Name")
    # nx.set_node_attributes(G, values=EdgeLine, name="Line")
    # print(nx.info(G))
    # print(G.nodes())
    print()
    print("Calling Numer of nodes: ",G.number_of_nodes())
   
    print("###################################\n"*2)

    # print("pos",pos,"\n",type(pos['53051']))
    # nx.draw(G,pos=Node_Properties['Pos'])
    # print(G.edges())
    # print("Edge Propertiy:",G['53010']['52895']['Line'])
    # nx.draw_networkx_nodes(G,pos=Node_Properties['Pos'],node_color= Node_Color,node_size=50)
    # nx.draw_networkx_edges(G,pos=Node_Properties['Pos'],edge_color=Edge_Color)
    # pylab.show()
    # Path=nx.shortest_path(G,"53051","51233")
    # print(Path)
    # print(nx.has_path(G,"53051","51233"))
    # print(nx.closeness_centrality(G, u="51233", distance=None, wf_improved=True))
    # print(nx.closeness_centrality(G, u=None, distance=None, wf_improved=True))
    return {'G':G,'Node_Color':Node_Color,'Edge_Color':Edge_Color,"Edge_Properties":Edge_Properties,"Node_Properties":Node_Properties}
    # return G,Node_Color,Edge_Color,Edge_Properties,Node_Properties

def GetcXcY(List_Coords):
    # print(List_Coords)
    ValX=[]
    ValY=[]
    for key in List_Coords:
        co=List_Coords[key]
        # print("co",co)
        if co[0] not in ValX: ValX.append(co[0])
        if co[1] not in ValY: ValY.append(co[1])
    return {'MaxX':max(ValX),'MinX':min(ValX),'MaxY':max(ValY),'MinY':min(ValY),'AvgX':(sum(ValX) / len(ValX)),'AvgY':(sum(ValY) / len(ValY))}



def PlotGraphs(G_List):
    # G_List=[{'G':G,'Node_Color':Node_Color,'Edge_Color':Edge_Color,"Edge_Properties":Edge_Properties,"Node_Properties":Node_Properties}]
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    PlotLenght=len(G_List)
    for idx,Gr in enumerate(G_List):
        plt.subplot(1,PlotLenght,idx+1)
        nx.draw_networkx_nodes(Gr['G'],pos=Gr['Node_Properties']['Pos'],node_color= Gr['Node_Color'],node_size=50)
        nx.draw_networkx_edges(Gr['G'],pos=Gr['Node_Properties']['Pos'],edge_color=Gr['Edge_Color'])
        ###############################################################################
        plt.tick_params(axis='both',labelcolor='white')
        Coords=GetcXcY(List_Coords=Gr['Node_Properties']['Pos'])
        print(Coords)
        # b=input()
        Info=nx.info(Gr['G'])+"\nNetwork Density: "+str(nx.density(Gr['G']))
        print(Info,type(Info))
        plt.text(Coords['AvgX'], Coords['MaxY']+1300, Gr['Node_Properties']['FileName'])
        plt.text(Coords['MinX'], Coords['MinY'],Info)
        # plt.text(.5, 1.1, Gr['Node_Properties']['FileName'])
        # plt.axis("off")
    plt.show()

def PlotNodeGraphs(G_List):
    # G_List=[{'G':G,'Node_Color':Node_Color,'Edge_Color':Edge_Color,"Edge_Properties":Edge_Properties,"Node_Properties":Node_Properties}]
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    PlotLenght=len(G_List)
    for idx,Gr in enumerate(G_List):
        plt.subplot(1,PlotLenght,idx+1)
        nx.draw_networkx_nodes(Gr['G'],pos=Gr['Node_Properties']['Pos'],node_color= 'red',node_size=50)
        nx.draw_networkx_edges(Gr['G'],pos=Gr['Node_Properties']['Pos'],edge_color=Gr['Edge_Color'])
        ###############################################################################
        plt.tick_params(axis='both',labelcolor='white')
        Coords=GetcXcY(List_Coords=Gr['Node_Properties']['Pos'])
        # print(Coords)
        # b=input()
        Info=nx.info(Gr['G'])+"\nNetwork Density: "+str(nx.density(Gr['G']))
        # print(Info,type(Info))
        plt.text(Coords['AvgX'], Coords['MaxY']+1300, Gr['Edge_Properties']['FileName'])
        plt.text(Coords['MinX'], Coords['MinY'],Info)
        # plt.text(.5, 1.1, Gr['Node_Properties']['FileName'])
        # plt.axis("off")
    plt.show()



def MergeBusStops(Path):

    BusStop_List=[]
    BusStop_Data={}

    sf = shapefile.Reader(Path)
    Shapes=sf.shapes()
    Records = sf.records()
    fields = sf.fields

    # for i,f in enumerate(fields):
    #     print(i-1,f,type(f))

    for record in Records:
        record=list(record)
        # print(record)
        if record[2] not in BusStop_List:
            BusStop_List.append(record[2])
            BusStop_Data[record[2]]={'Line':[record[3]],'X':record[5],'Y':record[6],'Name':record[4]}
        else:
            BusStop_Data[record[2]]['Line'].append(record[3])

    # print("length:",len(BusStop_List))
    return BusStop_List,BusStop_Data


    # 0 ['id', 'N', 16, 6] <class 'list'>
    # 1 ['Seq', 'N', 16, 6] <class 'list'>
    # 2 ['Stop', 'N', 16, 6] <class 'list'>
    # 3 ['Line', 'C', 254, 0] <class 'list'>
    # 4 ['Name', 'C', 254, 0] <class 'list'>
    # 5 ['X', 'N', 16, 6] <class 'list'>
    # 6 ['Y', 'N', 16, 6] <class 'list'>
    # 7 ['Coords', 'C', 50, 0] <class 'list'>



def AgregatedStopsToNetwork(AgregatedNodes,Edge_List,Edge_Properties):
    G = nx.DiGraph()
    StopToNode={}
    Node_Properties={'Pos':{}}
    for idx,Node in enumerate(AgregatedNodes):
        print("#########################################################################################################################################################################\n"*4)
        Xval=Node[0]
        Yval=Node[1]
        NumRouts=Node[2]
        Routes=Node[3]
        ContainedStops=Node[4]
        # print("Node",Node,"\n")
        # print("ContainedStops",ContainedStops)
        # print("ContainedStops[0]",ContainedStops[0],type(ContainedStops[0]))
        # print()
        for Stop in ContainedStops:
            # print("Stop",Stop,type(Stop))
            StopToNode[Stop]=idx


            # if idx not in StopToNode.keys():
            #     print("StopToNode.keys(before)",StopToNode.keys())
            #     StopToNode[Stop]=idx
            #     print(idx,"Todo normal")
            #     print("StopToNode.keys(after)",StopToNode.keys())
            #     print()
            #     # b1=input()
            # else:

            #     if idx in StopToNode.keys():
            #         print("IDX IS ALREADY IN",idx,"StopToNode",StopToNode[idx])
            #         if StopToNode[Stop]==idx:
            #             print("ok resulta que StopToNode[Stop] y idx son iguales")
            #         else:
            #             print("NO resulta que StopToNode[Stop] y idx NO SON IGUALES")
            #     else:
            #         print("IDX IS ALREADY IN")

            #     print(idx,"WHAAAAAAAAAAAAAAAAAAAAAAAAAAT a crazy thing happend")
            #     print("StopToNode.keys()",StopToNode.keys())
            #     print("Stop",Stop,type(Stop))
            #     b1=input()
        # print("Xval",Xval)
        # print("Yval",Yval)
        # print("NumRouts",NumRouts)
        # print("Routes",Routes)
        # print("ContainedStops",ContainedStops)
        # b=input()
        Node_Properties['Pos'][idx]=(Xval,Yval)
        Node_Properties['BusStopCount']=NumRouts
        Node_Properties['BusStopList']=ContainedStops
        Node_Properties['Line']=Routes
        G.add_node(idx, pos=(Xval,Yval),weight=NumRouts,Routes=Routes,ContainedStops=ContainedStops)
        # G.add_node(Node, time=Dic[Node])
    # for key in StopToNode.keys():
        # print(key,StopToNode[key])
    # b=input()
    Edge_Node_List=[]
    New_Edge_Properties={}
    # print(Edge_Properties)
    LineProperties={}

    for key in Edge_Properties['Line'].keys():
        edge=list(key)
        print("\t",edge[0],edge[1])
        if edge[0] in StopToNode and edge[1] in StopToNode:
            New_Edge=(StopToNode[edge[0]],StopToNode[edge[1]])
            LineProperties[New_Edge]=Edge_Properties['Line'][key]
        # print(key,type(key),Edge_Properties['Line'][key])
        # print("\t",StopToNode[edge[0]],"-",StopToNode[edge[1]])
        # print("\t\t",LineProperties[New_Edge])

    New_Edge_Properties={'Line':LineProperties}

    for edge in Edge_List:
        # print(edge,"\t",StopToNode[edge[0]],"-",StopToNode[edge[1]])
        if edge[0] in StopToNode and edge[1] in StopToNode:
            New_Edge=(StopToNode[edge[0]],StopToNode[edge[1]])
            Edge_Node_List.append(New_Edge)

    G.add_edges_from(Edge_Node_List)
    nx.set_edge_attributes(G,values=New_Edge_Properties['Line'],name="Line")
    
    Edge_Color=GetLineColorsEdges(List_edges=Edge_Node_List,Dict_Lines=New_Edge_Properties['Line'])

    # nx.draw_networkx_nodes(G,pos=Node_Properties['Pos'],node_color= "red",node_size=50)
    # nx.draw_networkx_edges(G,pos=Node_Properties['Pos'],edge_color=Edge_Color)
    # pylab.show()
    # return {'G':G,'Node_Color':Node_Color,'Edge_Color':Edge_Color,"Edge_Properties":Edge_Properties,"Node_Properties":Node_Properties}
    return {'G':G,'Edge_Color':Edge_Color,"Edge_Properties":Edge_Properties,"Node_Properties":Node_Properties}

    # print(list(G.nodes(data=True)))
    # print(G.edges(data=True))







def AgregatedGTFSStopsToNetwork(AgregatedNodes,EdgeList):
    G = nx.DiGraph()
    StopToNode={}
    Node_Properties={'Pos':{}}
    for idx,Node in enumerate(AgregatedNodes):

        print("Node",Node)
        # b=input("CHECK THE NODE HERE")
        Xval=Node[0]
        Yval=Node[1]
        NumRouts=Node[2]
        Routes=Node[3]
        ContainedStops=Node[4]
        Status=Node[5]
        SuperNode=Node[5]
        Wheelchair=Node[6]
        # print("Node",Node,"\n")
        # print("ContainedStops",ContainedStops)
        # print("ContainedStops[0]",ContainedStops[0],type(ContainedStops[0]))
        # print()
        for Stop in ContainedStops:
            # print("Stop",Stop,type(Stop))
            StopToNode[Stop]=idx
        if Status=='S':
            Weigth=4*NumRouts
        if Status=='N':
            Weigth=NumRouts
        Node_Properties['Pos'][idx]=(Xval,Yval)
        Node_Properties['BusStopCount']=Weigth
        Node_Properties['BusStopList']=ContainedStops
        Node_Properties['Line']=Routes
        Node_Properties['SuperNode']=SuperNode
        Node_Properties['Wheelchair']=Wheelchair

        G.add_node(idx, pos=(Xval,Yval),weight=Weigth,Routes=Routes,ContainedStops=ContainedStops,SuperNode=SuperNode,Wheelchair=Wheelchair)
        # G.add_node(Node, time=Dic[Node])
    # for key in StopToNode.keys():
        # print(key,StopToNode[key])
    # print("Netwrok is on the node side",G)
    # b=input()
    # print("EdgeList",len(EdgeList))
    NodeEdgeLisr=[]
    for Di in EdgeList:
        print(type(Di),len(Di))
        LiKyes=list(Di.keys())
        # for key in LiKyes[:10]:
        for key in LiKyes:
            print(key)
            for bound in Di[key]:
                print("bound",bound)
                for trip in Di[key][bound]:
                    print(trip)
                    print(trip[0],"->",trip[1])
                    Start=None
                    EndTr=None
                    for idx,Node in enumerate(AgregatedNodes):
                        if trip[0] in Node[4]:
                            Start=idx
                            break
                    for idx,Node in enumerate(AgregatedNodes):
                        if trip[1] in Node[4]:
                            EndTr=idx
                            break
                    if Start is not None and EndTr is not None:
                        if Start != EndTr:
                            NodeEdgeLisr.append([Start,EndTr])
    G.add_edges_from(NodeEdgeLisr)
    # for i in NodeEdgeLisr:
    #     print(i)
    print("All good")
    # for bound in EdgeList:
    #     print("bound",bound)
        # for stop in EdgeList[bound]:
        #     print("\tstops",stop)
    return G






def ExportGeoJsonLines(PathBase,ListOfLines):
    def Container(ListSegments):
        Text='{\n        "features": [\n'
        for Segment in ListSegments:
            if Segment==ListSegments[-1]:
                Text=Text+'{\n'+Segment+'\n}\n\n '
            else:
                Text=Text+'{\n'+Segment+'\n},\n'
        Text=Text+'],\n'+'"type": "FeatureCollection"\n}'
        return Text

    def FormatLine(TextProp,Coordinates,Iden):
        Text='"type": "Feature",\n'+'"properties": '+TextProp+',\n'
        Text=Text+'"geometry": {\n'+'"coordinates": [\n'
        for Coords in Coordinates:
            if Coords != Coordinates[-1]:
                Text=Text+'\t['+str(Coords[1])+','+str(Coords[0])+'],\n'
            else:
                Text=Text+'\t['+str(Coords[1])+','+str(Coords[0])+']\n'
        Text=Text+'],\n'
        Text=Text+'"type": "LineString"\n'+'},\n'
        Text=Text+'"id": "'+Iden+'"'
        return Text


    # L=FormatLine(Line="10",Heading="10 North",Coordinates=[[-73.610016,45.525287],[-73.584541,45.513928],[-73.589173,45.509709]],Iden="1000000000001")
    # print(P)
    # print(Container(ListSegments=[L,P]))



def ExportGeoJsonPoints(ListOfPoints,PChar,NetworkIndex):
    # print(PChar)
    # b=input()
    # print(NetworkIndex)
    def Container(ListSegments):
        Text='{\n        "features": [\n'
        for Segment in ListSegments:
            if Segment==ListSegments[-1]:
                Text=Text+'{\n'+Segment+'\n}\n\n '
            else:
                Text=Text+'{\n'+Segment+'\n},\n'
        Text=Text+'],\n'+'"type": "FeatureCollection"\n}'
        return Text

    def FormatPoint(TextProp,Coordinates,Iden):
        Text='"type": "Feature",\n'
        Text=Text+'"properties": '+TextProp+',\n'
        Text=Text+'"geometry": {\n'+'"coordinates": ['+str(Coordinates[1])+','+str(Coordinates[0])+'],\n'
        Text=Text+'"type": "Point"\n        },\n        "id": "'+Iden+'"\n'
        return Text

    Keys=list(PChar.keys())
    # b=input("LIST OF VARIABLES!!!!!")
    # print("Keys:",Keys)
    # b=input()
    # print(ListOfPoints)
    # b=input()
    FormatedPoints=[]
    # if RearPaths(Key='NetworkSimple1')!="":
    #     ident = EpsgIdent()
    #     ValEPSG=ident.read_prj_from_file(RearPaths(Key='EPSGIN'))
    # if RearPaths(Key='NetworkNodeLine1')!="":
    #     ident = EpsgIdent()
    #     ValEPSG=ident.read_prj_from_file(RearPaths(Key='EPSGIN'))

    # EpsgInput="epsg:"+str(RearPaths(Key='EPSGIN'))
    # print("EpsgInput",EpsgInput)
    # input_projection = Proj(init=EpsgInput)
    # output_projection = Proj(init="epsg:4326")
    Iden=999999999999999
    for i,Point in enumerate(ListOfPoints):
        # Point=int(Point)
        # print("Point",Point,type(Point))
        # b=input()
        ProgressBarColor(current=i+1,total=len(ListOfPoints))
        if Point==0 and Iden>999999999999999:
            break
        TextProp='{"StopCode":"'+str(Point)+'",'
        Iden=Iden+1
        # print(Point)
        # print(TextProp)
        # print()
        # for key in Keys:
            # print(key)
            # print(list(PChar[key].keys())[:20])
            # print(Point,type(Point))
            # print("#######################################################################################################\n"*3)
        # b=input()
        # for key in Keys:
        #     print("key", key)
        #     try:
        #         # print("PChar[key][Point]",key,type(PChar[key][Point]),PChar[key][Point])
        #     except :
        #         print("Does not exist")
        #         b=input('Press Enter ...')


        for key in Keys:
            # print("key",key)
            # print("PChar[key]",PChar[key])
            # b=input("Press enter")
            # b=input("ANOTHER CHECK POINT IN THE LAST PART OF THE PUSH")
            #  Point=int(Point)
            # print("############################################\n"*3)
            # print("key:",key,type(key),end="\t")
            # print("Point",Point,type(Point))
            # print("############################################\n"*3)
            # print(list(PChar[key].keys())[0],type(list(PChar[key].keys())[0]))
            # print(PChar['Pos'].keys())
            # print(PChar[key],type(PChar[key]),"\n\n\n")
            # print("PChar[key][Point]",key,type(PChar[key][Point]),PChar[key][Point])
            if key =='Pos' or key =='pos':
                Coordinates=PChar[key][Point]
            #     new_x, new_y = transform(input_projection, output_projection, PChar[key][Point][0], PChar[key][Point][1])
                # new_x, new_y = transform(input_projection, output_projection, x, y)
                # print(Point,new_x, new_y)
                # Coordinates=(new_x, new_y)
            elif type(PChar[key][Point]) ==type(list()):
                Var=",".join([str(item) for item in PChar[key][Point] ])
                TextProp=TextProp+'"'+key+'": '+'"'+",".join([str(item) for item in PChar[key][Point] ])+'"'
                if key !=Keys[-1]:
                    TextProp=TextProp+", "

            elif type(PChar[key][Point]) ==type(float()):
                TextProp=TextProp+'"'+key+'": '+str('%.12f' %PChar[key][Point])
                if key !=Keys[-1]:
                    TextProp=TextProp+", "

            elif type(PChar[key][Point]) ==type(int()):
                TextProp=TextProp+'"'+key+'": '+str(PChar[key][Point])
                if key !=Keys[-1]:
                    TextProp=TextProp+", "
            else:
                TextProp=TextProp+'"'+key+'": '+'"'+str(PChar[key][Point])+'"'
                if key !=Keys[-1]:
                    TextProp=TextProp+", "
                # TextProp[key]=PChar[key][int(Point)]
            if key ==Keys[-1]:
                TextProp=TextProp+"}"
            # print("\t",key,":",Var,type(Var), end="\t")
        # print("\n-------------------------------------------------------------------")
        # print(TextProp)
        # print("Coordinates",Coordinates,"\n\n\n")
        # print("-------------------------------------------------------------------")
        P=FormatPoint(TextProp=str(TextProp),Coordinates=Coordinates,Iden=str(Iden))
        FormatedPoints.append(P)
        # print(P)
        # b=input()
    # print(Container(ListSegments=FormatedPoints))
    files = [('GeoJson', '*.geojson'), 
    ('Text Document', '*.txt')]
    Titles=["Bus Network","Rail Network","Metro Network","Light Rail Netwrok","Other Network","Node Network"]
    Path = asksaveasfile(filetypes = files, defaultextension = files,title = Titles[NetworkIndex]) 

    fw=open(Path.name,"w",encoding='utf-8')
    # print(Container(ListSegments=FormatedPoints))
    fw.write(Container(ListSegments=FormatedPoints))
    fw.close


def ListToGeoJson(ListBusStops):
    
    ListofPoints=[]
    PropCharac={'Pos':{},'weigth':{},'Line':{},'SuperNode':{}}
    for idx,Point in enumerate(ListBusStops):
        Point=list(Point)
        print(Point,type(Point))
        # b=input(".......................................check point")
        ListofPoints.append(idx)
        PropCharac['Pos'][idx]=[Point[0],Point[1]]
        PropCharac['weigth'][idx]=Point[2]
        PropCharac['Line'][idx]=Point[3]
        # PropCharac['Line'][idx]=Point[5]


        # print(idx,'Pos',PropCharac['Pos'][idx],'weigth',PropCharac['weigth'][idx],'Line',PropCharac['Line'][idx])

    ExportGeoJsonPoints(ListOfPoints=ListofPoints,PChar=PropCharac)

#######################################################################

def NetWorkToGeoJson(G,NetworkIndex):
    # USES TK to get path
    print(G,type(G),dir(G))
    # b=input("STOP HERE")


    PointCharacteristics={}
    ListOfPoints=[]
    Cont=0
    # print("number_of_nodes",G.number_of_nodes(),"\n\n")
    for Node in G.nodes(data=True):
        Cont=Cont+1
        ListOfKeys=list(Node[1].keys())
        if Cont==1:
            break
        # print("ListOfKeys",ListOfKeys)
        # b=input()


    for key in ListOfKeys:
        PointCharacteristics[key]={}
    for Node in G.nodes(data=True):
        NodeIndex=Node[0]
        ListOfPoints.append(Node[0])
        Keys=Node[1].keys()
        if len(Keys)==0:
            break
        Dict=Node[1]
        # print(Dict)
        # print(type(Dict))
        # print(Dict.keys())
        for key in ListOfKeys:
            # print("key",key)
            # print("Dict",Dict[key])
            # b=input("Press enter")

            # PointCharacteristics[key][NodeIndex]=1
            PointCharacteristics[key][NodeIndex]=Dict[key]
        # print("######################################################\n"*3)
        # PointCharacteristics['Line'][int(Node[0])]=Node[1]['Line']
        # PointCharacteristics['Pos'][int(Node[0])]=Node[1]['Pos']
        # PointCharacteristics['weight'][int(Node[0])]=Node[1]['weight']
        # PointCharacteristics['ContainedStops'][int(Node[0])]=Node[1]['ContainedStops']
        # print(PointCharacteristics)
        print(PointCharacteristics[key])


    print("Calculating Centrality degree\n")

    degree_centrality = nx.degree_centrality(G)
    # PointCharacteristics['CenDeg']=degree_centrality
    PointCharacteristics['CenDeg']={}
    # print(degree_centrality,"\nCentrality degree")
    # b=input()
    
    for key in degree_centrality:
        # print(key,type(key))
        # b=input()
        # if type(key)== type(int()):
        PointCharacteristics['CenDeg'][key] = degree_centrality[key]
        # if type(key)==type(float()):
        #     PointCharacteristics['CenDeg'][int(key)] = degree_centrality[key]
    # print(PointCharacteristics['CenDeg'],"\nCentrality")
    # b=input()
    try:
        LI=list(PointCharacteristics['CenDeg'].values())
        arr = np.array(LI)
        Ranges_DegCen=Calculations.NaturalBreaksNumpyList(Data=LI, Classess=5)
        # Ranges_DegCen=jenkspy.jenks_breaks(arr, nb_class=5)


        # print("Ranges_DegCen",Ranges_DegCen,len(Ranges_DegCen))
        # print("Min",min(LI))
        # print("Max",max(LI))
        # b=input()
        PointCharacteristics['CatCenDeg']={}
        for key in PointCharacteristics['CenDeg'].keys():
            # print(key,PointCharacteristics['CenDeg'])
            # b=input()
            if Ranges_DegCen[0]<=PointCharacteristics['CenDeg'][key] and PointCharacteristics['CenDeg'][key]<=Ranges_DegCen[1]:
                PointCharacteristics['CatCenDeg'][key]=1
            elif Ranges_DegCen[1]<=PointCharacteristics['CenDeg'][key] and PointCharacteristics['CenDeg'][key]<=Ranges_DegCen[2]:
                PointCharacteristics['CatCenDeg'][key]=2
            elif Ranges_DegCen[2]<=PointCharacteristics['CenDeg'][key] and PointCharacteristics['CenDeg'][key]<=Ranges_DegCen[3]:
                PointCharacteristics['CatCenDeg'][key]=3
            elif Ranges_DegCen[3]<=PointCharacteristics['CenDeg'][key] and PointCharacteristics['CenDeg'][key]<=Ranges_DegCen[4]:
                PointCharacteristics['CatCenDeg'][key]=4
            elif Ranges_DegCen[4]<=PointCharacteristics['CenDeg'][key] and PointCharacteristics['CenDeg'][key]<=Ranges_DegCen[5]:
                PointCharacteristics['CatCenDeg'][key]=5
            else:
                print("Not working")
                b1=input()
    except :
        print("Can't Classify")

    # for key in PointCharacteristics['CatCenDeg'].keys():
    #     print(key,type(key),PointCharacteristics['CatCenDeg'][key])



    # b=input()
    print("Calculating Centrality Closennes\n")
    # try:
    closeness_centrality = nx.closeness_centrality(G)
    PointCharacteristics['Clossnes']={}
    for key in closeness_centrality:    
        # if type(key)==type(int()):
        PointCharacteristics['Clossnes'][key] =  closeness_centrality[key]*100
        # if type(key)==type(float()):
        #     PointCharacteristics['Clossnes'][int(key)] =  closeness_centrality[key]*100

    try:
        LI=list(PointCharacteristics['Clossnes'].values())
        arr = np.array(LI)

        Ranges_ClosCen=Calculations.NaturalBreaksNumpyList(Data=LI, Classess=5)

        # Ranges_ClosCen=jenkspy.jenks_breaks(arr, nb_class=5)



        # print("Ranges_ClosCen",Ranges_ClosCen,len(Ranges_ClosCen))
        # print("Min",min(LI))
        # print("Max",max(LI))
        # b=input()
        PointCharacteristics['CatClossnes']={}
        # print("crea di")
        for key in PointCharacteristics['Clossnes'].keys():
            if Ranges_ClosCen[0]<=PointCharacteristics['Clossnes'][key] and PointCharacteristics['Clossnes'][key]<=Ranges_ClosCen[1]:
                PointCharacteristics['CatClossnes'][key]=1
            elif Ranges_ClosCen[1]<=PointCharacteristics['Clossnes'][key] and PointCharacteristics['Clossnes'][key]<=Ranges_ClosCen[2]:
                PointCharacteristics['CatClossnes'][key]=2
            elif Ranges_ClosCen[2]<=PointCharacteristics['Clossnes'][key] and PointCharacteristics['Clossnes'][key]<=Ranges_ClosCen[3]:
                PointCharacteristics['CatClossnes'][key]=3
            elif Ranges_ClosCen[3]<=PointCharacteristics['Clossnes'][key] and PointCharacteristics['Clossnes'][key]<=Ranges_ClosCen[4]:
                PointCharacteristics['CatClossnes'][key]=4
            elif Ranges_ClosCen[4]<=PointCharacteristics['Clossnes'][key] and PointCharacteristics['Clossnes'][key]<=Ranges_ClosCen[5]:
                PointCharacteristics['CatClossnes'][key]=5
            else:
                print(key,"Not working")
                b1=input()
            # print(key,PointCharacteristics['Clossnes'][key],PointCharacteristics['CatClossnes'][key])
            # b=input()
    except:
        print("Can't Classify")

    # except:
    #      print("No closeness_centrality")
    # print(PointCharacteristics['CatClossnes'],"CatClossnes")
    # b=input()
    # print(PointCharacteristics['Clossnes'],'Clossnes')
    # b=input()
    # for key in PointCharacteristics['CatCenDeg'].keys():
        # print(key,type(key),PointCharacteristics['CatCenDeg'][key])


    print("Calculating Centrality Eigen\n")
    try:
        eigenvector_centrality = nx.eigenvector_centrality_numpy(G)
        PointCharacteristics['Eigen']={}
        for key in eigenvector_centrality:
            # if type(key)==type(int()):
            PointCharacteristics['Eigen'][key] = eigenvector_centrality[key]*100000
                # if type(key)==type(float()):
                #     PointCharacteristics['Eigen'][int(key)] = eigenvector_centrality[key]*100000

        # print(PointCharacteristics['Eigen'])
        # b=input()
        LI=list(PointCharacteristics['Eigen'])
        arr = np.array(LI)
        Ranges_EgiCen=Calculations.NaturalBreaksNumpyList(Data=LI, Classess=5)
        # Ranges_EgiCen=jenkspy.jenks_breaks(arr, nb_class=5)


        # print("Ranges_EgiCen",Ranges_EgiCen)

        # print("Ranges_EgiCen",Ranges_EgiCen,len(Ranges_EgiCen))
        # print("Min",min(LI))
        # print("Max",max(LI))
        # b=input()
        PointCharacteristics['CatEigen']={}
        for key in PointCharacteristics['Eigen'].keys():
            # print(key,PointCharacteristics['Eigen'][key])
            # b=input()
            if  PointCharacteristics['Eigen'][key]<=Ranges_EgiCen[1]:
            # if Ranges_EgiCen[0]<=PointCharacteristics['Eigen'][key] and PointCharacteristics['Eigen'][key]<=Ranges_EgiCen[1]:
                PointCharacteristics['CatEigen'][key]=1
            elif Ranges_EgiCen[1]<=PointCharacteristics['Eigen'][key] and PointCharacteristics['Eigen'][key]<=Ranges_EgiCen[2]:
                PointCharacteristics['CatEigen'][key]=2
            elif Ranges_EgiCen[2]<=PointCharacteristics['Eigen'][key] and PointCharacteristics['Eigen'][key]<=Ranges_EgiCen[3]:
                PointCharacteristics['CatEigen'][key]=3
            elif Ranges_EgiCen[3]<=PointCharacteristics['Eigen'][key] and PointCharacteristics['Eigen'][key]<=Ranges_EgiCen[4]:
                PointCharacteristics['CatEigen'][key]=4
            elif Ranges_EgiCen[4]<=PointCharacteristics['Eigen'][key]:
            # elif Ranges_EgiCen[4]<=PointCharacteristics['Eigen'][key] and PointCharacteristics['Eigen'][key]<=Ranges_EgiCen[5]:
                PointCharacteristics['CatEigen'][key]=5
            else:
                print(key,"Not working")
                b1=input()
    except:
         print("No eigenvector_centrality")

    # print("PointCharacteristics",PointCharacteristics.keys())
    # print("start printing")

    # for key in PointCharacteristics.keys():
    #     print("key:",key," is ",type(PointCharacteristics[key])," has ",len(PointCharacteristics[key].keys()))

    # b=input()

    ExportGeoJsonPoints(ListOfPoints=ListOfPoints,PChar=PointCharacteristics,NetworkIndex=NetworkIndex)

#######################################################################


def NewNetWorkToGeoJson(G,NetworkIndex):
    # USES TK to get path
    print(G,type(G),dir(G))
    b=input("STOP HERE")


    PointCharacteristics={}
    ListOfPoints=[]
    Cont=0
    # print("number_of_nodes",G.number_of_nodes(),"\n\n")
    for Node in G.nodes(data=True):
        Cont=Cont+1
        ListOfKeys=list(Node[1].keys())
        if Cont==1:
            break
        # print("ListOfKeys",ListOfKeys)
        # b=input()


    for key in ListOfKeys:
        PointCharacteristics[key]={}
    for Node in G.nodes(data=True):
        NodeIndex=Node[0]
        ListOfPoints.append(Node[0])
        Keys=Node[1].keys()
        if len(Keys)==0:
            break
        Dict=Node[1]
        # print(Dict)
        # print(type(Dict))
        # print(Dict.keys())
        for key in ListOfKeys:
            # print("key",key)
            # print("Dict",Dict[key])
            # b=input("Press enter")

            # PointCharacteristics[key][NodeIndex]=1
            PointCharacteristics[key][NodeIndex]=Dict[key]
        # print("######################################################\n"*3)
        # PointCharacteristics['Line'][int(Node[0])]=Node[1]['Line']
        # PointCharacteristics['Pos'][int(Node[0])]=Node[1]['Pos']
        # PointCharacteristics['weight'][int(Node[0])]=Node[1]['weight']
        # PointCharacteristics['ContainedStops'][int(Node[0])]=Node[1]['ContainedStops']
        # print(PointCharacteristics)
        print(PointCharacteristics[key])


    print("Calculating Harmonic degree\n")

    degree_centrality = nx.harmonic_centrality(G, nbunch=None, distance=None, sources=None)
    # PointCharacteristics['CenDeg']=degree_centrality
    PointCharacteristics['HarmCen']={}
    # print(degree_centrality,"\nCentrality degree")
    # b=input()
    
    for key in degree_centrality:
        # print(key,type(key))
        # b=input()
        # if type(key)== type(int()):
        PointCharacteristics['HarmCen'][key] = degree_centrality[key]
        # if type(key)==type(float()):
        #     PointCharacteristics['CenDeg'][int(key)] = degree_centrality[key]
    # print(PointCharacteristics['CenDeg'],"\nCentrality")
    # b=input()
    try:
        LI=list(PointCharacteristics['HarmCen'].values())
        arr = np.array(LI)
        Ranges_DegCen=Calculations.NaturalBreaksNumpyList(Data=LI, Classess=5)
        # Ranges_DegCen=jenkspy.jenks_breaks(arr, nb_class=5)


        # print("Ranges_DegCen",Ranges_DegCen,len(Ranges_DegCen))
        # print("Min",min(LI))
        # print("Max",max(LI))
        # b=input()
        PointCharacteristics['CatHarmCen']={}
        for key in PointCharacteristics['HarmCen'].keys():
            # print(key,PointCharacteristics['CenDeg'])
            # b=input()
            if Ranges_DegCen[0]<=PointCharacteristics['HarmCen'][key] and PointCharacteristics['HarmCen'][key]<=Ranges_DegCen[1]:
                PointCharacteristics['CatHarmCen'][key]=1
            elif Ranges_DegCen[1]<=PointCharacteristics['HarmCen'][key] and PointCharacteristics['HarmCen'][key]<=Ranges_DegCen[2]:
                PointCharacteristics['CatHarmCen'][key]=2
            elif Ranges_DegCen[2]<=PointCharacteristics['HarmCen'][key] and PointCharacteristics['HarmCen'][key]<=Ranges_DegCen[3]:
                PointCharacteristics['CatHarmCen'][key]=3
            elif Ranges_DegCen[3]<=PointCharacteristics['HarmCen'][key] and PointCharacteristics['HarmCen'][key]<=Ranges_DegCen[4]:
                PointCharacteristics['CatHarmCen'][key]=4
            elif Ranges_DegCen[4]<=PointCharacteristics['HarmCen'][key] and PointCharacteristics['HarmCen'][key]<=Ranges_DegCen[5]:
                PointCharacteristics['CatHarmCen'][key]=5
            else:
                print("Not working")
                b1=input()
    except :
        print("NO HARMONIC CENTRALITY")

    # for key in PointCharacteristics['CatCenDeg'].keys():
    #     print(key,type(key),PointCharacteristics['CatCenDeg'][key])



    # b=input()
    print("Calculating Centrality Closennes\n")
    # try:
    for node in G.nodes(data=True):
        print('node i hope:',node,type(node))
        # print(node[])
        b=input('.................................')
    closeness_centrality = nx.closeness_centrality(G)
    PointCharacteristics['Clossnes']={}
    for key in closeness_centrality:    
        # if type(key)==type(int()):
        PointCharacteristics['Clossnes'][key] =  closeness_centrality[key]*100
        # if type(key)==type(float()):
        #     PointCharacteristics['Clossnes'][int(key)] =  closeness_centrality[key]*100

    try:
        LI=list(PointCharacteristics['Clossnes'].values())
        arr = np.array(LI)

        Ranges_ClosCen=Calculations.NaturalBreaksNumpyList(Data=LI, Classess=5)

        # Ranges_ClosCen=jenkspy.jenks_breaks(arr, nb_class=5)



        # print("Ranges_ClosCen",Ranges_ClosCen,len(Ranges_ClosCen))
        # print("Min",min(LI))
        # print("Max",max(LI))
        # b=input()
        PointCharacteristics['CatClossnes']={}
        # print("crea di")
        for key in PointCharacteristics['Clossnes'].keys():
            if Ranges_ClosCen[0]<=PointCharacteristics['Clossnes'][key] and PointCharacteristics['Clossnes'][key]<=Ranges_ClosCen[1]:
                PointCharacteristics['CatClossnes'][key]=1
            elif Ranges_ClosCen[1]<=PointCharacteristics['Clossnes'][key] and PointCharacteristics['Clossnes'][key]<=Ranges_ClosCen[2]:
                PointCharacteristics['CatClossnes'][key]=2
            elif Ranges_ClosCen[2]<=PointCharacteristics['Clossnes'][key] and PointCharacteristics['Clossnes'][key]<=Ranges_ClosCen[3]:
                PointCharacteristics['CatClossnes'][key]=3
            elif Ranges_ClosCen[3]<=PointCharacteristics['Clossnes'][key] and PointCharacteristics['Clossnes'][key]<=Ranges_ClosCen[4]:
                PointCharacteristics['CatClossnes'][key]=4
            elif Ranges_ClosCen[4]<=PointCharacteristics['Clossnes'][key] and PointCharacteristics['Clossnes'][key]<=Ranges_ClosCen[5]:
                PointCharacteristics['CatClossnes'][key]=5
            else:
                print(key,"Not working")
                b1=input()
            # print(key,PointCharacteristics['Clossnes'][key],PointCharacteristics['CatClossnes'][key])
            # b=input()
    except:
        print("Can't Classify")

    # except:
    #      print("No closeness_centrality")
    # print(PointCharacteristics['CatClossnes'],"CatClossnes")
    # b=input()
    # print(PointCharacteristics['Clossnes'],'Clossnes')
    # b=input()
    # for key in PointCharacteristics['CatCenDeg'].keys():
        # print(key,type(key),PointCharacteristics['CatCenDeg'][key])


    print("Calculating Betweennes Centrality\n")
    try:
        eigenvector_centrality = nx.betweenness_centrality(G, k=None, normalized=True, weight=None, endpoints=False, seed=None)
        PointCharacteristics['BetCen']={}
        for key in eigenvector_centrality:
            # if type(key)==type(int()):
            PointCharacteristics['BetCen'][key] = eigenvector_centrality[key]*100000
                # if type(key)==type(float()):
                #     PointCharacteristics['Eigen'][int(key)] = eigenvector_centrality[key]*100000

        # print(PointCharacteristics['Eigen'])
        # b=input()
        LI=list(PointCharacteristics['BetCen'])
        arr = np.array(LI)
        Ranges_EgiCen=Calculations.NaturalBreaksNumpyList(Data=LI, Classess=5)
        # Ranges_EgiCen=jenkspy.jenks_breaks(arr, nb_class=5)


        # print("Ranges_EgiCen",Ranges_EgiCen)

        # print("Ranges_EgiCen",Ranges_EgiCen,len(Ranges_EgiCen))
        # print("Min",min(LI))
        # print("Max",max(LI))
        # b=input()
        PointCharacteristics['CatBetCen']={}
        for key in PointCharacteristics['BetCen'].keys():
            # print(key,PointCharacteristics['BetCen'][key])
            # b=input()
            if  PointCharacteristics['BetCen'][key]<=Ranges_EgiCen[1]:
            # if Ranges_EgiCen[0]<=PointCharacteristics['BetCen'][key] and PointCharacteristics['BetCen'][key]<=Ranges_EgiCen[1]:
                PointCharacteristics['CatBetCen'][key]=1
            elif Ranges_EgiCen[1]<=PointCharacteristics['BetCen'][key] and PointCharacteristics['BetCen'][key]<=Ranges_EgiCen[2]:
                PointCharacteristics['CatBetCen'][key]=2
            elif Ranges_EgiCen[2]<=PointCharacteristics['BetCen'][key] and PointCharacteristics['BetCen'][key]<=Ranges_EgiCen[3]:
                PointCharacteristics['CatBetCen'][key]=3
            elif Ranges_EgiCen[3]<=PointCharacteristics['BetCen'][key] and PointCharacteristics['BetCen'][key]<=Ranges_EgiCen[4]:
                PointCharacteristics['CatBetCen'][key]=4
            elif Ranges_EgiCen[4]<=PointCharacteristics['BetCen'][key]:
            # elif Ranges_EgiCen[4]<=PointCharacteristics['BetCen'][key] and PointCharacteristics['BetCen'][key]<=Ranges_EgiCen[5]:
                PointCharacteristics['CatBetCen'][key]=5
            else:
                print(key,"Not working")
                b1=input()
    except:
         print("NO BETWEENNESS CENTRALITY")

    # print("PointCharacteristics",PointCharacteristics.keys())
    # print("start printing")

    # for key in PointCharacteristics.keys():
    #     print("key:",key," is ",type(PointCharacteristics[key])," has ",len(PointCharacteristics[key].keys()))

    # b=input()

    ExportGeoJsonPoints(ListOfPoints=ListOfPoints,PChar=PointCharacteristics,NetworkIndex=NetworkIndex)


#######################################################################




def SimpleNetworkToGeoJson(G):
    # G = nx.DiGraph()
    # G.__getattribute__
    NetWorkToGeoJson(G=G['G'])

    # for node in  G['G'].nodes(data=True):
    #     print (node,type(node))
    #     print("#########################################################################################\n")
    # b=input()
    # for edge in G['G'].edges(data=True):
    #     print(edge)
    # b=input()
    # print(G.keys())
    # print(type(G['Node_Properties']))

    # for key in G['Node_Properties'].keys():
    #     print(key,"\t",G['Node_Properties'][key])


if __name__ == "__main__":
    # Sample=r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tools\SampleData\Network\SampleLine.csv"
    # Edges=readSample(Path=Sample)
    # CreateNetwork(List_Edges=Edges)
    # PathFull=r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tools\SampleData\Network\FullData.csv"
    # Fewlines=r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tools\SampleData\Network\FewLines.csv"

    # Fields={'Line':['Line',1],
    # 'StartName':["StartName",8],
    # 'StartCode':["StartCode",9],
    # 'EndName':["EndName",10],
    # 'EndCode':["EndCode",11],
    # }

    # SPFewLines=r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tools\SampleData\Network\FewLines.shp"
    # SpOtherLines=r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tools\SampleData\Network\OtherFewLines.shp"
    # AllLines=r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tools\SampleData\Network\BusLineVertex.shp"
    # SampleShp=r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tools\SampleData\Network\SampleLine.shp"

    ############################################################################################################################################
    # EdgeCollection,EdgeProperties,NodeCollection,NodeProperties=readSample(Path=Fewlines)
    # CreateNetwork(List_Edges=EdgeCollection,Edge_Properties=EdgeProperties,List_Nodes=NodeCollection,Node_Properties=NodeProperties)

    # EdgeCollection,EdgeProperties,NodeCollection,NodeProperties=readShpNetWork(Shapefile=SampleShp,Fileds=Fields)
    # CreateNetwork(List_Edges=EdgeCollection,Edge_Properties=EdgeProperties,List_Nodes=NodeCollection,Node_Properties=NodeProperties)



    # Test with two ShapeFiles
    # EdgeCollection,EdgeProperties,NodeCollection,NodeProperties=readShpNetWork(Shapefile=AllLines,Fileds=Fields)
    # G_Dict_1=CreateNetwork(List_Edges=EdgeCollection,Edge_Properties=EdgeProperties,List_Nodes=NodeCollection,Node_Properties=NodeProperties)
    # NetWorkToGeoJson(G=G_Dict_1['G'])


    # EdgeCollection,EdgeProperties,NodeCollection,NodeProperties=readShpNetWork(Shapefile=SpOtherLines,Fileds=Fields)
    # G_Dict_2=CreateNetwork(List_Edges=EdgeCollection,Edge_Properties=EdgeProperties,List_Nodes=NodeCollection,Node_Properties=NodeProperties)
    #  =[G_Dict_1,G_Dict_2]
    # PlotGraphs(G_List)

    # BusStops=r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tools\SampleData\Network\BusStopsIndividual.shp"
    # BusStop_List,BusStop_Data=MergeBusStops(Path=BusStops)
    # BusStopsAgregated=r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tools\SampleData\Network\BusStopsAgregated.txt"
    # fw=open(BusStopsAgregated,"w")
    # Text="Stop Code;Lines;X Val;Y Val;Name\n"
    # fw.write(Text)
    # for Bs in BusStop_List:a
    #     # print(Bs,BusStop_Data[Bs])
    #     # print(Bs,BusStop_Data[Bs]['Line'],BusStop_Data[Bs]['X'],BusStop_Data[Bs]['Y'],BusStop_Data[Bs]['Name'])
    #     Lines=""
    #     for L in BusStop_Data[Bs]['Line']:
    #         Lines=Lines+L
    #         if len(BusStop_Data[Bs]['Line'])>1:
    #             if L!=BusStop_Data[Bs]['Line'][-1]:
    #                 Lines=Lines+","
    #     Text=str(Bs)+";"+Lines+";"+str(BusStop_Data[Bs]['X'])+";"+str(BusStop_Data[Bs]['Y'])+";"+BusStop_Data[Bs]['Name']+"\n"
    #     fw.write(Text)
    # fw.close()


    # SampleNA_Line=r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tools\SampleData\Network Cleaner Data\Sample_Lines_10t15.shp"
    # # SampleNA_Line=r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tools\SampleData\Network Cleaner Data\Sample_Lines_24.shp"
    # Fields={'Line':['Line',1],
    # 'StartName':["StartName",8],
    # 'StartCode':["StartCode",9],
    # 'EndName':["EndName",10],
    # 'EndCode':["EndCode",11],
    # }
    # EdgeCollection,EdgeProperties=readShpNetWorkForSimplification(Shapefile=SampleNA_Line,Fileds=Fields)

    # # SampleNA_Bus=r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tools\SampleData\Network Cleaner Data\Sample_BusStops_24.shp"
    # SampleNA_Bus=r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tools\SampleData\Network Cleaner Data\Sample_BusStops_10t15.shp"

    # LBS1=CalculateVecinityBusStops(Shapefile=SampleNA_Bus,FieldId=["StopCode",0] ,Routes= ["Lines",1])
    # print("Len LBS1",len(LBS1))
    # print("End of CalculateVecinityBusStops")
    # Nodes= AgregateTransitNetwork(ListBusStops=LBS1,Range=75)

    # Gr=AgregatedStopsToNetwork(AgregatedNodes=Nodes,Edge_List=EdgeCollection,Edge_Properties=EdgeProperties)

    # NetWorkToGeoJson(G=G_Dict_1['G'])


    # PlotNodeGraphs(G_List=[Gr])
    # for idx,Node in enumerate(Nodes):
    #     print(idx,end="t")
    #     for El in Node:
    #         print(El,end="\t")
    #     print()



    print("..............fin.....................")