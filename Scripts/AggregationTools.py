import collections 
import utm
import Calculations

from ClassCollection import Station


def ListStation(ListBusStops,Range):
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
            ListX=[]
            ListY=[]
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
                print("..",BsC.Id,"..", end="\t")
            
            ACoordX=(Bs1.CoordX+SumCX)/(len(Bs1.Cluster)+1)
            ACoordY=(Bs1.CoordY+SumCY)/(len(Bs1.Cluster)+1)
            print("ListX",ListX)
            print("ListY",ListY)
            BCoordX=sum(ListX)/len(ListX)
            BCoordY=sum(ListY)/len(ListX)
            Aroutes=SumRoutes+len(Bs1.Routes)
            print("X1:",ACoordX,"\tY2:",ACoordY,"             # Routes",Aroutes)
            print("X2:",)

            # b=input('Press Enter ...')
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


def AgregateTransit(ListBusStops,Range):
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
                ListDist.append(D)
                if D <= Range:
                    Bs1.Cluster.append(Bs2)
                KeyListDist[(D,Bs1.Id)]=Bs2.Id
    Listb=[]
    ExitValues=[]

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
                # print("..",BsC.Id,"..", end="\t")
            
            ACoordX=(Bs1.CoordX+SumCX)/(len(Bs1.Cluster)+1)
            ACoordY=(Bs1.CoordY+SumCY)/(len(Bs1.Cluster)+1)
            # print("ListX",ListX)
            # print("ListY",ListY)
            # BCoordX=sum(ListX)/len(ListX)
            # BCoordY=sum(ListY)/len(ListX)
            Aroutes=SumRoutes+len(Bs1.Routes)
            # print("X1:",ACoordX,"\tY2:",ACoordY,"             # Routes",Aroutes)
            # print("X2:",)

            # b=input('Press Enter ...')
            # Var=str(ACoordX)+","+str(ACoordY)+","+str(Aroutes)+","+str(RouteCol)+"\n"
            ExitValues.append([ACoordX,ACoordY,Aroutes,RouteCol,StopCode])

    return ExitValues



def SuperNodeTrainMetro(TrainStops,MetroStops,DataStops):
    print("Creating Super Node for Metro and Train")
    SuperNodes={}

    TotalDict={}
    for i in TrainStops:
        TotalDict[i]=TrainStops[i]
    for i in MetroStops:
        TotalDict[i]=MetroStops[i]

    print("Length Total Heavy rail",len(TotalDict))
    print("Length Train ",len(TrainStops) )
    print("Length Metro ",len(MetroStops) )

    for route in TotalDict.keys():
        print("route",route)
        print(route,TotalDict[route])
        if collections.Counter(set(TotalDict[route]['0'])) == collections.Counter(set(TotalDict[route]['1'])):
            print("They same!!")
            for station in TotalDict[route]['0']:
                if station not in SuperNodes.keys():
                    SuperNodes[station]={'id_stop':station,'route':route,'lat':DataStops[station]['stop_lat'],'lon':DataStops[station]['stop_lon']}

            DoubleNode=[]
            for node1 in SuperNodes.keys():
                print("node",node1,utm.from_latlon(float(SuperNodes[node1]['lat']),float(SuperNodes[node1]['lon'])))
                D1=utm.from_latlon(float(SuperNodes[node1]['lat']),float(SuperNodes[node1]['lon']))
                for node2 in SuperNodes.keys():
                    D2=utm.from_latlon(float(SuperNodes[node2]['lat']),float(SuperNodes[node2]['lon']))
                    P1x=D1[0]
                    P1y=D1[1]
                    P2x=D2[0]
                    P2y=D2[1]
                    if node2 != node1 :
                        if node1 not in DoubleNode:
                            Dist = Calculations.CalcDistance(P1x,P1y,P2x,P2y)
                            if Dist <100:
                                DoubleNode.append(node2)
                                print("······································· a small stuff  node 1",node1, " node 2 ",node2 )
            print("DoubleNode,",DoubleNode)
            for delnode in DoubleNode:
                SuperNodes.pop(delnode)
            return SuperNodes


        else:
            print("##########################################################")
            # for heading in TotalDict[route]:
            #     print("heading",heading)
            #     for station in TotalDict[route][heading]:
            #         print(station,DataStops[station]['stop_lat'],DataStops[station]['stop_lon'])
            # print("\n"*3)
            for route in TotalDict.keys():
                for heading in TotalDict[route]:
                    for station in TotalDict[route][heading]:
                        SuperNodes[station]={'id_stop':station,'route':route,'lat':DataStops[station]['stop_lat'],'lon':DataStops[station]['stop_lon']}
                # TotalDict[route]['0']
                # TotalDict[route]['1']

            DoubleNode=[]
            for node1 in SuperNodes.keys():
                # print("node",node1,utm.from_latlon(float(SuperNodes[node1]['lat']),float(SuperNodes[node1]['lon'])))
                D1=utm.from_latlon(float(SuperNodes[node1]['lat']),float(SuperNodes[node1]['lon']))
                for node2 in SuperNodes.keys():
                    D2=utm.from_latlon(float(SuperNodes[node2]['lat']),float(SuperNodes[node2]['lon']))
                    P1x=D1[0]
                    P1y=D1[1]
                    P2x=D2[0]
                    P2y=D2[1]
                    if node2 != node1 :
                        if node1 not in DoubleNode:
                            Dist = Calculations.CalcDistance(P1x,P1y,P2x,P2y)
                            if Dist <100:
                                DoubleNode.append(node2)
                                print("······································· a small stuff  node 1",node1, " node 2 ",node2 )

            print("DoubleNode,",DoubleNode)
            for delnode in DoubleNode:
                SuperNodes.pop(delnode)
        return SuperNodes







