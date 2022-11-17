from logging.config import stopListening
import readline
import Calculations
import datetime


import utm
import os
import csv
import pyproj
import zipfile
import math
import sqlite3
import decimal
decimal.getcontext().prec = 10
from datetime import time
from tqdm import tqdm


from FeatureOperations import ConvertToUTM
from FeatureOperations import Agregate

from NetworkAnalisys import GtfsToNetwork
from Databases import TransportNames
from NetworkAnalisys import AgregatedGTFSStopsToNetwork
from NetworkAnalisys import NetWorkToGeoJson
from NetworkAnalisys import NewNetWorkToGeoJson
from NetworkAnalisys import NetworkLineAgregator
from AggregationTools import CreateNodes

from Clasification import TransformStopsCsvToGeoJson
from Clasification import GetStopDensity

from ClassCollection import BusStop

from GFTSsideProc import GetInfoData

import networkx as nx

from Tools import ProgressBarColor
from Tools import TimeDelta


def DataCleanerTrips(ListToClean):
    if len(ListToClean)>0:
        DictA={}
        # print(len(ListToClean))
        # b=input()  
        for var in ListToClean:
            if str(var) not in DictA.keys():
                DictA[str(var)]=[1,var]
            else:
                DictA[str(var)][0]=DictA[str(var)][0]+1
        ListOfFreq=[]
        DictB={}
        for key in DictA.keys():
            ListOfFreq.append(DictA[key][0])
            DictB[DictA[key][0]]=DictA[key][1]
            # print(key,DictA[key][0] )
            # print(DictA[key][1])
            # print()
        # print(max(ListOfFreq))
        # print(DictB[max(ListOfFreq)])
        return DictB[max(ListOfFreq)]
        # b=input()
    else:
        return []



def GetPosition(Field,Elements):
    for idx, Elem in enumerate(Elements):
        if Elem == Field: 
            return idx


def Distance(P1,P2):
    PX=math.pow(decimal.Decimal(P2[0])-decimal.Decimal(P1[0]),2)
    PY=math.pow(decimal.Decimal(P2[1])-decimal.Decimal(P1[1]),2)
    # print("X2:",P2[0],"X1:",P1[0],"D:",math.sqrt(PX+PY))
    # print("Y2:",P2[1],"y1:",P1[1])
    # print()
    return math.sqrt(PX+PY)


def ConstructSpatialNetworkSHP(DictStops,DataSequence,DataTrips,DataRoutes,DataStops):
    print("#######################################################################\n"*5)
    # This function requieres the following element 
    #   · DictStops | The list in sequence containing all the stops in the SELECTED system
    #   · DataSequence | The dictionary containing all the sequence of stops 
    #   · DataTrips | The dictionary containing all the trips in the routes in the system
    #   · DataRoutes | The dictionary containing  all the trips
    #   · DataStops | The dictionary containing all the stops in the system

    # print("DataStops",type(DataStops))
    # print(list(DataStops.keys())[:10])

    # b=input()
    # Setting the distance for the evaluation
    DistanceNode=75
    # print(type(DictStops))
    # obtaing the keys for the dictionary containing all the stops in the system
    KeysDS=list(DictStops.keys())
    # print("Length of Keys:",KeysDS)
    # print(KeysDS[:10])
    # A dictionary to contain the lines 
    CollectionLines={}
    # A cicle where all the 
    for i,key in enumerate(KeysDS):
        ProgressBarColor(current=1+i,total=len(KeysDS))
        # print("Line:",key)
        CollectionLines[key]=[[]]
        StoredStops=[]
        # print("A total of ",len(DictStops[key]['0']),"  of bus stops ")
        ListOutbound=DictStops[key]['0']
        ListInbound =DictStops[key]['1']
        ListInbound.reverse()

        if len(ListInbound)==0:
            CollectionLines[key]=[ListOutbound]
            continue 
        if len(ListOutbound)==0:
            CollectionLines[key]=[ListInbound]
            continue 

        # print("ListOutbound:",ListOutbound)
        # print("ListInbound: ",ListInbound)
  
        if len(ListOutbound)>len(ListInbound):
            # print("List Outbound (",len(ListOutbound),") is larger than List Inbound (",len(ListInbound))
            GuideListStops=ListOutbound
            ComplementListStop=ListInbound
        else:
            # print("List Outbound (",len(ListOutbound),") is shorter than List Inbound",len(ListInbound))
            GuideListStops=ListInbound
            ComplementListStop=ListOutbound

        # The longest is used to loop
        for idx,WorkStop in enumerate(GuideListStops):

            if idx < len(ComplementListStop):
                SecIdx=idx
            else:
                Num=len(ComplementListStop)-1-i
                while abs(Num)>len(ComplementListStop):
                    Num=Num+1
                SecIdx=Num

            # It is converted to UTM for both points 
            LatA=float(DataStops[WorkStop]['stop_lat'])
            LonA=float(DataStops[WorkStop]['stop_lon'])
            
            CoordUtm=list(utm.from_latlon(LatA, LonA))
            XA1=CoordUtm[0]
            YA1=CoordUtm[1]
            Val_EPSG1A=CoordUtm[2]
            # XA1,YA1,Val_EPSG1A=ConvertToUTM(lat=LatA,lon=LonA)

            LatB=float(DataStops[ComplementListStop[SecIdx]]['stop_lat'])
            LonB=float(DataStops[ComplementListStop[SecIdx]]['stop_lon'])

            CoordUtm=list(utm.from_latlon(LatB, LonB))
            XB1=CoordUtm[0]
            YB1=CoordUtm[1]
            Val_EPSG1B=CoordUtm[2]


            # XB1,YB1,Val_EPSG1B=ConvertToUTM(lat=LatB,lon=LonB)

            # dist=Distance(P1=(XA1,YA1),P2=(XB1,YB1))
            dist=Calculations.CalcDistance(XA1,YA1,XB1,YB1)

            if dist < DistanceNode:
                if WorkStop==ComplementListStop[SecIdx]:
                    CollectionLines[key][0].append(WorkStop)
                    StoredStops.append(WorkStop)
                else:
                    CollectionLines[key][0].append((WorkStop,ComplementListStop[SecIdx]))
                    StoredStops.append(WorkStop)
                    StoredStops.append(ComplementListStop[SecIdx])

            # print(CollectionLines[key][0])
            # print("\t Out Bound Stop: (",idx,") ",WorkStop," |  In Bound Stop (",SecIdx,")",ComplementListStop[SecIdx],dist)
            if dist > DistanceNode:
                ConditionCheck=False
                InferiorLimit=idx-3
                SuperiorLimit=idx+4
                if SuperiorLimit < len(ComplementListStop):
                    RangeOfOperation=list(range(InferiorLimit,SuperiorLimit))
                elif len(ComplementListStop)==2:
                    RangeOfOperation=[-2,-1,0,1]
                elif len(GuideListStops)==2:
                    RangeOfOperation=[-2,-1,0,1]
                # elif len(GuideListStops)==3:
                #     RangeOfOperation=[-3,-2,-1,0,1,2]

                else:
                    RangeOfOperation=[]
                    for i in range(InferiorLimit,SuperiorLimit):
                        # print("I calculaton",i)
                        if i < len(ComplementListStop):
                            RangeOfOperation.append(i)
                        else:
                            Num=len(ComplementListStop)-1-i
                            while abs(Num)>len(ComplementListStop):
                                Num=Num+1
                            RangeOfOperation.append(Num)
                        
                    # print(RangeOfOperation)
                # print(idx,"movingStop",RangeOfOperation,"Total in Guide:",len(GuideListStops)," Total in counterpart",len(ComplementListStop))
                for MovingIndex in RangeOfOperation:
                    # print("Work Stop",WorkStop,"MovingIndex",MovingIndex,ComplementListStop[MovingIndex])
                    LatA=float(DataStops[WorkStop]['stop_lat'])
                    LonA=float(DataStops[WorkStop]['stop_lon'])
                    CoordUtm=list(utm.from_latlon(LatA, LonA))
                    XA1=CoordUtm[0]
                    YA1=CoordUtm[1]
                    Val_EPSG1A=CoordUtm[2]

                    LatB=float(DataStops[ComplementListStop[MovingIndex]]['stop_lat'])
                    LonB=float(DataStops[ComplementListStop[MovingIndex]]['stop_lon'])
                    CoordUtm=list(utm.from_latlon(LatB, LonB))
                    XB1=CoordUtm[0]
                    YB1=CoordUtm[1]
                    Val_EPSG1B=CoordUtm[2]

                    # distMobile=Distance(P1=(XA1,YA1),P2=(XB1,YB1))
                    distMobile=Calculations.CalcDistance(XA1,YA1,XB1,YB1)

                    # print("\t\t",distMobile)
                    if distMobile<DistanceNode:
                        # print("Heeeeeeeeeeey")
                        ConditionCheck=True
                        NewMatch=ComplementListStop[MovingIndex]
                        break
                if ConditionCheck==False:
                    CollectionLines[key][0].append(WorkStop)
                    StoredStops.append(WorkStop)
                else:
                    CollectionLines[key][0].append((WorkStop,NewMatch))
                    StoredStops.append(WorkStop)
                    StoredStops.append(NewMatch)

        BackStored=False
        for idx, CompStop in enumerate(ComplementListStop):
            if CompStop not in StoredStops:
                # print("CollectionLines[key][-1]",CollectionLines[key][-1])
                if BackStored==True:
                    # print("Storing Simple")
                    CollectionLines[key][-1].append(CompStop)
                    StoredStops.append(CompStop)
                else:
                    # print("Add list")
                    BackStored=True
                    CollectionLines[key].append([])
                    CollectionLines[key][-1].append(ComplementListStop[idx-1])
                    CollectionLines[key][-1].append(CompStop)
                    StoredStops.append(CompStop)

            else:
                if BackStored==True: 
                    CollectionLines[key][-1].append(CompStop)
                BackStored=False
                

        # print("CollectionLines",CollectionLines[key],"\n")
        # print("ListInbound: ",ListInbound,"\n")
        # print("ListOutbound:",ListOutbound,"\n")
    return CollectionLines
        # b=input("Hello!")

