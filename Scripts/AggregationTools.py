import collections
from curses.ascii import BS 
import utm
import Calculations

from ClassCollection import Station
from ClassCollection import BusStop
from Tools import ProgressBarColor

def WheelchariEval(ListAccesibility):
    sumA=0
    if len(ListAccesibility)==1:
        if ListAccesibility[0]=='1':
            Wheelchair="Yes"
        else:
            Wheelchair="No"
    else:  
        for x in ListAccesibility:
            sumA+=int(x)
        if sumA/len(ListAccesibility)==2:
            Wheelchair="No"
        elif sumA > len(ListAccesibility):
            Wheelchair="Mixed"
        else:
            Wheelchair="Yes"
    return Wheelchair

def AgregateStops(ListBusStops,Range):
    # datetime object containing current date and time
    # dd/mm/YY H:M:S
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
                D=Calculations.CalcDistance(P1x=Bs1.CoordX, P1y=Bs1.CoordY,P2x=Bs2.CoordX, P2y=Bs2.CoordY)

                # print("D",D," Point 1:",Bs1.CoordX,Bs1.CoordY,"  - Point 2:",Bs2.CoordX,Bs2.CoordY)
                # b=input('Press Enter ...')
                ListDist.append(D)
                if D <= Range:
                    Bs1.Cluster.append(Bs2)
                KeyListDist[(D,Bs1.Id)]=Bs2.Id
                # print(Bs1.Id,Bs2.Id,D)
        # print("Bs1:",Bs1.Id,KeyListDist[(min(ListDist),Bs1.Id)],"-",min(ListDist))
            # ListDist[(Bs1.Id,Bs2)]
        EvaluatedBusStops.append(Bs1)
            # print(D)


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
            ListX=[]
            ListY=[]
            print("checking the methods . . . . .")
            print("Bs1:",dir(Bs1))
            ListAccesibility=[Bs1.Wheelchair]
            print(Bs1.Cluster)
            for BsC in Bs1.Cluster:
                Listb.append(BsC)
                StopCode.append(BsC.Id)
                SumCX=SumCX+BsC.CoordX
                ListX.append(BsC.CoordX)
                ListY.append(BsC.CoordY)
                SumCY=SumCY+BsC.CoordY
                SumRoutes=SumRoutes+len(BsC.Routes)
                RouteCol=RouteCol+BsC.Routes
                ListAccesibility.append(BsC.Wheelchair)
                print("..",BsC.Id,"..", end="\t")
            ACoordXutm=(Bs1.CoordX+SumCX)/(len(Bs1.Cluster)+1)
            ACoordYutm=(Bs1.CoordY+SumCY)/(len(Bs1.Cluster)+1)
            # print("ListX",ListX)
            # print("ListY",ListY)
            # BCoordX=sum(ListX)/len(ListX)
            # BCoordY=sum(ListY)/len(ListX)
            Aroutes=SumRoutes+len(Bs1.Routes)
            # print("X1:",ACoordX,"\tY2:",ACoordY,"             # Routes",Aroutes)
            # print("X2:",)
            Letter=Bs1.Epsg[-1]
            Num=int(str(Bs1.Epsg[-3])+str(Bs1.Epsg[-2]))
            # print("Bs1.Epsg[-2]",Bs1.Epsg[-2],type(Bs1.Epsg[-2]))
            # print("Bs1.Epsg[-3]",Bs1.Epsg[-3],type(Bs1.Epsg[-3]))
            # print("Num",Num,type(Num))
            Coords=utm.to_latlon(ACoordXutm, ACoordYutm, Num, Letter )
            Wheelchair=WheelchariEval(ListAccesibility=ListAccesibility)

            ExitValues.append([Coords[0],Coords[1],Aroutes,RouteCol,StopCode,"N",Wheelchair])  

            # RouteCol=[]
            print()
            # print("===========================================")
            # b=input()
            # f.write(Var)
    # f.close()
    # for Node in ExitValues:
    #     print(Node)
    return ExitValues

