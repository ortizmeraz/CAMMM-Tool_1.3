#! python3.
import os
import sys
import io
import datetime
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from tkinter.filedialog import asksaveasfile 

from tkinter import messagebox
from shutil import copyfile
import tkinter
import numpy as np
import tkinter as tk
import sqlite3


from PIL import ImageTk, Image
import os

from functools import partial
import math 
from scipy._lib.six import xrange
import statistics
import shapefile
import pyproj
from pyproj import Proj
from geojson import Point, Feature, FeatureCollection, dump
import subprocess
import time
import os, shutil
from fractions import Fraction
from datetime import datetime
import networkx as nx
import numpy as np
import pandas
import pylab
from colour import Color
import shapefile
from pyproj import Proj, transform
import jenkspy

import decimal
decimal.getcontext().prec = 10




class PlotingData:
    def __init__(self, ShapeFiles, Titles):
        self.ShapeFiles = ShapeFiles
        self.Titles = Titles

class Paths:
    def __init__(self,ProcessFolder):
        self.ProcessFolder=ProcessFolder

    def TempoFolder():
        return r"E:\\OneDrive - Concordia University - Canada\\RA-CAMM\\Software\\CAMMM-Soft-Tools\\Operational\\"

class DataBucket:
    def __init__(self,name):
        self.name


class ClassDataCentroid(DataBucket):
    def __init__(self, ShapeFiles, Titles,CityArea,Ratio,):
        self.ShapeFiles=ShapeFiles
        self.Titles=Titles
        self.CityArea=CityArea
        self.Ratio=Ratio
       


class CentroidData(PlotingData):
    def __init__(self, ShapeFiles, Titles):
        super().__init__(ShapeFiles, Titles)
        self.graduationyear = 2019

class Coord:
    def __init__(self,X,Y):
        self.X = X
        self.Y = Y
        

class Station(Coord):
    def __init__(self,Id,Type,Lines,Coords,RawDirectConections,RawIndirectConnections):
        self.Id = Id
        self.Type = Type
        self.Lines = Lines
        self.Coords = Coords
        self.RawDirectConections = RawDirectConections
        self.RawIndirectConnections = RawIndirectConnections
        
class Line():
    def __init__(self,Type,Name,NumberStations,AverageStationDistance,Lenght,ConectingLines):
        self.Type
        self.Name
        self.NumberStations
        self.AverageStationDistance
        self.Lenght
        self.ConectingLines


class  CriteriaData():
    def __init__(self,MinDistMask,MaxDistMask,NameFieldLines,NameFieldStop,NeigbourDistance,AdjacentDistance):
        self.MinDistMask
        self.MaxDistMask
        self.NameFieldLines
        self.NameFieldStop
        self.NeigbourDistance
        self.AdjacentDistance

# B12345=BusStop(Id=1,Lines="2",Coords=Coord(X=10,Y=20))


class Street:
    def __init__(self,Name="",CoordXA=0,CoordYA=0,CoordXB=0,CoordYB=0,Segments=[]):
        self.Name=Name
        self.CoordXA=CoordXA
        self.CoordYA=CoordYA
        self.CoordXB=CoordXB
        self.CoordYB=CoordYB
        self.Segments=[]



class Segment:
    def __init__(self, CoordXA=0,CoordXB=0,CoordYA=0,CoordYB=0):
        self.CoordXA=CoordXA
        self.CoordXB=CoordXB
        self.CoordYA=CoordYA
        self.CoordYB=CoordYB
    def Dist(self):
        return math.sqrt(((self.CoordXB-self.CoordXA)**2)+((self.CoordYB-self.CoordYA)**2))
    def M(self):
        return (self.CoordYB-self.CoordYA)/(self.CoordXB-self.CoordXA)
    def B(self):
        return self.CoordYB-((self.CoordYB-self.CoordYA)/(self.CoordXB-self.CoordXA)*self.CoordXB)

class Point:
    """ Create a new Point, at coordinates x, y """

    def __init__(self, x=0, y=0):
        """ Create a new point at x, y """
        self.x = x
        self.y = y

    def distance_from_origin(self):
        """ Compute my distance from the origin """
        return ((self.x ** 2) + (self.y ** 2)) ** 0.5


def Dictionary():
    RowPaths={'SampleData':1,
    'Importance1':2,
    'Importance2':3,
    'NetworkSimple1':4,
    'NetworkSimple2':5,
    'NetworkNodeLine1':6,
    'NetworkBusStops1':7,
    'NetworkNodeLine2':8,
    'NetworkBusStops2':9,
    'end':0}
    return RowPaths

def RearPaths(Key):
    PathDB="Scripts\Database.db"
    RowPaths=Dictionary()
    db = sqlite3.connect(PathDB)
    cursor = db.cursor()
    Comand='SELECT * FROM ListPaths WHERE "_rowid_"=\'2\';'
    Data=cursor.execute('SELECT * FROM ListPaths WHERE "_rowid_"=\''+str(RowPaths[Key])+'\';')
    List=list(Data)
    # print("Key: ",Key)
    # print("Path:",List[0][2])
    # b=input()
    return List[0][2]

def UpdatePath(Key,NewPath):
    # print("NewPath",NewPath)
    RowPaths=Dictionary()
    # PathDB="E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tools\Scripts\Database.db"
    PathDB="Scripts\Database.db"
    db = sqlite3.connect(PathDB)
    cursor = db.cursor()
    Comand='UPDATE "main"."ListPaths" SET "Path"=\''+NewPath+'\' WHERE "_rowid_"=\''+str(RowPaths[Key])+'\';'
    print("Comand",Comand)
    cursor.execute(Comand)
    db.commit()





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
    if len(PL1)==1:PL1=Shapefile.split("\\")
    # print(PL1)
    FileName=PL1[-1].split(".")[0]
    print(FileName)
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
        print("record",record,type(record))
        for i,r in enumerate(record):
            print(r)
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
    print(nx.info(G))
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
        print(Coords)
        # b=input()
        Info=nx.info(Gr['G'])+"\nNetwork Density: "+str(nx.density(Gr['G']))
        print(Info,type(Info))
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

    print("length:",len(BusStop_List))
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
        # print(Node)
        Xval=Node[0]
        Yval=Node[1]
        NumRouts=Node[2]
        Routes=Node[3]
        ContainedStops=Node[4]
        for Stop in ContainedStops:
            if idx not in StopToNode.keys():
                StopToNode[Stop]=idx
            else:
                print("WHAAAAAAAAAAAAAAAAAAAAAAAAAAT a crazy thing happend")
                b1=input()
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
        New_Edge=(StopToNode[edge[0]],StopToNode[edge[1]])
        LineProperties[New_Edge]=Edge_Properties['Line'][key]
        # print(key,type(key),Edge_Properties['Line'][key])
        # print("\t",edge[0],edge[1])
        # print("\t",StopToNode[edge[0]],"-",StopToNode[edge[1]])
        # print("\t\t",LineProperties[New_Edge])

    New_Edge_Properties={'Line':LineProperties}

    for edge in Edge_List:
        # print(edge,"\t",StopToNode[edge[0]],"-",StopToNode[edge[1]])
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
                Text=Text+'\t['+str(Coords[0])+','+str(Coords[1])+'],\n'
            else:
                Text=Text+'\t['+str(Coords[0])+','+str(Coords[1])+']\n'
        Text=Text+'],\n'
        Text=Text+'"type": "LineString"\n'+'},\n'
        Text=Text+'"id": "'+Iden+'"'
        return Text


    L=FormatLine(Line="10",Heading="10 North",Coordinates=[[-73.610016,45.525287],[-73.584541,45.513928],[-73.589173,45.509709]],Iden="1000000000001")
    # print(P)
    # print(Container(ListSegments=[L,P]))



def ExportGeoJsonPoints(ListOfPoints,PChar):
    # print(PChar)
    # b=input()

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
        Text=Text+'"geometry": {\n'+'"coordinates": ['+str(Coordinates[0])+','+str(Coordinates[1])+'],\n'
        Text=Text+'"type": "Point"\n        },\n        "id": "'+Iden+'"\n'
        return Text

    Keys=list(PChar.keys())
    # print("Keys:",Keys)
    # b=input()
    # print(ListOfPoints)
    # b=input()
    FormatedPoints=[]
    input_projection = Proj(init="epsg:32618")
    output_projection = Proj(init="epsg:4326")
    Iden=999999999999999
    for Point in ListOfPoints:
        Point=int(Point)
        if Point==0 and Iden>999999999999999:
            break
        TextProp='{"StopCode":'+str(Point)+","
        Iden=Iden+1
        # print(Point)
        # print(TextProp)
        # print()
        # for key in Keys:
            # print(key)
            # print(list(PChar[key].keys())[:20])
            # print(Point,type(Point))
            # print("#######################################################################################################\n"*3)
        for key in Keys:
            # Point=int(Point)
            # print("############################################\n"*3)
            # print("key:",key,type(key),end="\t")
            # print("Point",Point,type(Point))
            # print("############################################\n"*3)
            # print(list(PChar[key].keys())[0],type(list(PChar[key].keys())[0]))
            # print(PChar['Pos'].keys())
            # print(PChar[key],type(PChar[key]),"\n\n\n")
            if key =='Pos':
                new_x, new_y = transform(input_projection, output_projection, PChar[key][int(Point)][0], PChar[key][int(Point)][1])
                # new_x, new_y = transform(input_projection, output_projection, x, y)
                # print(Point,new_x, new_y)
                Coordinates=(new_x, new_y)
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
        # print(Coordinates,"\n\n\n")
        # print("-------------------------------------------------------------------")
        P=FormatPoint(TextProp=str(TextProp),Coordinates=Coordinates,Iden=str(Iden))
        FormatedPoints.append(P)
        # print(P)
        # b=input()
    # print(Container(ListSegments=FormatedPoints))
    files = [('GeoJson', '*.geojson'), 
    ('Text Document', '*.txt')] 
    Path = asksaveasfile(filetypes = files, defaultextension = files) 

    fw=open(Path.name,"w")
    fw.write(Container(ListSegments=FormatedPoints))
    fw.close


def ListToGeoJson(ListBusStops):
    
    ListofPoints=[]
    PropCharac={'Pos':{},'weigth':{},'Line':{}}
    for idx,Point in enumerate(ListBusStops):
        Point=list(Point)
        # print(Point,type(Point))
        ListofPoints.append(idx)
        PropCharac['Pos'][idx]=[Point[0],Point[1]]
        PropCharac['weigth'][idx]=Point[2]
        PropCharac['Line'][idx]=Point[3]

        # print(idx,'Pos',PropCharac['Pos'][idx],'weigth',PropCharac['weigth'][idx],'Line',PropCharac['Line'][idx])

    ExportGeoJsonPoints(ListOfPoints=ListofPoints,PChar=PropCharac)