def SuperNode(MetroStops,DataStops):
    print("Creating Super Node for Metro Only")
    SuperNodeId=0
    SuperNodes={}
    print(MetroStops)
    for route in MetroStops.keys():
        print("route",route)
        print(route,MetroStops[route])
        if collections.Counter(set(MetroStops[route]['0'])) == collections.Counter(set(MetroStops[route]['1'])):
            print("They same!!")
            for station in MetroStops[route]['0']:
                if station not in SuperNodes.keys():
                    SuperNodes[station]={'id_stop':station,'lat':DataStops[station]['stop_lat'],'lon':DataStops[station]['stop_lon']}
        else:
            print("##########################################################")
            for heading in MetroStops[route]:
                print("heading",heading)
                for station in MetroStops[route][heading]:
                    print(station,DataStops[station]['stop_lat'],DataStops[station]['stop_lon'])
            print("\n"*3)
        # for key in route.keys():
    DoubleNode=[]
    for node1 in SuperNodes.keys():
        print("node",node1,utm.from_latlon(float(SuperNodes[node1]['lat']),float(SuperNodes[node1]['lon'])))
        D1=utm.from_latlon(float(SuperNodes[node1]['lat']),float(SuperNodes[node1]['lon']))
        for node2 in SuperNodes.keys():
            D2=utm.from_latlon(float(SuperNodes[node2]['lat']),float(SuperNodes[node2]['lon']))
            P1x=D1[0]
            P1y=D1[1]
            P2x=D2[0]
            P2y=D2[1]
            if node2 != node1 :
                if node1 not in DoubleNode:
                    Dist = Calculations.CalcDistance(P1x,P1y,P2x,P2y)
                    if Dist <100:
                        DoubleNode.append(node2)
                        # print("······································· a small stuff  node 1",node1, " node 2 ",node2 )
    for delnode in DoubleNode:
        SuperNodes.pop(delnode)
    # print("DoubleNode,",DoubleNode)
    return SuperNodes

def AddBusTram(SuperNode,LigthTravel,SuperRange,NodeRange):

    pass

def GetEPSG(letter,zone):
    North=["N","O","P","Q","R","S","T","U","V"]
    South=["M","L","K","J","H","G","F","E"]
    if letter in North:
        return "326"+str(zone)
    if letter in South:
        return "325"+str(zone)

def ConvertStations(ListDicts,DataStops,Systems):

    class Station:
        def __init__(self,Id="",CoordX=0,CoordY=0,Epsg="",Routes=[],Cluster=[],System=[]):
            self.Id=Id
            self.CoordX=CoordX
            self.CoordY=CoordY
            self.Epsg=""
            self.Routes=[]
            self.Cluster=[]
            self.System=[]


    ListStation=[]
    for idx,Stations in enumerate(ListDicts):
        for Estacion in Stations:
            # print(Estacion)
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
            # Sta.Routes=[]
            # Sta.Cluster=[]
            Sta.System=[Systems[idx]]
            ListStation.append(Sta)
            ListStation[idx]=Sta
    #         print(Sta.Id,Sta.CoordX,Sta.CoordY)
    #         print("Sta",Sta)
    #         for st in ListStation:
    #             print("+",st.Id,st.CoordX)
    #         print(".")
    # for st in ListStation:
    #     print("-",st.Id,st.CoordX)
    return ListStation

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
    if TrainCond and MetroCond:
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
                LiSta=ConvertStations(ListDicts=[Innbound],DataStops=DataStops,Systems=["1"])
                ListSations=ListSations+LiSta
            else:
                LiSta=ConvertStations(ListDicts=[Innbound,Outbound],DataStops=DataStops,Systems=["1","1"])
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
                LiSta=ConvertStations(ListDicts=[Innbound],DataStops=DataStops,Systems=["2"])
                ListSations=ListSations+LiSta
            else:
                LiSta=ConvertStations(ListDicts=[Innbound,Outbound],DataStops=DataStops,Systems=["2","2"])
                ListSations=ListSations+LiSta
    elif MetroCond:
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
                LiSta=ConvertStations(ListDicts=[Innbound],DataStops=DataStops,Systems=["2"])

            else:
                LiSta=ConvertStations(ListDicts=[Innbound,Outbound],DataStops=DataStops,Systems=["2","2"])
            ListSations=ListSations+LiSta
    # print("................................",ListSations)
    # for st in ListSations:
    #     print(st.Id,st.CoordX,st.CoordY,st.System)
    SuperNodeList=AgregateTransit(ListBusStops=ListSations,Range=100)
    print("Super NODES")
    for Sn in SuperNodeList:
        print(Sn)