def AgregateHeavyTransit(ListBusStops,Range):
    # b=input("AgregateHeavyTransit")
    for i,Bs1 in enumerate(ListBusStops):
        ProgressBarColor(current=i+1,total=len(ListBusStops))
        ListDist=[]
        KeyListDist={}
        for Bs2 in ListBusStops:
            if Bs1 == Bs2:
                continue
            # elif Bs2 in EvaluatedBusStops:
            #     continue
            else:
                D=Calculations.CalcDistance(P1x=Bs1.CoordX, P1y=Bs1.CoordY,P2x=Bs2.CoordX, P2y=Bs2.CoordY)
                ListDist.append(D)
                if D <= Range:
                    Bs1.Cluster.append(Bs2)
                KeyListDist[(D,Bs1.Id)]=Bs2.Id
    Listb=[]
    ExitValues=[]

    for i,Bs1 in enumerate(ListBusStops):
        ProgressBarColor(current=i+1,total=len(ListBusStops))
        if Bs1 in Listb:
            pass
            # print("next")
        else:
            # print("Id",Bs1.Id,"Len",len(Bs1.Cluster),"X:",Bs1.CoordX,"\tY:",Bs1.CoordY,"Routes",Bs1.Routes)
            # print("Appends", end= " ")
            # print("EPSG:",Bs1.Epsg)
            # b=input("Press enter")
            SumCX=0
            SumCY=0
            SumRoutes=0
            StopCode=[Bs1.Id]
            RouteCol=Bs1.Routes
            ListX=[]
            ListY=[]
            ListAccesibility=[Bs1.WheelChair]
            # print(Bs1.Cluster)
            for BsC in Bs1.Cluster:
                Listb.append(BsC)
                StopCode.append(BsC.Id)
                SumCX=SumCX+BsC.CoordX
                ListX.append(BsC.CoordX)
                ListY.append(BsC.CoordY)
                SumCY=SumCY+BsC.CoordY
                SumRoutes=SumRoutes+len(BsC.Routes)
                RouteCol=RouteCol+BsC.Routes
                ListAccesibility.append(BsC.WheelChair)
                # print("Wheelchair in ",BsC.Id, "  -   WC:",BsC.WheelChair)

            ACoordXutm=(Bs1.CoordX+SumCX)/(len(Bs1.Cluster)+1)
            ACoordYutm=(Bs1.CoordY+SumCY)/(len(Bs1.Cluster)+1)
            # print("ListX",ListX)
            # print("ListY",ListY)
            # BCoordX=sum(ListX)/len(ListX)
            # BCoordY=sum(ListY)/len(ListX)
            Aroutes=SumRoutes+len(Bs1.Routes)
            # print("X1:",ACoordX,"\tY2:",ACoordY,"             # Routes",Aroutes)
            # print("X2:",)
            Letter=Bs1.Epsg[-1]
            Num=int(str(Bs1.Epsg[-3])+str(Bs1.Epsg[-2]))
            # print("Bs1.Epsg[-2]",Bs1.Epsg[-2],type(Bs1.Epsg[-2]))
            # print("Bs1.Epsg[-3]",Bs1.Epsg[-3],type(Bs1.Epsg[-3]))
            # print("Num",Num,type(Num))
            Coords=utm.to_latlon(ACoordXutm, ACoordYutm, Num, Letter )
            # Wheelchair procesing
            # print("ListAccesibility:",ListAccesibility)

            Wheelchair=WheelchariEval(ListAccesibility=ListAccesibility)
            # print("len:",len(ListAccesibility),"SumA",sumA)
            # print("WheelChair",WheelChair)
            # b=input("Press enter--------------------------------")
            # print(Coords)
            # b=input('Press Enter ...')
            # Var=str(ACoordX)+","+str(ACoordY)+","+str(Aroutes)+","+str(RouteCol)+"\n"
            ExitValues.append([Coords[0],Coords[1],Aroutes,RouteCol,StopCode,"S",Wheelchair])

    return ExitValues

