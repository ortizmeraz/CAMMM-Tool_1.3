
#! python3.
import os
import sys
import io
import datetime
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import filedialog
from tkinter.filedialog import askdirectory
from tkinter import messagebox
from shutil import copyfile
import tkinter
import numpy as np
import tkinter as tk

from PIL import ImageTk, Image
import os
from epsg_ident import EpsgIdent

from functools import partial

from FeatureOperations import ReadFieldNames
from FeatureOperations import CalculateVecinityBusStops
from FeatureOperations import ReadTransitNetwork


# from ClassCollection import PlotingData
from ClassCollection import ClassDataCentroid

from Databases import UpdatePath
from Databases import RearPaths
from NetworkAnalisys import readShpNetWork
from NetworkAnalisys import CreateNetwork
# from NetworkAnalisys import PlotGraphs
from NetworkAnalisys import readShpNetWorkForSimplification
from NetworkAnalisys import AgregateTransitNetwork
from NetworkAnalisys import AgregatedStopsToNetwork
from NetworkAnalisys import NetWorkToGeoJson
from NetworkAnalisys import ListToGeoJson
from NetworkAnalisys import SimpleNetworkToGeoJson
from GFSTop import GTFS
from setup import Update


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

# def NodeRelevanceTab(frame):

#     ComboNodeImp1Fid= ttk.Combobox(frame)
#     ComboNodeImp1Routes= ttk.Combobox(frame)
#     NewList1=[]

#     ComboNodeImp2Fid= ttk.Combobox(frame)
#     ComboNodeImp2Routes= ttk.Combobox(frame)
#     NewList2=[]

#     def ReqFields1():
#         print("\n"*2)
#         print(".................we get into the Fields 1........................")
#         P1=RearPaths(Key='Importance1')
#         print(P1)
#         if P1=='':
#             return None
#         List1=ReadFieldNames(Shapefile=P1)
#         # print(List1)
#         print(P1)
#         for elment in List1:
#             print("----------------------------------------------------------------------------",elment)
#             NewList1.append(elment[0])
#         ComboNodeImp1Fid.config(width=17,values=NewList1)
#         ComboNodeImp1Fid.place(x=120,y=140)
#         labelImp1Fid = Label(frame, text="Field with Node ID", font='Helvetica 12')
#         labelImp1Fid.place(x=120, y=120, anchor=W)
#         ComboNodeImp1Routes.config(width=17,values=NewList1)
#         ComboNodeImp1Routes.place(x=280,y=140)
#         labelImp1Routes = Label(frame, text="Field with Routes/Lines", font='Helvetica 12')
#         labelImp1Routes.place(x=280, y=120, anchor=W)

#     def ReqFields2():
#         print("\n"*2)
#         print(".................we get into the Fields 2........................")
#         P2=RearPaths(Key='Importance2')
#         print(P2)
#         if P2=='':
#             return None
#         List2=ReadFieldNames(Shapefile=P2)
#         # print(List2)
#         print(P2)
#         for elment in List2:
#             print("----------------------------------------------------------------------------",elment)
#             NewList2.append(elment[0])
#         ComboNodeImp2Fid.config(width=17,values=NewList2)
#         ComboNodeImp2Fid.place(x=120,y=340)
#         labelImp2Fid = Label(frame, text="Field with Node ID", font='Helvetica 12')
#         labelImp2Fid.place(x=120, y=320, anchor=W)
#         ComboNodeImp2Routes.config(width=17,values=NewList2)
#         ComboNodeImp2Routes.place(x=280,y=340)
#         labelImp2Routes = Label(frame, text="Field with Routes/Lines", font='Helvetica 12')
#         labelImp2Routes.place(x=280, y=320, anchor=W)

#     def RunAnalaysis():
#         print(RearPaths(Key='Importance1'))
#         InputValFid1=int(ComboNodeImp1Fid.current())-1
#         InputValFLi1=int(ComboNodeImp1Routes.current())-1
#         print("ComboNodeImp1Fid   ",ComboNodeImp1Fid.current(),InputValFid1)
#         print("ComboNodeImp1Routes",ComboNodeImp1Routes.current(),InputValFLi1)
#         print(NewList1,"\n",NewList1[int(ComboNodeImp1Fid.current())],"\n",NewList1[int(ComboNodeImp1Routes.current())])
#         P1=RearPaths(Key='Importance1')
#         print(P1)
#         print(ReadFieldNames(Shapefile=P1))
#         print(".................................................................................................")

#         print("\n"*3)
#         print(RearPaths(Key='Importance2'))
#         InputValFid2=int(ComboNodeImp2Fid.current())-1
#         InputValFLi2=int(ComboNodeImp2Routes.current())-1
#         print("ComboNodeImp2Fid   ",ComboNodeImp2Fid.current(),InputValFid2)
#         print("ComboNodeImp2Routes",ComboNodeImp2Routes.current(),InputValFLi2)
#         print(NewList2,"\n",NewList2[int(ComboNodeImp2Fid.current())],"\n",NewList2[int(ComboNodeImp2Routes.current())])
#         P2=RearPaths(Key='Importance2')
#         print(P2)
#         print(ReadFieldNames(Shapefile=P2))
#         print(".................................................................................................")
#         print("Shapefile",P1)
#         print("FieldId",[NewList2[int(ComboNodeImp1Fid.current())],InputValFid1] )
#         print("Routes", [NewList2[int(ComboNodeImp1Routes.current())],InputValFLi1])
#         LBS1=CalculateVecinityBusStops(Shapefile=P1,FieldId=[NewList1[int(ComboNodeImp1Fid.current())],InputValFid1] ,Routes= [NewList1[int(ComboNodeImp1Routes.current())],InputValFLi1])
#         Data1=ReadTransitNetwork(ListBusStops=LBS1,Range=75)
        
