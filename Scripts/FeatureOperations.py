#! python3.7
import os
import math 

# from scipy._lib.six import xrange
import decimal
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



from ClassCollection import Station
from ClassCollection import CriteriaData
# from ClassCollection import StreetSegment
from ClassCollection import Paths
from ClassCollection import Segment
from ClassCollection import Street

import decimal
decimal.getcontext().prec = 10


def ConvertToUTM(lat,lon):
    import warnings
    warnings.filterwarnings("ignore")
    Zone=int((float(lon)/6)+31)
    if lat>0:
        Val_EPSG="epsg:326"+str(Zone)
    elif lat<0:
        Val_EPSG="epsg:325"+str(Zone)
    proj_wgs84 = pyproj.Proj(init="epsg:4326")
    proj_utm = pyproj.Proj(init=str(Val_EPSG))
    x, y = pyproj.transform(proj_wgs84, proj_utm, lon, lat)
    # print("lat",lat,"lon",lon)
    # print("x",x,"y",y)
    # b=input('Press Enter ...')

    return x,y,Val_EPSG

def ConvertToLatLon(x,y,Val_EPSG):
    inProj = pyproj.Proj(init=Val_EPSG)
    outProj = pyproj.Proj(init='epsg:4326')
    x2,y2 = pyproj.transform(inProj,outProj,x,y)
    # print (x2,y2)
    return x2,y2




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
        
        # print("\n\n")

        #if node has been assigned ignore
        if stop in StopsAlreadyInNodes:
            # print("Skip")
            pass

        #node not used is processed
        elif stop not in StopsAlreadyInNodes:
            # print("New Record")
            NodesOperation=[]
            NodesOperation.append(stop)
            StopsAlreadyInNodes.append(stop)
            StopsInCurrentNode
            # print("DictDist2Stop[stop.Id]",DictDist2Stop[stop.Id])
            if len(DictDist2Stop[stop.Id].keys())==0:
                # print("Routes",stop.Routes)
                lon,lat=ConvertToLatLon(x=stop.CoordX,y=stop.CoordY,Val_EPSG=stop.Epsg)
                ExitValues.append([lat,lon,len(stop.Routes),stop.Routes,stop.Id])
            else:
                NearNeigDist=min(DictDist2Stop[stop.Id].keys())
                StopsAlreadyInNodes.append(DictStops[DictDist2Stop[stop.Id][NearNeigDist]])
                NodesOperation.append(DictStops[DictDist2Stop[stop.Id][NearNeigDist]])
                DictStops[DictDist2Stop[stop.Id][NearNeigDist]]
                Xav,Yav=AveragCoords(inListStops=NodesOperation)
                # print("Base Coords for Node:")
                # print(Xav,Yav)  
                SetListStops=set(ListStops)
                # b=input('Press Enter ...')
                # SetStopsAlreadyInNodes=set(StopsAlreadyInNodes)
                NotUsed = SetListStops.difference(StopsAlreadyInNodes)
                # print("NotUsed", type(NotUsed))
                for NoSto in list(NotUsed):
                    # print(NoSto.Id,end="\t")
                    D=float(Distance(P1=[Xav,Yav],P2=[NoSto.CoordX,NoSto.CoordY]))
                    if D<=Range:
                        NodesOperation.append(NoSto)
                        StopsAlreadyInNodes.append(NoSto)
                        Xav,Yav=AveragCoords(inListStops=NodesOperation)
                        # b=input('Press Enter ...')
                # print("\nFinal Coords:",Xav,Yav)
                # print("\nused stops in node:",end="\t")
                # for used in NodesOperation:
                #     print(used.Id,end="-\t-") 
                # print("\n\nBurnneds stops: ",end="")
                # for used in StopsAlreadyInNodes:
                #     print(used.Id,end="-\t-")

                # Calculation of the Data on each node
                RoutesInNode=[]
                StopCodesInNode=[]
                EpsgVal=""
                for stop in NodesOperation:
                    for route in stop.Routes:
                        if route not in RoutesInNode: RoutesInNode.append(route)
                    StopCodesInNode.append(stop.Id)
                    if EpsgVal=="":
                        EpsgVal=stop.Epsg
                    else:
                        if EpsgVal!=stop.Epsg:
                            b=input('ERROR THERE ARE MULTIPLE UTM ZONES; PLEASE RE DOE THE MODULE')
                AmountRoutes=len(StopCodesInNode)

                lon,lat=ConvertToLatLon(x=Xav,y=Yav,Val_EPSG=EpsgVal)
                ExitValues.append([lat,lon,AmountRoutes,RoutesInNode,StopCodesInNode])
            # print("ExitValues",ExitValues)
            # b=input('Press Enter ...')
    return ExitValues