def NetWorkToGeoJson(G):
    PointCharacteristics={}
    ListOfPoints=[]
    Cont=0
    for Node in G.nodes(data=True):
        Cont=Cont+1
        ListOfKeys=list(Node[1].keys())
        if Cont==1:
            break
        print("ListOfKeys",ListOfKeys)
        # b=input()


    for key in ListOfKeys:
        PointCharacteristics[key]={}
    for Node in G.nodes(data=True):
        NodeIndex=int(Node[0])
        ListOfPoints.append(int(Node[0]))
        Keys=Node[1].keys()
        if len(Keys)==0:
            break
        Dict=Node[1]
        # print(Dict)
        # print(type(Dict))
        # print(Dict.keys())
        for key in ListOfKeys:
            # print(Dict[key])

            PointCharacteristics[key][NodeIndex]=1
            PointCharacteristics[key][NodeIndex]=Dict[key]
        # print("######################################################\n"*3)
        # PointCharacteristics['Line'][int(Node[0])]=Node[1]['Line']
        # PointCharacteristics['Pos'][int(Node[0])]=Node[1]['Pos']
        # PointCharacteristics['weight'][int(Node[0])]=Node[1]['weight']
        # PointCharacteristics['ContainedStops'][int(Node[0])]=Node[1]['ContainedStops']
        # print(PointCharacteristics)
    # print(PointCharacteristics)

    # b=input()
    print("Calculating Centrality degree\n")

    degree_centrality = nx.degree_centrality(G)
    # PointCharacteristics['CenDeg']=degree_centrality
    PointCharacteristics['CenDeg']={}
    print(degree_centrality,"\nCentrality degree")
    # b=input()
    
    for key in degree_centrality:
        # print(key,type(key))
        # b=input()
        if type(key)== type(int()):
            PointCharacteristics['CenDeg'][key] = degree_centrality[key]
        if type(key)==type(float()):
            PointCharacteristics['CenDeg'][int(key)] = degree_centrality[key]
    # print(PointCharacteristics['CenDeg'],"\nCentrality")
    # b=input()
    try:
        LI=list(PointCharacteristics['CenDeg'].values())
        arr = np.array(LI)
        Ranges_DegCen=jenkspy.jenks_breaks(arr, nb_class=5)
        print("Ranges_DegCen",Ranges_DegCen,len(Ranges_DegCen))
        print("Min",min(LI))
        print("Max",max(LI))
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
        if type(key)==type(int()):
            PointCharacteristics['Clossnes'][key] =  closeness_centrality[key]*100
        if type(key)==type(float()):
            PointCharacteristics['Clossnes'][int(key)] =  closeness_centrality[key]*100

    try:
        LI=list(PointCharacteristics['Clossnes'].values())
        arr = np.array(LI)
        Ranges_ClosCen=jenkspy.jenks_breaks(arr, nb_class=5)
        print("Ranges_ClosCen",Ranges_ClosCen,len(Ranges_ClosCen))
        print("Min",min(LI))
        print("Max",max(LI))
        # b=input()
        PointCharacteristics['CatClossnes']={}
        print("crea di")
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
            if type(key)==type(int()):
                PointCharacteristics['Eigen'][key] = eigenvector_centrality[key]*100000
            if type(key)==type(float()):
                PointCharacteristics['Eigen'][int(key)] = eigenvector_centrality[key]*100000

        # print(PointCharacteristics['Eigen'])
        # b=input()
        LI=list(PointCharacteristics['Eigen'])
        arr = np.array(LI)
        Ranges_EgiCen=jenkspy.jenks_breaks(arr, nb_class=5)
        # print("Ranges_EgiCen",Ranges_EgiCen)

        print("Ranges_EgiCen",Ranges_EgiCen,len(Ranges_EgiCen))
        print("Min",min(LI))
        print("Max",max(LI))
        # b=input()
        PointCharacteristics['CatEigen']={}
        for key in PointCharacteristics['Eigen'].keys():
            print(key,PointCharacteristics['Eigen'][key])
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

    print("PointCharacteristics",PointCharacteristics.keys())
    print("start printing")

    ExportGeoJsonPoints(ListOfPoints=ListOfPoints,PChar=PointCharacteristics)


def SimpleNetworkToGeoJson(G):
    # G = nx.DiGraph()
    # G.__getattribute__
    NetWorkToGeoJson(G=G['G'])



def BusStops_Lines(Shapefile,CriteriaData):
    BusId=0
    sf = shapefile.Reader(Shapefile)
    if sf.shapeTypeName == 'POINT':
        print("Type is ok")
        fields = sf.fields
        # print(fields)
        Coordinates=[]
        BusLineRecords=[]
        LineList=[]
        LineDetails={}
        LineConections={}
        BusStopData={}
        print("step 1")

        # Step 1 The file is read, the index of the Field that contains the informations is extracted,
        # the record that contains the lines per station and coordinates are extracted and stored in 
        # separate variables
        for idx, field in enumerate(fields):
            
            # if field[0]==CriteriaData.NameFieldStop:
            #     IndexIdStopId=idx
            if field[0]==CriteriaData.NameFieldLines:
                IndexIdLines=idx
        print(fields[IndexIdLines][0],IndexIdLines)
        Records = sf.records()
        IndexIdLines-=1
        for Record in Records:
            RecordList=list(Record)
            BusLineRecords.append(RecordList[IndexIdLines])
        Shapes=sf.shapes()
        for shape in Shapes:
            for vertex in shape.points:
                Coordinates.append(vertex)

        print("step 2")
        # Step 2 the Coordinates and lines are aggregated to a single dictionary
        for idx, Lines in enumerate(BusLineRecords):
            BusStopData[idx]={"Lines":Lines.split(","),"Coords":Coordinates[idx]}
            # print(idx,BusStopData[idx]["Lines"],BusStopData[idx]["Coords"])
        for key in BusStopData:
            # print(key,BusStopData[key])
            for Line in BusStopData[key]["Lines"]:
                if Line in LineList:
                    pass
                else:
                    LineList.append(Line)
        LineList.sort()
    if "" in LineList:
        LineList.remove('')

    # for key in BusStopData:
    #     print(key,",",end="")
    # print()
    # b=input()
    print("step 3")
    print("step 4")
    # Data is transfered to the container by line
    for OutLine in LineList:
        # print("OutLine",OutLine)
        LineDetails[OutLine]={"RawDirectConections":0,"ConectingLines":[],"ListCoordinates":[],"ListDistance":[],"NumberStations":0}
        # b=input()
        for key in BusStopData:
            # b=input()
            if OutLine in BusStopData[key]["Lines"]:
                if BusStopData[key]['Coords'] in LineDetails[OutLine]["ListCoordinates"]:
                    pass
                else:
                    LineDetails[OutLine]["ListCoordinates"].append(BusStopData[key]['Coords'])
                    LineDetails[OutLine]["NumberStations"]+=1

            if OutLine in BusStopData[key]["Lines"] and len(BusStopData[key]["Lines"])>1:
                LineDetails[OutLine]["RawDirectConections"]+=1
                # print(BusStopData[key])
                # print("OutLine",OutLine,"-",BusStopData[key]["Lines"],len(BusStopData[key]["Lines"]),"RawDirectConections",LineDetails[OutLine]["RawDirectConections"])
                # print("Coords",BusStopData[key]["Coords"])
                # b=input()
                for InLine in BusStopData[key]["Lines"] :
                    if InLine =="":
                        continue
                    if InLine in LineDetails[OutLine]["ConectingLines"] or InLine == OutLine:
                        pass
                    else:
                        LineDetails[OutLine]["ConectingLines"].append(InLine)
    print("Step 5")
    for OutLine in LineList:
        ListCoord=LineDetails[OutLine]["ListCoordinates"]
        # print(ListCoord,len(ListCoord))

        for idx, Coord in enumerate(ListCoord):
            if idx == len(ListCoord):
                continue
            idx2=idx+1
            TemporaryDistList=[]
            for NextId in range(idx2,len(ListCoord)):
                DifX=ListCoord[idx][0]-ListCoord[NextId][0]
                DifY=ListCoord[idx][1]-ListCoord[NextId][1]
                Dist=math.sqrt((math.pow(DifX,2))+(math.pow(DifY,2)))
                # print(idx,"-",idx,"Coordinates X1:",ListCoord[idx][0],"Coordinates Y1:",ListCoord[idx][1])
                # print(idx,"-",NextId,"Coordinates X2:",ListCoord[NextId][0],"Coordinates Y2:",ListCoord[NextId][1])
                # print("Distance:",Dist)
                # print()
                if Dist >= CriteriaData.MinDistMask:
                    TemporaryDistList.append(Dist)
            if len(TemporaryDistList)>0:
                # print("Line",OutLine,"id",idx,min(TemporaryDistList))
                LineDetails[OutLine]["ListDistance"].append(min(TemporaryDistList))
            # b=input()

    for OutLine in LineList:
        print("Line:",OutLine,"Raw Conections:",LineDetails[OutLine]["RawDirectConections"],)
        print("Connecting Lines:",LineDetails[OutLine]["ConectingLines"],"N Con. Lines",len(LineDetails[OutLine]["ConectingLines"]))
        print("NumberStations",LineDetails[OutLine]["NumberStations"],"\t Length:",sum(LineDetails[OutLine]["ListDistance"]))
        print("ListCoordinates",LineDetails[OutLine]["ListCoordinates"],"Total:",len(LineDetails[OutLine]["ListCoordinates"]))
        print("ListDistance",LineDetails[OutLine]["ListDistance"],"Total:",len(LineDetails[OutLine]["ListDistance"]))
        print("·······································································································\n\n")


    print("There is a total of ", len(BusStopData), "Satations")

def BusStops_City(Shapefile,CriteriaData):
    BusId=0
    sf = shapefile.Reader(Shapefile)
    if sf.shapeTypeName == 'POINT':
        print("Type is ok")
        fields = sf.fields
        # print(fields)
        Coordinates=[]
        BusLineRecords=[]
        BusStopId=[]
        LineList=[]
        LineDetails={}
        LineConections={}
        BusStopData={}
        print("step 1")

        # Step 1 The file is read, the index of the Field that contains the informations is extracted,
        # the record that contains the lines per station and coordinates are extracted and stored in 
        # separate variables
        for idx, field in enumerate(fields):
            if field[0]==CriteriaData.NameFieldStop:
                IndexIdStopId=idx
            if field[0]==CriteriaData.NameFieldLines:
                IndexIdLines=idx
        # print(fields[IndexIdLines][0],IndexIdLines)
        Records = sf.records()
        IndexIdLines-=1
        IndexIdStopId-=1
        print("Records:")
        for Record in Records:
            RecordList=list(Record)
            BusLineRecords.append(RecordList[IndexIdLines])
            BusStopId.append(RecordList[IndexIdStopId])
            print(RecordList[IndexIdStopId],RecordList[IndexIdLines])
            # b=input()

        Shapes=sf.shapes()
        for shape in Shapes:
            for vertex in shape.points:
                Coordinates.append(vertex)
        # b=input()
        print("step 2")
        # Step 2 the Coordinates and lines are aggregated to a single dictionary
        for idx, Lines in enumerate(BusLineRecords):
            BusStopData[idx]={"Id_Stop":BusStopId[idx],"Lines":Lines.split(","),"Coords":Coordinates[idx]}
            # print(idx,BusStopData[idx]["Lines"],BusStopData[idx]["Coords"])
        for key in BusStopData:
            # print(key,BusStopData[key])
            for Line in BusStopData[key]["Lines"]:
                if Line in LineList:
                    pass
                else:
                    LineList.append(Line)
        LineList.sort()
    if "" in LineList:
        LineList.remove('')

    print("step 3")
    CityNodeDistnce={}
    ListOfAdjacent=[]
    CityDistances=[]
    for key in BusStopData:
        CityNodeDistnce[key]={"List":[],"MinDist":0,"MinNode":"","MaxDist":0,"MaxNode":"","NeigbourNodes":[],"AdjacentNodes":[]}
        print(key,"/",BusStopData[key])
        # if key ==len(BusStopData):
        #     continue
        key2=key+1
        Distances=[]
        DistanceName={}
        for NextKey in BusStopData:
        # for NextKey in range(key2,(len(BusStopData))):
            DifX=BusStopData[NextKey]["Coords"][0]-BusStopData[key]["Coords"][0]
            DifY=BusStopData[NextKey]["Coords"][1]-BusStopData[key]["Coords"][1]
            Dist=math.sqrt((math.pow(DifX,2))+(math.pow(DifY,2)))
            if Dist>0:
                # print("Dist",Dist,"\n\n")
                DistanceName[Dist]=BusStopData[NextKey]["Id_Stop"]
                Distances.append(Dist)
            # if NextKey ==30:
            #     b=input()
            if Dist<=CriteriaData.NeigbourDistance:
                CityNodeDistnce[key]["NeigbourNodes"].append([BusStopData[NextKey]["Id_Stop"],Dist])
            if Dist<=CriteriaData.AdjacentDistance and BusStopData[NextKey]["Lines"] != BusStopData[key]["Lines"]:
                print(key,Dist,"OutKey",BusStopData[key]["Lines"],"InKey",BusStopData[NextKey]["Lines"],BusStopData[NextKey]["Id_Stop"])
                # b=input()
                CityNodeDistnce[key]["AdjacentNodes"].append(BusStopData[NextKey]["Id_Stop"])
                ListOfAdjacent.append((key,NextKey))
        print("\t",CityNodeDistnce[key]["AdjacentNodes"])
        CityDistances.append(min(Distances))
        CityNodeDistnce[key]["MinDist"]=min(Distances)
        CityNodeDistnce[key]["MinNode"]=DistanceName[min(Distances)]
        CityNodeDistnce[key]["MaxDist"]=max(Distances)
        CityNodeDistnce[key]["MaxNode"]=DistanceName[max(Distances)]

    # print("Line List",LineList)
    # print("································································································")
    # print("································································································")
    # print("································································································")
    # print("ListOfAdjacent",ListOfAdjacent)
    # print("································································································")
    # print("································································································")
    # print("································································································")
    # # print("CityDistances",CityDistances)
    # print("································································································")
    # print("································································································")
    # print("································································································")
    # print("Average minimum distance between nodes at a city level",statistics.mean(CityDistances))
    # print("································································································")
    # print("································································································")
    # print("································································································")
    # print("There is a total of ", len(BusStopData), "Satations")
    # print("································································································")
    # print("································································································")
    # print("································································································")