def GetEPSG(letter,zone):
    North=["N","O","P","Q","R","S","T","U","V"]
    South=["M","L","K","J","H","G","F","E"]
    if letter in North:
        return "326"+str(zone)+letter
    if letter in South:
        return "325"+str(zone)+letter

def ConvertStations(ListDicts,Route,DataStops,Systems,SuperNode):

    class Station:
        def __init__(self,Id="",CoordX=0,CoordY=0,Epsg="",Routes=[],Cluster=[],System=[],SuperNode=0,WheelChair=0):
            self.Id=Id
            self.CoordX=CoordX
            self.CoordY=CoordY
            self.Epsg=""
            self.Routes=[]
            self.Cluster=[]
            self.System=[]
            self.SuperNode=SuperNode
            self.WheelChair=WheelChair

    ListStation=[]
    for idx,Stations in enumerate(ListDicts):
        ProgressBarColor(current=idx+1,total=len(ListDicts))
        for Estacion in Stations:
            # print("Estacion",Estacion)
            # print("DataStops[Estacion]",DataStops[Estacion])

            Lat=DataStops[Estacion]['stop_lat']
            Lon=DataStops[Estacion]['stop_lon']
            # print(Lat,Lon)
            UTM=utm.from_latlon(float(Lat),float(Lon))
            Sta=Station() #(Id=Estacion,CoordX=float(UTM[0]),CoordY=float(UTM[1]))
            Sta.Id=Estacion
            Sta.Epsg=GetEPSG(letter=UTM[3],zone=UTM[2])
            Sta.CoordX=float(UTM[0])
            Sta.CoordY=float(UTM[1])
            # print(UTM)
            # print(Sta.Epsg)
            Sta.Routes=[Route]
            # Sta.Cluster=[]
            Sta.System=[Systems[idx]]
            Sta.SuperNode=SuperNode
            Sta.WheelChair=DataStops[Estacion]['wheelchair_boarding']
            ListStation.append(Sta)
            ListStation[idx]=Sta
    #         print(Sta.Id,Sta.CoordX,Sta.CoordY)
            # print("Sta",Sta)
            # print("wheelchair_boarding",Sta.WheelChair)
            # b=input("Press enter")
    #         for st in ListStation:
    #             print("+",st.Id,st.CoordX)
    #         print(".")
    # for st in ListStation:
    #     print("-",st.Id,st.CoordX)
    return ListStation

def ConvertToStopObj(List,Route,DataStops):
    OutList=[]
    for stop in List:
        Lat=DataStops[stop]['stop_lat']
        Lon=DataStops[stop]['stop_lon']
        # print(Lat,Lon)
        UTM=utm.from_latlon(float(Lat),float(Lon))
        BStop=BusStop()
        BStop.Id=stop
        BStop.CoordX=float(UTM[0])
        BStop.CoordY=float(UTM[1])
        BStop.Routes=[Route]
        BStop.Epsg=GetEPSG(letter=UTM[3],zone=UTM[2])
        BStop.LocationType=DataStops[stop]['location_type']
        BStop.ParentStation=DataStops[stop]['parent_station']
        BStop.Wheelchair=DataStops[stop]['wheelchair_boarding']

        # print(stop,Route,DataStops[stop]['stop_lat'],DataStops[stop]['stop_lon'])
        # print(BStop.Id,BStop.Routes,BStop.CoordX,BStop.CoordY)
        OutList.append(BStop)
    return OutList