#         LBS2=CalculateVecinityBusStops(Shapefile=P2,FieldId=[NewList2[int(ComboNodeImp2Fid.current())],InputValFid2] ,Routes= [NewList2[int(ComboNodeImp2Routes.current())],InputValFLi2])
#         Data2=ReadTransitNetwork(ListBusStops=LBS2,Range=75)
#         # PlottingImportance(Data1=Data1,Data2=Data2)
#         print("\n\n############################################################ Data 1 ############################################################")
#         ListToGeoJson(ListBusStops=Data1)
#         # for data in Data1:
#         #     print(data)
#         print(type(Data1))
#         print("\n\n############################################################ Data 2############################################################")
#         ListToGeoJson(ListBusStops=Data2)
#         # for data in Data2:
#         #     print(data)
#         print(type(Data2))
#         # b=input()
#         UpdatePath(Key='Importance1',NewPath="")
#         UpdatePath(Key='Importance2',NewPath="")

#     ###############################################################################################
#     #First City
#     Geom1={'Coords':{'X':30,'Y':60},'Sizes':{'Hei':60,'Wid':650}}
#     Config1={"System":1,'TitleFrame':'Nodes','Command':'GetShpPath','Key':'Importance1'}
#     PathSHP(Frame=frame,Geom=Geom1,Config=Config1,)
#     print("#################################################")
#     print("#################################################")

#     Button=ttk.Button(frame,text="Get Fields")
#     Button.config(command=(ReqFields1))
#     Button.place(x=30, y=150, anchor=W)

#     ###############################################################################################
#     #Second City
#     Geom2={'Coords':{'X':30,'Y':280},'Sizes':{'Hei':60,'Wid':650}}
#     Config2={"System":2,'TitleFrame':'Nodes','Command':'GetShpPath','Key':'Importance2'}
#     PathSHP(Frame=frame,Geom=Geom2,Config=Config2)
#     print("#################################################")
#     print("#################################################")

#     Button=ttk.Button(frame,text="Get Fields")
#     Button.config(command=(ReqFields2))
#     Button.place(x=30, y=380, anchor=W)

#     ###############################################################################################
#     ###############################################################################################
#     Button=ttk.Button(frame,text="RUN")
#     Button.config(command=(RunAnalaysis))
#     Button.place(x=350, y=450, anchor=W)




# def NetworkAnalysis(frame):


#     ComboShp1Routes= ttk.Combobox(frame)
#     ComboShp1StartCode= ttk.Combobox(frame)
#     ComboShp1StartName= ttk.Combobox(frame)
#     ComboShp1EndCode= ttk.Combobox(frame)
#     ComboShp1EndName= ttk.Combobox(frame)

#     ComboShp2Routes = ttk.Combobox(frame)
#     ComboShp2StartCode = ttk.Combobox(frame)
#     ComboShp2StartName = ttk.Combobox(frame)
#     ComboShp2EndCode = ttk.Combobox(frame)
#     ComboShp2EndName = ttk.Combobox(frame)


#     NewList1=[]
#     NewList2 = []




#     def RunAnalaysis():
#         ########################################
#         # Get Variables for the first Shapefile

#         # Read the Path of the Shapefile
#         # print(RearPaths(Key='NetworkSimple1'))
#         P1=RearPaths(Key='NetworkSimple1')

#         # Get the Values from the ComboBoxes for the Field Index
#         InputIndexShp1Routes=int(ComboShp1Routes.current())-1
#         InputIndexShp1StartCode=int(ComboShp1StartCode.current())-1
#         InputIndexShp1StartName=int(ComboShp1StartName.current())-1
#         InputIndexShp1EndCode=int(ComboShp1EndCode.current())-1
#         InputIndexShp1EndName=int(ComboShp1EndName.current())-1
        
#         # Get the Values from the ComboBoxes for the Field Name
#         InputFieldNameShp1Routes=NewList1[int(ComboShp1Routes.current())]
#         InputFieldNameShp1StartCode=NewList1[int(ComboShp1StartCode.current())]
#         InputFieldNameShp1StartName=NewList1[int(ComboShp1StartName.current())]
#         InputFieldNameShp1EndCode=NewList1[int(ComboShp1EndCode.current())]
#         InputFieldNameShp1EndName=NewList1[int(ComboShp1EndName.current())]
        
#         # Show the values of each field
#         print("ComboShp1Routes  ",InputFieldNameShp1Routes,InputIndexShp1Routes)
#         print("ComboShp1StartCode  ",InputFieldNameShp1StartCode,InputIndexShp1StartCode)
#         print("ComboShp1StartName  ",InputFieldNameShp1StartName,InputIndexShp1StartName)
#         print("ComboShp1EndCode  ",InputFieldNameShp1EndCode,InputIndexShp1EndCode)
#         print("ComboShp1EndName  ",InputFieldNameShp1EndName,InputIndexShp1EndName)
#         # b=input()
#         # The Dictionary with the fields is created
#         FieldsShp1={'Line':[InputFieldNameShp1Routes,InputIndexShp1Routes],
#         'StartCode':[InputFieldNameShp1StartCode,InputIndexShp1StartCode],
#         'StartName':[InputFieldNameShp1StartName,InputIndexShp1StartName],
#         'EndCode':[InputFieldNameShp1EndCode,InputIndexShp1EndCode],
#         'EndName':[InputFieldNameShp1EndName,InputIndexShp1EndName],
#         }
#         print("FieldsShp1",FieldsShp1)
#         # b=input()
#         print(ReadFieldNames(Shapefile=P1))
#         print(".................................................................................................")

#         ########################################
#         # Get Variables for the Second Shapefile
#         # Read the Path of the Shapefile
#         # print(RearPaths(Key='NetworkSimple2'))
#         P2=RearPaths(Key='NetworkSimple2')

