import os
import csv
import pyproj
import zipfile
import math
import sqlite3
import decimal
decimal.getcontext().prec = 10


from FeatureOperations import ConvertToUTM
from FeatureOperations import Agregate

from Databases import TransportNames

from NetworkAnalisys import GtfsToNetwork
from NetworkAnalisys import AgregatedGTFSStopsToNetwork
from NetworkAnalisys import NetWorkToGeoJson

from ClassCollection import BusStop

import networkx


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
    # print("DataStops",type(DataStops))
    # print(list(DataStops.keys())[:10])

    # b=input()
    DistanceNode=75
    # print(type(DictStops))
    KeysDS=list(DictStops.keys())
    # print("Length of Keys:",KeysDS)
    # print(KeysDS[:10])
    CollectionLines={}
    for key in KeysDS:
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

        print("ListOutbound:",ListOutbound)
        print("ListInbound: ",ListInbound)
        # SameStartEnd=False
        # if ListInbound[0]==ListOutbound[0] and ListInbound[-1]==ListOutbound[-1]:
        #     SameStartEnd=True
            # CollectionLines[key].append(ListOutbound[0])
        # else: 
        #     # Comparing the ends of the Lines by distance
        #     LatAstart=float(DataStops[ListOutbound[0]]['stop_lat'])
        #     LonAstart=float(DataStops[ListOutbound[0]]['stop_lon'])
        #     XA1,YA1,Val_EPSG1A=ConvertToUTM(lat=LatAstart,lon=LonAstart)

        #     LatBstart=float(DataStops[ListInbound[0]]['stop_lat'])
        #     LonBstart=float(DataStops[ListInbound[0]]['stop_lon'])
        #     XB1,YB1,Val_EPSG1B=ConvertToUTM(lat=LatBstart,lon=LonBstart)

        #     distStart=Distance(P1=(XA1,YA1),P2=(XB1,YB1))
        #     if distStart <30:
        #         SameStartEnd=True
                # CollectionLines[key].append((ListOutbound[0],ListInbound[0]))

        # print("Status of the lines: Same start and end=",SameStartEnd)

        if len(ListOutbound)>len(ListInbound):
            # print("List Outbound (",len(ListOutbound),") is larger than List Inbound (",len(ListInbound))
            GuideListStops=ListOutbound
            ComplementListStop=ListInbound
        else:
            print("List Outbound (",len(ListOutbound),") is shorter than List Inbound",len(ListInbound))
            GuideListStops=ListInbound
            ComplementListStop=ListOutbound

        for idx,WorkStop in enumerate(GuideListStops):

            if idx < len(ComplementListStop):
                SecIdx=idx
            else:
                Num=len(ComplementListStop)-1-i
                while abs(Num)>len(ComplementListStop):
                    Num=Num+1
                SecIdx=Num


            LatA=float(DataStops[WorkStop]['stop_lat'])
            LonA=float(DataStops[WorkStop]['stop_lon'])
            XA1,YA1,Val_EPSG1A=ConvertToUTM(lat=LatA,lon=LonA)

            LatB=float(DataStops[ComplementListStop[SecIdx]]['stop_lat'])
            LonB=float(DataStops[ComplementListStop[SecIdx]]['stop_lon'])
            XB1,YB1,Val_EPSG1B=ConvertToUTM(lat=LatB,lon=LonB)

            dist=Distance(P1=(XA1,YA1),P2=(XB1,YB1))

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
                    XA1,YA1,Val_EPSG1A=ConvertToUTM(lat=LatA,lon=LonA)
                    print(MovingIndex)
                    LatB=float(DataStops[ComplementListStop[MovingIndex]]['stop_lat'])
                    LonB=float(DataStops[ComplementListStop[MovingIndex]]['stop_lon'])
                    XB1,YB1,Val_EPSG1B=ConvertToUTM(lat=LatB,lon=LonB)

                    distMobile=Distance(P1=(XA1,YA1),P2=(XB1,YB1))
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
                Dist=Distance(P1=P1,P2=P2)
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
                    P1=ConvertToUTM(lat=float(DataStops[tup[0]]['stop_lat']),lon=float(DataStops[tup[0]]['stop_lon']))
                    P2=ConvertToUTM(lat=float(DataStops[tup[1]]['stop_lat']),lon=float(DataStops[tup[1]]['stop_lon']))
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

    


def ReadGTFS(PathRoutes,PathTrips,PathStopTimes,PathStops):
    #############################################################################
    ######    READ THE STOP TIME FILE
    #############################################################################
    #############################################################################

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