def AddStopsSuperNode(SuperNodeList,ListStops,Range):
    AssocStops={}
    LinkStopSN={}
    RoutesStops={}
    IsolatedStops=[]
    for stop in ListStops:
        RoutesStops[stop.Id]=stop.Routes
    for idx, node in enumerate(SuperNodeList):
        Coords=utm.from_latlon(node[0],node[1])
        
        Xnode=float(Coords[0])
        Ynode=float(Coords[1])
        # print("-",node)
        for stop in ListStops:
            # print(stop)
            Xstop=stop.CoordX
            Ystop=stop.CoordY
            D=Calculations.CalcDistance(P1x=Xnode, P1y=Ynode,P2x=Xstop, P2y=Ystop)
            if D < Range:
                # print(stop.Id)
                if idx not in AssocStops.keys():
                    AssocStops[idx]=[]
                AssocStops[idx].append([stop.Id,D])

                if stop.Id not in LinkStopSN.keys():
                    LinkStopSN[stop.Id]=[idx,D]
                else:
                    if LinkStopSN[stop.Id][1]<D:
                        LinkStopSN[stop.Id][1]=D
    for key in LinkStopSN.keys():
        SuperNodeList[LinkStopSN[key][0]][3].append(RoutesStops[key][0])
        SuperNodeList[LinkStopSN[key][0]][4].append(key)
        print()
        print(key,LinkStopSN[key],"SuperNode",SuperNodeList[LinkStopSN[key][0]])
    for stop in ListStops:
        if  stop.Id not in LinkStopSN.keys():
            IsolatedStops.append(stop)

    return SuperNodeList,IsolatedStops