#         # Get the Values from the ComboBoxes for the Field Index
#         InputIndexShp2Routes=int(ComboShp2Routes.current())-1
#         InputIndexShp2StartCode=int(ComboShp2StartCode.current())-1
#         InputIndexShp2StartName=int(ComboShp2StartName.current())-1
#         InputIndexShp2EndCode=int(ComboShp2EndCode.current())-1
#         InputIndexShp2EndName=int(ComboShp2EndName.current())-1
        
#         # Get the Values from the ComboBoxes for the Field Name
#         InputFieldNameShp2Routes=NewList1[int(ComboShp2Routes.current())]
#         InputFieldNameShp2StartCode=NewList1[int(ComboShp2StartCode.current())]
#         InputFieldNameShp2StartName=NewList1[int(ComboShp2StartName.current())]
#         InputFieldNameShp2EndCode=NewList1[int(ComboShp2EndCode.current())]
#         InputFieldNameShp2EndName=NewList1[int(ComboShp2EndName.current())]
        
#         # Show the values of each field
#         print("ComboShp2Routes  ",InputFieldNameShp2Routes,InputIndexShp2Routes)
#         print("ComboShp2StartCode  ",InputFieldNameShp2StartCode,InputIndexShp2StartCode)
#         print("ComboShp2StartName  ",InputFieldNameShp2StartName,InputIndexShp2StartName)
#         print("ComboShp2EndCode  ",InputFieldNameShp2EndCode,InputIndexShp2EndCode)
#         print("ComboShp2EndName  ",InputFieldNameShp2EndName,InputIndexShp2EndName)

#         # The Dictionary with the fields is created
#         FieldsShp2={'Line':[InputFieldNameShp2Routes,InputIndexShp2Routes],
#         'StartCode':[InputFieldNameShp2StartCode,InputIndexShp2StartCode],
#         'StartName':[InputFieldNameShp2StartName,InputIndexShp2StartName],
#         'EndCode':[InputFieldNameShp2EndCode,InputIndexShp2EndCode],
#         'EndName':[InputFieldNameShp2EndName,InputIndexShp2EndName],
#         }
#         print("FieldsShp2",FieldsShp2)
#         # b=input()
#         print(ReadFieldNames(Shapefile=P2))
#         print(".................................................................................................")

#         ########################################
#         # Call for the External functions 

#         EdgeCollection,EdgeProperties,NodeCollection,NodeProperties=readShpNetWork(Shapefile=P1,Fileds=FieldsShp1)
#         G_Dict_1=CreateNetwork(List_Edges=EdgeCollection,Edge_Properties=EdgeProperties,List_Nodes=NodeCollection,Node_Properties=NodeProperties)
#         P2Prj=str(P1.split(".shp")[0])+".prj"
#         ident = EpsgIdent()
#         ident.read_prj_from_file(P2Prj)
#         Epsg1=ident.get_epsg()
#         print("Epsg1",Epsg1)
#         UpdatePath(Key='EPSGIN',NewPath=str(Epsg1))
#         SimpleNetworkToGeoJson(G=G_Dict_1)


#         EdgeCollection,EdgeProperties,NodeCollection,NodeProperties=readShpNetWork(Shapefile=P2,Fileds=FieldsShp2)
#         G_Dict_2=CreateNetwork(List_Edges=EdgeCollection,Edge_Properties=EdgeProperties,List_Nodes=NodeCollection,Node_Properties=NodeProperties)
#         P2Prj=str(P2.split(".shp")[0])+".prj"
#         ident = EpsgIdent()
#         ident.read_prj_from_file(P2Prj)
#         Epsg1=ident.get_epsg()
#         print("Epsg1",Epsg1)
#         UpdatePath(Key='EPSGIN',NewPath=str(Epsg1))
#         SimpleNetworkToGeoJson(G=G_Dict_2)


#         # G_List=[G_Dict_1,G_Dict_2]
#         # # PlotGraphs(G_List)
#         # for G_Dict in G_List:
#         #         SimpleNetworkToGeoJson(G=G_Dict)
#         #         b=input()

#         UpdatePath(Key='EPSGIN',NewPath="")

#         UpdatePath(Key='NetworkSimple1',NewPath="")
#         UpdatePath(Key='NetworkSimple2',NewPath="")


#     def ReqFields1():
#         print("\n"*2)
#         print(".................we get into the Fields 1........................")
#         P1=RearPaths(Key='NetworkSimple1')
#         print(P1)
#         if P1=='':
#             return None
#         List1=ReadFieldNames(Shapefile=P1)
#         print(List1)
#         # print(P1)
#         for elment in List1:
#             print("----------------------------------------------------------------------------",elment)
#             NewList1.append(elment[0])
#         ###################################################################################
#         ComboShp1Routes.config(width=17,values=NewList1)
#         ComboShp1Routes.place(x=120,y=140)
#         labelShp1Routes = Label(frame, text="Field with Routes/Line", font='Helvetica 12')
#         labelShp1Routes.place(x=120, y=120, anchor=W)
#         ###########################
#         ComboShp1StartCode.config(width=17,values=NewList1)
#         ComboShp1StartCode.place(x=280,y=140)
#         labelShp1StartCode = Label(frame, text="Field with Start Code", font='Helvetica 12')
#         labelShp1StartCode.place(x=280, y=120, anchor=W)
#         ###########################
#         ComboShp1StartName.config(width=17,values=NewList1)
#         ComboShp1StartName.place(x=440,y=140)
#         labelShp1StartName = Label(frame, text="Field with Start Name", font='Helvetica 12')
#         labelShp1StartName.place(x=440, y=120, anchor=W)
#         ###########################
#         ComboShp1EndCode.config(width=17,values=NewList1)
#         ComboShp1EndCode.place(x=280,y=200)
#         labelShp1EndCode = Label(frame, text="Field with End Code", font='Helvetica 12')
#         labelShp1EndCode.place(x=280, y=180, anchor=W)
#         ###########################
#         ComboShp1EndName.config(width=17,values=NewList1)
#         ComboShp1EndName.place(x=440,y=200)
#         labelShp1EndName = Label(frame, text="Field with End Name", font='Helvetica 12')
#         labelShp1EndName.place(x=440, y=180, anchor=W)

    
#     def ReqFields2():
#         print("\n"*2)
#         print(".................we get into the Fields 2........................")
#         P2=RearPaths(Key='NetworkSimple2')
#         print(P2)
#         if P2=='':
#             return None

