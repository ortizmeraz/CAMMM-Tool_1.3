import os
import csv
import pyproj
import zipfile

from FeatureOperations import ConvertToUTM
from FeatureOperations import Agregate

from Databases import TransportNames

from NetworkAnalisys import GtfsToNetwork
from NetworkAnalisys import AgregatedGTFSStopsToNetwork
from NetworkAnalisys import NetWorkToGeoJson

from ClassCollection import BusStop



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
    print("lat",lat,"lon",lon)
    print("x",x,"y",y)
    # b=input('Press Enter ...')

    return x,y,Val_EPSG

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
    Runnzip(Path=Path)
    print("Finish unpacking")
    O_PathAgencyData=r"Operational\agency.txt"
    O_PathRoutes=r"Operational\routes.txt"
    O_PathTrips=r"Operational\trips.txt"
    O_PathStopTimes=r"Operational\stop_times.txt"
    O_PathStops=r"Operational\stops.txt"

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
        EdgeList.append(GetOrder(Data=d))
    print("End - Step 3")
    # print("Data_Buses")
    # print("Data_Train")
    # print("Data_Metro")
    # print("Data_Tram")
    # print("Data_Other")
    print("Len of ListofStops",len(ListofStops))
    print("Len of EdgeList",len(EdgeList))
    # for DS in ListofStops:
    #     print(type(DS),len(DS.keys()))
    if len(ListofStops)!=len(EdgeList):
        print("#"*30,"\n")
        print("Error")
    ["Data_Buses","Data_Train","Data_Metro","Data_Tram","Data_Other"]
    print("RequestedData",RequestedData)
    # b=input()
    if RequestedData["BusNetworkAnalysis"]==True:
        print("Start Bus network")
        for idx,a in enumerate(ListofStops):
            print(idx,a)
            CityStat_NumberOfStops=GtfsToNetwork(EdgeData=EdgeList[idx],DataStops=DataStops)
            # CityStat_NumberOfStops=GtfsToNetwork(EdgeData=EdgeData,DataStops=DataStops)
            print(idx,a)
            print("FIN DE LA RED.......................................")
            # b=input()
        print("End Bus network")

    # if RequestedData["NodeNetworkAnalysis"]==True:
    #     EdgeList,EdgeLine=GetEdgeLists(EdgeData)
    #     ListObjStops=ListGTFStoObjectBusStop(EdgeData=EdgeData,DataStops=DataStops,Data_Buses=Data_Buses)
    #     Nodes=Agregate(ListStops=ListObjStops,Range=75)
    #     G_Dict_1=AgregatedGTFSStopsToNetwork(AgregatedNodes=Nodes,Edge_List=EdgeList,Edge_Properties=EdgeLine)
    #     NetWorkToGeoJson(G=G_Dict_1['G'])
    # print("City Stattistics:")
    # print(CityStat_NumberOfStops)
    CleanFiles()    




if __name__ == "__main__":
    RequestedData={"BusNetworkAnalysis":True,"NodeNetworkAnalysis":True}
    listPath=[]
    # listPath.append(r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tool_V1.1\SampleData\Berlin_GTFS\BVG_VBB_bereichsscharf.zip")
    # listPath.append(r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tool_V1.1\SampleData\Boston_GTFS\MBTA_GTFS.zip")
    # listPath.append(r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tool_V1.1\SampleData\Melbourne_GTFS\gtfs (1).zip")
    # listPath.append(r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tool_V1.1\SampleData\Oslo_GTFS\gtfs (3).zip")
    # listPath.append(r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tool_V1.1\SampleData\Quebec_GTFS\gtfs.zip")
    listPath.append(r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tool_V1.1\SampleData\Montreal GTFS\gtfs.zip")
    # listPath.append(r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tool_V1.1\SampleData\Torino_GTFS\gtfs (2).zip")
    # listPath.append(r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tool_V1.1\SampleData\Toulouse_GTFS\tisseo_gtfs.zip")

    for Path in listPath:
        print(Path)
        GTFS(Path,RequestedData)




    print("..........fin...............")