def CreateNodes(SuperRange,NodeRange,ListofStops,DataStops):

    NetworkNames=["Data_Buses","Data_Train","Data_Metro","Data_Tram","Data_Other"]
    for idx,sys in enumerate(ListofStops):
        print("---",NetworkNames[idx],idx,len(sys),type(sys))
        for key in list(sys.keys())[:20]:
            print(key,sys[key])
            print("\n"*3)
    # NetworkNames=["Data_Buses","Data_Train","Data_Metro","Data_Tram","Data_Other"]
    # Data_Buses
    if len(ListofStops[0])>0:
        BusesStops=ListofStops[0]
        BusesCond=True
    else:
        BusesCond=False
    # Data_Train                
    if len(ListofStops[1])>0:
        TrainStops=ListofStops[1]
        TrainCond=True
    else:
        TrainCond=False
    # Data_Metro
    if len(ListofStops[2])>0:
        MetroStops=ListofStops[2]
        MetroCond=True

    else:
        MetroCond=False
    # Data_Tram
    if len(ListofStops[3])>0:
        LightStops=ListofStops[3]
        LightCond=True
    else:
        LightCond=False
    # Data_Tram        
    if len(ListofStops[4])>0:
        OtherStops=ListofStops[4]
        OtherCond=True
    else:
        OtherCond=False

    ListSations=[]
    ManStper=True
    if TrainCond and MetroCond and ManStper:
        # SuNode=SuperNodeTrainMetro(TrainStops=TrainStops,MetroStops=MetroStops,DataStops=DataStops)
        # for key in SuNode.keys():
        #     print(key,DataStops[key]['stop_lat'],DataStops[key]['stop_lon'])
        # print("Length:",len(SuNode))

        for MetroRoute in TrainStops.keys():
            Innbound=TrainStops[MetroRoute]['0']
            Outbound=TrainStops[MetroRoute]['1']
            Outbound.reverse()
            # print( Innbound)
            # print( Outbound)
            # print("··························",DataStops[Outbound[0]])
            if Innbound == Outbound:
                # print("They match")
                LiSta=ConvertStations(ListDicts=[Innbound],Route=MetroRoute,DataStops=DataStops,Systems=["1"],SuperNode=1)
                ListSations=ListSations+LiSta
            else:
                LiSta=ConvertStations(ListDicts=[Innbound,Outbound],Route=MetroRoute,DataStops=DataStops,Systems=["1","1"],SuperNode=1)
                ListSations=ListSations+LiSta

        for MetroRoute in MetroStops.keys():
            Innbound=MetroStops[MetroRoute]['0']
            Outbound=MetroStops[MetroRoute]['1']
            Outbound.reverse()
            # print( Innbound)
            # print( Outbound)
            # print("··························",DataStops[Outbound[0]])
            if Innbound == Outbound:
                # print("They match")
                LiSta=ConvertStations(ListDicts=[Innbound],Route=MetroRoute,DataStops=DataStops,Systems=["2"],SuperNode=1)
                ListSations=ListSations+LiSta
            else:
                LiSta=ConvertStations(ListDicts=[Innbound,Outbound],Route=MetroRoute,DataStops=DataStops,Systems=["2","2"],SuperNode=1)
                ListSations=ListSations+LiSta
    elif MetroCond and ManStper:
        # SuNode=SuperNodeMetro(MetroStops=MetroStops,DataStops=DataStops)
        # print("SuNode",SuNode)
        # for key in SuNode.keys():
        #     print(key,DataStops[key])
        # print("Length:",len(SuNode))
        for MetroRoute in MetroStops.keys():
            Innbound=MetroStops[MetroRoute]['0']
            Outbound=MetroStops[MetroRoute]['1']
            Outbound.reverse()
            # print( Innbound)
            # print( Outbound)
            # print("··························",DataStops[Outbound[0]])
            if Innbound == Outbound:
                # print("They match")
                LiSta=ConvertStations(ListDicts=[Innbound],Route=MetroRoute,DataStops=DataStops,Systems=["2"],SuperNode=1)

            else:
                LiSta=ConvertStations(ListDicts=[Innbound,Outbound],Route=MetroRoute,DataStops=DataStops,Systems=["2","2"],SuperNode=1)
            ListSations=ListSations+LiSta
    # print("................................",ListSations)
    # for st in ListSations:
    #     print(st.Id,st.CoordX,st.CoordY,st.System)
    SuperNodeList=AgregateHeavyTransit(ListBusStops=ListSations,Range=100)
    # print("Super NODES")
    # for Sn in SuperNodeList:
    #     print(Sn)
    # b=input("CHECK THE NODES!!!!!!!!")

    ListStops=[]
    if LightCond:
        # print(type(LightStops))
        for key in LightStops.keys():
            # print(key)
            # print(LightStops[key]['0'])
            # print(LightStops[key]['1'])
            Innbound=LightStops[key]['0']
            Outbound=LightStops[key]['1']
            Outbound.reverse()
            if Innbound == Outbound:
                # print("Innbound == Outbound")
                ListStops=ListStops+ConvertToStopObj(List=Innbound,Route=key,DataStops=DataStops)
            else:
                # print("NOT")
                ListStops=ListStops+ConvertToStopObj(List=Innbound,Route=key,DataStops=DataStops)
                ListStops=ListStops+ConvertToStopObj(List=Outbound,Route=key,DataStops=DataStops)
    # for Sn in ListStops:
    #     print(Sn.Id,Sn.Routes,Sn.CoordX,Sn.CoordY)
    if BusesCond:
        # print(type(BusesStops))
        for key in BusesStops.keys():
            # print(key)
            # print(BusesStops[key]['0'])
            # print(BusesStops[key]['1'])
            Innbound=BusesStops[key]['0']
            Outbound=BusesStops[key]['1']
            Outbound.reverse()
            if Innbound == Outbound:
                # print("Innbound == Outbound")
                ListStops=ListStops+ConvertToStopObj(List=Innbound,Route=key,DataStops=DataStops)
            else:
                # print("NOT")
                ListStops=ListStops+ConvertToStopObj(List=Innbound,Route=key,DataStops=DataStops)
                ListStops=ListStops+ConvertToStopObj(List=Outbound,Route=key,DataStops=DataStops)

    CompleteSuperNodeList,IsolatedStops=AddStopsSuperNode(SuperNodeList=SuperNodeList,ListStops=ListStops,Range=SuperRange)
    # Check point
    # for i in CompleteSuperNodeList[:10]:
    #     print(i,dir(i),type(i))
    #     for j in i:
    #         print("\t",j,"\n",dir(j),type(j))
    #     print("\n"*10)
    # b=input("CHECK THE NODES!!!!!!!!")
  
    CompleteSuperNodeList+=AgregateStops(ListBusStops=IsolatedStops,Range=NodeRange)
    # print("Begining of the last check\n"*20)
    # for i in CompleteSuperNodeList:
    #     print(i[5])
    # b=input("CHECK THE NODES!!!!!!!!")

    return CompleteSuperNodeList
    # print(len(CompleteSuperNodeList))