#         List2=ReadFieldNames(Shapefile=P2)
#         print(List2)
#         # print(P2)
#         for elment in List2:
#             print("----------------------------------------------------------------------------",elment)
#             NewList2.append(elment[0])
#         ###################################################################################
#         ComboShp2Routes.config(width=17,values=NewList2)
#         ComboShp2Routes.place(x=120,y=340)
#         labelShp2Routes = Label(frame, text="Field with Routes/Line", font='Helvetica 12')
#         labelShp2Routes.place(x=120, y=320, anchor=W)
#         ###########################
#         ComboShp2StartCode.config(width=17,values=NewList2)
#         ComboShp2StartCode.place(x=280,y=340)
#         labelShp2StartCode = Label(frame, text="Field with Start Code", font='Helvetica 12')
#         labelShp2StartCode.place(x=280, y=320, anchor=W)
#         ###########################
#         ComboShp2StartName.config(width=17,values=NewList2)
#         ComboShp2StartName.place(x=440,y=340)
#         labelShp2StartName = Label(frame, text="Field with Start Name", font='Helvetica 12')
#         labelShp2StartName.place(x=440, y=320, anchor=W)
#         ###########################
#         ComboShp2EndCode.config(width=17,values=NewList2)
#         ComboShp2EndCode.place(x=280,y=400)
#         labelShp2EndCode = Label(frame, text="Field with End Code", font='Helvetica 12')
#         labelShp2EndCode.place(x=280, y=380, anchor=W)
#         ###########################
#         ComboShp2EndName.config(width=17,values=NewList2)
#         ComboShp2EndName.place(x=440,y=400)
#         labelShp2EndName = Label(frame, text="Field with End Name", font='Helvetica 12')
#         labelShp2EndName.place(x=440, y=380, anchor=W)


#     ###############################################################################################
#     #First City
#     Geom1={'Coords':{'X':30,'Y':60},'Sizes':{'Hei':60,'Wid':650}}
#     Config1={"System":1,'TitleFrame':'Nodes','Command':'GetShpPath','Key':'NetworkSimple1'}
#     PathSHP(Frame=frame,Geom=Geom1,Config=Config1,)
#     print("#################################################")
#     print("#################################################")

#     Button=ttk.Button(frame,text="Get Fields")
#     Button.config(command=(ReqFields1))
#     Button.place(x=30, y=150, anchor=W)


#     ###############################################################################################
#     #Second City
#     Geom2={'Coords':{'X':30,'Y':280},'Sizes':{'Hei':60,'Wid':650}}
#     Config2={"System":2,'TitleFrame':'Nodes','Command':'GetShpPath','Key':'NetworkSimple2'}
#     PathSHP(Frame=frame,Geom=Geom2,Config=Config2)
#     print("#################################################")
#     print("#################################################")

#     Button=ttk.Button(frame,text="Get Fields")
#     Button.config(command=(ReqFields2))
#     Button.place(x=30, y=380, anchor=W)


#     ###############################################################################################
#     ###############################################################################################
#     Button=ttk.Button(frame,text="RUN")
#     Button.config(command=(RunAnalaysis))
#     Button.place(x=350, y=450, anchor=W)


def GTFSOperation(frame):

    Path = ''
    def RunSingleZip():

        print("name:",RearPaths(Key='PathSingleGTFS'))
        Button["state"]=DISABLED
        SimpleNetwork=False
        if CheckVar1.get()==1:
            SimpleNetwork=True
        NodeNetwork=False
        if CheckVar2.get()==1:
            NodeNetwork=True
        RequestedData={"BusNetworkAnalysis":SimpleNetwork,"NodeNetworkAnalysis":NodeNetwork}

        GTFS(Path=RearPaths(Key='PathSingleGTFS'),RequestedData=RequestedData)

        print("CheckVar1:",CheckVar1.get(),SimpleNetwork)
        print("CheckVar2:",CheckVar2.get(),NodeNetwork)
        Button["state"]=NORMAL


    def PathZip():
        name = askopenfilename(initialdir=r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tools\SampleData",
                               filetypes=(("GTFS File", "*.zip"),
                                          ("All Files", "*.*")),
                               title="Choose a file.")
        Path = name

        print("#################################################")
        UpdatePath(Key='PathSingleGTFS', NewPath=name)
        if len(name) > 71:
            name = name[-65:]
            pass
        EntryElement.insert(0, name)
        print("Internal 1", Path,CheckVar1,CheckVar2)

    FrameElemento = ttk.LabelFrame(frame, height=70, width=750, text='Single file processing')
    FrameElemento.place(x=20, y=30, anchor=NW)

    CheckVar1 = IntVar()
    CheckVar2 = IntVar()
    C1 = Checkbutton(FrameElemento, text="Network Analysis",variable=CheckVar1)
    C2 = Checkbutton(FrameElemento, text="Node Network Analysis",variable=CheckVar2)
    C1.place(x=540, y=1, anchor=NW)
    C2.place(x=540, y=25, anchor=NW)

    EntryElement = ttk.Entry(FrameElemento, width=70)
    EntryElement.place(x=100, y=25, anchor=W)
    EntryElement.delete(0, END)
    EntryElement.insert(0, "")

    Button = ttk.Button(FrameElemento, text="Open")
    Button.config(command=(PathZip))
    Button.place(x=10, y=25, anchor=W)
    print("Internal 2", Path,CheckVar1,CheckVar2)

    Button = ttk.Button(FrameElemento, text="Run")
    Button.config(command=(RunSingleZip))
    Button.place(x=665, y=10, anchor=W)