def AverageDistanceBetweenStops(Data):
    ListDistance=[]
    for line in Data.keys():
        # print( line )
        for leg in Data[line]:
            # print()
            # print(leg)
            for idx,stop in enumerate(leg[:-1]):
                nextStop=leg[idx+1]
                # print(idx,stop,nextStop)
                P1=(stop[1],stop[2])
                P2=(nextStop[1],nextStop[2])
                # Dist=Distance(P1=P1,P2=P2)
                Dist=Calculations.CalcDistance(P1[0],P1[1],P2[0],P2[1])

                ListDistance.append(Dist)
    return sum(ListDistance)/len(ListDistance),len(ListDistance)







def GetMediumPoint(P1,P2):
    P3x=(P1[0]+P2[0])/2
    P3y=(P1[1]+P2[1])/2
    return P3x,P3y


def ConvertToUTM(lat,lon):
    import warnings
    warnings.filterwarnings("ignore")
    Zone=int((float(lon)/6)+31)
    if float(lat)>0:
        Val_EPSG="epsg:326"+str(Zone)
    elif float(lat)<0:
        Val_EPSG="epsg:325"+str(Zone)
    proj_wgs84 = pyproj.Proj(init="epsg:4326")
    proj_utm = pyproj.Proj(init=str(Val_EPSG))
    x, y = pyproj.transform(proj_wgs84, proj_utm, lon, lat)
    # print("lat",lat,"lon",lon)
    # print("x",x,"y",y)
    # b=input('Press Enter ...')

    return x,y,Val_EPSG

def GetMiddlePoint(CollLines,DataStops):
    # print("#######################################################################\n"*5)

    ExitCollection={}
    # for key in CollLines.keys():
    KeyList=list(CollLines.keys())
    for key in KeyList:
        # print()
        # print("#########################################################################################")
        ExitCollection[key]=[]
        # print(CollLines[key])
        for idx, line in enumerate(CollLines[key]):
            ExitCollection[key].append([])
            # print()

            # print("---",key)
            for idy,tup in enumerate(line):
                
                # print()
                # print(key,idx,".",idy,"|     ",tup,"    |",end="\t\t")
                # print("type:",type(tup),end=" | ")
                # if type(tup)=='tuple':
                # if type(tup)=='tuple':
                if isinstance(tup, tuple):
                    # P1=ConvertToUTM(lat=float(DataStops[tup[0]]['stop_lat']),lon=float(DataStops[tup[0]]['stop_lon']))
                    # P2=ConvertToUTM(lat=float(DataStops[tup[1]]['stop_lat']),lon=float(DataStops[tup[1]]['stop_lon']))

                    P1=list(utm.from_latlon(float(DataStops[tup[0]]['stop_lat']),float(DataStops[tup[0]]['stop_lon'])))

                    P2=list(utm.from_latlon(float(DataStops[tup[1]]['stop_lat']),float(DataStops[tup[1]]['stop_lon'])))
                    P3x,P3y=GetMediumPoint(P1=P1,P2=P2)
                    # print(key,idy,P3x,P3y,"Calculated middle point",end="")
                elif type(tup)  is str:
                    P3x,P3y,Epsg=ConvertToUTM(lat=float(DataStops[tup]['stop_lat']),lon=float(DataStops[tup]['stop_lon']))
                    # print(key,idy,P3x,P3y,"Direct transfer",end="")
                # print(key,idy,P3x,"\t",P3y,"\t|",tup)
                ExitCollection[key][-1].append((tup,P3x,P3x))
            # print("ExitCollection[key]",key,ExitCollection[key])
    return ExitCollection

                

        
    



def ConvertToLatLon(x,y,Val_EPSG):

    inProj = pyproj.Proj(init=Val_EPSG)
    outProj = pyproj.Proj(init='epsg:4326')
    x2,y2 = pyproj.transform(inProj,outProj,x,y)
    print (x2,y2)

    return x2,y2

    


def ReadGTFS(PathRoutes,PathTrips,PathStopTimes,PathStops,PathCalendar):
    #############################################################################
    ######    READ THE STOP TIME FILE
    #############################################################################
    #############################################################################



    # A container to store the sequence of stops
    DataCalendar={}
    # The file is opened using the python-csv tool
    with open(PathCalendar,encoding="utf-8-sig") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        headers = next(csv_reader, None)
        # print(headers)
        # b=input()
        for row in csv_reader:
            Dict={}
            # print(row,type(row),len(row))
            for idx,Element in enumerate(row):
                Dict[headers[idx]]=Element
            # print(Dict)
            # When there is a new trip, from the trips the routs are obtained.
            # if Dict['service_id'] not in DataCalendar.keys():
            #     DataCalendar[Dict['service_id']]={}
            DataCalendar[Dict['service_id']]=Dict
    # print(len(DataCalendar.keys()))
    # print("CHECK HERE")
    # b=input('.................................')



    # A container to store the sequence of stops
    DataSequence={}
    # The file is opened using the python-csv tool
    with open(PathStopTimes,encoding="utf-8-sig") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        headers = next(csv_reader, None)
        # print(headers)
        # b=input()
        for row in csv_reader:
            Dict={}
            # print(row,type(row),len(row))
            for idx,Element in enumerate(row):
                Dict[headers[idx]]=Element
            # print(Dict.keys())
            # When there is a new trip, from the trips the routs are obtained.
            if Dict['trip_id'] not in DataSequence.keys():
                DataSequence[Dict['trip_id']]={}
            DataSequence[Dict['trip_id']][int(Dict['stop_sequence'])]=Dict

        #     print(Dict['trip_id'])
        #     print(Dict['stop_sequence'],type(Dict['stop_sequence']))
        #     print(Dict,"\n")
        #     print(DataSequence[Dict['trip_id']],[int(Dict['stop_sequence'])],"\n")
        #     print("DataSequence[Dict['trip_id']][int(Dict['stop_sequence'])]",DataSequence[Dict['trip_id']][int(Dict['stop_sequence'])])
        #     b=input()
        # b=input()
    # print("Done reading StopTimes")
    # b=input()

    #############################################################################
    ######    READ THE TRIPS FILE
    #############################################################################
    #############################################################################

    # A container is created to store the trips
    DataTrips={}
    # The file is opened using the python-csv tool
    with open(PathTrips,encoding="utf-8-sig") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        Headers = next(csv_reader, None)
        # print("TRIPS FILE",Headers)
        # b=input()
        for row in csv_reader:
            Dict={}
            # print(row,type(row),len(row))
            for idx,Element in enumerate(row):
                Dict[Headers[idx]]=Element
            if Dict['route_id'] not in DataTrips.keys():
                DataTrips[Dict['route_id']]={}
            DataTrips[Dict['route_id']][Dict['trip_id']]=Dict
            # print(DataTrips)
            # b=input()  
    # print("Done reading Trips")
    # b=input()

    #############################################################################
    ######    READ THE ROUTES FILE
    #############################################################################
    #############################################################################

    DataRoutes={}
    with open(PathRoutes,encoding="utf-8-sig") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        Headers = next(csv_reader, None)
        # print("ROUTES FILE",Headers)
        # b=input()
        for row in csv_reader:
            Dict={}
            # print(row,type(row),len(row))
            for idx,Element in enumerate(row):
                Dict[Headers[idx]]=Element
            DataRoutes[Dict['route_id']]=Dict

            # for keyRoute in DataRoutes.keys():
                # print(DataRoutes[keyRoute])
            # b=input()
    # print(DataRoutes)
    # print("Done reading Routes")
    # b=input()

    #############################################################################
    ######    READ THE STOPS FILE
    #############################################################################
    #############################################################################

    DataStops={}
    with open(PathStops,encoding="utf-8-sig") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        Headers = next(csv_reader, None)
        # print("ROUTES FILE",Headers)
        # b=input()
        for row in csv_reader:
            Dict={}
            # print(row,type(row),len(row))
            for idx,Element in enumerate(row):
                Dict[Headers[idx]]=Element
            # print(Dict.keys())
            DataStops[Dict['stop_id']]=Dict

            # for keyRoute in DataStops.keys():
            #     print(DataStops[keyRoute])
            # # print(Dict)
            # b=input()
    # print(DataRoutes)
    # print("Done reading Routes")
    # b=input()

    return DataSequence,DataTrips,DataRoutes,DataStops