def GtfsRouteCleaning(DataSequence,DataTrips,DataRoutes,DataStops):
    print("Starts #################### GtfsRouteCleaning ####################")
    # b=input()
    GeneralData_Frequencys={}
    BusRoutes={}
    TrainRoutes={}
    TramRoutes={}
    MetroRoutes={}
    OtherRoutes={}


    # for DS in DataSequence.keys():
    #     print(DS)
    #     if '4143-1111' in DS:
    #         print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAARGGGGGGGGGGGGGGGGGGGGGGGGGGGG")
    #         # b=input()
    #     if '4143-1111-1' in DS:
    #         b=input()

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
    CountType={'0':0,'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'11':0,'12':0,
    '100':0,'109':0,'116':0,
    '400':0,'401':0,'402':0,'403':0,'404':0,'405':0,
    '700':0,'701':0,'702':0,'704':0,'705':0,'707':0,'800':0,
    '900':0,'901':0,'902':0,'903':0,'906':0,
    '1000':0,
    '1400':0}

    BusType=['3','700','701','702','704','705','707','800']
    TrainType=['2','100','109','116']
    Metrotype=['1','400','401','402','403','404','405']
    TramType= ['900','901','902','903','906']
    OtherType=['1000','1400']

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
                VarDirectionId=DataTrips[VarRouteId][Tripkey]['direction_id']
                if Tripkey in DataSequence.keys():
                    for SeqKey in DataSequence[Tripkey].keys():
                        ListOfStops.append(DataSequence[Tripkey][SeqKey]['stop_id'])
                if VarDirectionId=='0':
                    ListOfStopsCero.append(ListOfStops)
                if VarDirectionId=='1':
                    ListOfStops_One.append(ListOfStops)
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
    # b=input()


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
        print("zipfil  e",zipfile)
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
                pass
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
                pass
        fw.close()


    b=input("Waiting")

def DatabaseConnection():
    print("Into the Op")
    conn = sqlite3.connect('./Databases/CityDataStorage.db')
    print("Conected")
    cursor = conn.execute("Select * From CityData")
    print("Cursorr read")

    for row in cursor:
        print(row)
    return conn

def TextSqLite(idx):
    Text=[]
    Text[0]="INSERT INTO CityData "
    Text[1]="(Id,FirstAgency,name,AreaSqKm,PopulationMillion,DensityPersonSqKm,NumBoroughs,NumTransitSystems,Type0,NumStops0,NumLines0,AvgDisStops0,Type1,NumStops1,NumLines1,AvgDisStops1,Type2,NumStops2,NumLines2,AvgDisStops2,Type3,NumStops3,NumLines3,AvgDisStops3,Type4,NumStops4,NumLines4,AvgDisStops4)"
    Text[2]=" VALUES "
    return idx


def CleanFiles():
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