# def NodeNetworkAnalysis(frame):

#     ###############################################################################################
#     # Frame that holds the tabs
#     FrameElemento=ttk.LabelFrame(frame,height = 550, width =650,text ='City Selection')
#     FrameElemento.place(x=30, y=30, anchor=NW)

#     nbCities = ttk.Notebook(frame)
#     nbCities.place(x=5,y=5)

#     T1 = tkinter.Frame(nbCities)
#     T2 = tkinter.Frame(nbCities)

#         #Add the tab
#     nbCities.add(T1, text="First City")
#     T1.config(height=540,width=640)
#     T1.config(relief= RIDGE)

#     #Add the tab
#     nbCities.add(T2, text="SecondCity")
#     T2.config(height=540,width=640)
#     T2.config(relief= RIDGE)


#     ComboShpA1Routes= ttk.Combobox(T1)
#     ComboShpA1StartCode= ttk.Combobox(T1)
#     ComboShpA1StartName= ttk.Combobox(T1)
#     ComboShpA1EndCode= ttk.Combobox(T1)
#     ComboShpA1EndName= ttk.Combobox(T1)

#     ComboShpA2Fid= ttk.Combobox(T1)
#     ComboShpA2Route= ttk.Combobox(T1)

#     ComboShpB1Routes = ttk.Combobox(T2)
#     ComboShpB1StartCode = ttk.Combobox(T2)
#     ComboShpB1StartName = ttk.Combobox(T2)
#     ComboShpB1EndCode = ttk.Combobox(T2)
#     ComboShpB1EndName = ttk.Combobox(T2)

#     ComboShpB2Fid= ttk.Combobox(T2)
#     ComboShpB2Route= ttk.Combobox(T2)


#     NewListA1=[]
#     NewListA2 = []
#     NewListB1=[]
#     NewListB2 = []

#     def RunAnalaysis():
#         ########################################
#         # Get Variables for the first Shapefile

#         # Read the Path of the Shapefile
#         # print(RearPaths(Key='NetworkSimple1'))
#         P1=RearPaths(Key='NetworkNodeLine1')

#         # Get the Values from the ComboBoxes for the Field Index
#         InputIndexShpA1Routes=int(ComboShpA1Routes.current())-1
#         InputIndexShpA1StartCode=int(ComboShpA1StartCode.current())-1
#         InputIndexShpA1StartName=int(ComboShpA1StartName.current())-1
#         InputIndexShpA1EndCode=int(ComboShpA1EndCode.current())-1
#         InputIndexShpA1EndName=int(ComboShpA1EndName.current())-1
        
#         # Get the Values from the ComboBoxes for the Field Name
#         InputFieldNameShpA1Routes=NewListA1[int(ComboShpA1Routes.current())]
#         InputFieldNameShpA1StartCode=NewListA1[int(ComboShpA1StartCode.current())]
#         InputFieldNameShpA1StartName=NewListA1[int(ComboShpA1StartName.current())]
#         InputFieldNameShpA1EndCode=NewListA1[int(ComboShpA1EndCode.current())]
#         InputFieldNameShpA1EndName=NewListA1[int(ComboShpA1EndName.current())]
        
#         # Show the values of each field
#         print("ComboShpA1Routes  ",InputFieldNameShpA1Routes,InputIndexShpA1Routes)
#         print("ComboShpA1StartName  ",InputFieldNameShpA1StartName,InputIndexShpA1StartName)
#         print("ComboShpA1StartCode  ",InputFieldNameShpA1StartCode,InputIndexShpA1StartCode)
#         print("ComboShpA1EndName  ",InputFieldNameShpA1EndName,InputIndexShpA1EndName)
#         print("ComboShpA1EndCode  ",InputFieldNameShpA1EndCode,InputIndexShpA1EndCode)
#         print("\n\n",P1)
#         # b=input()
#         # The Dictionary with the fields is created
#         FieldsShpA1={'Line':[InputFieldNameShpA1Routes,InputIndexShpA1Routes],
#         'StartCode':[InputFieldNameShpA1StartCode,InputIndexShpA1StartCode],
#         'StartName':[InputFieldNameShpA1StartName,InputIndexShpA1StartName],
#         'EndCode':[InputFieldNameShpA1EndCode,InputIndexShpA1EndCode],
#         'EndName':[InputFieldNameShpA1EndName,InputIndexShpA1EndName],
#         }
#         print(FieldsShpA1)
#         print(ReadFieldNames(Shapefile=P1))
#         print(".................................................................................................")
#         # b=input()

#         print(RearPaths(Key='NetworkBusStops1'))
#         InputIndexShpA2Fid=int(ComboShpA2Fid.current())-1
#         InputIndexShpA2FLine=int(ComboShpA2Route.current())-1
#         # InputIndexShpA2Fid=int(ComboShpA2Fid.current())
#         # InputIndexShpA2FLine=int(ComboShpA2Route.current())

#         InputFieldNameShpA2Fid=NewListA2[int(ComboShpA2Fid.current())]
#         InputFieldNameShpA2Routes=NewListA2[int(ComboShpA2Route.current())]

#         print("ComboShpA2Fid   ",InputIndexShpA2Fid,InputFieldNameShpA2Fid)
#         print("ComboShpA2Route",InputIndexShpA2FLine,InputFieldNameShpA2Routes)
#         # b=input()
#         # print(NewListA2,"\n",NewListA2[int(ComboShpA2Fid.current())],"\n",NewListA2[int(ComboShpA2Route.current())])
#         P2=RearPaths(Key='NetworkBusStops1')
#         print(P2)
#         print(ReadFieldNames(Shapefile=P2))
#         print(".................................................................................................")
#         # b=input()
#         #################################################################################################
#         #################################################################################################
#         #################################################################################################