def StreetReading(Shapefile):
    StreetData=[]
    sf = shapefile.Reader(Shapefile)
    fields = sf.fields
    Records = sf.records()
    Shapes=sf.shapes()
    StreetName=[]
    for idx, field in enumerate(fields):
        if field[0]=="name":
            IndexIdStopId=idx-1
    for Record in Records:
        RecordList=list(Record)
        # print(RecordList[IndexIdStopId])
        StreetName.append(RecordList[IndexIdStopId])
    Cont=-1
    for shape in Shapes:
        StreetData.append({"Name":StreetName[Cont],"Extreme":StreetSegment,"Segments":[]})
        Cont+=1
        # print(shape,"..........................",StreetName[Cont])
        CoordX=[]
        CoordY=[]
        ListOfVertex=list(shape.points)
        # print(ListOfVertex)
        AllCoordsX=[]
        AllCoordsY=[]
        for Coords in ListOfVertex:
            AllCoordsX.append(Coords[0])
            AllCoordsY.append(Coords[1])
        # StreetData[-1]["Extreme"]=[[min(AllCoordsX),min(AllCoordsY)],[max(AllCoordsX),max(AllCoordsY)]]
        M,B,CoordX0,CoordX1,CoordY0,CoordY1=CalculateFormula(Coords=[[min(AllCoordsX),max(AllCoordsX)],[min(AllCoordsY),max(AllCoordsY)]])
        StreetData[-1]["Extreme"].M=M
        StreetData[-1]["Extreme"].B=B
        StreetData[-1]["Extreme"].CoordX0=CoordX0
        StreetData[-1]["Extreme"].CoordX1=CoordX1
        StreetData[-1]["Extreme"].CoordY0=CoordY0
        StreetData[-1]["Extreme"].CoordY1=CoordY1
        for vertex in shape.points:
            Segment=StreetSegment
            
            # print(vertex)
            CoordX.append(vertex[0])
            CoordY.append(vertex[1])
            if len(CoordX)==2:
                # print("Calculating")
                if CoordX[0]==CoordX[1]:
                    continue
                StreetData[-1]["Segments"].append(Segment)
                M,B,CoordX0,CoordX1,CoordY0,CoordY1=CalculateFormula(Coords=[CoordX,CoordY])
                StreetData[-1]["Segments"][-1].M=M
                StreetData[-1]["Segments"][-1].B=B
                StreetData[-1]["Segments"][-1].CoordX0=CoordX0
                StreetData[-1]["Segments"][-1].CoordX1=CoordX1
                StreetData[-1]["Segments"][-1].CoordY0=CoordY0
                StreetData[-1]["Segments"][-1].CoordY1=CoordY1
                CoordX=[]
                CoordY=[]
                CoordX.append(vertex[0])
                CoordY.append(vertex[1])
    print(len(Shapes))
    print(len(StreetName))
    print(type(StreetData))

    for Street in StreetData:
        print(Street["Name"])
        print("M",Street["Extreme"].M)
        print("B",Street["Extreme"].B)
        print("CoordX0",Street["Extreme"].CoordX0)
        print("CoordX1",Street["Extreme"].CoordX1)
        print("CoordY0",Street["Extreme"].CoordY0)
        print("CoordY1",Street["Extreme"].CoordY1)
        for Segment in Street["Segments"]:
            print("\tM:",Segment.M)
            print("\tB:",Segment.B)
            print("\tCoordX0:",Segment.CoordX0)
            print("\tCoordX1:",Segment.CoordX1)
            print("\tCoordY0:",Segment.CoordY0)
            print("\tCoordY1:",Segment.CoordY1)
            print()
        print()
    return StreetData

def StreetReadingv2(Shapefile):
    print("..street reading..")
    from ClassCollection import Segment
    StreetData=[]
    sf = shapefile.Reader(Shapefile)
    fields = sf.fields
    Records = sf.records()
    Shapes=sf.shapes()
    StreetName=[]
    RecordCoords=[]
    for idx, field in enumerate(fields):
        if field[0]=="name":
            IndexIdStopId=idx-1
    for Record in Records:
        RecordList=list(Record)
        # print(RecordList)
        # print(RecordList[IndexIdStopId])
        StreetName.append(RecordList[IndexIdStopId])
        RecordCoords.append([RecordList[2],RecordList[3],RecordList[4],RecordList[5]])
    Cont=-1
    for shape in Shapes:
        Cont+=1
        StreetData.append({"Name":StreetName[Cont],"Extreme":Segment(),"Segments":[]})
        print("\n",shape,"..........................",StreetName[Cont],Cont)
        CoordX=[]
        CoordY=[]
        ListOfVertex=list(shape.points)
        print(ListOfVertex)
        AllCoordsX=[]
        AllCoordsY=[]
        for Coords in ListOfVertex:
            AllCoordsX.append(Coords[0])
            AllCoordsY.append(Coords[1])
        StreetData[Cont]["Extreme"].CoordXA=min(AllCoordsX)
        StreetData[Cont]["Extreme"].CoordXB=max(AllCoordsX)
        StreetData[Cont]["Extreme"].CoordYA=min(AllCoordsY)
        StreetData[Cont]["Extreme"].CoordYB=max(AllCoordsY)
        StreetData[Cont]["Coords"]=RecordCoords[Cont]
        for vertex in shape.points:
            # print(vertex)
            CoordX.append(vertex[0])
            CoordY.append(vertex[1])
            if len(CoordX)==2:
                # print("Calculating")
                if CoordX[0]==CoordX[1]:
                    CoordX.pop()
                    CoordY.pop()
                    continue
                StreetData[Cont]["Segments"].append(Segment())
                StreetData[Cont]["Segments"][-1].CoordXA=CoordX[0]
                StreetData[Cont]["Segments"][-1].CoordXB=CoordX[1]
                StreetData[Cont]["Segments"][-1].CoordYA=CoordY[0]
                StreetData[Cont]["Segments"][-1].CoordYB=CoordY[1]
                CoordX=[]
                CoordY=[]
                CoordX.append(vertex[0])
                CoordY.append(vertex[1])
    for idx,st in enumerate(StreetData):
        print(idx,st["Name"])
        # for Seg in StreetData[Cont]["Segments"]:
        #     print (Seg.CoordXA,Seg.CoordYA)
        #     print (Seg.CoordXB,Seg.CoordYB)
    return StreetData

def StreetReadingv3(Shapefile):
    print("..street reading..")
    from ClassCollection import Segment
    from ClassCollection import Street
    StreetData=[]
    sf = shapefile.Reader(Shapefile)
    fields = sf.fields
    Records = sf.records()
    Shapes=sf.shapes()
    StreetName=[]
    RecordCoords=[]
    for idx, field in enumerate(fields):
        if field[0]=="name":
            IndexIdStopId=idx-1
    for Record in Records:
        RecordList=list(Record)
        # print(RecordList[IndexIdStopId])
        StreetName.append(RecordList[IndexIdStopId])
        # RecordCoords.append([RecordList[2],RecordList[3],RecordList[4],RecordList[5]])
    Cont=-1
    print(StreetName)
    for shape in Shapes:
        Cont+=1
        StObject=Street()
        StObject.Name=StreetName[Cont]
        # print("\n",Cont,shape,"..........................",StreetName[Cont],"---",StObject.Name)
        CoordX=[]
        CoordY=[]
        ListOfVertex=list(shape.points)
        # print("ListOfVertex",len(ListOfVertex),ListOfVertex)
        AllCoordsX=[]
        AllCoordsY=[]
        for vertex in shape.points:
            AllCoordsX.append(vertex[0])
            AllCoordsY.append(vertex[1])
        StObject.CoordXA=ListOfVertex[0][0]
        StObject.CoordYA=ListOfVertex[0][1]
        StObject.CoordXB=ListOfVertex[-1][0]
        StObject.CoordYB=ListOfVertex[-1][1]
        # print(StObject.CoordXA,StObject.CoordYA,StObject.CoordXB,StObject.CoordYB)
        for idx, Vertex in enumerate(ListOfVertex):
            if idx > 0:
                # print("XA:",ListOfVertex[idx-1][0],"YA:",ListOfVertex[idx-1][1])
                # print("XB:",ListOfVertex[idx][0],"YB:",ListOfVertex[idx][1])
                # print("_______________________________")
                Seg=Segment()
                Seg.CoordXA=ListOfVertex[idx-1][0]
                Seg.CoordYA=ListOfVertex[idx-1][1]
                Seg.CoordXB=ListOfVertex[idx][0]
                Seg.CoordYB=ListOfVertex[idx][1]
                StObject.Segments.append(Seg)
        StreetData.append(StObject)
    return StreetData

def CalculateFormula(Coords):
    CoordX=Coords[0]
    CoordY=Coords[1]
    CoordX0=CoordX[0]
    CoordX1=CoordX[1]
    CoordY0=CoordY[0]
    CoordY1=CoordY[1]
    M=(CoordY[1]-CoordY[0])/(CoordX[1]-CoordX[0])
    # print("\t",CoordY[1],"-",CoordY[0],"=",M)
    # print("\t",CoordX[1],"-",CoordX[0])
    B=CoordY[1]-(M*CoordX[1])
    # print("B",B)
    return M,B,CoordX0,CoordX1,CoordY0,CoordY1