def GTFS(Path,RequestedData):
    print("Enters the function")
    print("Finish unpacking")
    if os.name=='nt':
        Runnzip(Path=Path)
        O_PathAgencyData=r"Operational\agency.txt"
        O_PathRoutes=r"Operational\routes.txt"
        O_PathTrips=r"Operational\trips.txt"
        O_PathStopTimes=r"Operational\stop_times.txt"
        O_PathStops=r"Operational\stops.txt"
    if os.name=='posix':
        RunZipUnix(Path=Path)
        O_PathAgencyData="Operational/agency.txt"
        O_PathRoutes="Operational/routes.txt"
        O_PathTrips="Operational/trips.txt"
        O_PathStopTimes="Operational/stop_times.txt"
        O_PathStops="Operational/stops.txt"

    print("Start - Step 1")
    GetSystemData(Path=O_PathAgencyData)
    # b=input(".................................")

    DataSequence,DataTrips,DataRoutes,DataStops=ReadGTFS(PathRoutes=O_PathRoutes,PathTrips=O_PathTrips,PathStopTimes=O_PathStopTimes,PathStops=O_PathStops)
    print("End - Step 1")
    # #############################################################
    GetTypesofTransport(InputDict=DataRoutes)
    # GetNumberOfStops(InputDict=DataStops)
    # print(type(DataStops))
    # for key in DataStops.keys():
    #     print(key,DataStops[key])
    #     print("\n\n")
    #     for key2 in DataTrips[key]:
    #         print(DataTrips[key][key2])
    print("Start - Step 2")
    ListofStops=GtfsRouteCleaning(DataSequence=DataSequence,DataTrips=DataTrips,DataRoutes=DataRoutes,DataStops=DataStops)
    print("ListofData: ",len(ListofStops))
    print("End - Step 2")
    print("Start - Step 3")
    EdgeList=[]
    for d in ListofStops:
        if len(d)>0:
            EdgeList.append(GetOrder(Data=d))
    print("End - Step 3")
    # print("Data_Buses")
    # print("Data_Train")
    # print("Data_Metro")
    # print("Data_Tram")
    # print("Data_Other")
    print("Len of ListofStops",len(ListofStops))
    print("Len of EdgeList",len(EdgeList))
    print("ListofStops is ",type(ListofStops))
    # for DS in ListofStops:
    #     print(DS)
    #     print("########################")
    #     # print(type(DS),len(DS.keys()))
    CleanFiles()    
    NetworkNames=["Data_Buses","Data_Train","Data_Metro","Data_Tram","Data_Other"]
    print("RequestedData",RequestedData)
    print("Checking the list of stops",len(ListofStops))
    for Stops in ListofStops:
        print(type(Stops),len(Stops))
        if len(Stops)>0:
            for stop in list(Stops.keys())[:10]:
                print(stop,type(stop))
    print("Checking the list of Edges",len(EdgeList))
    for Edges in EdgeList:
        print(type(Edges),len(Edges))
    # b=input()
    ListOfNeworks=[]

    if RequestedData["BusNetworkAnalysis"]==True:
        print("Start Bus network")
        print("LEN ListofStops:",len(ListofStops))
        for idx,a in enumerate(ListofStops):
            print(idx,"Type:",type(a),len(a.keys()))
        for idx,a in enumerate(ListofStops):
            if len(a.keys())>0:
                print(idx,"---------------------------------------------------------------------------------------------------------------------------------------------------------------")
                AnalyzedNetwork=GtfsToNetwork(EdgeData=EdgeList[idx],DataStops=DataStops,NetworkIndex=idx)
                ListOfNeworks.append(AnalyzedNetwork)
                # CityStat_NumberOfStops=GtfsToNetwork(EdgeData=EdgeData,DataStops=DataStops)
                print(idx,a)
                print("FIN DE LA RED.......................................")
                # b=input()
            elif len(a.keys())==0:
                print("No",idx)
        print("End Bus network")
    for net in ListOfNeworks:
        print(type(net))
        # networkx.readwrite.nx_shp.write_shp(net,r"D:\GitHub\CAMMM-Tool_1.3\Output")
    # if RequestedData["NodeNetworkAnalysis"]==True:
    #     EdgeList,EdgeLine=GetEdgeLists(EdgeData)
    #     ListObjStops=ListGTFStoObjectBusStop(EdgeData=EdgeData,DataStops=DataStops,Data_Buses=Data_Buses)
    #     Nodes=Agregate(ListStops=ListObjStops,Range=75)
    #     G_Dict_1=AgregatedGTFSStopsToNetwork(AgregatedNodes=Nodes,Edge_List=EdgeList,Edge_Properties=EdgeLine)
    #     NetWorkToGeoJson(G=G_Dict_1['G'])
    # print("City Stattistics:")
    # print(CityStat_NumberOfStops)
    if RequestedData["NetworkToShpLines"]==True:

        ConnectiorDB=DatabaseConnection()

        TransitChar={}
        for idx,Sys in enumerate(ListofStops):
            CollectionLines=ConstructSpatialNetworkSHP(DictStops=ListofStops[0],DataSequence=DataSequence,DataTrips=DataTrips,DataRoutes=DataRoutes,DataStops=DataStops)
            CollMiddlePoints=GetMiddlePoint(CollLines=CollectionLines,DataStops=DataStops)
            AvDist,NumStops=AverageDistanceBetweenStops(Data=CollMiddlePoints)
            print("The average distance is: ",AvDist)
            print("The number of stops  is: ",NumStops)
            TransitChar[idx]={"AvDist":AvDist,"NumStops":NumStops}
        

        for Sys in TransitChar.keys():
            print("For ",Sys,"The average distance is: ",TransitChar[Sys]["AvDist"])
            print("For ",Sys,"The number of stops  is: ",TransitChar[Sys]["NumStops"])

        Insert=TextSqLite(idx=0)
        Variables=TextSqLite(idx=1)
        Values=TextSqLite(idx=2)



        # ConnectiorDB.execute()

        # print("DataSequence")
        # KeysDS=list(DataSequence.keys())
        # print(KeysDS[:10])
        # print(type(DataSequence))
        # b=input()
        # print(type(DataTrips))
        # print("DataTrips")
        # b=input()
        # print(type(DataRoutes))
        # print("DataRoutes")
        # b=input()
        # print(type(DataStops))
        # print("DataStops")




if __name__ == "__main__":
    # DatabaseOperations()
    # b=input()
    RequestedData={"BusNetworkAnalysis":False,"NodeNetworkAnalysis":False,"NetworkToShpLines":True}
    listPath=[]
    # listPath.append(r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tool_V1.1\SampleData\Berlin_GTFS\BVG_VBB_bereichsscharf.zip")
    # listPath.append(r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tool_V1.1\SampleData\Boston_GTFS\MBTA_GTFS.zip")
    # listPath.append(r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tool_V1.1\SampleData\Melbourne_GTFS\gtfs (1).zip")
    # listPath.append(r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tool_V1.1\SampleData\Oslo_GTFS\gtfs (3).zip")
    # if os.name=='nt':
    #     print('WIN10')
    #     listPath.append(r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tool_V1.1\SampleData\Quebec_GTFS\gtfs.zip")
    # if os.name=='posix':
    #     print('UNIX')
    #     listPath.append(r"/mnt/e/OneDrive - Concordia University - Canada/RA-CAMM/Software/CAMMM-Soft-Tool_V1.1/SampleData/Quebec_GTFS/gtfs.zip")
    listPath.append(r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tool_V1.1\SampleData\Montreal GTFS\gtfs.zip")
    # listPath.append(r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tool_V1.1\SampleData\Torino_GTFS\gtfs (2).zip")
    # listPath.append(r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tool_V1.1\SampleData\Toulouse_GTFS\tisseo_gtfs.zip")

    for Path in listPath:
        print(Path)
        GTFS(Path,RequestedData)




    print("..........fin...............")