#         ########################################
#         # Get Variables for the Second Shapefile
#         # Read the Path of the Shapefile
#         # print(RearPaths(Key='NetworkSimple2'))
#         P3=RearPaths(Key='NetworkNodeLine2')

#         # Get the Values from the ComboBoxes for the Field Index
#         InputIndexShpB1Routes=int(ComboShpB1Routes.current())-1
#         InputIndexShpB1StartCode=int(ComboShpB1StartCode.current())-1
#         InputIndexShpB1StartName=int(ComboShpB1StartName.current())-1
#         InputIndexShpB1EndCode=int(ComboShpB1EndCode.current())-1
#         InputIndexShpB1EndName=int(ComboShpB1EndName.current())-1
        
#         # Get the Values from the ComboBoxes for the Field Name
#         InputFieldNameShpB1Routes=NewListB1[int(ComboShpB1Routes.current())]
#         InputFieldNameShpB1StartCode=NewListB1[int(ComboShpB1StartCode.current())]
#         InputFieldNameShpB1StartName=NewListB1[int(ComboShpB1StartName.current())]
#         InputFieldNameShpB1EndCode=NewListB1[int(ComboShpB1EndCode.current())]
#         InputFieldNameShpB1EndName=NewListB1[int(ComboShpB1EndName.current())]
        
#         # Show the values of each field
#         print("ComboShpB1Routes  ",InputFieldNameShpB1Routes,InputIndexShpB1Routes)
#         print("ComboShpB1StartCode  ",InputFieldNameShpB1StartCode,InputIndexShpB1StartCode)
#         print("ComboShpB1StartName  ",InputFieldNameShpB1StartName,InputIndexShpB1StartName)
#         print("ComboShpB1EndCode  ",InputFieldNameShpB1EndCode,InputIndexShpB1EndCode)
#         print("ComboShpB1EndName  ",InputFieldNameShpB1EndName,InputIndexShpB1EndName)
#         # b=input()
#         # The Dictionary with the fields is created
#         FieldsShpB1={'Line':[InputFieldNameShpB1Routes,InputIndexShpB1Routes],
#         'StartCode':[InputFieldNameShpB1StartCode,InputIndexShpB1StartCode],
#         'StartName':[InputFieldNameShpB1StartName,InputIndexShpB1StartName],
#         'EndCode':[InputFieldNameShpB1EndCode,InputIndexShpB1EndCode],
#         'EndName':[InputFieldNameShpB1EndName,InputIndexShpB1EndName],
#         }
#         print(FieldsShpB1)
#         # print(ReadFieldNames(Shapefile=P3))
#         print(".................................................................................................")

#         print(RearPaths(Key='NetworkBusStops2'))
#         InputIndexShpB2Fid=int(ComboShpB2Fid.current())-1
#         InputIndexShpB2FLine=int(ComboShpB2Route.current())-1
#         # InputIndexShpB4Fid=int(ComboShpB2Fid.current())
#         # InputIndexShpB4FLine=int(ComboShpB2Route.current())

#         InputFieldNameShpB2Fid=NewListB2[int(ComboShpB2Fid.current())]
#         InputFieldNameShpB2Routes=NewListB2[int(ComboShpB2Route.current())]

#         print("ComboShpB2Fid   ",InputIndexShpB2Fid,InputFieldNameShpB2Fid)
#         print("ComboShpB2Route",InputIndexShpB2FLine,InputFieldNameShpB2Routes)
#         # b=input()
#         # print(NewListB2,"\n",NewListB2[int(ComboShpB2Fid.current())],"\n",NewListB2[int(ComboShpB2Route.current())])
#         P4=RearPaths(Key='NetworkBusStops2')
#         print(P4)
#         print(ReadFieldNames(Shapefile=P4))
#         print(".................................................................................................")

#         # b=input()
#         ########################################
#         # Call for the External functions 
#         # from NetworkAnalisys import AgregateTransitNetwork

#         EdgeCollection,EdgeProperties=readShpNetWorkForSimplification(Shapefile=P1,Fileds=FieldsShpA1)
#         LBS1=CalculateVecinityBusStops(Shapefile=P2,FieldId=[InputFieldNameShpA2Fid,InputIndexShpA2Fid] ,Routes= [InputFieldNameShpA2Routes,InputIndexShpA2FLine])
#         Nodes= AgregateTransitNetwork(ListBusStops=LBS1,Range=75)
#         G_Dict_1=AgregatedStopsToNetwork(AgregatedNodes=Nodes,Edge_List=EdgeCollection,Edge_Properties=EdgeProperties)
#         P2Prj=str(P2.split(".shp")[0])+".prj"
#         ident = EpsgIdent()
#         ident.read_prj_from_file(P2Prj)
#         Epsg1=ident.get_epsg()
#         print("Epsg1",Epsg1)
#         UpdatePath(Key='EPSGIN',NewPath=str(Epsg1))
#         NetWorkToGeoJson(G=G_Dict_1['G'])

#         EdgeCollection,EdgeProperties=readShpNetWorkForSimplification(Shapefile=P3,Fileds=FieldsShpB1)
#         LBS1=CalculateVecinityBusStops(Shapefile=P4,FieldId=[InputFieldNameShpB2Fid,InputIndexShpB2Fid] ,Routes= [InputFieldNameShpB2Routes,InputIndexShpB2FLine])
#         Nodes= AgregateTransitNetwork(ListBusStops=LBS1,Range=75)
#         G_Dict_2=AgregatedStopsToNetwork(AgregatedNodes=Nodes,Edge_List=EdgeCollection,Edge_Properties=EdgeProperties)
#         P2Prj=str(P4.split(".shp")[0])+".prj"
#         ident = EpsgIdent()
#         ident.read_prj_from_file(P2Prj)
#         Epsg1=ident.get_epsg()
#         print("Epsg1",Epsg1)
#         UpdatePath(Key='EPSGIN',NewPath=str(Epsg1))
#         NetWorkToGeoJson(G=G_Dict_2['G'])

