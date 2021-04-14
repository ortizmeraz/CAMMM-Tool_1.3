import statistics


from ClassCollection import BusStop
from FeatureOperations import Distance

def Iniciar():
    ListStops=[]
    for i in range(0,25):
        obj=BusStop()
        ListStops.append(obj)


    ListStops[0].Id=1
    ListStops[0].CoordX=611307
    ListStops[0].CoordY=5044873

    ListStops[1].Id=2
    ListStops[1].CoordX=611303
    ListStops[1].CoordY=5044879

    ListStops[2].Id=3
    ListStops[2].CoordX=611299
    ListStops[2].CoordY=5044873

    ListStops[3].Id=4
    ListStops[3].CoordX=611310
    ListStops[3].CoordY=5044877

    ListStops[4].Id=5
    ListStops[4].CoordX=611295
    ListStops[4].CoordY=5044843

    ListStops[5].Id=6
    ListStops[5].CoordX=611271
    ListStops[5].CoordY=5044896

    ListStops[6].Id=7
    ListStops[6].CoordX=611531
    ListStops[6].CoordY=5044791

    ListStops[7].Id=8
    ListStops[7].CoordX=611523
    ListStops[7].CoordY=5044774

    ListStops[8].Id=9
    ListStops[8].CoordX=611536
    ListStops[8].CoordY=5044774

    ListStops[9].Id=10
    ListStops[9].CoordX=611538
    ListStops[9].CoordY=5044784

    ListStops[10].Id=11
    ListStops[10].CoordX=611495
    ListStops[10].CoordY=5044791

    ListStops[11].Id=12
    ListStops[11].CoordX=611571
    ListStops[11].CoordY=5044767

    ListStops[12].Id=13
    ListStops[12].CoordX=611418
    ListStops[12].CoordY=5044617

    ListStops[13].Id=14
    ListStops[13].CoordX=611430
    ListStops[13].CoordY=5044648

    ListStops[14].Id=15
    ListStops[14].CoordX=611417
    ListStops[14].CoordY=5044617

    ListStops[15].Id=16
    ListStops[15].CoordX=611422
    ListStops[15].CoordY=5044637

    ListStops[16].Id=17
    ListStops[16].CoordX=611404
    ListStops[16].CoordY=5044622

    ListStops[17].Id=18
    ListStops[17].CoordX=611403
    ListStops[17].CoordY=5044598

    ListStops[18].Id=19
    ListStops[18].CoordX=611418
    ListStops[18].CoordY=5044604

    ListStops[19].Id=20
    ListStops[19].CoordX=611428
    ListStops[19].CoordY=5044617

    ListStops[20].Id=21
    ListStops[20].CoordX=611188
    ListStops[20].CoordY=5044576

    ListStops[21].Id=22
    ListStops[21].CoordX=611193
    ListStops[21].CoordY=5044587

    ListStops[22].Id=23
    ListStops[22].CoordX=611201
    ListStops[22].CoordY=5044599

    ListStops[23].Id=24
    ListStops[23].CoordX=611252
    ListStops[23].CoordY=5044830

    ListStops[24].Id=25
    ListStops[24].CoordX=611237
    ListStops[24].CoordY=5044824

    # for LiSt in ListStops:
    #     print(LiSt.Id)

    return ListStops


def MenFunc(inList):
   return sum(inList)/len(inList)


def AveragCoords(inListStops):
    XcoordList=[]
    YcoordList=[]
    for Stop in inListStops:
        XcoordList.append(Stop.CoordX)
        YcoordList.append(Stop.CoordY)
    Xav=MenFunc(inList=XcoordList)
    Yav=MenFunc(inList=YcoordList)
    return Xav,Yav