def DestroyProcessFiles(Path):
    for filename in os.listdir(Path):
        file_path = os.path.join(Path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def NetworkNodeEdgeRatio(Shapefile,CriteriaData):
    LineRecords=[]
    NumEdges=[]
    IndRatio=[]
    sf = shapefile.Reader(Shapefile)
    Records = sf.records()
    fields = sf.fields
    for idx, field in enumerate(fields):
        if field[0]==CriteriaData.NameFieldLines:
            IndexIdLines=idx-1

    for Record in Records:
        RecordList=list(Record)
        LineRecords.append(RecordList[IndexIdLines])
        NumEdges.append(len(RecordList[IndexIdLines]))
        IndRatio.append(1/(len(RecordList[IndexIdLines])))
    Ratio=(sum(IndRatio)/len(IndRatio))
    print("Ratio",Ratio)
    return Ratio

def Density(ListSystems,ListWeigths,Area):
    NumberFeatures=[]
    for System in ListSystems:
        FullPathIn=System.split("\\")
        print(System,"-",FullPathIn[-1])
        PathIn=FullPathIn[-1].split(".")
        OutShp=Paths.TempoFolder()+PathIn[0]+"_Clipped.shp"
        print(OutShp)
        ClipPointFeature(Area=Area,OutPut=OutShp,InPut=System)
        NumberFeatures.append(FeatCount(PathSHP=OutShp))
    DestroyProcessFiles(Path=Paths.TempoFolder())
    print("NumberFeatures",NumberFeatures)


def Distance(P1,P2):
    PX=math.pow(decimal.Decimal(P2[0])-decimal.Decimal(P1[0]),2)
    PY=math.pow(decimal.Decimal(P2[1])-decimal.Decimal(P1[1]),2)
    # print("X2:",P2[0],"X1:",P1[0],"D:",math.sqrt(PX+PY))
    # print("Y2:",P2[1],"y1:",P1[1])
    # print()
    return math.sqrt(PX+PY)

def DistanceTest(Var,List):
    Cond=0
    for P in List:
        D=Distance(P1=Var,P2=P)
        if D < 2:
            Cond=1
    if Cond==1:
        return True
    else:
        return False
 
def StreetNodeEdgeRatio(Shapefile):
    print("..StreetNodeEdgeRatio..")
    StreetData=StreetReadingv3(Shapefile=Shapefile)
    print("..StreetNodeEdgeRatio..")
    SegmentCol=[]
    Intersections=[]
    IntersectionsRep={}
    Index=0
    RatioList=[]
    for St1 in StreetData:
        print(St1.Name)
        for St2 in StreetData:
            if St1==St2:
                continue
            for ix1, Seg1 in enumerate(St1.Segments):
                for ix2, Seg2 in enumerate(St2.Segments):
                    pt= Intersect(Seg1XA=Seg1.CoordXA,Seg1YA=Seg1.CoordYA,Seg1XB=Seg1.CoordXB,Seg1YB=Seg1.CoordYB,
                                Seg2XA=Seg2.CoordXA,Seg2YA=Seg2.CoordYA,Seg2XB=Seg2.CoordXB,Seg2YB=Seg2.CoordYB)
                    if pt is None:
                        pass
                        # print("No intersection")
                    else:
                        if pt in Intersections:
                            pass
                            # print("-------")
                        elif DistanceTest(Var=pt,List=Intersections):
                            print ("Dist min found!!!!!!!!!!!!!")
                        else:
                            print("\t.......",St1.Name,"-",St2.Name,pt)
                            # print("Seg1XA",Seg1.CoordXA,"Seg1YA",Seg1.CoordYA,"Seg1XB",Seg1.CoordXB,"Seg1YB",Seg1.CoordYB,
                            #     "\nSeg2XA",Seg2.CoordXA,"Seg2YA",Seg2.CoordYA,"Seg2XB",Seg2.CoordXB,"Seg2YB",Seg2.CoordYB,"\n")
                            Intersections.append(pt)
                            # print()
                            Check=[2,2]
                            D=Distance(P1=pt,P2=(St1.CoordXA,St1.CoordYA))
                            # print("D1A",D,St1.Name,St1.CoordXA,St1.CoordYA)
                            if D <5:
                                Check[0]=1
                            D=Distance(P1=pt,P2=(St1.CoordXB,St1.CoordYB))
                            # print("D1B",D,St1.Name,St1.CoordXB,St1.CoordYB,"-",Seg1.CoordYB)
                            if D <5:
                                Check[0]=1
                            D=Distance(P1=pt,P2=(St2.CoordXA,St2.CoordYA))
                            # print("D2A",D,St2.Name,St2.CoordXA,St1.CoordYA)
                            if D <5:
                                Check[1]=1
                            D=Distance(P1=pt,P2=(St2.CoordXB,St2.CoordYB))
                            # print("D2B",D,St2.Name)
                            if D <5:
                                Check[1]=1
                            print ("\t\tCheck",Check)
                            RatioList.append(1/sum(Check))
    print(sum(RatioList)/len(RatioList))
    # print(Fraction(sum(RatioList)/len(RatioList)))
    print("List of intersections:",len(Intersections))
    print(Intersections)

class BusStop:
    def __init__(self,Id="",CoordX=0,CoordY=0,Routes=[],Cluster=[]):
        self.Id=Id
        self.CoordX=CoordX
        self.CoordY=CoordY
        self.Routes=[]
        self.Cluster=[]

class Line:
    def __init__(self,Id=0,Name="",Nodes=[]):
        self.Id=Id
        self.Name=Name
        self.Nodes=Nodes

class Node:
    def __init__(self,NodeId=0,BusStopIdS=[],CoordX=0,CoordY=0,Routes=[]):
        self.NodeId=NodeId
        self.BusStopIdS=BusStopIdS
        self.CoordX=CoordX
        self.CoordY=CoordY
        self.Routes=Routes




def CalculateVecinityBusStops(Shapefile,FieldId,Routes):
    ListBusStops=[]
    sf = shapefile.Reader(Shapefile)
    Shapes=sf.shapes()
    Records = sf.records()
    fields = sf.fields
    ## Show fields in shape file
    # for idx, fi in enumerate(fields):
    #     print(idx,fi)
    # print( fields[FieldId[1]+1][0])
    # print( fields[Routes[1]+1][0])
    # b=input()
    for idx,record in enumerate(Records):
        BusStopObj=BusStop()
        RecordList=list(record)
        # print(RecordList)
        BusStopObj.Id=RecordList[FieldId[1]]
        # print("Routes[1]",Routes[1])
        # print("RecordList[Routes[1]]",Routes[1],RecordList[Routes[1]],type(RecordList[Routes[1]]))
        BusStopObj.Routes=RecordList[Routes[1]].split(",")
        # b=input()
        # print(BusStopObj.Id,BusStopObj.Routes)
        ListBusStops.append(BusStopObj)
    # print( Records)
    for idx,shape in enumerate(Shapes):
        # print(shape)
        for vertex in shape.points:
            # print("\t",vertex)
            ListBusStops[idx].CoordX=vertex[0]
            ListBusStops[idx].CoordY=vertex[1]
    # for Bs in ListBusStops:
    #     print(Bs.Id,Bs.CoordX,Bs.CoordY,Bs.Routes)
    return ListBusStops
    # Distance(P1,P2)

def AgregateTransitNetwork(ListBusStops,Range):
    # datetime object containing current date and time
    now1 = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now1.strftime("%d%m%Y-%H.%M.%S")
    print("date and time =", dt_string)
    EvaluatedBusStops=[]
    for Bs1 in ListBusStops:
        ListDist=[]
        KeyListDist={}
        for Bs2 in ListBusStops:
            if Bs1 == Bs2:
                continue
            # elif Bs2 in EvaluatedBusStops:
            #     continue
            else:
                D=Distance(P1=[Bs1.CoordX,Bs1.CoordY],P2=[Bs2.CoordX,Bs2.CoordY])
                ListDist.append(D)
                if D <= Range:
                    Bs1.Cluster.append(Bs2)
                KeyListDist[(D,Bs1.Id)]=Bs2.Id
                # print(Bs1.Id,Bs2.Id,D)
        # print("Bs1:",Bs1.Id,KeyListDist[(min(ListDist),Bs1.Id)],"-",min(ListDist))
            # ListDist[(Bs1.Id,Bs2)]
        EvaluatedBusStops.append(Bs1)
            # print(D)
    # datetime object containing current date and time
    now2 = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now2.strftime("%d%m%Y-%H.%M.%S")
    print("date and time =", dt_string)
    RevisedNodes=[]

    # ExitFile=r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tools\Result"+str(dt_string)+".txt"
    # f = open(ExitFile, "a")
    Var="X,Y,W\n"
    # f.write(Var)
    Listb=[]
    ExitValues=[]
    # for Bs in ListBusStops:
    #     print(Bs.Routes)

    for Bs1 in ListBusStops:
        if Bs1 in Listb:
            pass
            # print("next")
        else:
            # print("Id",Bs1.Id,"Len",len(Bs1.Cluster),"X:",Bs1.CoordX,"\tY:",Bs1.CoordY,"          Routes",Bs1.Routes)
            # print("Appends", end= " ")
            SumCX=0
            SumCY=0
            SumRoutes=0
            StopCode=[Bs1.Id]
            RouteCol=Bs1.Routes
            for BsC in Bs1.Cluster:
                Listb.append(BsC)
                StopCode.append(BsC.Id)
                SumCX=SumCX+BsC.CoordX
                SumCY=SumCY+BsC.CoordY
                SumRoutes=SumRoutes+len(BsC.Routes)
                RouteCol=RouteCol+BsC.Routes
                print("..",BsC.Id,"..", end="\t")
            ACoordX=(Bs1.CoordX+SumCX)/(len(Bs1.Cluster)+1)
            ACoordY=(Bs1.CoordY+SumCY)/(len(Bs1.Cluster)+1)
            Aroutes=SumRoutes+len(Bs1.Routes)
            # print("X:",ACoordX,"\tY:",ACoordY,"             # Routes",Aroutes)
            Var=str(ACoordX)+","+str(ACoordY)+","+str(Aroutes)+","+str(RouteCol)+"\n"
            ExitValues.append([ACoordX,ACoordY,Aroutes,RouteCol,StopCode])
            # RouteCol=[]
            print()
            # print("===========================================")
            # b=input()
            # f.write(Var)
    # f.close()
    # for Node in ExitValues:
    #     print(Node)
    return ExitValues

def ReadTransitNetwork(ListBusStops,Range):
    # datetime object containing current date and time
    now1 = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now1.strftime("%d%m%Y-%H.%M.%S")
    print("date and time =", dt_string)
    EvaluatedBusStops=[]
    for Bs1 in ListBusStops:
        ListDist=[]
        KeyListDist={}
        for Bs2 in ListBusStops:
            if Bs1 == Bs2:
                continue
            # elif Bs2 in EvaluatedBusStops:
            #     continue
            else:
                D=Distance(P1=[Bs1.CoordX,Bs1.CoordY],P2=[Bs2.CoordX,Bs2.CoordY])
                ListDist.append(D)
                if D <= Range:
                    Bs1.Cluster.append(Bs2)
                KeyListDist[(D,Bs1.Id)]=Bs2.Id
                # print(Bs1.Id,Bs2.Id,D)
        # print("Bs1:",Bs1.Id,KeyListDist[(min(ListDist),Bs1.Id)],"-",min(ListDist))
            # ListDist[(Bs1.Id,Bs2)]
        EvaluatedBusStops.append(Bs1)
            # print(D)
    # datetime object containing current date and time
    now2 = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now2.strftime("%d%m%Y-%H.%M.%S")
    print("date and time =", dt_string)
    RevisedNodes=[]

    ExitFile=r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tools\Result"+str(dt_string)+".txt"
    f = open(ExitFile, "a")
    Var="X,Y,W\n"
    f.write(Var)
    Listb=[]
    ExitValues=[]
    # for Bs in ListBusStops:
    #     print(Bs.Routes)

    for Bs1 in ListBusStops:
        if Bs1 in Listb:
            pass
            # print("next")
        else:
            print("Id",Bs1.Id,"Len",len(Bs1.Cluster),"X:",Bs1.CoordX,"\tY:",Bs1.CoordY,"          Routes",Bs1.Routes)
            print("Appends", end= " ")
            SumCX=0
            SumCY=0
            SumRoutes=0
            RouteCol=Bs1.Routes
            for BsC in Bs1.Cluster:
                Listb.append(BsC)
                SumCX=SumCX+BsC.CoordX
                SumCY=SumCY+BsC.CoordY
                SumRoutes=SumRoutes+len(BsC.Routes)
                RouteCol=RouteCol+BsC.Routes
                print("..",BsC.Id,"..", end="\t")
            ACoordX=(Bs1.CoordX+SumCX)/(len(Bs1.Cluster)+1)
            ACoordY=(Bs1.CoordY+SumCY)/(len(Bs1.Cluster)+1)
            Aroutes=SumRoutes+len(Bs1.Routes)
            print("X:",ACoordX,"\tY:",ACoordY,"             # Routes",Aroutes)
            Var=str(ACoordX)+","+str(ACoordY)+","+str(Aroutes)+","+str(RouteCol)+"\n"
            ExitValues.append([ACoordX,ACoordY,Aroutes,RouteCol])
            # RouteCol=[]
            print()
            # print("===========================================")
            # b=input()
            f.write(Var)
    f.close()
    # for Node in ExitValues:
    #     print(Node)
    return ExitValues



def ReadFieldNames(Shapefile):
    sf = shapefile.Reader(Shapefile)
    fields = sf.fields 
    print(type(fields),len(fields))
    return fields


def SimpleListToNodeList(ListofNodes):
    ListObjNodes=[]
    for Node in ListofNodes:
        NodObj=BusStop()
        NodObj.CoordX=Node[0]
        NodObj.CoordY=Node[1]
        NodObj.Cluster=[*range(1,Node[2]+1,1)]
        NodObj.Routes=Node[3]
        ListObjNodes.append(NodObj)
    return ListObjNodes

def LineBuilder(LoN):
    print("-----------------------")
    ListofLines=[]
    for Node in LoN:
        ListofLines=ListofLines+Node.Routes
    NewList=list(set(ListofLines))
    # print(NewList)
    ListofLines=[]
    for TextLine in NewList:
        ListofNodesInLine=[]
        for Node in LoN:
            # print("Node.Rotues",type(Node),Node.Routes,type(Node.Routes))
            if TextLine in Node.Routes:
                ListofNodesInLine.append(Node)
        LineObj=Line()
        LineObj.Nodes=ListofNodesInLine
        LineObj.Id=TextLine
        ListofLines.append(LineObj)
        print(LineObj.Id,"############",LineObj.Nodes)





def Intersect(Seg1XA,Seg1YA,Seg1XB,Seg1YB,Seg2XA,Seg2YA,Seg2XB,Seg2YB):
    Seg1XA=int(Seg1XA)
    Seg1YA=int(Seg1YA)
    Seg1XB=int(Seg1XB)
    Seg1YB=int(Seg1YB)
    Seg2XA=int(Seg2XA)
    Seg2YA=int(Seg2YA)
    Seg2XB=int(Seg2XB)
    Seg2YB=int(Seg2YB)
        
    if Seg1XA== Seg2XA and Seg1YA== Seg2YA and Seg1XB== Seg2XB and Seg1YB== Seg2YB:
        return None

    else:
        if (int(Seg1XB)-int(Seg1XA))==0:
            Seg1XB=Seg1XB+1
            Seg1XA=Seg1XA-1
        if (int(Seg2XB)-int(Seg2XA))==0:
            Seg2XB=Seg2XB-1
            Seg2XA=Seg2XA+1
        IntersectCoords=[]
        CalSeg2YValues=[]
        Line1Coords=[]
        Line2Coords=[]
        M1=(int(Seg1YB)-int(Seg1YA))/(int(Seg1XB)-int(Seg1XA))
        B1=int(int(Seg1YB)-(M1*Seg1XB))

        M2=(int(Seg2YB)-int(Seg2YA))/(int(Seg2XB)-int(Seg2XA))
        B2=int(int(Seg2YB)-(M2*Seg2XB))
        ######################

        if Seg2XA > Seg2XB:
            # print("Seg2XA > Seg2XB")
            for x in range(int(Seg2XB),int(Seg2XA)):
                C=int((M2*x)+B2)
                Line2Coords.append([x,C])
        else:                      
            # print("Seg2XB > Seg2XA")
            for x in range(int(Seg2XA),int(Seg2XB)):
                C=int((M2*x)+B2)
                Line2Coords.append([x,C])

        if Seg1XA > Seg1XB:
            # print("Seg1XA > Seg1XB")
            for x in range(int(Seg1XB),int(Seg1XA)):
                CalYVal=int((M1*x)+B1)
                Line1Coords.append([x,CalYVal])
        else:
            for x in range(int(Seg1XA),int(Seg1XB)):
                CalYVal=int((M1*x)+B1)
                Line1Coords.append([x,CalYVal])

        for L1 in Line1Coords:
            for L2 in Line2Coords:
                D=Distance(P1=L1,P2=L2)
                # if D <5:
                #     print(L1,L2,D)
                if D<2.5:
                    # print(Seg1XA,Seg1YA,Seg1XB,Seg1YB,"|",Seg2XA,Seg2YA,Seg2XB,Seg2YB)
                    # print("Intersection!!!",L1,L2,min(Line1Coords),min(Line2Coords))
                    if L1>L2:
                        return L1
                    if L2>L1:
                        return L2




def ActionSelect(Config,Entry):
    global DataBucket
    print(Config["City"])
    print(DataBucket)

    if Config['Command']=='GetShpPath':
            # print("hello")
            name = askopenfilename(initialdir=r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tools\SampleData",
                            filetypes =(("Shape File", "*.shp"),("All Files","*.*")),
                            title = "Choose a file."
                            )
            Entry.insert(0,name)
    print("name",name)
    DataBucket["Centroid"][Config["City"]]={}
    DataBucket["Centroid"][Config["City"]]['Path']=name
    return name


def PathEntry(Frame,Geom,Config):
    FrameElemento=ttk.LabelFrame(Frame,height = Geom['Sizes']['Hei'], width =Geom['Sizes']['Wid'],text =Config['TitleFrame'])
    FrameElemento.place(x=int(Geom['Coords']['X']), y=Geom['Coords']['Y'], anchor=W)

    EntryElement= ttk.Entry(FrameElemento,width=70)
    EntryElement.place(x=100, y=25, anchor=W)
    EntryElement.delete(0, END)
    EntryElement.insert(0,"")

    LabelElement = Label(FrameElemento, text="", font='Helvetica 12')
    LabelElement.place(x=550, y=25, anchor=W)

    button=ttk.Button(FrameElemento,text="Open")
    button.config(command=partial(ActionSelect,Config,EntryElement))
    button.place(x=10, y=25, anchor=W)


def PathSHP(Frame,Geom,Config):
    # Geom={'Coords':{'X':30,'Y':(Yval)},'Sizes':{'Hei':90,'Wid':650}}
    # Config={"City":i,'TitleFrame':'City '+str(i)+' - Area of the City','Command':'GetShpPath','action':'Centroid'}
    Path=''
    def Path():
        name = askopenfilename(initialdir=r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tools\SampleData",
                            filetypes =(("Shape File", "*.shp"),("All Files","*.*")),
                            title = "Choose a file.")
        Path=name
        print(Path)
        print(Config['Key'])
        print("#################################################")
        UpdatePath(Key=Config['Key'],NewPath=name)
        if len(name)>71:
            name=name[-65:]
            pass
        EntryElement.insert(0,name)
        print("Internal 1",Path)
        # return Path

    FrameElement=ttk.LabelFrame(Frame,height = Geom['Sizes']['Hei'], width =Geom['Sizes']['Wid'],text =Config['TitleFrame'])
    FrameElement.place(x=int(Geom['Coords']['X']), y=Geom['Coords']['Y'], anchor=W)
    EntryElement= ttk.Entry(FrameElement,width=70)
    EntryElement.place(x=100, y=25, anchor=W)
    EntryElement.delete(0, END)
    EntryElement.insert(0,"")
    Button=ttk.Button(FrameElement,text="Open")
    Button.config(command=(Path))
    Button.place(x=10, y=25, anchor=W)
    print("Internal 2",Path)
    # return Path



def PathEntryName(Frame,Geom,Config):
    global DataBucket
    FrameElemento=ttk.LabelFrame(Frame,height = Geom['Sizes']['Hei'], width =Geom['Sizes']['Wid'],text =Config['TitleFrame'])
    FrameElemento.place(x=int(Geom['Coords']['X']), y=Geom['Coords']['Y'], anchor=W)

    EntryElement= ttk.Entry(FrameElemento,width=70)
    EntryElement.place(x=100, y=40, anchor=W)
    EntryElement.delete(0, END)
    EntryElement.insert(0,"")

    EntryName= ttk.Entry(FrameElemento,width=70)
    EntryName.place(x=100, y=15, anchor=W)
    # EntryName.delete(0, END)
    # EntryName.insert(0,"")

    LabelElement = Label(FrameElemento, text="", font='Helvetica 12')
    LabelElement.place(x=550, y=40, anchor=W)

    button=ttk.Button(FrameElemento,text="Open")
    button.config(command=partial(ActionSelect,Config,EntryElement))
    button.place(x=10, y=40, anchor=W)

    def SeltName(buttonName):
        global CityNames
        Var=EntryName.get()
        CityNames.append(Var)
        print("Config[City",Config["City"])
        # DataBucket["Centroid"][Config["City"]]['CityName']=Var
        FrameElemento.config(text ="City "+str(Config["City"])+" - Area for "+Var)
        print(DataBucket)
        buttonName.config(state=DISABLED)

    buttonName=ttk.Button(FrameElemento,text="Set Name")
    buttonName.config(command=partial(SeltName,buttonName))
    buttonName.place(x=10, y=15, anchor=W)

def NodeRelevanceTab(frame):

    ComboNodeImp1Fid= ttk.Combobox(frame)
    ComboNodeImp1Routes= ttk.Combobox(frame)
    NewList1=[]

    ComboNodeImp2Fid= ttk.Combobox(frame)
    ComboNodeImp2Routes= ttk.Combobox(frame)
    NewList2=[]

    def ReqFields1():
        print("\n"*2)
        print(".................we get into the Fields 1........................")
        P1=RearPaths(Key='Importance1')
        print(P1)
        if P1=='':
            return None
        List1=ReadFieldNames(Shapefile=P1)
        # print(List1)
        print(P1)
        for elment in List1:
            print("----------------------------------------------------------------------------",elment)
            NewList1.append(elment[0])
        ComboNodeImp1Fid.config(width=17,values=NewList1)
        ComboNodeImp1Fid.place(x=120,y=140)
        labelImp1Fid = Label(frame, text="Field with Node ID", font='Helvetica 12')
        labelImp1Fid.place(x=120, y=120, anchor=W)
        ComboNodeImp1Routes.config(width=17,values=NewList1)
        ComboNodeImp1Routes.place(x=280,y=140)
        labelImp1Routes = Label(frame, text="Field with Routes/Lines", font='Helvetica 12')
        labelImp1Routes.place(x=280, y=120, anchor=W)

    def ReqFields2():
        print("\n"*2)
        print(".................we get into the Fields 2........................")
        P2=RearPaths(Key='Importance2')
        print(P2)
        if P2=='':
            return None
        List2=ReadFieldNames(Shapefile=P2)
        # print(List2)
        print(P2)
        for elment in List2:
            print("----------------------------------------------------------------------------",elment)
            NewList2.append(elment[0])
        ComboNodeImp2Fid.config(width=17,values=NewList2)
        ComboNodeImp2Fid.place(x=120,y=340)
        labelImp2Fid = Label(frame, text="Field with Node ID", font='Helvetica 12')
        labelImp2Fid.place(x=120, y=320, anchor=W)
        ComboNodeImp2Routes.config(width=17,values=NewList2)
        ComboNodeImp2Routes.place(x=280,y=340)
        labelImp2Routes = Label(frame, text="Field with Routes/Lines", font='Helvetica 12')
        labelImp2Routes.place(x=280, y=320, anchor=W)

    def RunAnalaysis():
        print(RearPaths(Key='Importance1'))
        InputValFid1=int(ComboNodeImp1Fid.current())-1
        InputValFLi1=int(ComboNodeImp1Routes.current())-1
        print("ComboNodeImp1Fid   ",ComboNodeImp1Fid.current(),InputValFid1)
        print("ComboNodeImp1Routes",ComboNodeImp1Routes.current(),InputValFLi1)
        print(NewList1,"\n",NewList1[int(ComboNodeImp1Fid.current())],"\n",NewList1[int(ComboNodeImp1Routes.current())])
        P1=RearPaths(Key='Importance1')
        print(P1)
        print(ReadFieldNames(Shapefile=P1))
        print(".................................................................................................")

        print("\n"*3)
        print(RearPaths(Key='Importance2'))
        InputValFid2=int(ComboNodeImp2Fid.current())-1
        InputValFLi2=int(ComboNodeImp2Routes.current())-1
        print("ComboNodeImp2Fid   ",ComboNodeImp2Fid.current(),InputValFid2)
        print("ComboNodeImp2Routes",ComboNodeImp2Routes.current(),InputValFLi2)
        print(NewList2,"\n",NewList2[int(ComboNodeImp2Fid.current())],"\n",NewList2[int(ComboNodeImp2Routes.current())])
        P2=RearPaths(Key='Importance2')
        print(P2)
        print(ReadFieldNames(Shapefile=P2))
        print(".................................................................................................")
        print("Shapefile",P1)
        print("FieldId",[NewList2[int(ComboNodeImp1Fid.current())],InputValFid1] )
        print("Routes", [NewList2[int(ComboNodeImp1Routes.current())],InputValFLi1])
        LBS1=CalculateVecinityBusStops(Shapefile=P1,FieldId=[NewList1[int(ComboNodeImp1Fid.current())],InputValFid1] ,Routes= [NewList1[int(ComboNodeImp1Routes.current())],InputValFLi1])
        Data1=ReadTransitNetwork(ListBusStops=LBS1,Range=75)
        
        LBS2=CalculateVecinityBusStops(Shapefile=P2,FieldId=[NewList2[int(ComboNodeImp2Fid.current())],InputValFid2] ,Routes= [NewList2[int(ComboNodeImp2Routes.current())],InputValFLi2])
        Data2=ReadTransitNetwork(ListBusStops=LBS2,Range=75)
        # PlottingImportance(Data1=Data1,Data2=Data2)
        print("\n\n############################################################ Data 1 ############################################################")
        ListToGeoJson(ListBusStops=Data1)
        # for data in Data1:
        #     print(data)
        print(type(Data1))
        print("\n\n############################################################ Data 2############################################################")
        ListToGeoJson(ListBusStops=Data2)
        # for data in Data2:
        #     print(data)
        print(type(Data2))
        b=input()
        UpdatePath(Key='Importance1',NewPath="")
        UpdatePath(Key='Importance2',NewPath="")

    ###############################################################################################
    #First City
    Geom1={'Coords':{'X':30,'Y':60},'Sizes':{'Hei':60,'Wid':650}}
    Config1={"System":1,'TitleFrame':'Nodes','Command':'GetShpPath','Key':'Importance1'}
    PathSHP(Frame=frame,Geom=Geom1,Config=Config1,)
    print("#################################################")
    print("#################################################")

    Button=ttk.Button(frame,text="Get Fields")
    Button.config(command=(ReqFields1))
    Button.place(x=30, y=150, anchor=W)

    ###############################################################################################
    #Second City
    Geom2={'Coords':{'X':30,'Y':280},'Sizes':{'Hei':60,'Wid':650}}
    Config2={"System":2,'TitleFrame':'Nodes','Command':'GetShpPath','Key':'Importance2'}
    PathSHP(Frame=frame,Geom=Geom2,Config=Config2)
    print("#################################################")
    print("#################################################")

    Button=ttk.Button(frame,text="Get Fields")
    Button.config(command=(ReqFields2))
    Button.place(x=30, y=380, anchor=W)

    ###############################################################################################
    ###############################################################################################
    Button=ttk.Button(frame,text="RUN")
    Button.config(command=(RunAnalaysis))
    Button.place(x=350, y=450, anchor=W)

def NetworkAnalysis(frame):


    ComboShp1Routes= ttk.Combobox(frame)
    ComboShp1StartCode= ttk.Combobox(frame)
    ComboShp1StartName= ttk.Combobox(frame)
    ComboShp1EndCode= ttk.Combobox(frame)
    ComboShp1EndName= ttk.Combobox(frame)

    ComboShp2Routes = ttk.Combobox(frame)
    ComboShp2StartCode = ttk.Combobox(frame)
    ComboShp2StartName = ttk.Combobox(frame)
    ComboShp2EndCode = ttk.Combobox(frame)
    ComboShp2EndName = ttk.Combobox(frame)


    NewList1=[]
    NewList2 = []




    def RunAnalaysis():
        ########################################
        # Get Variables for the first Shapefile

        # Read the Path of the Shapefile
        # print(RearPaths(Key='NetworkSimple1'))
        P1=RearPaths(Key='NetworkSimple1')

        # Get the Values from the ComboBoxes for the Field Index
        InputIndexShp1Routes=int(ComboShp1Routes.current())-1
        InputIndexShp1StartCode=int(ComboShp1StartCode.current())-1
        InputIndexShp1StartName=int(ComboShp1StartName.current())-1
        InputIndexShp1EndCode=int(ComboShp1EndCode.current())-1
        InputIndexShp1EndName=int(ComboShp1EndName.current())-1
        
        # Get the Values from the ComboBoxes for the Field Name
        InputFieldNameShp1Routes=NewList1[int(ComboShp1Routes.current())]
        InputFieldNameShp1StartCode=NewList1[int(ComboShp1StartCode.current())]
        InputFieldNameShp1StartName=NewList1[int(ComboShp1StartName.current())]
        InputFieldNameShp1EndCode=NewList1[int(ComboShp1EndCode.current())]
        InputFieldNameShp1EndName=NewList1[int(ComboShp1EndName.current())]
        
        # Show the values of each field
        print("ComboShp1Routes  ",InputFieldNameShp1Routes,InputIndexShp1Routes)
        print("ComboShp1StartCode  ",InputFieldNameShp1StartCode,InputIndexShp1StartCode)
        print("ComboShp1StartName  ",InputFieldNameShp1StartName,InputIndexShp1StartName)
        print("ComboShp1EndCode  ",InputFieldNameShp1EndCode,InputIndexShp1EndCode)
        print("ComboShp1EndName  ",InputFieldNameShp1EndName,InputIndexShp1EndName)
        # b=input()
        # The Dictionary with the fields is created
        FieldsShp1={'Line':[InputFieldNameShp1Routes,InputIndexShp1Routes],
        'StartCode':[InputFieldNameShp1StartCode,InputIndexShp1StartCode],
        'StartName':[InputFieldNameShp1StartName,InputIndexShp1StartName],
        'EndCode':[InputFieldNameShp1EndCode,InputIndexShp1EndCode],
        'EndName':[InputFieldNameShp1EndName,InputIndexShp1EndName],
        }
        print("FieldsShp1",FieldsShp1)
        # b=input()
        print(ReadFieldNames(Shapefile=P1))
        print(".................................................................................................")

        ########################################
        # Get Variables for the Second Shapefile

        # Read the Path of the Shapefile
        # print(RearPaths(Key='NetworkSimple2'))
        P2=RearPaths(Key='NetworkSimple2')

        # Get the Values from the ComboBoxes for the Field Index
        InputIndexShp2Routes=int(ComboShp2Routes.current())-1
        InputIndexShp2StartCode=int(ComboShp2StartCode.current())-1
        InputIndexShp2StartName=int(ComboShp2StartName.current())-1
        InputIndexShp2EndCode=int(ComboShp2EndCode.current())-1
        InputIndexShp2EndName=int(ComboShp2EndName.current())-1
        
        # Get the Values from the ComboBoxes for the Field Name
        InputFieldNameShp2Routes=NewList1[int(ComboShp2Routes.current())]
        InputFieldNameShp2StartCode=NewList1[int(ComboShp2StartCode.current())]
        InputFieldNameShp2StartName=NewList1[int(ComboShp2StartName.current())]
        InputFieldNameShp2EndCode=NewList1[int(ComboShp2EndCode.current())]
        InputFieldNameShp2EndName=NewList1[int(ComboShp2EndName.current())]
        
        # Show the values of each field
        print("ComboShp2Routes  ",InputFieldNameShp2Routes,InputIndexShp2Routes)
        print("ComboShp2StartCode  ",InputFieldNameShp2StartCode,InputIndexShp2StartCode)
        print("ComboShp2StartName  ",InputFieldNameShp2StartName,InputIndexShp2StartName)
        print("ComboShp2EndCode  ",InputFieldNameShp2EndCode,InputIndexShp2EndCode)
        print("ComboShp2EndName  ",InputFieldNameShp2EndName,InputIndexShp2EndName)

        # The Dictionary with the fields is created
        FieldsShp2={'Line':[InputFieldNameShp2Routes,InputIndexShp2Routes],
        'StartCode':[InputFieldNameShp2StartCode,InputIndexShp2StartCode],
        'StartName':[InputFieldNameShp2StartName,InputIndexShp2StartName],
        'EndCode':[InputFieldNameShp2EndCode,InputIndexShp2EndCode],
        'EndName':[InputFieldNameShp2EndName,InputIndexShp2EndName],
        }
        print("FieldsShp2",FieldsShp2)
        # b=input()
        print(ReadFieldNames(Shapefile=P2))
        print(".................................................................................................")



        ########################################
        # Call for the External functions 

        EdgeCollection,EdgeProperties,NodeCollection,NodeProperties=readShpNetWork(Shapefile=P1,Fileds=FieldsShp1)
        G_Dict_1=CreateNetwork(List_Edges=EdgeCollection,Edge_Properties=EdgeProperties,List_Nodes=NodeCollection,Node_Properties=NodeProperties)

        EdgeCollection,EdgeProperties,NodeCollection,NodeProperties=readShpNetWork(Shapefile=P2,Fileds=FieldsShp2)
        G_Dict_2=CreateNetwork(List_Edges=EdgeCollection,Edge_Properties=EdgeProperties,List_Nodes=NodeCollection,Node_Properties=NodeProperties)

        G_List=[G_Dict_1,G_Dict_2]
        # PlotGraphs(G_List)
        for G_Dict in G_List:
                SimpleNetworkToGeoJson(G=G_Dict)
                b=input()

        UpdatePath(Key='NetworkSimple1',NewPath="")
        UpdatePath(Key='NetworkSimple2',NewPath="")


    def ReqFields1():
        print("\n"*2)
        print(".................we get into the Fields 1........................")
        P1=RearPaths(Key='NetworkSimple1')
        print(P1)
        if P1=='':
            return None
        List1=ReadFieldNames(Shapefile=P1)
        print(List1)
        # print(P1)
        for elment in List1:
            print("----------------------------------------------------------------------------",elment)
            NewList1.append(elment[0])
        ###################################################################################
        ComboShp1Routes.config(width=17,values=NewList1)
        ComboShp1Routes.place(x=120,y=140)
        labelShp1Routes = Label(frame, text="Field with Routes/Line", font='Helvetica 12')
        labelShp1Routes.place(x=120, y=120, anchor=W)
        ###########################
        ComboShp1StartCode.config(width=17,values=NewList1)
        ComboShp1StartCode.place(x=280,y=140)
        labelShp1StartCode = Label(frame, text="Field with Start Code", font='Helvetica 12')
        labelShp1StartCode.place(x=280, y=120, anchor=W)
        ###########################
        ComboShp1StartName.config(width=17,values=NewList1)
        ComboShp1StartName.place(x=440,y=140)
        labelShp1StartName = Label(frame, text="Field with Start Name", font='Helvetica 12')
        labelShp1StartName.place(x=440, y=120, anchor=W)
        ###########################
        ComboShp1EndCode.config(width=17,values=NewList1)
        ComboShp1EndCode.place(x=280,y=200)
        labelShp1EndCode = Label(frame, text="Field with End Code", font='Helvetica 12')
        labelShp1EndCode.place(x=280, y=180, anchor=W)
        ###########################
        ComboShp1EndName.config(width=17,values=NewList1)
        ComboShp1EndName.place(x=440,y=200)
        labelShp1EndName = Label(frame, text="Field with End Name", font='Helvetica 12')
        labelShp1EndName.place(x=440, y=180, anchor=W)

    
    def ReqFields2():
        print("\n"*2)
        print(".................we get into the Fields 2........................")
        P2=RearPaths(Key='NetworkSimple2')
        print(P2)
        if P2=='':
            return None

        List2=ReadFieldNames(Shapefile=P2)
        print(List2)
        # print(P2)
        for elment in List2:
            print("----------------------------------------------------------------------------",elment)
            NewList2.append(elment[0])
        ###################################################################################
        ComboShp2Routes.config(width=17,values=NewList2)
        ComboShp2Routes.place(x=120,y=340)
        labelShp2Routes = Label(frame, text="Field with Routes/Line", font='Helvetica 12')
        labelShp2Routes.place(x=120, y=320, anchor=W)
        ###########################
        ComboShp2StartCode.config(width=17,values=NewList2)
        ComboShp2StartCode.place(x=280,y=340)
        labelShp2StartCode = Label(frame, text="Field with Start Code", font='Helvetica 12')
        labelShp2StartCode.place(x=280, y=320, anchor=W)
        ###########################
        ComboShp2StartName.config(width=17,values=NewList2)
        ComboShp2StartName.place(x=440,y=340)
        labelShp2StartName = Label(frame, text="Field with Start Name", font='Helvetica 12')
        labelShp2StartName.place(x=440, y=320, anchor=W)
        ###########################
        ComboShp2EndCode.config(width=17,values=NewList2)
        ComboShp2EndCode.place(x=280,y=400)
        labelShp2EndCode = Label(frame, text="Field with End Code", font='Helvetica 12')
        labelShp2EndCode.place(x=280, y=380, anchor=W)
        ###########################
        ComboShp2EndName.config(width=17,values=NewList2)
        ComboShp2EndName.place(x=440,y=400)
        labelShp2EndName = Label(frame, text="Field with End Name", font='Helvetica 12')
        labelShp2EndName.place(x=440, y=380, anchor=W)


    ###############################################################################################
    #First City
    Geom1={'Coords':{'X':30,'Y':60},'Sizes':{'Hei':60,'Wid':650}}
    Config1={"System":1,'TitleFrame':'Nodes','Command':'GetShpPath','Key':'NetworkSimple1'}
    PathSHP(Frame=frame,Geom=Geom1,Config=Config1,)
    print("#################################################")
    print("#################################################")

    Button=ttk.Button(frame,text="Get Fields")
    Button.config(command=(ReqFields1))
    Button.place(x=30, y=150, anchor=W)


    ###############################################################################################
    #Second City
    Geom2={'Coords':{'X':30,'Y':280},'Sizes':{'Hei':60,'Wid':650}}
    Config2={"System":2,'TitleFrame':'Nodes','Command':'GetShpPath','Key':'NetworkSimple2'}
    PathSHP(Frame=frame,Geom=Geom2,Config=Config2)
    print("#################################################")
    print("#################################################")

    Button=ttk.Button(frame,text="Get Fields")
    Button.config(command=(ReqFields2))
    Button.place(x=30, y=380, anchor=W)


    ###############################################################################################
    ###############################################################################################
    Button=ttk.Button(frame,text="RUN")
    Button.config(command=(RunAnalaysis))
    Button.place(x=350, y=450, anchor=W)


def NodeNetworkAnalysis(frame):

    ###############################################################################################
    # Frame that holds the tabs
    FrameElemento=ttk.LabelFrame(frame,height = 550, width =650,text ='City Selection')
    FrameElemento.place(x=30, y=30, anchor=NW)

    nbCities = ttk.Notebook(frame)
    nbCities.place(x=5,y=5)

    T1 = tkinter.Frame(nbCities)
    T2 = tkinter.Frame(nbCities)

        #Add the tab
    nbCities.add(T1, text="First City")
    T1.config(height=540,width=640)
    T1.config(relief= RIDGE)

    #Add the tab
    nbCities.add(T2, text="SecondCity")
    T2.config(height=540,width=640)
    T2.config(relief= RIDGE)


    ComboShpA1Routes= ttk.Combobox(T1)
    ComboShpA1StartCode= ttk.Combobox(T1)
    ComboShpA1StartName= ttk.Combobox(T1)
    ComboShpA1EndCode= ttk.Combobox(T1)
    ComboShpA1EndName= ttk.Combobox(T1)

    ComboShpA2Fid= ttk.Combobox(T1)
    ComboShpA2Route= ttk.Combobox(T1)

    ComboShpB1Routes = ttk.Combobox(T2)
    ComboShpB1StartCode = ttk.Combobox(T2)
    ComboShpB1StartName = ttk.Combobox(T2)
    ComboShpB1EndCode = ttk.Combobox(T2)
    ComboShpB1EndName = ttk.Combobox(T2)

    ComboShpB2Fid= ttk.Combobox(T2)
    ComboShpB2Route= ttk.Combobox(T2)


    NewListA1=[]
    NewListA2 = []
    NewListB1=[]
    NewListB2 = []

    def RunAnalaysis():
        ########################################
        # Get Variables for the first Shapefile

        # Read the Path of the Shapefile
        # print(RearPaths(Key='NetworkSimple1'))
        P1=RearPaths(Key='NetworkNodeLine1')

        # Get the Values from the ComboBoxes for the Field Index
        InputIndexShpA1Routes=int(ComboShpA1Routes.current())-1
        InputIndexShpA1StartCode=int(ComboShpA1StartCode.current())-1
        InputIndexShpA1StartName=int(ComboShpA1StartName.current())-1
        InputIndexShpA1EndCode=int(ComboShpA1EndCode.current())-1
        InputIndexShpA1EndName=int(ComboShpA1EndName.current())-1
        
        # Get the Values from the ComboBoxes for the Field Name
        InputFieldNameShpA1Routes=NewListA1[int(ComboShpA1Routes.current())]
        InputFieldNameShpA1StartCode=NewListA1[int(ComboShpA1StartCode.current())]
        InputFieldNameShpA1StartName=NewListA1[int(ComboShpA1StartName.current())]
        InputFieldNameShpA1EndCode=NewListA1[int(ComboShpA1EndCode.current())]
        InputFieldNameShpA1EndName=NewListA1[int(ComboShpA1EndName.current())]
        
        # Show the values of each field
        print("ComboShpA1Routes  ",InputFieldNameShpA1Routes,InputIndexShpA1Routes)
        print("ComboShpA1StartName  ",InputFieldNameShpA1StartName,InputIndexShpA1StartName)
        print("ComboShpA1StartCode  ",InputFieldNameShpA1StartCode,InputIndexShpA1StartCode)
        print("ComboShpA1EndName  ",InputFieldNameShpA1EndName,InputIndexShpA1EndName)
        print("ComboShpA1EndCode  ",InputFieldNameShpA1EndCode,InputIndexShpA1EndCode)
        print("\n\n",P1)
        # b=input()
        # The Dictionary with the fields is created
        FieldsShpA1={'Line':[InputFieldNameShpA1Routes,InputIndexShpA1Routes],
        'StartCode':[InputFieldNameShpA1StartCode,InputIndexShpA1StartCode],
        'StartName':[InputFieldNameShpA1StartName,InputIndexShpA1StartName],
        'EndCode':[InputFieldNameShpA1EndCode,InputIndexShpA1EndCode],
        'EndName':[InputFieldNameShpA1EndName,InputIndexShpA1EndName],
        }
        print(FieldsShpA1)
        print(ReadFieldNames(Shapefile=P1))
        print(".................................................................................................")
        # b=input()

        print(RearPaths(Key='NetworkBusStops1'))
        InputIndexShpA2Fid=int(ComboShpA2Fid.current())-1
        InputIndexShpA2FLine=int(ComboShpA2Route.current())-1
        # InputIndexShpA2Fid=int(ComboShpA2Fid.current())
        # InputIndexShpA2FLine=int(ComboShpA2Route.current())

        InputFieldNameShpA2Fid=NewListA2[int(ComboShpA2Fid.current())]
        InputFieldNameShpA2Routes=NewListA2[int(ComboShpA2Route.current())]

        print("ComboShpA2Fid   ",InputIndexShpA2Fid,InputFieldNameShpA2Fid)
        print("ComboShpA2Route",InputIndexShpA2FLine,InputFieldNameShpA2Routes)
        # b=input()
        # print(NewListA2,"\n",NewListA2[int(ComboShpA2Fid.current())],"\n",NewListA2[int(ComboShpA2Route.current())])
        P2=RearPaths(Key='NetworkBusStops1')
        print(P2)
        print(ReadFieldNames(Shapefile=P2))
        print(".................................................................................................")
        # b=input()
        #################################################################################################
        #################################################################################################
        #################################################################################################

        ########################################
        # Get Variables for the Second Shapefile
        # Read the Path of the Shapefile
        # print(RearPaths(Key='NetworkSimple2'))
        P3=RearPaths(Key='NetworkNodeLine2')

        # Get the Values from the ComboBoxes for the Field Index
        InputIndexShpB1Routes=int(ComboShpB1Routes.current())-1
        InputIndexShpB1StartCode=int(ComboShpB1StartCode.current())-1
        InputIndexShpB1StartName=int(ComboShpB1StartName.current())-1
        InputIndexShpB1EndCode=int(ComboShpB1EndCode.current())-1
        InputIndexShpB1EndName=int(ComboShpB1EndName.current())-1
        
        # Get the Values from the ComboBoxes for the Field Name
        InputFieldNameShpB1Routes=NewListB1[int(ComboShpB1Routes.current())]
        InputFieldNameShpB1StartCode=NewListB1[int(ComboShpB1StartCode.current())]
        InputFieldNameShpB1StartName=NewListB1[int(ComboShpB1StartName.current())]
        InputFieldNameShpB1EndCode=NewListB1[int(ComboShpB1EndCode.current())]
        InputFieldNameShpB1EndName=NewListB1[int(ComboShpB1EndName.current())]
        
        # Show the values of each field
        print("ComboShpB1Routes  ",InputFieldNameShpB1Routes,InputIndexShpB1Routes)
        print("ComboShpB1StartCode  ",InputFieldNameShpB1StartCode,InputIndexShpB1StartCode)
        print("ComboShpB1StartName  ",InputFieldNameShpB1StartName,InputIndexShpB1StartName)
        print("ComboShpB1EndCode  ",InputFieldNameShpB1EndCode,InputIndexShpB1EndCode)
        print("ComboShpB1EndName  ",InputFieldNameShpB1EndName,InputIndexShpB1EndName)
        # b=input()
        # The Dictionary with the fields is created
        FieldsShpB1={'Line':[InputFieldNameShpB1Routes,InputIndexShpB1Routes],
        'StartCode':[InputFieldNameShpB1StartCode,InputIndexShpB1StartCode],
        'StartName':[InputFieldNameShpB1StartName,InputIndexShpB1StartName],
        'EndCode':[InputFieldNameShpB1EndCode,InputIndexShpB1EndCode],
        'EndName':[InputFieldNameShpB1EndName,InputIndexShpB1EndName],
        }
        print(FieldsShpB1)
        # print(ReadFieldNames(Shapefile=P3))
        print(".................................................................................................")

        print(RearPaths(Key='NetworkBusStops2'))
        InputIndexShpB2Fid=int(ComboShpB2Fid.current())-1
        InputIndexShpB2FLine=int(ComboShpB2Route.current())-1
        # InputIndexShpB4Fid=int(ComboShpB2Fid.current())
        # InputIndexShpB4FLine=int(ComboShpB2Route.current())

        InputFieldNameShpB2Fid=NewListB2[int(ComboShpB2Fid.current())]
        InputFieldNameShpB2Routes=NewListB2[int(ComboShpB2Route.current())]

        print("ComboShpB2Fid   ",InputIndexShpB2Fid,InputFieldNameShpB2Fid)
        print("ComboShpB2Route",InputIndexShpB2FLine,InputFieldNameShpB2Routes)
        # b=input()
        # print(NewListB2,"\n",NewListB2[int(ComboShpB2Fid.current())],"\n",NewListB2[int(ComboShpB2Route.current())])
        P4=RearPaths(Key='NetworkBusStops2')
        print(P4)
        print(ReadFieldNames(Shapefile=P4))
        print(".................................................................................................")

        # b=input()
        ########################################
        # Call for the External functions 
        # from NetworkAnalisys import AgregateTransitNetwork

        EdgeCollection,EdgeProperties=readShpNetWorkForSimplification(Shapefile=P1,Fileds=FieldsShpA1)
        LBS1=CalculateVecinityBusStops(Shapefile=P2,FieldId=[InputFieldNameShpA2Fid,InputIndexShpA2Fid] ,Routes= [InputFieldNameShpA2Routes,InputIndexShpA2FLine])
        Nodes= AgregateTransitNetwork(ListBusStops=LBS1,Range=75)
        G_Dict_1=AgregatedStopsToNetwork(AgregatedNodes=Nodes,Edge_List=EdgeCollection,Edge_Properties=EdgeProperties)
        NetWorkToGeoJson(G=G_Dict_1['G'])

        EdgeCollection,EdgeProperties=readShpNetWorkForSimplification(Shapefile=P3,Fileds=FieldsShpB1)
        LBS1=CalculateVecinityBusStops(Shapefile=P4,FieldId=[InputFieldNameShpB2Fid,InputIndexShpB2Fid] ,Routes= [InputFieldNameShpB2Routes,InputIndexShpB2FLine])
        Nodes= AgregateTransitNetwork(ListBusStops=LBS1,Range=75)
        G_Dict_2=AgregatedStopsToNetwork(AgregatedNodes=Nodes,Edge_List=EdgeCollection,Edge_Properties=EdgeProperties)
        G_List=[G_Dict_1,G_Dict_2]

        for G_Dict in G_List:
            NetWorkToGeoJson(G=G_Dict['G'])



        UpdatePath(Key='NetworkNodeLine1',NewPath="")
        UpdatePath(Key='NetworkBusStops1',NewPath="")
        UpdatePath(Key='NetworkNodeLine2',NewPath="")
        UpdatePath(Key='NetworkBusStops2',NewPath="")


    def ReqFieldsA1():
        print("\n"*2)
        print(".................we get into the Fields 1........................")
        P1=RearPaths(Key='NetworkNodeLine1')
        print(P1)
        if P1=='':
            return None
        List1=ReadFieldNames(Shapefile=P1)
        print(List1)
        # print(P1)
        for elment in List1:
            print("----------------------------------------------------------------------------",elment)
            NewListA1.append(elment[0])
        ###################################################################################
        ComboShpA1Routes.config(width=17,values=NewListA1)
        ComboShpA1Routes.place(x=120,y=140)
        labelShpA1Routes = Label(T1, text="Field with Routes/Line", font='Helvetica 12')
        labelShpA1Routes.place(x=120, y=120, anchor=W)
        ###########################
        ComboShpA1StartCode.config(width=17,values=NewListA1)
        ComboShpA1StartCode.place(x=280,y=140)
        labelShpA1StartCode = Label(T1, text="Field with Start Code", font='Helvetica 12')
        labelShpA1StartCode.place(x=280, y=120, anchor=W)
        ###########################
        ComboShpA1StartName.config(width=17,values=NewListA1)
        ComboShpA1StartName.place(x=440,y=140)
        labelShpA1StartName = Label(T1, text="Field with Start Name", font='Helvetica 12')
        labelShpA1StartName.place(x=440, y=120, anchor=W)
        ###########################
        ComboShpA1EndCode.config(width=17,values=NewListA1)
        ComboShpA1EndCode.place(x=280,y=200)
        labelShpA1EndCode = Label(T1, text="Field with End Code", font='Helvetica 12')
        labelShpA1EndCode.place(x=280, y=180, anchor=W)
        ###########################
        ComboShpA1EndName.config(width=17,values=NewListA1)
        ComboShpA1EndName.place(x=440,y=200)
        labelShpA1EndName = Label(T1, text="Field with End Name", font='Helvetica 12')
        labelShpA1EndName.place(x=440, y=180, anchor=W)


    def ReqFieldsA2():

        print("\n"*2)
        print(".................we get into the Fields 2........................")
        P2=RearPaths(Key='NetworkBusStops1')
        print(P2)
        if P2=='':
            return None
        List2=ReadFieldNames(Shapefile=P2)
        # print(List2)
        print(P2)
        for elment in List2:
            print("----------------------------------------------------------------------------",elment)
            NewListA2.append(elment[0])
        ComboShpA2Fid.config(width=17,values=NewListA2)
        ComboShpA2Fid.place(x=130,y=360)
        labelImp2Fid = Label(T1, text="Field with Node ID", font='Helvetica 12')
        labelImp2Fid.place(x=130, y=320, anchor=W)

        ComboShpA2Route.config(width=17,values=NewListA2)
        ComboShpA2Route.place(x=300,y=360)
        labelImp2Routes = Label(T1, text="Field with Routes/Lines", font='Helvetica 12')
        labelImp2Routes.place(x=300, y=320, anchor=W)


    def ReqFieldsB1():
        print("\n"*2)
        print(".................we get into the Fields 3........................")
        P3=RearPaths(Key='NetworkNodeLine2')
        print(P3)
        if P3=='':
            return None
        List1=ReadFieldNames(Shapefile=P3)
        print(List1)
        # print(P3)
        for elment in List1:
            print("----------------------------------------------------------------------------",elment)
            NewListB1.append(elment[0])
        ###################################################################################
        ComboShpB1Routes.config(width=17,values=NewListB1)
        ComboShpB1Routes.place(x=120,y=140)
        labelShpB1Routes = Label(T2, text="Field with Routes/Line", font='Helvetica 12')
        labelShpB1Routes.place(x=120, y=120, anchor=W)
        ###########################
        ComboShpB1StartCode.config(width=17,values=NewListB1)
        ComboShpB1StartCode.place(x=280,y=140)
        labelShpB1StartCode = Label(T2, text="Field with Start Code", font='Helvetica 12')
        labelShpB1StartCode.place(x=280, y=120, anchor=W)
        ###########################
        ComboShpB1StartName.config(width=17,values=NewListB1)
        ComboShpB1StartName.place(x=440,y=140)
        labelShpB1StartName = Label(T2, text="Field with Start Name", font='Helvetica 12')
        labelShpB1StartName.place(x=440, y=120, anchor=W)
        ###########################
        ComboShpB1EndCode.config(width=17,values=NewListB1)
        ComboShpB1EndCode.place(x=280,y=200)
        labelShpB1EndCode = Label(T2, text="Field with End Code", font='Helvetica 12')
        labelShpB1EndCode.place(x=280, y=180, anchor=W)
        ###########################
        ComboShpB1EndName.config(width=17,values=NewListB1)
        ComboShpB1EndName.place(x=440,y=200)
        labelShpB1EndName = Label(T2, text="Field with End Name", font='Helvetica 12')
        labelShpB1EndName.place(x=440, y=180, anchor=W)

    def ReqFieldsB2():

        print("\n"*2)
        print(".................we get into the Fields 4........................")
        P4=RearPaths(Key='NetworkBusStops2')
        print(P4)
        if P4=='':
            return None
        List2=ReadFieldNames(Shapefile=P4)
        # print(List2)
        print(P4)
        for elment in List2:
            print("----------------------------------------------------------------------------",elment)
            NewListB2.append(elment[0])
        ComboShpB2Fid.config(width=17,values=NewListB2)
        ComboShpB2Fid.place(x=130,y=360)
        labelImpB2Fid = Label(T1, text="Field with Node ID", font='Helvetica 12')
        labelImpB2Fid.place(x=130, y=320, anchor=W)

        ComboShpB2Route.config(width=17,values=NewListB2)
        ComboShpB2Route.place(x=300,y=360)
        labelImpB2Routes = Label(T1, text="Field with Routes/Lines", font='Helvetica 12')
        labelImpB2Routes.place(x=300, y=320, anchor=W)







    ###############################################################################################
    ###########################        First City               ###################################
    ###############################################################################################

    Geom1={'Coords':{'X':30,'Y':60},'Sizes':{'Hei':60,'Wid':650}}
    Config1={"System":1,'TitleFrame':'Lines [First City]','Command':'GetShpPath','Key':'NetworkNodeLine1'}
    PathSHP(Frame=T1,Geom=Geom1,Config=Config1,)
    print("#################################################")
    print("#################################################")

    Button=ttk.Button(T1,text="Get Fields")
    Button.config(command=(ReqFieldsA1))
    Button.place(x=30, y=150, anchor=W)

    ###############################################################################################
    #Second City
    Geom2={'Coords':{'X':30,'Y':280},'Sizes':{'Hei':60,'Wid':650}}
    Config2={"System":2,'TitleFrame':'Nodes  [First City]','Command':'GetShpPath','Key':'NetworkBusStops1'}
    PathSHP(Frame=T1,Geom=Geom2,Config=Config2)
    print("#################################################")
    print("#################################################")

    Button=ttk.Button(T1,text="Get Fields")
    Button.config(command=(ReqFieldsA2))
    Button.place(x=30, y=380, anchor=W)

    ###############################################################################################
    Button=ttk.Button(T1,text="RUN")
    Button.config(command=(RunAnalaysis))
    Button.place(x=350, y=450, anchor=W)


    ###############################################################################################
    ###########################        Second City              ###################################
    ###############################################################################################

    Geom1={'Coords':{'X':30,'Y':60},'Sizes':{'Hei':60,'Wid':650}}
    Config1={"System":1,'TitleFrame':'Lines [Second City]','Command':'GetShpPath','Key':'NetworkNodeLine2'}
    PathSHP(Frame=T2,Geom=Geom1,Config=Config1,)
    print("#################################################")
    print("#################################################")

    Button=ttk.Button(T2,text="Get Fields")
    Button.config(command=(ReqFieldsB1))
    Button.place(x=30, y=150, anchor=W)

    ###############################################################################################
    #Second City
    Geom2={'Coords':{'X':30,'Y':280},'Sizes':{'Hei':60,'Wid':650}}
    Config2={"System":2,'TitleFrame':'Nodes [Second City]','Command':'GetShpPath','Key':'NetworkBusStops2'}
    PathSHP(Frame=T2,Geom=Geom2,Config=Config2)
    print("#################################################")
    print("#################################################")

    Button=ttk.Button(T2,text="Get Fields")
    Button.config(command=(ReqFieldsB2))
    Button.place(x=30, y=380, anchor=W)

    ###############################################################################################
    Button=ttk.Button(T2,text="RUN")
    Button.config(command=(RunAnalaysis))
    Button.place(x=350, y=450, anchor=W)



def Correr(root):
    global DataBucket
    DataBucket={}
    NumberCities=3
    NumberCities=NumberCities+1
    DataBucket={
        'Centroid':{}
    }
    # for i in range(1,NumberCities):
    #     DataBucket[i]={"Data":{"BusStops":0,"Area":0}}
    print(DataBucket)
    # root.attributes('-topmost', True)
    root.title("Concordia Research Chair in Integrated Design, Ecology And Sustainability for the Built Environment")
    FrameMaestro =ttk.Frame(root)
    FrameMaestro.config(height=900,width=1000) # Configura altura y ancho
    FrameMaestro.config(relief= RIDGE)        # Tipod de frame
    FrameMaestro.config(padding=(30, 15))     # Acolchonado de frame
    FrameMaestro.pack()                       # ANade frame
    ####################################################################
    ####################################################################
    ####################################################################
    # img1 = ImageTk.PhotoImage(Image.open(r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tools\Lib\idea2.png"))
    # img1 = ImageTk.PhotoImage(Image.open(r".\..\..\CAMMM-Soft-Tools\Lib\idea2.png"))
    img1 = ImageTk.PhotoImage(Image.open(r"Scripts\Lib\camm2.png"))

    panel1 = Label(FrameMaestro, image = img1)
    panel1.place(x=0,y=0)

    # img2 = ImageTk.PhotoImage(Image.open(r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tools\Lib\camm2.png"))
    # img2 = ImageTk.PhotoImage(Image.open(r".\..\..\CAMMM-Soft-Tools\Lib\camm2.png"))
    img2 = ImageTk.PhotoImage(Image.open(r"Scripts\Lib\camm2.png"))
    panel2 = Label(FrameMaestro, image = img2)
    panel2.place(x=50,y=100)

    labelTitle1 = Label(FrameMaestro, text="Urban Morphological Analysis\nfor Multimodal Mobility", font='Helvetica 18 bold')
    labelTitle1.place(x=120, y=250, anchor=W)

    ####################################################################
    ####################################################################
    ####################################################################
    NotebookHeight=500
    NotebookWidth=800

    nb = ttk.Notebook(FrameMaestro)
    nb.place(x=50,y=300)
    ####################################################################
    ####################################################################


    def GenInputsNodeImportance():
        print("···································",comboNumCitiesI1)
        NumCities=comboNumCitiesI1.current()+1
        print("NumCities",NumCities,type(NumCities))
        YvalOringal=60
        for i in range(1,(NumCities+2)):
            Yval=YvalOringal+(200*i)


            Geom2={'Coords':{'X':30,'Y':(Yval+20)},'Sizes':{'Hei':90,'Wid':650}}
            Config2={'TitleFrame':'Area of the City'}
            PathEntry(Frame=f2,Geom=Geom2,Config=Config2)
            print("In tab, ",Pathshp)

    # ####################################################################
    # def GenInputsCompactness(comboNumCitiesI1):
    #     print("GenInputsCompactness                         ···································",comboNumCitiesI1,comboNumCitiesI1.current())
    #     NumCities=comboNumCitiesI1.current()+1
    #     print("NumCities",NumCities,type(NumCities))
    #     YvalOringal=60
    #     for i in range(1,(NumCities+2)):
    #         Yval=YvalOringal+(80*i)
    #         Geom={'Coords':{'X':30,'Y':(Yval)},'Sizes':{'Hei':90,'Wid':650}}
    #         print(Geom)
    #         Config={"City":i,'TitleFrame':'City '+str(i)+' - Area of the City','Command':'GetShpPath','action':'Centroid'}
    #         Pathshp=PathEntryName(Frame=f1,Geom=Geom,Config=Config)
    #         print("In tab, ",Pathshp)

    # def CalculateIndexCompactness():
    #     # print("LOCAL LOCAL LOCAL LOCAL LOCAL LOCAL LOCAL LOCAL LOCAL LOCAL LOCAL LOCAL LOCAL LOCAL LOCAL LOCAL LOCAL LOCAL LOCAL LOCAL LOCAL LOCAL \n"*10)
    #     # b=input()
    #     global CityNames
    #     print("···································")
    #     NumCities=comboNumCitiesI1.current()+1
    #     print("NumCities",NumCities,type(NumCities))
    #     ShapeFiles=[]
    #     CityAreas=[]
    #     Ratios=[]
    #     for i in range(1,(NumCities+2)):
    #         ShapeFiles.append(DataBucket["Centroid"][i]['Path'])
    #         print("Centroid",DataBucket["Centroid"][i])
    #         CityArea,ClipArea,ExoArea,Ratio,Centroid,CircleRadious=CalculateCompactness(DataBucket["Centroid"][i]['Path'])
    #         # print("·······CityArea",CityArea)
    #         # print("·······ClipArea",ClipArea)
    #         # print("·······ExoArea",ExoArea)
    #         # print("·······Ratio",Ratio)
    #         CityAreas.append(CityArea)
    #         Ratios.append(Ratio)
    #     os.system('cls')
    #     Data=ClassDataCentroid(ShapeFiles=ShapeFiles, Titles=CityNames,CityArea=CityAreas,Ratio=Ratios)
    #     print("............................................................................................"*10)
    #     print(Data)
    #     print(Data.ShapeFiles)
    #     print(Data.Titles)
    #     # b=input()
    #     PlottingCompactness(Data)



    #Make 1st tab
    f1 = tkinter.Frame(nb)
    f2 = tkinter.Frame(nb)
    f3 = tkinter.Frame(nb)
    f4 = tkinter.Frame(nb)
    # f5 = tkinter.Frame(nb)

    #Add the tab
    nb.add(f1, text="Presentation")
    f1.config(height=NotebookHeight,width=NotebookWidth)
    f1.config(relief= RIDGE)

    #Add the tab
    nb.add(f2, text="Node Weight")
    f2.config(height=NotebookHeight,width=NotebookWidth)
    f2.config(relief= RIDGE)

    #Add the tab
    nb.add(f3, text="Network Analysis")
    f3.config(height=NotebookHeight,width=NotebookWidth)
    f3.config(relief= RIDGE)

    # Add the tab
    nb.add(f4, text="Node Notework Analysis")
    f4.config(height=NotebookHeight,width=NotebookWidth)
    f4.config(relief= RIDGE)
 

 
    ##################################################################
    ##################################################################
    ###  TAB 2
    comboNumCitiesI1 = ttk.Combobox(f2,width=5,values=["2","3","4","5"])
    comboNumCitiesI1.place(x=230,y=31)
    
    NodeRelevanceTab(frame=f2)
    NetworkAnalysis(frame=f3)
    NodeNetworkAnalysis(frame=f4)
    
    # labelText1 = Label(f2, text="Number of cities to evaluate", font='Helvetica 12 ')
    # labelText1.place(x=20, y=40, anchor=W)
    
    # buttonGenerate = tk.Button(f2,text="Generate", font=40, command=GenInputsNodeImportance)
    # buttonGenerate.place(x=300, y=27)
    
    # buttonCalculate = tk.Button(f2,text="Calculate", font=40, command=CalculateIndexCompactness)
    # buttonCalculate.place(x=380, y=27)
    
    ##################################################################
    ##################################################################
    ###  TAB 1
    
    # comboNumCitiesI1 = ttk.Combobox(f1,width=5,values=["2","3","4","5"])
    # comboNumCitiesI1.place(x=230,y=31)
    # print("#######################################################################################################"*10)
    # print(comboNumCitiesI1)
    # print("#######################################################################################################"*10)

    # labelText1 = Label(f1, text="Number of cities to evaluate", font='Helvetica 12 ')
    # labelText1.place(x=20, y=40, anchor=W)

    # buttonGenerate = tk.Button(f1,text="Generate", font=40, command=partial(GenInputsCompactness,comboNumCitiesI1))
    # buttonGenerate.place(x=300, y=27)

    # buttonCalculate = tk.Button(f1,text="Calculate", font=40, command=CalculateIndexCompactness)
    # buttonCalculate.place(x=380, y=27)

    ##################################################################

    nb.enable_traversal()

    root.mainloop()



def main():
    global root
    global CityNames
    CityNames=[]
    # CityNames.append("")
    root=Tk()
    Correr(root)


if __name__ == '__main__':
    main()
    Path=r'Paths.db'
    db = sqlite3.connect(Path)
    cursor = db.cursor()