#         # G_List=[G_Dict_1,G_Dict_2]

        

#         # for G_Dict in G_List:
#         #     NetWorkToGeoJson(G=G_Dict['G'])



#         UpdatePath(Key='EPSGIN',NewPath="")
#         UpdatePath(Key='NetworkNodeLine1',NewPath="")
#         UpdatePath(Key='NetworkBusStops1',NewPath="")
#         UpdatePath(Key='NetworkNodeLine2',NewPath="")
#         UpdatePath(Key='NetworkBusStops2',NewPath="")


#     def ReqFieldsA1():
#         print("\n"*2)
#         print(".................we get into the Fields 1........................")
#         P1=RearPaths(Key='NetworkNodeLine1')
#         print(P1)
#         if P1=='':
#             return None
#         List1=ReadFieldNames(Shapefile=P1)
#         print(List1)
#         # print(P1)
#         for elment in List1:
#             print("----------------------------------------------------------------------------",elment)
#             NewListA1.append(elment[0])
#         ###################################################################################
#         ComboShpA1Routes.config(width=17,values=NewListA1)
#         ComboShpA1Routes.place(x=120,y=140)
#         labelShpA1Routes = Label(T1, text="Field with Routes/Line", font='Helvetica 12')
#         labelShpA1Routes.place(x=120, y=120, anchor=W)
#         ###########################
#         ComboShpA1StartCode.config(width=17,values=NewListA1)
#         ComboShpA1StartCode.place(x=280,y=140)
#         labelShpA1StartCode = Label(T1, text="Field with Start Code", font='Helvetica 12')
#         labelShpA1StartCode.place(x=280, y=120, anchor=W)
#         ###########################
#         ComboShpA1StartName.config(width=17,values=NewListA1)
#         ComboShpA1StartName.place(x=440,y=140)
#         labelShpA1StartName = Label(T1, text="Field with Start Name", font='Helvetica 12')
#         labelShpA1StartName.place(x=440, y=120, anchor=W)
#         ###########################
#         ComboShpA1EndCode.config(width=17,values=NewListA1)
#         ComboShpA1EndCode.place(x=280,y=200)
#         labelShpA1EndCode = Label(T1, text="Field with End Code", font='Helvetica 12')
#         labelShpA1EndCode.place(x=280, y=180, anchor=W)
#         ###########################
#         ComboShpA1EndName.config(width=17,values=NewListA1)
#         ComboShpA1EndName.place(x=440,y=200)
#         labelShpA1EndName = Label(T1, text="Field with End Name", font='Helvetica 12')
#         labelShpA1EndName.place(x=440, y=180, anchor=W)


#     def ReqFieldsA2():

#         print("\n"*2)
#         print(".................we get into the Fields 2........................")
#         P2=RearPaths(Key='NetworkBusStops1')
#         print(P2)
#         if P2=='':
#             return None
#         List2=ReadFieldNames(Shapefile=P2)
#         # print(List2)
#         print(P2)
#         for elment in List2:
#             print("----------------------------------------------------------------------------",elment)
#             NewListA2.append(elment[0])
#         ComboShpA2Fid.config(width=17,values=NewListA2)
#         ComboShpA2Fid.place(x=130,y=360)
#         labelImp2Fid = Label(T1, text="Field with Node ID", font='Helvetica 12')
#         labelImp2Fid.place(x=130, y=320, anchor=W)

#         ComboShpA2Route.config(width=17,values=NewListA2)
#         ComboShpA2Route.place(x=300,y=360)
#         labelImp2Routes = Label(T1, text="Field with Routes/Lines", font='Helvetica 12')
#         labelImp2Routes.place(x=300, y=320, anchor=W)


#     def ReqFieldsB1():
#         print("\n"*2)
#         print(".................we get into the Fields 3........................")
#         P3=RearPaths(Key='NetworkNodeLine2')
#         print(P3)
#         if P3=='':
#             return None
#         List1=ReadFieldNames(Shapefile=P3)
#         print(List1)
#         # print(P3)
#         for elment in List1:
#             print("----------------------------------------------------------------------------",elment)
#             NewListB1.append(elment[0])
#         ###################################################################################
#         ComboShpB1Routes.config(width=17,values=NewListB1)
#         ComboShpB1Routes.place(x=120,y=140)
#         labelShpB1Routes = Label(T2, text="Field with Routes/Line", font='Helvetica 12')
#         labelShpB1Routes.place(x=120, y=120, anchor=W)
#         ###########################
#         ComboShpB1StartCode.config(width=17,values=NewListB1)
#         ComboShpB1StartCode.place(x=280,y=140)
#         labelShpB1StartCode = Label(T2, text="Field with Start Code", font='Helvetica 12')
#         labelShpB1StartCode.place(x=280, y=120, anchor=W)
#         ###########################
#         ComboShpB1StartName.config(width=17,values=NewListB1)
#         ComboShpB1StartName.place(x=440,y=140)
#         labelShpB1StartName = Label(T2, text="Field with Start Name", font='Helvetica 12')
#         labelShpB1StartName.place(x=440, y=120, anchor=W)
#         ###########################
#         ComboShpB1EndCode.config(width=17,values=NewListB1)
#         ComboShpB1EndCode.place(x=280,y=200)
#         labelShpB1EndCode = Label(T2, text="Field with End Code", font='Helvetica 12')
#         labelShpB1EndCode.place(x=280, y=180, anchor=W)
#         ###########################
#         ComboShpB1EndName.config(width=17,values=NewListB1)
#         ComboShpB1EndName.place(x=440,y=200)
#         labelShpB1EndName = Label(T2, text="Field with End Name", font='Helvetica 12')
#         labelShpB1EndName.place(x=440, y=180, anchor=W)