def GetSystemData(Path):

    if os.name=='nt':
        with open(Path,encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            headers = next(csv_reader, None)
            # print(headers)
            # b=input()
            print(csv_reader)
            for idx,row in enumerate(csv_reader):
                print(idx,row)
                if idx==0:
                    Agency=row[1]
            print("................................\n")
            print("Agency",Agency)
            print("................................\n")
            return Agency
            # b=input('Press Enter ...')
    if os.name=="posix":
        with open(Path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            headers = next(csv_reader, None)
            # print(headers)
            # b=input()
            print(csv_reader)
            for idx,row in enumerate(csv_reader):
                print(idx,row)
                if idx==0:
                    Agency=row[1]
            print("................................\n")
            print("Agency",Agency)
            print("................................\n")
            return Agency



def GtfsRouteCleaning(DataSequence,DataTrips,DataRoutes,DataStops,CatalogTypes,CountType):
    print("Starts #################### GtfsRouteCleaning ####################")
    # b=input()
    GeneralData_Frequencys={}
    BusRoutes={}
    TrainRoutes={}
    TramRoutes={}
    MetroRoutes={}
    OtherRoutes={}


    #'0':Tram, Streetcar, Light rail. Any light rail or street level system within a metropolitan area.
    #'1':Subway, Metro. Any underground rail system within a metropolitan area.
    #'2':Rail. Used for intercity or long-distance travel.
    #'3':Bus. Used for short- and long-distance bus routes.
    #'4':Ferry. Used for short- and long-distance boat service.
    #'5':Cable tram. Used for street-level rail cars where the cable runs beneath the vehicle, e.g., cable car in San Francisco.
    #'6':Aerial lift, suspended cable car (e.g., gondola lift, aerial tramway). Cable transport where cabins, cars, gondolas or open chairs are suspended by means of one or more cables.
    #'7':Funicular. Any rail system designed for steep inclines.
    #'11':Trolleybus. Electric buses that draw power from overhead wires using poles.
    #'12':Monorail. Railway in which the track consists of a single rail or a beam.
    #---------------------------------
    #'100':Railway Service
    #'109':Suburban Railway
    #'116':Rack and Pinion Railway
    #---------------------------------
    #'400':Urban Railway Service
    #'401':Metro Service
    #'402':Underground Service
    #'403':Urban Railway Service
    #'404':All Urban Railway Services
    #'405':Monorail
    #---------------------------------
    #'700':Bus Service
    #'701':Regional Bus Service
    #'702':Express Bus Service
    #'704':Local Bus Service
    #'705':Night Bus Service
    #'707':Special Needs Bus
    #'800':Trolleybus Service
    #---------------------------------
    #'900':Tram Service
    #'901':City Tram Service
    #'902':Local Tram Service
    #'903':Regional Tram Service
    #'906':All Tram Services
    #---------------------------------
    #'1000':Water Transport Service
    #'1400':Funicular Service
    #---------------------------------

    BusType=CatalogTypes['BusType']
    TrainType=CatalogTypes['TrainType']
    Metrotype=CatalogTypes['Metrotype']
    TramType=CatalogTypes['TramType']
    OtherType=CatalogTypes['OtherType']

    for key in DataRoutes.keys():
        # print(DataRoutes[key]['route_type'],type(DataRoutes[key]['route_type']))
        CountType[DataRoutes[key]['route_type']]=CountType[DataRoutes[key]['route_type']]+1
        # print(DataRoutes)
        if DataRoutes[key]['route_type'] in BusType:
            BusRoutes[key]=DataRoutes[key]
        if DataRoutes[key]['route_type'] in TrainType:
            TrainRoutes[key]=DataRoutes[key]
        if DataRoutes[key]['route_type'] in TramType:
            TramRoutes[key]=DataRoutes[key]
        if DataRoutes[key]['route_type'] in Metrotype:
            MetroRoutes[key]=DataRoutes[key]
        if DataRoutes[key]['route_type'] in OtherType:
            OtherRoutes[key]=DataRoutes[key]

    #######################################################################
    def RoutSeparator(TransportCodes):
        OutputList=[]
        for RouteKey in DataRoutes.keys():
            BusStopsInRoute={}
            if DataRoutes[RouteKey]['route_type'] in TransportCodes:
                # print('route_id',DataRoutes[RouteKey]['route_id'])
                VarRouteId=DataRoutes[RouteKey]['route_id']
                # print("-----------------------------------------------------------------------------------------------------------------------------------")
                # print("VarRouteId",VarRouteId)
                if VarRouteId in DataTrips:
                    OutputList.append(VarRouteId)
        return OutputList
        # print("#########################################################################################################\n"*5)
        # print("ListofBusRoutes",type(ListofBusRoutes),len(ListofBusRoutes))
        # print(ListofBusRoutes[:15])

    ListofBusRoutes=RoutSeparator(TransportCodes=BusType)
    ListofTrainRoutes=RoutSeparator(TransportCodes=TrainType)
    ListofMetroRoutes=RoutSeparator(TransportCodes=Metrotype)
    ListofTramRoutes=RoutSeparator(TransportCodes=TramType)
    ListofOtherRoutes=RoutSeparator(TransportCodes=OtherType)
    ##################################################

    def DataGenerator(ListOfElements):
        Data={}
        for RouteKey in ListOfElements:
            VarRouteId=DataRoutes[RouteKey]['route_id']
            Data[RouteKey]={'0':[],'1':[]}
            ListOfStopsCero=[]
            ListOfStops_One=[]
            for Tripkey in DataTrips[VarRouteId]:
                ListOfStops=[]
                # print("#########################################################################")
                # print("DataTrips[VarRouteId][Tripkey]")
                # print(DataTrips[VarRouteId][Tripkey])
                if Tripkey in DataSequence.keys():
                    for SeqKey in DataSequence[Tripkey].keys():
                        ListOfStops.append(DataSequence[Tripkey][SeqKey]['stop_id'])
                if 'direction_id' in DataTrips[VarRouteId][Tripkey]:
                    VarDirectionId=DataTrips[VarRouteId][Tripkey]['direction_id']
                    if VarDirectionId=='0':
                        ListOfStopsCero.append(ListOfStops)
                    if VarDirectionId=='1':
                        ListOfStops_One.append(ListOfStops)
                else:
                    print(DataTrips[VarRouteId][Tripkey])
                    b=input("It works")
            Data[RouteKey]['0']=DataCleanerTrips(ListToClean=ListOfStopsCero)
            Data[RouteKey]['1']=DataCleanerTrips(ListToClean=ListOfStops_One)
        return Data

    # print("ListofBusRoutes",len(ListofBusRoutes))
    # print("ListofTrainRoutes",len(ListofTrainRoutes))
    # print("ListofMetroRoutes",len(ListofMetroRoutes))
    # print("ListofMetroRoutes",len(ListofMetroRoutes))
    # print("ListofOtherRoutes",len(ListofOtherRoutes))
    # b=input()
    Data_Buses=DataGenerator(ListOfElements=ListofBusRoutes)
    Data_Train=DataGenerator(ListOfElements=ListofTrainRoutes)
    Data_Metro=DataGenerator(ListOfElements=ListofMetroRoutes)
    Data_Tram=DataGenerator(ListOfElements=ListofTramRoutes)
    Data_Other=DataGenerator(ListOfElements=ListofOtherRoutes)
    print("Data_Buses",len(Data_Buses.keys()))
    print("Data_Train",len(Data_Train.keys()))
    print("Data_Metro",len(Data_Metro.keys()))
    print("Data_Tram",len(Data_Tram.keys()))
    print("Data_Other",len(Data_Other.keys()))


    return [Data_Buses,Data_Train,Data_Metro,Data_Tram,Data_Other]



def GetOrder(Data):
    LegData={}
    for key in Data.keys():
        # print( key)
        # print("\t",Data[key]['0'])
        LegData[key]={'0':[],'1':[]}
        Data0=Data[key]['0']
        if len(Data0)>0:
            # print(len(Data0),type(Data0),"Last Value:",Data0[-1])
            for idx,Stop in enumerate(Data0[:-1]):
                iD1=idx
                iD2=idx+1
                LegData[key]['0'].append((Data0[iD1],Data0[iD2]))
                # print("\t\t",iD1,iD2,Data0[iD1],Data0[iD2])
        # print("\t",Data[key]['1'])
        Data1=Data[key]['1']
        if len(Data1)>0:
            # print(len(Data1),type(Data1),"Last Value:",Data1[-1])
            for idx,Stop in enumerate(Data1[:-1]):
                iD1=idx
                iD2=idx+1
                LegData[key]['1'].append((Data1[iD1],Data1[iD2]))
                # print("\t\t",iD1,iD2,Data1[iD1],Data1[iD2])
        # print("---------------------")
        # for leg in LegData[key]['0']:
        #     print(leg)
        # print("---------------------")
        # for leg in LegData[key]['1']:
        #     print(leg)

    return LegData


def ListGTFStoObjectBusStop(EdgeData,DataStops,Data_Buses):
    List_Nodes_Key=list(DataStops.keys())
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

    LinkStopRoutes={}
    ListStoptsObj=[]
    for Stop in List_Nodes:#[:100]
        LinkStopRoutes[Stop]=[]
        # print("Stop",Stop, end="")
        x,y,Val_EPSG=ConvertToUTM(lat=DataStops[Stop]['stop_lat'],lon=DataStops[Stop]['stop_lon'])
        # print("stop_lat",DataStops[Stop]['stop_lat'],"stop_lon",DataStops[Stop]['stop_lon'])
        # print("\t",x,"-",y)
        # b=input('Press Enter ...')
        # print(DataStops[Stop])
        NdObj=BusStop()
        NdObj.Id=Stop
        NdObj.CoordX=x
        NdObj.CoordY=y
        NdObj.Epsg=Val_EPSG
        ListStoptsObj.append(NdObj)

    print("Len List_Nodes",len(List_Nodes))
    for RoKey in Data_Buses.keys():
        # print(RoKey)
        for DirKey in Data_Buses[RoKey].keys():
            # print("\t",DirKey)
            # print("\t\t",Data_Buses[RoKey][DirKey])
            for Stop in Data_Buses[RoKey][DirKey]:
                if RoKey not in LinkStopRoutes[Stop]:
                    LinkStopRoutes[Stop].append(RoKey)

    for ObjStop in ListStoptsObj:
        ObjStop.Routes=LinkStopRoutes[ObjStop.Id]
    #    print(ObjStop.Id,"  X:",ObjStop.CoordX,"  Y:",ObjStop.CoordY,"  Routes:",ObjStop.Routes)
    return ListStoptsObj

def GetEdgeLists(EdgeData):
    EdgeList=[]
    EdgeLine={'Line':{}}
    for key in EdgeData.keys():
        # print("key",key,type(EdgeData[key]))
        for key2 in EdgeData[key]:
            # print("\t\tkey2",key2,type(key2),type(EdgeData[key][key2]))
            LocalEdgeList=EdgeData[key][key2]
            for edge in LocalEdgeList:
                # print("\t\t\t",edge)
                if edge not in EdgeList:
                    EdgeList.append(edge)
                    EdgeLine['Line'][edge]=[]
                    EdgeLine['Line'][edge].append(key)
                elif edge in EdgeLine.keys():
                    EdgeLine['Line'][edge].append(key)
    return EdgeList,EdgeLine

def Runnzip(Path):
    import zipfile
    archive = zipfile.ZipFile(Path, 'r')
    with archive as zip: 
        ZipList=zip.namelist()
    archive = zipfile.ZipFile(Path, 'r')
    for zipfile in ZipList:
        # print("zipfil  e",zipfile)
        fw=open(r"Operational\\"+zipfile,"w", encoding="utf-8")
        FilePointer=archive.open(zipfile)
        for line in FilePointer.readlines():
            # print(line,type(line))
            try:
                text=line.decode("utf-8-sig").rstrip()
                if text[-1]=="\n":
                    text=text.rstrip()
                if text !="":
                    text=text+"\n"
                    fw.write(text)
                # if zipfile=="stop_times.txt":
                #     print("#",text,"#",type(text))
                #     b=input('Press Enter ...')
            # b=input('Press Enter ...')
            except:
                print("Cannot decopress ")

        fw.close()

def RunZipUnix(Path):
    print("Getting into Run Zip for unix")
    import zipfile
    import pathlib

    Pa=pathlib.Path().absolute()
    print("ffffffffffffffffffffffffffffffffffffffffffffffffff",Pa)

    archive = zipfile.ZipFile(Path, 'r')
    with archive as zip: 
        ZipList=zip.namelist()
    archive = zipfile.ZipFile(Path, 'r')
    for zipfile in ZipList:
        print("zipfil  e",zipfile)
        fw=open(r"Operational/"+zipfile,"w", encoding="utf-8")
        FilePointer=archive.open(zipfile)
        for line in FilePointer.readlines():
            # print(line,type(line))
            try:
                text=line.decode("utf-8-sig").rstrip()
                if text[-1]=="\n":
                    text=text.rstrip()
                if text !="":
                    text=text+"\n"
                    fw.write(text)
                # if zipfile=="stop_times.txt":
                #     print("#",text,"#",type(text))
                #     b=input('Press Enter ...')
            # b=input('Press Enter ...')
            except:
                print("Cannot decopress ")
        fw.close()


    # b=input("Waiting")

def DatabaseConnection():
    print("Into the Op")
    conn = sqlite3.connect('./Databases/CityDataStorage.db')
    print("Conected")
    cursor = conn.execute("Select * From CityData")
    print("Cursorr read")

    for row in cursor:
        print(row)
    return conn



def CleanFiles():
    print("······································")
    print("···· CLEANING      ···················")
    print("······································")
    entries = os.listdir("Operational")	
    for entry in entries:
        # print(entry,type(entry))
        FullPath=os.path.abspath("Operational/"+entry)
        # print(FullPath)
        # print()text
        os.remove(FullPath)

def GetTypesofTransport(InputDict):
    ExitList=[]
    Names=TransportNames()
    TypesOfTransport={}
    for key in InputDict.keys():
        # print(key,'route_type',InputDict[key]['route_type'])
        if InputDict[key]['route_type'] in TypesOfTransport.keys():
            TypesOfTransport[InputDict[key]['route_type']]=TypesOfTransport[InputDict[key]['route_type']]+1
        else:
            TypesOfTransport[InputDict[key]['route_type']]=1
    # print(TypesOfTransport)
    # print("Number of Routes:")
    for Type in TypesOfTransport.keys():
        # print(Names[Type],TypesOfTransport[Type])
        ExitList.append([Names[Type],TypesOfTransport[Type]])
    return ExitList

# def GetNumberOfStops(InputDict):
    # for key in InputDict.keys():
    #     print(InputDict[key])
def GetLineNums(Path,CatalogTypes):
        print("#############################################")
        print("################GetLineNums##################")
        
        ExitNums={0:0,1:0,2:0,3:0,4:0}

        for key in CatalogTypes.keys():
            print(key, "          ",CatalogTypes[key],"\n")
        cont=0
        with open(Path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            header=[]
            # print(dir(reader))
            for row in reader:
                cont+=1
                if cont==1:
                    print(row,type(row))
                    for idx, head in enumerate(row):
                        print(str(idx),str(head),end="\t")
                        header.append(head)
                        if str(head) =="route_type":
                            IndexType=idx
                    print("\nheader")
                    print(header)
                    # b=input('.................................')
                    # print("IndexType",IndexType,str(row[IndexType]))     
        #             # b=input(".................")

                else:
                    print("\t\t",row[IndexType],type(row[IndexType]))
                    for i,key in enumerate(CatalogTypes.keys()):
                        if row[IndexType] in CatalogTypes[key]:
                            ExitNums[i]+=1
                    # b=input('.................................')
        #             if int(row[IndexType].replace("\"","")) in CountType:
        #                 if row[IndexType] not in Nums.keys():
        #                     Nums[row[IndexType]]=1
        #                 else:
        #                     Nums[row[IndexType]]+=1
        #             # else:
        #             #     b=input(".................")

        # for k in ExitNums.keys():
        #     print(k,"  -  ",ExitNums[k])
        # b=input('.................................')
        return ExitNums

def StoreCityData(NameOfCity,TransitChar,NumberLines,City):
    ###################################################
    ####### Individual file  ##########################
    ###################################################
    #Overwrites the file for the city
    Titles=["Bus Network","Rail Network","Metro Network","Light Rail Netwrok","Other Network","Node Network"]
    NameOfCity=NameOfCity.replace("/",".")
    Path=r"/mnt/e/GitHub/CAMMM-Tool_1.3/Results/CityMetrics/"+NameOfCity+".txt"
    print("NameOfCity:",NameOfCity)
    print("TransitChar")
    print(TransitChar)
    print("NumberLines")
    print(NumberLines)
    fw=open(Path,"w")
    Text=""
    Text+="###### Numer of Stops\n"
    for Sys in TransitChar.keys():
        Text+=str(Titles[int(Sys)])+","+str(Sys)+","+str(TransitChar[Sys]["NumStops"])+"\n"
    Text+="###### Avg Dist of stops\n"
    for Sys in TransitChar.keys():
        Text+=str(Titles[int(Sys)])+","+str(Sys)+","+str(TransitChar[Sys]["AvDist"])+"\n"
    Text+="###### Numer of lines\n"
    for Sys in NumberLines.keys():
        if Sys in TransitChar.keys():
            Text+=str(Titles[int(Sys)])+","+str(Sys)+","+str(NumberLines[Sys])+"\n"
    fw.write(Text)
    fw.close()

    ###################################################
    ####### General Table #############################
    ###################################################

    GeneralPath="/mnt/e/GitHub/CAMMM-Tool_1.3/Results/CityMetrics/GeneralData.csv"
    import csv
    headers=["City","Bus_NumStops","Bus_AvDist","Bus_NumLines","Rail_NumStops","Rail_AvDist","Rail_NumLines","Metro_NumStops","Metro_AvDist","Metro_NumLines","LightRail_NumStops","LightRail_AvDist","LightRail_NumLines","Other_NumStops","Other_AvDist","Other_NumLines"]
    Data=[]
    with open(GeneralPath,encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        headersZ = next(csv_reader, None)
        print(csv_reader)
        for idx,row in enumerate(csv_reader):
            print(idx,row,type(row))
            # print("····················································")
            if row[0]!=City:
                Data.append(row)
    csv_file.close()
    # hay un problema aqui
    data_file = open(GeneralPath, 'w')
    # create the csv writer object
    csv_writer = csv.writer(data_file)
    csv_writer.writerow(headers)

    for city in Data:
        csv_writer.writerow(city)
    DataToStore=[City]
    for Sys in range(0,5):
        if Sys in TransitChar.keys():
            DataToStore.append(str(TransitChar[Sys]["NumStops"]))
            DataToStore.append(str(TransitChar[Sys]["AvDist"]))
        else:
            DataToStore.append(0)
            DataToStore.append(0)
        DataToStore.append(str(NumberLines[Sys]))
    print("DataToStore",DataToStore)
    # b=input('.................................')
    csv_writer.writerow(DataToStore)
    data_file.close()


def GTFS(Path,RequestedData,DictType,CountType):
    CleanFiles() 
    print("Enters the Main function")
    if os.name=='nt':
        Runnzip(Path=Path)
        O_PathAgencyData=r"Operational\agency.txt"
        O_PathRoutes=r"Operational\routes.txt"
        O_PathTrips=r"Operational\trips.txt"
        O_PathStopTimes=r"Operational\stop_times.txt"
        O_PathStops=r"Operational\stops.txt"
        O_PathShapes=r"Operational\shapes.txt"
        O_PathCalendar=r"Operational\calendar.txt"
        O_PathStopsGeoJson=r"Operational\Geostops.geojson"
        O_GridStopDensity=r"Operational\Grid.geojson"
    if os.name=='posix':
        RunZipUnix(Path=Path)
        O_PathAgencyData="Operational/agency.txt"
        O_PathRoutes="Operational/routes.txt"
        O_PathTrips="Operational/trips.txt"
        O_PathStopTimes="Operational/stop_times.txt"
        O_PathStops="Operational/stops.txt"
        O_PathShapes="Operational/shapes.txt"
        O_PathStopsGeoJson="Operational/Geostops.geojson"
        O_PathCalendar="Operational/calendar.txt"

        O_GridStopDensity="Operational/Grid.geojson"
        O_GridStopDensity="Operational/Grid.geojson"
    print("Finish unpacking")

    print("Start - Step 1")
    Agency=GetSystemData(Path=O_PathAgencyData)
    CityName=[]
    AgencyFile=open(O_PathAgencyData,'r')
    HeaderLine=AgencyFile.readline()
    IndxAG=999999
    IndxNa=999999
    IndxTi=999999
    Header=HeaderLine.split(",")
    for idx, head in enumerate(Header):
        print(str(idx),str(head),end="\t") 
        if str(head)=="agency_id":
            IndxAG=idx
        if str(head)=="agency_name":
            IndxNa=idx
        if str(head)=="agency_timezone":
            IndxTi=idx
    # b=input(".................................")
    DataCityLine=AgencyFile.readline()
    DataCity=DataCityLine.split(",")
    if IndxAG!=999999 and IndxNa !=999999 and IndxTi!=999999:
        NameOfCity=str(DataCity[IndxTi])+"_"+str(DataCity[IndxAG])+"_"+str(DataCity[IndxNa])
    if IndxAG==999999 and IndxNa !=999999 and IndxTi!=999999:
        NameOfCity=str(DataCity[IndxTi])+"_"+str(DataCity[IndxNa])

    NameOfCity = NameOfCity.replace('\"',"")
    NameOfCity = NameOfCity.replace("/",".")

    print("NameOfCity1",NameOfCity)
    # NumberLines=GetLineNums(Path=O_PathRoutes)
    # print(NameOfCity)
    DataSequence,DataTrips,DataRoutes,DataStops=ReadGTFS(PathRoutes=O_PathRoutes,PathTrips=O_PathTrips,PathStopTimes=O_PathStopTimes,PathStops=O_PathStops,PathCalendar=O_PathCalendar)
    print("End - Step 1")
    # #############################################################
    print("Start - Step 2")
    GetTypesofTransport(InputDict=DataRoutes)

    ListofStops=GtfsRouteCleaning(DataSequence=DataSequence,DataTrips=DataTrips,DataRoutes=DataRoutes,DataStops=DataStops,CatalogTypes=DictType,CountType=CountType)
    print("ListofData: ",len(ListofStops))
    print("End - Step 2")
    print("Start - Step 3")
    EdgeList=[]
    for d in ListofStops:
        if len(d)>0:
            EdgeList.append(GetOrder(Data=d))
        else:
            EdgeList.append({})
    print("End - Step 3")

    print("Step 4 Start")
    FileList = os.listdir('Operational')
    PathList = []
    for File in FileList:
        PathFile= os.path.abspath('Operational/'+File)
        PathList.append(PathFile)
        # print(File,PathFile)
    GetInfoData(List=PathList,NameOfCity=NameOfCity)
    print("Step 4 End")
    # #############################################################
    ###################################################
    ###################################################
    ####### TESTING AREA    ###############################
    ###################################################
    ###################################################

    # print("ListofStops",type(ListofStops))
    # for i,x in enumerate(ListofStops[:10]):
    #     print(i,x)

    # for i,x in enumerate(EdgeList[:10]):
    #     # print(i,x)
    #     for j,y in enumerate(x):
    #         print(y,x[y])
    #         b=input('.................................')
    ListOfTrips=[]
    BackLink={}
    for i,route in enumerate(DataTrips.keys()):
        if route in ('1','2','3','4','5'):
            # print(route,type(route), type(DataTrips[route]))
            for j,y in enumerate(DataTrips[route].keys()):
                # print(j,"-",y,"-",DataTrips[route][y])
                if DataTrips[route][y]['direction_id']=='0':
                    ListOfTrips.append(y)
                    BackLink[y]=route
    # print("ListOfTrips")
    # print(ListOfTrips)
    # b=input('.................................')
    print("##################################################")
    # for i in ('1','2','3','4','5'):
    #     print("EdgeData[",i,"]={}")
    # for i in ('1','2','3','4','5'):
    # for j in ListOfTrips:
    #     print("EdgeData[",BackLink[j],"]['",j,"']={}")
        # Station Berri-UQAM        99      9999111-9999112-9999114
        # Station Snowdon           98      9999495-9999492
        # Station Jean-Talon        97      9999055-9999052
    ####### STOPER BEFORE WE GO INTO THE OPERATIONS ##########
    ##########################################################
    # print(RequestedData)
    # b=input("....STOPER BEFORE WE GO INTO THE OPERATIONS.............................")
    ##########################################################

    ListOfNeworks=[]
    # CleanFiles() 

    # Sequence to obtain the average distance between stops 
    ##########################################################
    ListOfWorkStops=[]
    if RequestedData["WorkFrequency"]:


        # def Hour2Hour(HourSTR):
        #     Hour=HourSTR[]

        TripsToWorkWith=[]


        DictExit={}

        count=0
        for stop in DataStops.keys():
            count+=1
            Skip=False
            for let in stop:
                if let not in ["1","2","3","4","5","6","7","8","9","0"]:
                    Skip=True
            if Skip:
                next
            # print(stop,DataStops[stop])
            ListOfWorkStops.append(stop)
            # if count==500
            #     break
        # b=input("Delete")

        count=0
        for trip in DataTrips.keys():
            if trip not in ['1','2','3','4','5']:
                count+=1
                if count==5:
                    break
                print(trip,type(trip))
                # print(trip,DataTrips[trip])
                # print("type(DataTrips[trip])",type(DataTrips[trip]))
                for seq in DataTrips[trip]:
                    # print("\t",seq)
                    for time in DataSequence[seq]:
                        # print("\t\t",time, DataSequence[seq][time]['stop_id'],DataSequence[seq][time]['arrival_time'])
                        ArrTime=DataSequence[seq][time]['arrival_time']
                        Stop=DataSequence[seq][time]['stop_id']
                        if Stop not in DictExit.keys():
                            DictExit[Stop]=[]
                        if [Stop,ArrTime] not in DictExit[Stop]:
                            DictExit[Stop].append([Stop,ArrTime])

        # b=input("Delete")
        for stop in DictExit.keys():
            print(stop,DictExit[stop])
            # b=input('.................................')
        # for 






        # import statistics
        # for trip in DataTrips.keys():
        #     print(trip)
        # # if True:
        #     # print(DataTrips['10'])
        #     Route=DataTrips[trip]
        #     # print('direction_id',Route[trip]['direction_id'])
        #     # print(Route[trip])
        #     if trip not in ['0','1','2','3','4','5','121E']:
        #         ListCount=[[],[]]
        #         for trip in Route.keys():
        #             # print("trip",trip,len(DataSequence[trip]))
        #             # print(trip,Route[trip])
        #             # for i in DataSequence[trip]:
        #                 # print("\t",i,DataSequence[trip][i])
        #             # print(trip,len(DataSequence[trip]))
        #             ListCount[int(Route[trip]['direction_id'])].append(len(DataSequence[trip]))
        #         M0=statistics.mode(ListCount[0])
        #         M1=statistics.mode(ListCount[1])
        #         Sample0=0
        #         Sample1=0
        #         for trip in Route.keys():
        #             if Route[trip]['direction_id']=='0' and len(DataSequence[trip])==M0 and Sample0==0:
        #                 Sample0=trip
        #             if Route[trip]['direction_id']=='1' and len(DataSequence[trip])==M1 and Sample1==0:
        #                 Sample1=trip
        #         # print("ready:")
        #         # print("Sample0:",Sample0)
        #         # print("Sample1:",Sample1)
        #         TripsToWorkWith.append(Sample0)
        #         TripsToWorkWith.append(Sample1)
        #     # print("\n","trip:",trip)
        #     # if DataTrips[trip]['route_id']=='10':
        #     #     print(trip)

        # # b=input("Delete")
        # # print(type())
        # # b=input("Delete")
        # StopTimeCatalog={}
        # # ['stop_id']
        # for trip in TripsToWorkWith:
        #     print(trip)
        #     for stop in DataSequence[trip]:
        #         print("\t",stop,DataSequence[trip][stop])
        #         if DataSequence[trip][stop]['stop_id'] in StopTimeCatalog.keys():
        #             key=DataSequence[trip][stop]['stop_id']
        #             ArrivTime=DataSequence[trip][stop]['arrival_time']
        #             DeparTime=DataSequence[trip][stop]['departure_time']
        #             StopTimeCatalog[key].append(ArrivTime)
        #             print("key:",key)
        #             print("ArrivTime:",ArrivTime)
        #             print("DeparTime:",DeparTime)
        #         else:
        #             key=DataSequence[trip][stop]['stop_id']
        #             ArrivTime=DataSequence[trip][stop]['arrival_time']
        #             DeparTime=DataSequence[trip][stop]['departure_time']
        #             print("key:",key)
        #             print("ArrivTime:",ArrivTime)
        #             print("DeparTime:",DeparTime)
        #             # b=input("Delete")
        #             StopTimeCatalog[key]=[]
        #             StopTimeCatalog[key].append(ArrivTime)
        
        # for key in StopTimeCatalog.keys():
        #     print(key)
        #     print("\t",StopTimeCatalog[key],"\n")
        # print("len",len(StopTimeCatalog))
        # print("DataStops",len(DataStops))

    if RequestedData["NewNetworkAnalysis"]:
        TimeData={}
        BackConnection={}
        BusesPerStop={}
        # CheckList=[]
        # ConnectionTripId2Route={}
        ########################################################
        # for key in DataTrips.keys():
        #     # print("Key DataTrips",key,type(DataTrips[key]))
        #     for kk in DataTrips[key].keys():
        #         # print(kk,DataTrips[key][kk])
        #         ConnectionTripId2Route[DataTrips[key][kk]['trip_id']]=DataTrips[key][kk]['route_id']
        #         CheckList.append(DataTrips[key][kk]['trip_id'])
        # for ii in CheckList[:10]:
        #     print(ii,ConnectionTripId2Route[ii])
        # b=input('.................................')

        # print("DataStops",type(DataStops))
        for Sta in DataStops.keys():
            # print("Key DataStops",key,type(key))
            if Sta in ('9999111','9999112','9999114'):
                Sta='99'
            if Sta in ('9999495','9999492'):
                Sta='98'
            if Sta in ('9999055','9999052'):
                Sta='97'
            BusesPerStop[Sta]=[]
        # b=input('.................................')
        for trip in DataTrips.keys():
            # print(trip,type(DataTrips[trip]),len(DataTrips[trip]),DataTrips[trip].keys())
            # print()
            TimeData[trip]={}
            for ixy in DataTrips[trip].keys():
                BackConnection[ixy]=trip
                TimeData[trip][ixy]={}
            # print(trip,len(TimeData[trip]))
            # print(TimeData[trip])


        print("DataTrips",len(DataTrips))
        print("ListOfTrips",len(ListOfTrips))
        print("~~~~~~~~~~~~~~~~~~~~")
        # b=input('.................................')
        for i,tripid in enumerate(DataSequence.keys()):
            # if tripid in ListOfTrips:
                LegList=list(DataSequence[tripid].keys())
                # print("LegList",LegList)
                # b=input('.................................')
                for j,leg in enumerate(DataSequence[tripid].keys()):
                    if leg ==LegList[-1]:
                        break
                    # print("#########################################")
                    # print(DataSequence[tripid][leg])
                    # print("#########################################")
                    StartTime=DataSequence[tripid][leg]['arrival_time'].split(":")
                    if len(StartTime) ==1: 
                        print(DataSequence[tripid][leg])
                        # print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"*10)
                        continue                    
                    StartTime = [int(i) for i in StartTime]
                    EnddTime=DataSequence[tripid][LegList[j+1]]['arrival_time'].split(":")
                    # print("EnddTime",EnddTime,type(EnddTime),len(EnddTime))
                    if len(EnddTime) ==1: 
                        print(DataSequence[tripid][leg])
                        # print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"*10)
                        continue
                    EnddTime = [int(i) for i in EnddTime]
                    Sta=DataSequence[tripid][leg]['stop_id']
                    if Sta in ('9999111','9999112','9999114'):
                        Sta='99'
                    if Sta in ('9999495','9999492'):
                        Sta='98'
                    if Sta in ('9999055','9999052'):
                        Sta='97'
                    BusesPerStop[Sta].append(DataSequence[tripid][leg]['departure_time'])

        ExitDict={}
        for stop in BusesPerStop.keys():
            if stop in ('9999111','9999112','9999114'):
                stop='99'
            if stop in ('9999495','9999492'):
                stop='98'
            if stop in ('9999055','9999052'):
                stop='97'
            BusCountPerHour= {hr:0 for hr in range(0,24)}
            # print("stop",stop,BusesPerStop[stop],len(BusesPerStop[stop]))
            # print("stop",stop)
            for hr in BusesPerStop[stop]:
                Hour=int(hr[0]+hr[1])
                if Hour >= 24:
                    Hour=Hour-24

                BusCountPerHour[Hour]+=1
            ExitDict[stop]=BusCountPerHour
            # print(BusCountPerHour)
            # b=input('.................................')
        print(len(BusesPerStop))          
        Path=r"/mnt/e/GitHub/CAMMM-Tool_1.3/Results/Montreal/BusPerHour.csv"
        f = open(Path, "w")
        Header="Stop,"
        for h in range(0,24):
            Header+=str(h)+","
        Header+="\n"
        f.write(Header)
        text=""
        for key in ExitDict.keys():
            Summ=0
            for h in range(0,24):
                Summ+=ExitDict[key][h]
            print(key,"SUM:",Summ,ExitDict[key])
            # b=input('.................................')
            if Summ !=0:
                text=key+","
                # print("type(ExitDict",type(ExitDict[key]))
                for k in range(0,24):
                    text+=str(ExitDict[key][k])+","
                #     text+=str(ExitDict[text][k])+","
                # text+=",".join(k+","+BusesPerStop[text][k] for k in BusesPerStop[text])
                text+="\n"
                print(text)
                f.write(text)
        # print(text)
        # b=input('.................................')
        f.close()
        # b=input('.................................')
        # for i,tripid in enumerate(DataSequence.keys()):
        #     # if tripid in ListOfTrips:
        #         LegList=list(DataSequence[tripid].keys())
        #         # print("LegList",LegList)
        #         # b=input('.................................')
        #         for j,leg in enumerate(DataSequence[tripid].keys()):
        #             if leg ==LegList[-1]:
        #                 break
        #             print("#########################################")
        #             print(DataSequence[tripid][leg])
        #             print("#########################################")
        #             StartTime=DataSequence[tripid][leg]['arrival_time'].split(":")
        #             if len(StartTime) ==1: 
        #                 print(DataSequence[tripid][leg])
        #                 print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"*10)
        #                 continue                    
        #             StartTime = [int(i) for i in StartTime]
        #             EnddTime=DataSequence[tripid][LegList[j+1]]['arrival_time'].split(":")
        #             # print("EnddTime",EnddTime,type(EnddTime),len(EnddTime))
        #             if len(EnddTime) ==1: 
        #                 print(DataSequence[tripid][leg])
        #                 print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"*10)
        #                 continue
        #             EnddTime = [int(i) for i in EnddTime]
        #             DeltaTime=TimeDelta(T1=StartTime,T2=EnddTime)
        #             Sta=DataSequence[tripid][leg]['stop_id']
        #             if Sta in ('9999111','9999112','9999114'):
        #                 Sta='99'
        #             if Sta in ('9999495','9999492'):
        #                 Sta='98'
        #             if Sta in ('9999055','9999052'):
        #                 Sta='97'
        #             End=DataSequence[tripid][LegList[j+1]]['stop_id']
        #             if End in ('9999111','9999112','9999114'):
        #                 End='99'
        #             if End in ('9999495','9999492'):
        #                 End='98'
        #             if End in ('9999055','9999052'):
        #                 End='97'
        #             # print("BackConnection[trçipid]",BackConnection[tripid])
        #             # print(TimeData[BackConnection[tripid]])
        #             # if tripid in TimeData[BackConnection[tripid]]:
        #             #     print("tripid",tripid," is in TimeData",BackConnection[tripid])
        #             #     b=input('.................................')
        #             TimeData[BackConnection[tripid]][tripid][leg]=DeltaTime

        #             print("EdgeData[",Sta,",",End,"]",end="")
        #             print("['",tripid,"']",end="")
        #             print("=",DeltaTime)
        #             print("PAY Attention here")
        #             # print(j,"   -    ",leg,">",LegList[j+1],DeltaTime,"\t",DataSequence[tripid][leg]['stop_id'] )
        #             # print("\t",leg,DataSequence[tripid][leg])
        #             b=input('.................................')



    if RequestedData["NetworkAnalysis"]:
        print("ListofStops len ",len(ListofStops))
        print("EdgeList len",len(EdgeList))
        print("Enters into the agregation mode")
    #     print(len(ListofStops))
    #     print(type(ListofStops))
        # for i in EdgeList:
        #     print(type(i),len(i))
        # b=input("####################################")
        # b=input()
        # print(EdgeList)
        # b=input()
    #     print("Start Bus network")
    #     print("LEN ListofStops:",len(ListofStops))
        Titles=["Bus Network","Rail Network","Metro Network","Light Rail Netwrok","Other Network","Node Network"]
        # for idx,a in enumerate(ListofStops):
        #     print(idx,"Type:",type(a),len(a.keys()))
        for idx,a in enumerate(ListofStops):
            print("Start of",Titles[idx],"network")
            if len(a.keys())>0:
                print(idx,"---------------------------------------------------------------------------------------------------------------------------------------------------------------")
                print("Tpye EdgeList",len(EdgeList[idx]))
                print("Tpye EdgeList",type(EdgeList[idx]))
                print("NetworkIndex=idx",idx)
                AnalyzedNetwork=GtfsToNetwork(EdgeData=EdgeList[idx],DataStops=DataStops,NetworkIndex=idx,DataRoutes=DataRoutes,DataSequence=DataSequence,DataTrips=DataTrips)
                ListOfNeworks.append(AnalyzedNetwork)
                print("Network:",Titles[idx])
                NetWorkToGeoJson(G=AnalyzedNetwork,NetworkIndex=idx)
                # print("FIN DE LA RED.......................................")
                # b=input("Press enter")
            elif len(a.keys())==0:
                print("No",idx)
            print("End of",Titles[idx],"network")
            # print("Type of AnalyzedNetwork",type(AnalyzedNetwork))
            # b=input("..DELETE...............................")
            # for node in AnalyzedNetwork:
                # print(node,node["wheelchair_boarding"],dir(node),"\n\n\n")
                # print(nx.get_node_attributes(AnalyzedNetwork, node))
                # color = nx.get_node_attributes(AnalyzedNetwork, "wheelchair_boarding")
                # print(color)
            # b=input("..DELETE...............................")
            print("")

    if RequestedData["NodeNetworkAnalysis"]:
        Nodes=CreateNodes(SuperRange=400,NodeRange=75,ListofStops=ListofStops,DataStops=DataStops)
        print("Type of ListofStops",type(ListofStops))

        # for node in Nodes:
            # print(node)
            # print(node,node["wheelchair_boarding"],dir(node),"\n\n\n")
            # print(nx.get_node_attributes(AnalyzedNetwork, node))
            # color = nx.get_node_attributes(AnalyzedNetwork, "wheelchair_boarding")
            # print(color)
            # b=input("..DELETE...............................")


        Graph=AgregatedGTFSStopsToNetwork(AgregatedNodes=Nodes,EdgeList=EdgeList)
        print(type(Graph))

        NetWorkToGeoJson(G=Graph,NetworkIndex=5)

    ##########################################################
    # Sequence to obtain the average distance between stops 
    ##########################################################

    if RequestedData["CityMetrics"]:
        Titles=["Bus Network","Rail Network","Metro Network","Light Rail Netwrok","Other Network","Node Network"]
        ConnectiorDB=DatabaseConnection()
        NumberLines=GetLineNums(Path=O_PathRoutes,CatalogTypes=DictType)

        TransitChar={}
        for idx,Sys in enumerate(ListofStops):
            if len(ListofStops[idx])>0:
                print("Sistem in the works ",Sys)
                #############################################
                # The network is translated into a Shapefile
                CollectionLines=ConstructSpatialNetworkSHP(DictStops=ListofStops[idx],DataSequence=DataSequence,DataTrips=DataTrips,DataRoutes=DataRoutes,DataStops=DataStops)
                #############################################
                # The middle point is calculated
                CollMiddlePoints=GetMiddlePoint(CollLines=CollectionLines,DataStops=DataStops)
                #############################################
                # The Average distance and Number of stops are calculated
                AvDist,NumStops=AverageDistanceBetweenStops(Data=CollMiddlePoints)
                # print(Sys,"The average distance is: ",AvDist)
                # print(Sys,"The number of stops  is: ",NumStops)
                TransitChar[idx]={"AvDist":AvDist,"NumStops":NumStops}
        print("End  CityMetrics")
        # The data is stored in 'Resluts\CityMetrics'
        print("\n"*5)
        print("Results for",NameOfCity)
        for Sys in TransitChar.keys():
            print("For ",Sys,Titles[Sys],"The average distance is: ",TransitChar[Sys]["AvDist"])
            print("For ",Sys,Titles[Sys],"The number of stops  is: ",TransitChar[Sys]["NumStops"])
        # b=input('.................................')
        StoreCityData(NameOfCity=NameOfCity,TransitChar=TransitChar,NumberLines=NumberLines,City=NameOfCity)

    if RequestedData["RotatedGridAnalysis"]:
        TransformStopsCsvToGeoJson(PathStopsCSV=O_PathStops,PathStopsGeojson=O_PathStopsGeoJson,Agency=NameOfCity)
        # print("End of first FUnction")
        # input("Delete")
        GetStopDensity(PathFileGridUTM=O_GridStopDensity,PathStops=O_PathStopsGeoJson,PathTrip=O_PathTrips,PathShape=O_PathShapes,Pathroute=O_PathRoutes,Agency=NameOfCity)
        # TransformStopsCsvToGeoJson(PathStopsCSV,PathStopsGeojson,Agency="STM")
        # GetStopDensity(PathFileGridUTM=PathFileGridUTM,PathStops=PathStopsGeojson,PathFileGridExit=PathFileGridExit,PathTrip=PathTrip,PathShape=PathShape,Pathroute=Pathroute,Agency="STM")
    
    if RequestedData["NetworkLineAgregator"]:
        # for idx,Sys in enumerate(ListofStops):
        #     if len(ListofStops[idx])>0:
        NetworkLineAgregator(DataStops=DataStops,DataTrips=DataTrips,DataRoutes=DataRoutes,DataSequence=DataSequence,CityId=NameOfCity)

    # b=input('.................................')
    # CleanFiles() 
    ###################################################################
    ##################### END OF MAIN #################################
    ###################################################################

##############
## Main cycle
##############

if __name__ == "__main__":
    # DatabaseOperations()
    # b=input()
    RequestedData={"NetworkAnalysis":True,"NodeNetworkAnalysis":False,"CityMetrics":True,"RotatedGridAnalysis":False,"NetworkLineAgregator":False,"NewNetworkAnalysis":False,"WorkFrequency":False}
    listPath=[]
  

    # listPath.append(r"/mnt/e/OneDrive - Concordia University - Canada/RA-CAMM/Software/CAMMM-Soft-Tool_V1.1/SampleData/Quebec_GTFS/gtfs.zip")


    # listPath.append(r"/mnt/e/OneDrive - Concordia University - Canada/RA-CAMM/GTFS/Berlin_GTFS/BVG_VBB_bereichsscharf.zip")

    listPath.append(r"/mnt/e/GitHub/CAMMM-Tool_1.3/DATA/Montreal/gtfs_stm.zip")
    # listPath.append(r"/mnt/f/OneDrive - Concordia University - Canada/RA-CAMM/GTFS/Montreal_GTFS/gtfs.zip")
    # listPath.append(r"/mnt/f/OneDrive - Concordia University - Canada/RA-CAMM/GTFS/Quebec_GTFS/gtfs.zip")
    # listPath.append(r"/mnt/f/OneDrive - Concordia University - Canada/RA-CAMM/GTFS/Barcelona_GTFS/gtfs.zip")
    # listPath.append(r"/mnt/f/OneDrive - Concordia University - Canada/RA-CAMM/GTFS/Budapest_GFST/gtfs.zip")
    # listPath.append(r"/mnt/f/OneDrive - Concordia University - Canada/RA-CAMM/GTFS/Vienna_GTFS/gtfs.zip")

    # listPath.append(r"/mnt/f/OneDrive - Concordia University - Canada/RA-CAMM/GTFS/Boston_GTFS/MBTA_GTFS.zip")
    # listPath.append(r"/mnt/f/OneDrive - Concordia University - Canada/RA-CAMM/GTFS/Seattle/gtfs_puget_sound_consolidated.zip")  # Seattle
    # listPath.append(r"/mnt/f/OneDrive - Concordia University - Canada/RA-CAMM/GTFS/Toronto_GTFS/Data.zip")

    # listPath.append(r"/mnt/f/OneDrive - Concordia University - Canada/RA-CAMM/GTFS/Vancouver/VancouverGTFS.zip")
    # listPath.append(r"/mnt/f/OneDrive - Concordia University - Canada/RA-CAMM/GTFS/Longueuil_GTFS/20220404.zip")
    # listPath.append(r"/mnt/f/OneDrive - Concordia University - Canada/RA-CAMM/GTFS/Laval_GTFS/GTF_STL_v2.zip")


    # listPath.append(r"/mnt/e/OneDrive - Concordia University - Canada/RA-CAMM/GTFS/Oslo_GTFS/Oslo_gtfs.zip")
    # listPath.append(r"/mnt/e/GitHub/CAMMM-Tool_1.3/Data/new_gtfs1.zip")

    # listPath.append(r"/mnt/f/OneDrive - Concordia University - Canada/RA-CAMM/GTFS/Toronto/opendata_ttc_schedules.zip")
    # listPath.append(r"/mnt/f/OneDrive - Concordia University - Canada/RA-CAMM/GTFS/Toronto/hamilton.zip")
    # listPath.append(r"/mnt/f/OneDrive - Concordia University - Canada/RA-CAMM/GTFS/Toronto/burlington.zip")
    # listPath.append(r"/mnt/f/OneDrive - Concordia University - Canada/RA-CAMM/GTFS/Toronto/York.zip")
    # listPath.append(r"/mnt/f/OneDrive - Concordia University - Canada/RA-CAMM/GTFS/Toronto/Mississauga.zip")
    # listPath.append(r"/mnt/f/OneDrive - Concordia University - Canada/RA-CAMM/GTFS/Toronto/GTFS_Durham_TXT.zip")




    # print("RequestedData",RequestedData)
    # b=input()

    ###################################################
    ####### Data for types in code GTFS  ##############
    ###################################################

    DictType={}
    DictType['BusType']=['3','700','701','702','704','705','707','800','715']
    DictType['TrainType']=['2','100','109','116']
    DictType['Metrotype']=['1','400','401','402','403','404','405']
    DictType['TramType']= ['0','900','901','902','903','906']
    DictType['OtherType']=['4','5','1000','1400','1501']

    CountType={'0':0,'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'11':0,'12':0,
    '100':0,'109':0,'116':0,
    '400':0,'401':0,'402':0,'403':0,'404':0,'405':0,
    '700':0,'701':0,'702':0,'704':0,'705':0,'707':0,'800':0,'715':0,
    '900':0,'901':0,'902':0,'903':0,'906':0,
    '1000':0,
    '1400':0,
    '1501':0}

    for Path in tqdm(listPath):
        print(Path)
        GTFS(Path,RequestedData,DictType,CountType)




    print("..........fin...............")