if __name__ == "__main__":
    # CityArea,ClipArea,ExoArea,Ratio,Centroid,CircleRadious=CalculateCompactness(Shapefile=Shapefile)
    # print("CityArea",CityArea)
    # print("ClipArea",ClipArea)
    # print("ExoArea",ExoArea)
    # print("Ratio",Ratio)

    BusShape=r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tools\SampleData\LocalUTM\MEL_BusStops_32555.shp"
    # BusShape=r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tools\SampleData\TEST_BusStop_32618.shp"
    CritData=CriteriaData
    CritData.MinDistMask=50
    CritData.NeigbourDistance=500
    CritData.AdjacentDistance=50
    CritData.NameFieldLines="BusLines"
    CritData.NameFieldStop="STOP_ID"


    StreetShp=r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tools\SampleData\Villa Marie\MTL_VillaMarie_StreetsW2_32618.shp"
    # StreetReading(Shapefile=StreetShp)
    A1=r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tools\SampleData\Villa Marie\MTL_VillaMarie_TestArea1_32618.shp"
    A2=r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tools\SampleData\Villa Marie\MTL_VillaMarie_TestArea2_32618.shp"
    System1=r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tools\SampleData\Villa Marie\MTL_VillaMarie_BusStops_32618.shp"
    System2=r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tools\SampleData\Villa Marie\MTL_VillaMarie_System2_32618.shp"
    Test1=r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tools\Operational\testtxt.shp"
    # Density(ListSystems=[System1,System2],ListWeigths=[1,1],Area=A1)
    CritData=CriteriaData
    CritData.NameFieldLines="BusLines"
    BusShape=r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tools\SampleData\LocalUTM\MEL_BusStops_32555.shp"
    BusTestShp=r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tools\SampleData\Melbourne\Mel_BusTest.shp"
    # Ratio=NetworkNodeEdgeRatio(Shapefile=BusShape,CriteriaData=CritData)
    # ClipPointFeature(Area=A1,OutPut=Test1,InPut=System1)
    # StreetReadingv2(Shapefile=StreetShp)
    # StreetNodeEdgeRatio(Shapefile=StreetShp)

    # LBS=CalculateVecinityBusStops(Shapefile=BusTestShp,FieldId=["STOP_ID",0] ,Routes= ["BusLines",6])
    # for Bs in LBS:
    #     print(Bs.Id,Bs.Routes)
    # print("len LBS",len(LBS))
    # b=input()
    # Nodes= ReadTransitNetwork(ListBusStops=LBS,Range=75)
    # ListObjNode=SimpleListToNodeList(ListofNodes=Nodes)
    ###################################
     
    # LineBuilder(LoN=ListObjNode)
    # Nodes= AgregateTransitNetwork(ListBusStops=LBS,Range=75)


    NewNodes=r"E:\OneDrive - Concordia University - Canada\RA-CAMM\Software\CAMMM-Soft-Tools\SampleData\Network\Sample_MTL_individualStops.shx"
    LBS1=CalculateVecinityBusStops(Shapefile=NewNodes,FieldId=["StopCode",0] ,Routes= ["Lines",1])
    print("Len LBS1",len(LBS1))
    print("End of CalculateVecinityBusStops")
    Nodes= AgregateTransitNetwork(ListBusStops=LBS1,Range=75)



    for idx,Node in enumerate(Nodes):
        print(idx,end="t")
        for El in Node:
            print(El,end="\t")
        print()
    # ReadFieldNames(Shapefile=BusTestShp)

    print("......fin......")