#     def ReqFieldsB2():

#         print("\n"*2)
#         print(".................we get into the Fields 4........................")
#         P4=RearPaths(Key='NetworkBusStops2')
#         print(P4)
#         if P4=='':
#             return None
#         List2=ReadFieldNames(Shapefile=P4)
#         # print(List2)
#         print(P4)
#         for elment in List2:
#             print("----------------------------------------------------------------------------",elment)
#             NewListB2.append(elment[0])
#         ComboShpB2Fid.config(width=17,values=NewListB2)
#         ComboShpB2Fid.place(x=130,y=360)
#         labelImpB2Fid = Label(T2, text="Field with Node ID", font='Helvetica 12')
#         labelImpB2Fid.place(x=130, y=320, anchor=W)

#         ComboShpB2Route.config(width=17,values=NewListB2)
#         ComboShpB2Route.place(x=300,y=360)
#         labelImpB2Routes = Label(T2, text="Field with Routes/Lines", font='Helvetica 12')
#         labelImpB2Routes.place(x=300, y=320, anchor=W)







#     ###############################################################################################
#     ###########################        First City               ###################################
#     ###############################################################################################

#     Geom1={'Coords':{'X':30,'Y':60},'Sizes':{'Hei':60,'Wid':650}}
#     Config1={"System":1,'TitleFrame':'Lines [First City]','Command':'GetShpPath','Key':'NetworkNodeLine1'}
#     PathSHP(Frame=T1,Geom=Geom1,Config=Config1,)
#     print("#################################################")
#     print("#################################################")

#     Button=ttk.Button(T1,text="Get Fields")
#     Button.config(command=(ReqFieldsA1))
#     Button.place(x=30, y=150, anchor=W)

#     ###############################################################################################
#     #Second City
#     Geom2={'Coords':{'X':30,'Y':280},'Sizes':{'Hei':60,'Wid':650}}
#     Config2={"System":2,'TitleFrame':'Nodes  [First City]','Command':'GetShpPath','Key':'NetworkBusStops1'}
#     PathSHP(Frame=T1,Geom=Geom2,Config=Config2)
#     print("#################################################")
#     print("#################################################")

#     Button=ttk.Button(T1,text="Get Fields")
#     Button.config(command=(ReqFieldsA2))
#     Button.place(x=30, y=380, anchor=W)

#     ###############################################################################################
#     Button=ttk.Button(T1,text="RUN")
#     Button.config(command=(RunAnalaysis))
#     Button.place(x=350, y=450, anchor=W)


#     ###############################################################################################
#     ###########################        Second City              ###################################
#     ###############################################################################################

#     Geom1={'Coords':{'X':30,'Y':60},'Sizes':{'Hei':60,'Wid':650}}
#     Config1={"System":1,'TitleFrame':'Lines [Second City]','Command':'GetShpPath','Key':'NetworkNodeLine2'}
#     PathSHP(Frame=T2,Geom=Geom1,Config=Config1,)
#     print("#################################################")
#     print("#################################################")

#     Button=ttk.Button(T2,text="Get Fields")
#     Button.config(command=(ReqFieldsB1))
#     Button.place(x=30, y=150, anchor=W)

#     ###############################################################################################
#     #Second City
#     Geom2={'Coords':{'X':30,'Y':280},'Sizes':{'Hei':60,'Wid':650}}
#     Config2={"System":2,'TitleFrame':'Nodes [Second City]','Command':'GetShpPath','Key':'NetworkBusStops2'}
#     PathSHP(Frame=T2,Geom=Geom2,Config=Config2)
#     print("#################################################")
#     print("#################################################")

#     Button=ttk.Button(T2,text="Get Fields")
#     Button.config(command=(ReqFieldsB2))
#     Button.place(x=30, y=380, anchor=W)

#     ###############################################################################################
#     Button=ttk.Button(T2,text="RUN")
#     Button.config(command=(RunAnalaysis))
#     Button.place(x=350, y=450, anchor=W)




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

    # def GenInputsNodeImportance():
    #     print("···································",comboNumCitiesI1)
    #     NumCities=comboNumCitiesI1.current()+1
    #     print("NumCities",NumCities,type(NumCities))
    #     YvalOringal=60
    #     for i in range(1,(NumCities+2)):
    #         Yval=YvalOringal+(200*i)


    #         Geom2={'Coords':{'X':30,'Y':(Yval+20)},'Sizes':{'Hei':90,'Wid':650}}
    #         Config2={'TitleFrame':'Area of the City'}
    #         PathEntry(Frame=f2,Geom=Geom2,Config=Config2)
    #         print("In tab, ",Pathshp)


    #Make 1st tab
    f1 = tkinter.Frame(nb)
    f2 = tkinter.Frame(nb)
    f3 = tkinter.Frame(nb)
    f4 = tkinter.Frame(nb)
    f5 = tkinter.Frame(nb)

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
 
    # Add the tab
    nb.add(f5, text="GTFS Analysis")
    f5.config(height=NotebookHeight,width=NotebookWidth)
    f5.config(relief= RIDGE)
 

 
    ##################################################################
    ##################################################################
    ###  TAB 2
    comboNumCitiesI1 = ttk.Combobox(f2,width=5,values=["2","3","4","5"])
    comboNumCitiesI1.place(x=230,y=31)
    
    # NodeRelevanceTab(frame=f2)
    # NetworkAnalysis(frame=f3)
    # NodeNetworkAnalysis(frame=f4)
    GTFSOperation(frame=f5)

    
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


import sqlite3
if __name__ == '__main__':
    main()
    Path=r'Paths.db'
    db = sqlite3.connect(Path)
    cursor = db.cursor()