def Agregate(ListStops,Range):

    print("ListStops",type(ListStops))
    # for idx,Bs1 in enumerate(ListStops[:-1]):
    #     id2=idx+1
    #     print(ListStops[idx].Id)
    #     print(ListStops[id2].Id)

    NodeList=[]
    StopsAlreadyInNodes=[]
    DictStops={}
    DictDist2Stop={}
    DictStop2Dist={}
    ExitValues=[]
    
    for Bs1 in ListStops:
        DictStops[Bs1.Id]=Bs1
        DictDist2Stop[Bs1.Id]={}
        DictStop2Dist[Bs1.Id]={}


    # Distance calculations
    for key1 in DictStops.keys():
        print(key1,DictStops[key1])
        Bs1=DictStops[key1]
        for key2 in DictStops.keys():
            Bs2=DictStops[key2]
            if Bs1 == Bs2:
                continue
            else:
                D=float(Distance(P1=[Bs1.CoordX,Bs1.CoordY],P2=[Bs2.CoordX,Bs2.CoordY]))
                # print("Bs1",Bs1.Id,"Bs2",Bs2.Id,D)
                if D <= Range:
                    Bs1.Cluster.append((Bs2.Id,D))
                    DictStop2Dist[Bs1.Id][Bs2.Id]=D
                    DictDist2Stop[Bs1.Id][D]=Bs2.Id


    # Creation of the nodes
    StopsInCurrentNode=[]
    for stop in ListStops:
        
        print("\n\n")

        #if node has been assigned ignore
        if stop in StopsAlreadyInNodes:
            print("Skip")

        #node not used is processed
        elif stop not in StopsAlreadyInNodes:
            print("New Record")
            NodesOperation=[]
            NodesOperation.append(stop)
            StopsAlreadyInNodes.append(stop)
            StopsInCurrentNode
            NearNeigDist=min(DictDist2Stop[stop.Id].keys())
            StopsAlreadyInNodes.append(DictStops[DictDist2Stop[stop.Id][NearNeigDist]])
            NodesOperation.append(DictStops[DictDist2Stop[stop.Id][NearNeigDist]])
            DictStops[DictDist2Stop[stop.Id][NearNeigDist]]
            Xav,Yav=AveragCoords(inListStops=NodesOperation)
            print("Base Coords for Node:")
            print(Xav,Yav)  
            SetListStops=set(ListStops)
            # SetStopsAlreadyInNodes=set(StopsAlreadyInNodes)
            NotUsed = SetListStops.difference(StopsAlreadyInNodes)
            print("NotUsed", type(NotUsed))
            for NoSto in list(NotUsed):
                print(NoSto.Id,end="\t")
                D=float(Distance(P1=[Xav,Yav],P2=[NoSto.CoordX,NoSto.CoordY]))
                if D<=Range:
                    NodesOperation.append(NoSto)
                    StopsAlreadyInNodes.append(NoSto)
                    Xav,Yav=AveragCoords(inListStops=NodesOperation)
            print("\nFinal Coords:",Xav,Yav)
            print("\nused stops in node:",end="\t")
            for used in NodesOperation:
                print(used.Id,end="-\t-") 

            print("\n\nBurnneds stops: ",end="")
            for used in StopsAlreadyInNodes:
                print(used.Id,end="-\t-")

            # Calculation of the Data on each node
            RoutesInNode=[]
            StopCodesInNode=[]
            for stop in NodesOperation:
                for route in stop.Routes:
                    if route not in RoutesInNode: RoutesInNode.append(route)
                StopCodesInNode.append(stop.Id)
            AmountRoutes=len(StopCodesInNode)
            ExitValues.append([Xav,Yav,AmountRoutes,RoutesInNode,StopCodesInNode])
    return ExitValues


            # b=input('\nPress Enter ...')





    # print("-----------------------")
    # for Stop in ListStops:
    #     if Stop.Id not in StopsAlreadyInNodes:
    #         print("Evaluated Stop: ",Stop.Id)
    #         print("Used stops: ",end="")
    #         for used in StopsAlreadyInNodes:
    #             print(used.Id,end="-\t-")
    #         print()
    #         Node=[]
    #         NearNeigDist=min(DictDist2Stop[Stop.Id].keys())
    #         StopsAlreadyInNodes.append(Stop)
    #         StopsAlreadyInNodes.append(DictStops[DictDist2Stop[Stop.Id][NearNeigDist]])
    #         Node.append(Stop)
    #         Node.append(DictStops[DictDist2Stop[Stop.Id][NearNeigDist]])
    #         print(Stop.Id," su vecino más cercano es ",DictDist2Stop[Stop.Id][NearNeigDist]," a ",NearNeigDist)
    #         Xav,Yav=AveragCoords(inListStops=Node)
    #         print(Xav,Yav)
    #         for InnerStop in ListStops:
    #             if InnerStop not in StopsAlreadyInNodes:
    #                 D=float(Distance(P1=[Xav,Yav],P2=[InnerStop.CoordX,InnerStop.CoordY]))
    #                 if D<=Range:
    #                     Node.append(InnerStop)
    #                     StopsAlreadyInNodes.append(InnerStop)
    #                     Xav,Yav=AveragCoords(inListStops=Node)
    #                     print("\t\t\tSe anade")
    #                     print("\t\t\t",Xav,Yav)
    #         print("resulting Coords for Node:",Xav,Yav)
    #         for element in Node:
    #             print(element.Id)
    #         print("Used stops: ",end="")
    #         for used in StopsAlreadyInNodes:
    #             print(used.Id,end="\t")
    #         b=input('Press Enter ...')
    #         print("#######################################")
    #         print("#######################################")
    #         print("#######################################")
    #     else:
    #         print("works ")
    #         b=input('Press Enter ...')













if __name__ == "__main__":
    ListStops=Iniciar()
    Agregate(ListStops=ListStops,Range=75)
    # print(MenFunc(inList=[51,2513,458,5748,532,548,5485312,5,485,5,69874,684,9,41,687,451,84,169,4868,4,48,16,684,684,68,74896,46,87,488]))
    # A=[1,2,3,4,5,6,7,8,9]
    # for i in A[:-1]:
    #     print(i)