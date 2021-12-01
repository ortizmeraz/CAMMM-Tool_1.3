import csv
from sys import float_repr_style 
import jenkspy 
import statistics
import numpy as np
import math
import datetime
import utm
import fiona
import geopandas
import json 


import Calculations


def NaturalBreaksBare(Path):
    count=0
    Data=[]
    with open(Path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        # print("csv_reader",type(csv_reader),len(list(csv_reader)))
        for line in csv_reader:
            count+=1
            # print(line[-1])
            if count==1:
                pass
            else:
                Data.append(int(line[-1]))
            # if count==100:
            #     break

    breaks = jenkspy.jenks_breaks(Data, nb_class=5)
    return breaks


def NaturalBreaksNumpy():
    Classess=5
    Path=r"D:\GitHub\CAMMM-Tool_1.3\SampleData\Random\SampleData.csv"
    count=0
    Data=[]
    
    with open(Path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        # print("csv_reader",type(csv_reader),len(list(csv_reader)))
        # a = np.arange(len(list(csv_reader)))
        # print(a)
        for line in csv_reader:
            count+=1
            # print(line[-1])
            if count==1:
                pass
            else:
                Data.append(int(line[-1]))
            # if count==100:
            #     break
        Array=np.array(Data)

    breaks = jenkspy.jenks_breaks(Array, nb_class=Classess)
    return breaks


def QuantilesBare(Path):
    count=0
    Data=[]
    with open(Path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        # print("csv_reader",type(csv_reader),len(list(csv_reader)))
        for line in csv_reader:
            count+=1
            # print(line[-1])
            if count==1:
                pass
            else:
                Data.append(int(line[-1]))
            # if count==100:
            #     break

    breaks= statistics.quantiles(Data,n=5)
    return breaks

def StandardDeviations(Path):
    count=0
    Data=[]
    with open(Path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        # print("csv_reader",type(csv_reader),len(list(csv_reader)))
        for line in csv_reader:
            count+=1
            # print(line[-1])
            if count==1:
                pass
            else:
                Data.append(int(line[-1]))
            # if count==100:
            #     break

    StDev=statistics.stdev(Data)
    # print("Min",min(Data))
    # print("1 D",StDev)
    # print("1 D",StDev*2)
    # print("Max",max(Data))




def chunkIt(Path, num):
    ##################################################
    count=0
    Data=[]
    with open(Path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        # print("csv_reader",type(csv_reader),len(list(csv_reader)))
        for line in csv_reader:
            count+=1
            # print(line[-1])
            if count==1:
                pass
            else:
                Data.append(int(line[-1]))
    Data.sort()
    # print("max",max(Data))
    # print("Min",min(Data))

    avg = len(Data) / float(num)
    out = []
    last = 0.0

    while last < len(Data):
        out.append(Data[int(last):int(last + avg)])
        last += avg
    
    exit=[]
    for chunk in out[:-1]:
        exit.append(max(chunk))
    
    return exit
    
def WriteToJsonFile(Text,Path):
    fw=open(Path,'w')
    fw.write(Text)
    fw.write('\n')
    fw.close()


def RotatedCoords(Xval,Yval,RAngle):
    xR=(Xval*math.cos(RAngle))+(Yval*math.sin(RAngle))
    yR=((-1*Xval)*math.sin(RAngle))+(Yval*math.cos(RAngle))
    return xR,yR


def CalculateRotatedGrid(Angle,Distnace,StartX,StartY,NumCellX,NumCellY):
    RAngle=math.radians(Angle)
    GridList=[]
    # NumCellY+=1
    # print("Angle",Angle)
    # print("Distnace",Distnace)
    # print("StartX",StartX)
    # print("StartY",StartY)
    # print("NumCellX",NumCellX)
    # print("NumCellY",NumCellY)
    # b=input("HALT")
    for iY in range(NumCellY):
        YCoordTop=((iY+1)*Distnace)
        YCoordDow=((iY)*Distnace)
        # print("\n\n iY:",iY)
        # print("\n\tYCoordDow:",YCoordDow)
        # print("\n\tYCoordTop:",YCoordTop)
        for iX in range(0,NumCellX):
            XCoordRigth=((iX+1)*Distnace)
            XCoordLeftt=((iX)*Distnace)
            # print("\t\t iX:",iX)
            # print("\t\t StartX",StartX,"XCoordLeftt:",XCoordLeftt)
            # print("\t\t StartX",StartX,"XCoordRigth:",XCoordRigth)
    
            # Q1
            x1R,y1R=RotatedCoords(Xval=XCoordLeftt,Yval=YCoordDow,RAngle=RAngle)
            # print("Q1\n","\t x1R",x1R,x1R+StartX)
            # print("\t y1R",y1R,y1R+StartY)
            # Q2
            x2R,y2R=RotatedCoords(Xval=XCoordRigth,Yval=YCoordDow,RAngle=RAngle)
            # print("Q2\n","\t x2R",x2R,x2R+StartX)
            # print("\t y2R",y2R,y2R+StartY)
            # Q3
            x3R,y3R=RotatedCoords(Xval=XCoordRigth,Yval=YCoordTop,RAngle=RAngle)
            # print("Q3\n","\t x3R",x3R,x3R+StartX)
            # print("\t y3R",y3R,y3R+StartY)
            # Q4
            x4R,y4R=RotatedCoords(Xval=XCoordLeftt,Yval=YCoordTop,RAngle=RAngle)
            # print("Q4\n","\t x4R",x4R,x4R+StartX)
            # print("\t y4R",y4R,y4R+StartY)

            # b=input("HALT")

            Cx1R=x1R+StartX
            Cy1R=y1R+StartY

            Cx2R=x2R+StartX
            Cy2R=y2R+StartY

            Cx3R=x3R+StartX
            Cy3R=y3R+StartY

            Cx4R=x4R+StartX
            Cy4R=y4R+StartY

            # print(Cx1R,Cy1R,Cx2R,Cy2R,Cx3R,Cy3R,Cx4R,Cy4R)
            GridList.append([[Cx1R,Cy1R],[Cx2R,Cy2R],[Cx3R,Cy3R],[Cx4R,Cy4R]])
    return GridList
    

# def CalculateRotatedGrid(Angle,Distnace,StartX,StartY,NumCellX,NumCellY):
#     RAngle=math.radians(Angle)
#     GridList=[]
#     # NumCellY+=1
#     for iY in range(NumCellY):
#         # print("\n\n\nY:",iY)
#         DiY=iY+1
#         for iX in range(0,NumCellX):
#             DiX=iX+1
#             # print("||X:",iX)
#             # Q1 coords
#             X1Distnace=StartX+(iX*Distnace)
#             Y1Distnace=StartY+(iY*Distnace)
#             # print(end="\t"*1)
#             # print("Q1xD",X1Distnace,"Q1yD",Y1Distnace,end="\t")
#             # Q2 coords
#             X2Distnace=StartX+(DiX*Distnace)
#             Y2Distnace=StartY+(iY*Distnace)
#             # print("X:",iX,end="\t")
#             # print(end="\t"*1)
#             # print("Q2xD",X2Distnace,"Q2yD",Y2Distnace,end="\t")
#             # Q3 coords
#             X3Distnace=StartX+(DiX*Distnace)
#             Y3Distnace=StartY+(DiY*Distnace)
#             # print("X:",iX,end="\t")
#             # print(end="\t"*1)
#             # print("Q3xD",X3Distnace,"Q3yD",Y3Distnace,end="\t")
#             # Q4 coords
#             X4Distnace=StartX+(iX*Distnace)
#             Y4Distnace=StartY+(DiY*Distnace)
#             # print("X:",iX,end="\t")
#             # print(end="\t"*1)
#             # print("Q4xD",X4Distnace,"Q4yD",Y4Distnace,end="\t")
            
#             X1Distnace=X1Distnace+StartX
#             Y1Distnace=Y1Distnace+StartY
#             X2Distnace=X2Distnace+StartX
#             Y2Distnace=Y2Distnace+StartY
#             X3Distnace=X3Distnace+StartX
#             Y3Distnace=Y3Distnace+StartY
#             X4Distnace=X4Distnace+StartX
#             Y4Distnace=Y4Distnace+StartY


#             x1R,y1R=RotatedCoords(XDistnace=X1Distnace,YDistnace=Y1Distnace,RAngle=RAngle)
#             x2R,y2R=RotatedCoords(XDistnace=X2Distnace,YDistnace=Y2Distnace,RAngle=RAngle)
#             x3R,y3R=RotatedCoords(XDistnace=X3Distnace,YDistnace=Y3Distnace,RAngle=RAngle)
#             x4R,y4R=RotatedCoords(XDistnace=X4Distnace,YDistnace=Y4Distnace,RAngle=RAngle)

#             # print(x1R,y1R,x2R,y2R,x3R,y3R,x4R,y4R)
#             GridList.append([[x1R,y1R],[x2R,y2R],[x3R,y3R],[x4R,y4R]])
#     return GridList
    
def MakeCRS(Letter,Number):
    North=["N","P","Q","R","S","T","U","V","W","X"]
    South=["C","D","E","F","G","H","J","K","L","M"]
    if Letter in North:
        Exit="326"+str(Number)
    if Letter in South:
        Exit="325"+str(Number)
    return Exit

# def CreateGridObj(ListCoords,EPSGname,Name):
#     Start="{    \"type\": \"FeatureCollection\",   \"name\": \""+Name+"\",  \"crs\": {     \"type\": \"name\",     \"properties\": {  \"name\": \"urn:ogc:def:crs:EPSG::"+EPSGname+"\"    }    }, \"features\": ["
#     # Start="{ \"features\": ["
#     End="]}"
#     Header="            ,\"geometry\": {                \"type\": \"Polygon\",                \"coordinates\": [                    [ "
#     Footer="                ]            }        },"

#     ExitText=""
#     ExitText+=Start
#     for idx,poly in enumerate(ListCoords):
#         # print(idx)
#         Coords1=poly[0]
#         Coords2=poly[1]
#         Coords3=poly[2]
#         Coords4=poly[3]
#         if Coords1[1]==0 and Coords2[1]==0 and Coords3[1]==0 and Coords4[1]==0:
#             continue


#         TextCoord=str(Coords1)+", "+str(Coords2)+", "+str(Coords3)+", "+str(Coords4)+", "+str(Coords1)+"  ]"
#         TextData="        {            \"type\": \"Feature\",            \"properties\": {                \"Id\": "+str(idx)+"            }"
#         if poly ==ListCoords[-1]:
#                 Footer="                ]            }        }"

            
#         ExitText+=TextData
#         ExitText+=Header
#         ExitText+=TextCoord
#         ExitText+=Footer


#     ExitText+=End
#     return ExitText

def CreateGridObj(ListCoords,EPSGname,Name):
    Start="{    \"type\": \"FeatureCollection\",   \"name\": \""+Name+"\",  \"crs\": {     \"type\": \"name\",     \"properties\": {  \"name\": \"urn:ogc:def:crs:EPSG::"+EPSGname+"\"    }    }, \"features\": ["
    # Start="{ \"features\": ["
    End="]}"
    Footer="                ]            }        },\n"

    ExitText=""
    ExitText+=Start

    if len(ListCoords[0])==2:
        Header="            ,\"geometry\": {                \"type\": \"Point\",                \"coordinates\": [              "
        for idx,poly in enumerate(ListCoords):
            Coords1=poly[0]
            Coords2=poly[1]
            TextCoord=str(Coords1)+", "+str(Coords2)
            TextData="        {            \"type\": \"Feature\",            \"properties\": {                \"Id\": "+str(idx)+"            }"
            if poly ==ListCoords[-1]:
                    Footer="                ]            }        }"
            ExitText+=TextData
            ExitText+=Header
            ExitText+=TextCoord
            ExitText+=Footer
        ExitText+=End


    if len(ListCoords[0])==4:
        Header="            ,\"geometry\": {                \"type\": \"Polygon\",                \"coordinates\": [                    [ "
        for idx,poly in enumerate(ListCoords):
            # print(idx)
            Coords1=poly[0]
            Coords2=poly[1]
            Coords3=poly[2]
            Coords4=poly[3]
            if Coords1[1]==0 and Coords2[1]==0 and Coords3[1]==0 and Coords4[1]==0:
                continue
            TextCoord=str(Coords1)+", "+str(Coords2)+", "+str(Coords3)+", "+str(Coords4)+", "+str(Coords1)+"  ]"
            TextData="        {            \"type\": \"Feature\",            \"properties\": {                \"Id\": "+str(idx)+"            }"
            if poly ==ListCoords[-1]:
                    Footer="                ]            }        }"
            ExitText+=TextData
            ExitText+=Header
            ExitText+=TextCoord
            ExitText+=Footer


        ExitText+=End
    return ExitText

def CreateGridObjProperties(DictCoords,EPSGname,Name,Table):
    Start="{    \"type\": \"FeatureCollection\",   \"name\": \""+Name+"\",  \"crs\": {     \"type\": \"name\",     \"properties\": {  \"name\": \"urn:ogc:def:crs:EPSG::"+EPSGname+"\"    }    }, \"features\": ["
    End="]}"
    CoordHeader=" \"geometry\": {                \"type\": \"Polygon\",                \"coordinates\": [                    [ "
    Footer="                ]            }        },"
    TextData=" {            \"type\": \"Feature\",            "

    ExitText=""
    ExitText+=Start
    ListGrid=list(DictCoords.keys())
    for keyD in ListGrid:
        # print(idx)
        if Table["Count"][keyD]==0:
            next
        KeyList=list(Table.keys())
        PropertiesText="\"properties\": {"
        PropertiesText+="\"Id\":"+str(keyD)+","
        for k in KeyList:
            # print(Table[k][keyD],type(Table[k][keyD]))
            PropertiesText+="\""+str(k)+"\":"+str(Table[k][keyD])
            if k != KeyList[-1]:
                PropertiesText+=","
        PropertiesText+="},"
        # print(DictCoords[keyD])
        Coords1=DictCoords[keyD][0]
        Coords2=DictCoords[keyD][1]
        Coords3=DictCoords[keyD][2]
        Coords4=DictCoords[keyD][3]
        if Coords1[1]==0 and Coords2[1]==0 and Coords3[1]==0 and Coords4[1]==0:
            continue
        TextCoord="["+str(Coords1[1])+","+str(Coords1[0])+"], ["+str(Coords2[1])+","+str(Coords2[0])+"], ["+str(Coords3[1])+","+str(Coords3[0])+"], ["+str(Coords4[1])+","+str(Coords4[0])+"], ["+str(Coords1[1])+","+str(Coords1[0])+" ] ]"
        # print(ProText)
        if keyD == ListGrid[-1]:
            Footer="                ]            }        }"

        ExitText+=TextData
        ExitText+=PropertiesText
        ExitText+=CoordHeader
        ExitText+=TextCoord
        ExitText+=Footer
    ExitText+=End
    return ExitText

def CalcDistShapes(Data1,Data2):
    # print(Data1,Data2)
    # (latitude, longitude)
    # print("Data1['shape_pt_lat']",type(Data1['shape_pt_lat']),Data1['shape_pt_lat'])
    Lat=float(Data1['shape_pt_lat'])
    Lon=float(Data1['shape_pt_lon'])
    P1=utm.from_latlon(Lat, Lon)
    P1x=P1[0]
    P1y=P1[1]
    # print("P1",P1x,P1y)
    ######################
    Lat=float(Data2['shape_pt_lat'])
    Lon=float(Data2['shape_pt_lon'])
    P2=utm.from_latlon(Lat, Lon)
    P2x=P2[0]
    P2y=P2[1]
    # print("P2",P2x,P2y)
    Dist=Calculations.CalcDistance(P1x,P1y,P2x,P2y)
    # print("Dist",Dist)
    return Dist,P1x,P1y,P2x,P2y




def calculate_initial_compass_bearing(pointA, pointB):
    """
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing


def GetAngle(PathShapes,PathTrips,PathRoutes):
    DataShapes={}
    DataTrips={}
    DataRoutes=[]
    TripId={}
    LatCol=[]
    LonCol=[]
    VectorList=[]
    ShortAngles=[]
    LonggAngles=[]
    print("hi")
    with open(PathRoutes, 'r',encoding='utf8') as file:
        reader = csv.reader(file)
        Header=next(reader)
        # print("PathShapes",Header)
        for line in reader:
            # print(line,type(line))
            # b=input("Delete")
            DataRoutes.append(line[0])
            TripId[line[0]]={}
    # print(DataRoutes)
    with open(PathShapes, 'r',encoding='utf8') as file:
        reader = csv.reader(file)
        Header=next(reader)
        # print("PathShapes",Header)
        for line in reader:
            if line[0] in DataShapes:
                DataShapes[line[0]][line[3]]={'shape_pt_lat':line[1],'shape_pt_lon':line[2]}
                LatCol.append(line[1])
                LonCol.append(line[2])

            # 'shape_pt_sequence':
            else:
                DataShapes[line[0]]={}
                DataShapes[line[0]][line[3]]={'shape_pt_lat':line[1],'shape_pt_lon':line[2]}
                LatCol.append(line[1])
                LonCol.append(line[2])
        #     print(line)
        # print(DataShapes)
    with open(PathTrips, 'r',encoding='utf8') as file:
        reader = csv.reader(file)
        Header=next(reader)
        for line in reader:
            # print(line,type(line))
            # print(line[0],line[3],line[4],DataShapes[line[5]]['shape_pt_lat'],DataShapes[line[5]]['shape_pt_lon'],DataShapes[line[5]]['shape_pt_sequence'])
            TripId[line[0]][line[4]]=[line[3],line[5]]
        # print("PathTrips",Header)

    for Ro in DataRoutes:
        # print(Ro,TripId[Ro],"············································")
        # print("\n"*10)
        for Tri in TripId[Ro]:
            # print("\t",Tri,"-",TripId[Ro][Tri][1],DataShapes[TripId[Ro][Tri][1]])
            # print("*****************",Tri, len(DataShapes[TripId[Ro][Tri][1]]))
            # for key in DataShapes[TripId[Ro][Tri][1]].keys():
            #     print(key,DataShapes[TripId[Ro][Tri][1]][key])
            ShpIdList=list(DataShapes[TripId[Ro][Tri][1]].keys())
            MiniData=DataShapes[TripId[Ro][Tri][1]]
            # print(ShpIdList)
            for aPoint in range(0,len(DataShapes[TripId[Ro][Tri][1]])-1):
                bPoint=aPoint+1
                # print(aPoint,"-",ShpIdList[aPoint],MiniData[ShpIdList[aPoint]],"·······",bPoint,"-",ShpIdList[bPoint],MiniData[ShpIdList[bPoint]])
                Vect=CalcDistShapes(Data1=MiniData[ShpIdList[aPoint]],Data2=MiniData[ShpIdList[bPoint]])
                if Vect[0]>10:
                    VectorList.append(Vect)
                    
    print("VectorList",len(VectorList))
    for vect in VectorList:
        Angle=calculate_initial_compass_bearing(pointA=(vect[1],vect[2]), pointB=(vect[3],vect[4]))
        if Angle>180:
            Alfa=Angle-180
        else:
            Alfa=Angle
        if Alfa >=90:
            # print("Larger than")
            LonggAngles.append(Alfa)
        else:
            ShortAngles.append(Alfa)
        # print("Angle",Alfa)
    AvShort=sum(ShortAngles)/len(ShortAngles)
    AvLongg=sum(LonggAngles)/len(LonggAngles)

    # print("Short Average Angle is:  ",AvShort)
    # print("Long  Average Angle is:  ",AvLongg, (AvLongg-90))
    AvAngle=(AvShort+(AvLongg-90))/2
    # print("Average Angle: ",AvAngle)
    # Here you have the angle, still need to get the heading
    return AvAngle,LatCol,LonCol

def GetCoords(LatCol,LonCol):

    MinLon=float(min(LonCol))
    MinLat=float(min(LatCol))
    MaxLon=float(max(LonCol))
    MaxLat=float(max(LatCol))
    if MaxLon > 0 and MaxLat > 0:
        Coords=utm.from_latlon(MinLat,MinLon)
        # print(" Lon + | Lat + ")
        CoCoords=utm.from_latlon(MaxLat,MaxLon)

    if MaxLon > 0 and MaxLat < 0:
        Coords=utm.from_latlon(MaxLat,MinLon)
        # print("Lon + | Lat - ")
        CoCoords=utm.from_latlon(MinLat,MaxLon)

    if MaxLon < 0 and MaxLat < 0:
        Coords=utm.from_latlon(MaxLat,MaxLon)
        # print("Lon - | Lat - ")
        CoCoords=utm.from_latlon(MinLat,MinLon)
    
    if MaxLon < 0 and MaxLat > 0:
        Coords=utm.from_latlon(MinLat,MaxLon)
        # print("Lon - | Lat + ")
        CoCoords=utm.from_latlon(MaxLat,MinLon)

    # print(Coords)
    # print(CoCoords)
    return Coords,CoCoords


def RoundNumb(number):
    TextNumber=str(number)
    ListNum=TextNumber.split(".")
    if float(ListNum[1])>0.2:
        sum=1
    else:
        sum=0
    var = int(ListNum[0])+sum
    return var


def GeoOperation(RetPath,StopPath):
    # GeoGrid = geopandas.read_file(RetPath)
    # print("GeoGrid: ",type(GeoGrid))
    # print(GeoGrid)
    # GeoStops= geopandas.read_file(StopPath)
    # print("GeoStops: ",type(GeoStops))
    # print(GeoStops)
    # print(dir(GeoGrid))
    # for i in dir(GeoGrid):
    #     print(i)
    from shapely.geometry import Point
    from shapely.geometry.polygon import Polygon
    # pointSample = Point(0.5, 0.5)
    polygonSample = Polygon([(0, 0), (0, 1), (1, 1), (1, 0)])
    # print(polygonSample.contains(pointSample))
    #############################################################################
    #############################################################################

    # import geopandas

    # Read the data.
    polygons = geopandas.GeoDataFrame.from_file(RetPath)
    points = geopandas.GeoDataFrame.from_file(StopPath)

    # print("type of polygons",type(polygons),dir(polygons),"\n\n\n")
    # print("type of points",type(points),dir(points))
    # b=input("Delete")
    # Make a copy because I'm going to drop points as I
    # assign them to polys, to speed up subsequent search.
    pts = points.copy() 

    # We're going to keep a list of how many points we find.
    pts_in_polys = []

    # for j, pt in points.iterrows():
    #     print(j,pt.geometry)
    # b=input("Delete")

    # Loop over polygons with index i.
    # for i, poly in polygons.iterrows():
    #     print(i,poly.geometry)
    print(dir(polygons.iterrows()))
    print(polygons.iterrows().__sizeof__)
    # b=input("Delete")
    Count={}
    for i, poly in polygons.iterrows():
        print(i)
        Count[i]=0
        # print(i,poly.geometry,"\n")
        # print("poly",type(poly))
        # print("poly.geometry",type(poly.geometry))
        # print("polygonSample",type(polygonSample))
        # print(dir(poly.geometry))
        # print(poly.geometry)
        # b=input("Delete")
        for j, pt in points.iterrows():
            # print(j,pt.geometry)
            if poly.geometry.contains(pt.geometry):
                Count[i]=1+Count[i]
                continue
                # print(poly.geometry.contains(pt.geometry))
                # b=input("halt")
            # else:
            #     print(poly.geometry.contains(pt.geometry),end="")
        # if Count[i]>0:
        #     print(i,Count[i])
        #     b=input("halt")
        # Keep a list of points in this poly
        # pts_in_this_poly = []
    
    for i in Count.keys():
        if Count[i]>0:
            print(i,Count[i])
            # b=input("halt")
        # Now loop over all points with index j.
        # for j, pt in pts.iterrows():
        #     if poly.geometry.contains(pt.geometry):
        #         # Then it's a hit! Add it to the list,
        #         # and drop it so we have less hunting.
        #         pts_in_this_poly.append(pt.geometry)
        #         pts = pts.drop([j])

        # We could do all sorts, like grab a property of the
        # points, but let's just append the number of them.
        # pts_in_polys.append(len(pts_in_this_poly))

    # Add the number of points for each poly to the dataframe.
    # polygons['number of points'] = geopandas.GeoSeries(pts_in_polys)
    return Count
    #############################################################################
    #############################################################################

def RetrunLatLonGrid(GridUTMpath,CountData,Letter,Number):
    ExitList={}
    with open (GridUTMpath) as f:
        data = json.load(f)
        Features=data["features"]
        print("type",type(data["features"]))
        # print(Features)
        # [:10]
        for fe in Features:
            Id=fe['properties']['Id']
            print("FE:",Id)
            ExitList[Id]=[]
            # print(fe,type(fe))
            # 'properties'
            # 'geometry'
            #     'coordinates'

            # print(["properties"],type(fe['geometry']['coordinates']))
            # print(len(fe['geometry']['coordinates'][0]))
            # print(fe['geometry']['coordinates'][0])
            for CoordPair in fe['geometry']['coordinates'][0]:
                East=CoordPair[0]
                North=CoordPair[1]
                # print(East,type(East),North,type(North),Letter,type(Letter),Number,type(Number))
                Coordinates=utm.to_latlon(East, North,Number,Letter)
                ExitList[Id].append(Coordinates)
                # print(Coordinates)
            # print("Data: ",CountData[Id])
            # print(ExitList[Id])
            # print("\n\n")
    return ExitList




# Work in the trips part
# route_id	service_id	trip_id	trip_headsign	direction_id	shape_id	wheelchair_accessible	note_fr	note_en
#   0           1           2           3           4               5           6                           7

#    ______
#   |Q4  Q3|
#   |Q1__Q2|
#    
#
# Path=r"D:\GitHub\CAMMM-Tool_1.3\SampleData\Random\SampleData.csv"
# Lists=chunkIt(Path, 5)
# QuantilesBare(Path)
# print("chunkIt",Lists)


def TransformStopsCsvToGeoJson(PathStopsCSV,PathStopsGeojson,Agency):
    with open(PathStopsCSV, 'r',encoding='utf8') as file:
        reader = csv.reader(file)
        Header=next(reader)
        # print("PathShapes",Header)
        # b=input("Delete")
        ListStops=[]
        for line in reader:
            # print(line[3],type(line))
            Id=line[0]
            Lat=float(line[3])
            Lon=float(line[4])
            # print("Id: ",Id,"\tLat: ",Lat,"\tLon: ",Lon)
            Coords=utm.from_latlon(Lat,Lon)
            ListStops.append([Coords[0],Coords[1]])
        # print(Coords)
        # b=input("Delete")
        Number=Coords[2]
        Letter=Coords[3]
        EPSGvar=MakeCRS(Letter,Number)
        TextJSON=CreateGridObj(ListCoords=ListStops,EPSGname=EPSGvar,Name=Agency)
        WriteToJsonFile(Text=TextJSON,Path=PathStopsGeojson)



def GetStopDensity(PathFileGridUTM,PathStops,PathFileGridExit,PathTrip,PathShape,Pathroute,Agency):
    AvAngle,LatCol,LonCol=GetAngle(PathShapes=PathShape,PathTrips=PathTrip,PathRoutes=Pathroute)
    # print("Max Lat",max(LatCol))
    # print("Min Lat",min(LatCol))
    # print("Max Lon",max(LonCol))
    # print("Min Lon",min(LonCol))
    # AvAngle=0
    Coords,CoCoords=GetCoords(LatCol,LonCol)

    DifferenceX=int(abs(Coords[0]-CoCoords[0]))/1000
    DifferenceY=int(abs(Coords[1]-CoCoords[1]))/1000
    # print("DifferenceX",DifferenceX)
    # print("DifferenceY",DifferenceY)

    NumCellX=RoundNumb(number=DifferenceX)
    NumCellY=RoundNumb(number=DifferenceY)
    # print("NumCellX",NumCellX)
    # print("NumCellY",NumCellY)
    Letter=Coords[3]
    Number=Coords[2]
    # print("Coords",Coords)
    # Break=QuantilesBare(Path)
    # # print("QuantilesBare",Break)
    # print("Enters GridCoords")
    GridCoords=CalculateRotatedGrid(Angle=AvAngle,Distnace=1000,StartX=(Coords[0]-10000),StartY=(Coords[1]),NumCellX=(NumCellX+10),NumCellY=(NumCellY+25))
    # print(type(GridCoords))
    # print("Enters CreateGridObj")
    TextJSON=CreateGridObj(ListCoords=GridCoords,EPSGname=MakeCRS(Letter,Number),Name=Agency)
    # print(MakeCRS(Letter,Number))
    # print(TextJSON)
    # print("Enters WriteToJsonFile")
    WriteToJsonFile(Text=TextJSON,Path=PathFileGridUTM)
    # print("Enters GeoOperation")
    CountData=GeoOperation(RetPath=PathFileGridUTM,StopPath=PathStops)
    # print(CountData)
    # Dict2={0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0, 25: 0, 26: 0, 27: 0, 28: 0, 29: 0, 30: 0, 31: 0, 32: 0, 33: 0, 34: 0, 35: 0, 36: 0, 37: 0, 38: 0, 39: 0, 40: 0, 41: 0, 42: 0, 43: 0, 44: 0, 45: 0, 46: 0, 47: 0, 48: 0, 49: 0, 50: 0, 51: 0, 52: 0, 53: 0, 54: 0, 55: 0, 56: 0, 57: 0, 58: 0, 59: 0, 60: 0, 61: 0, 62: 0, 63: 0, 64: 0, 65: 0, 66: 0, 67: 0, 68: 0, 69: 0, 70: 0, 71: 0, 72: 0, 73: 0, 74: 0, 75: 0, 76: 0, 77: 0, 78: 0, 79: 0, 80: 0, 81: 0, 82: 0, 83: 0, 84: 0, 85: 0, 86: 0, 87: 0, 88: 0, 89: 0, 90: 0, 91: 0, 92: 0, 93: 0, 94: 0, 95: 0, 96: 0, 97: 0, 98: 0, 99: 0, 100: 0, 101: 0, 102: 0, 103: 0, 104: 0, 105: 0, 106: 0, 107: 0, 108: 0, 109: 0, 110: 0, 111: 0, 112: 0, 113: 0, 114: 0, 115: 0, 116: 0, 117: 0, 118: 0, 119: 0, 120: 0, 121: 0, 122: 0, 123: 0, 124: 0, 125: 0, 126: 0, 127: 0, 128: 0, 129: 0, 130: 0, 131: 0, 132: 0, 133: 0, 134: 0, 135: 0, 136: 0, 137: 0, 138: 0, 139: 0, 140: 0, 141: 0, 142: 0, 143: 0, 144: 0, 145: 0, 146: 0, 147: 0, 148: 0, 149: 0, 150: 0, 151: 0, 152: 0, 153: 0, 154: 0, 155: 0, 156: 0, 157: 0, 158: 0, 159: 0, 160: 0, 161: 0, 162: 0, 163: 0, 164: 0, 165: 0, 166: 0, 167: 0, 168: 0, 169: 0, 170: 0, 171: 0, 172: 0, 173: 0, 174: 0, 175: 0, 176: 0, 177: 0, 178: 0, 179: 0, 180: 0, 181: 0, 182: 0, 183: 0, 184: 0, 185: 0, 186: 0, 187: 0, 188: 0, 189: 0, 190: 0, 191: 0, 192: 0, 193: 0, 194: 0, 195: 0, 196: 0, 197: 0, 198: 0, 199: 0, 200: 0, 201: 0, 202: 0, 203: 0, 204: 0, 205: 0, 206: 0, 207: 0, 208: 0, 209: 0, 210: 0, 211: 0, 212: 0, 213: 0, 214: 0, 215: 0, 216: 0, 217: 0, 218: 0, 219: 0, 220: 0, 221: 0, 222: 0, 223: 0, 224: 0, 225: 0, 226: 0, 227: 0, 228: 0, 229: 0, 230: 0, 231: 0, 232: 0, 233: 0, 234: 0, 235: 0, 236: 0, 237: 0, 238: 0, 239: 0, 240: 0, 241: 0, 242: 0, 243: 0, 244: 0, 245: 0, 246: 0, 247: 0, 248: 0, 249: 0, 250: 0, 251: 0, 252: 0, 253: 0, 254: 0, 255: 0, 256: 0, 257: 0, 258: 0, 259: 0, 260: 0, 261: 0, 262: 0, 263: 0, 264: 0, 265: 0, 266: 0, 267: 0, 268: 0, 269: 0, 270: 0, 271: 0, 272: 0, 273: 0, 274: 0, 275: 0, 276: 0, 277: 0, 278: 0, 279: 0, 280: 0, 281: 0, 282: 0, 283: 0, 284: 0, 285: 0, 286: 0, 287: 0, 288: 0, 289: 0, 290: 0, 291: 0, 292: 0, 293: 0, 294: 0, 295: 0, 296: 0, 297: 0, 298: 0, 299: 0, 300: 0, 301: 0, 302: 0, 303: 0, 304: 0, 305: 0, 306: 0, 307: 0, 308: 0, 309: 0, 310: 0, 311: 0, 312: 0, 313: 0, 314: 0, 315: 0, 316: 0, 317: 0, 318: 0, 319: 0, 320: 0, 321: 0, 322: 0, 323: 0, 324: 0, 325: 0, 326: 0, 327: 0, 328: 0, 329: 0, 330: 0, 331: 0, 332: 0, 333: 0, 334: 0, 335: 10, 336: 14, 337: 0, 338: 0, 339: 0, 340: 0, 341: 0, 342: 0, 343: 0, 344: 0, 345: 0, 346: 0, 347: 0, 348: 0, 349: 0, 350: 0, 351: 0, 352: 0, 353: 0, 354: 0, 355: 0, 356: 0, 357: 0, 358: 0, 359: 0, 360: 0, 361: 0, 362: 0, 363: 0, 364: 0, 365: 0, 366: 0, 367: 0, 368: 0, 369: 0, 370: 0, 371: 0, 372: 0, 373: 0, 374: 0, 375: 0, 376: 0, 377: 0, 378: 0, 379: 0, 380: 0, 381: 0, 382: 3, 383: 9, 384: 6, 385: 0, 386: 0, 387: 0, 388: 0, 389: 0, 390: 0, 391: 0, 392: 0, 393: 0, 394: 0, 395: 0, 396: 0, 397: 0, 398: 0, 399: 0, 400: 0, 401: 0, 402: 0, 403: 0, 404: 0, 405: 0, 406: 0, 407: 0, 408: 0, 409: 0, 410: 0, 411: 0, 412: 0, 413: 0, 414: 0, 415: 0, 416: 0, 417: 0, 418: 0, 419: 0, 420: 0, 421: 0, 422: 0, 423: 0, 424: 0, 425: 0, 426: 0, 427: 0, 428: 0, 429: 2, 430: 3, 431: 8, 432: 0, 433: 0, 434: 0, 435: 0, 436: 0, 437: 0, 438: 0, 439: 0, 440: 0, 441: 0, 442: 0, 443: 0, 444: 0, 445: 0, 446: 0, 447: 0, 448: 0, 449: 0, 450: 0, 451: 0, 452: 0, 453: 0, 454: 0, 455: 0, 456: 0, 457: 0, 458: 0, 459: 0, 460: 0, 461: 0, 462: 0, 463: 0, 464: 0, 465: 0, 466: 0, 467: 0, 468: 0, 469: 0, 470: 0, 471: 0, 472: 0, 473: 0, 474: 0, 475: 0, 476: 6, 477: 10, 478: 4, 479: 4, 480: 0, 481: 0, 482: 0, 483: 0, 484: 0, 485: 0, 486: 0, 487: 0, 488: 0, 489: 0, 490: 0, 491: 0, 492: 0, 493: 0, 494: 0, 495: 0, 496: 0, 497: 0, 498: 0, 499: 0, 500: 0, 501: 0, 502: 0, 503: 0, 504: 0, 505: 0, 506: 0, 507: 0, 508: 0, 509: 0, 510: 0, 511: 0, 512: 0, 513: 0, 514: 0, 515: 0, 516: 0, 517: 0, 518: 0, 519: 0, 520: 0, 521: 0, 522: 0, 523: 0, 524: 10, 525: 2, 526: 6, 527: 0, 528: 0, 529: 0, 530: 0, 531: 0, 532: 0, 533: 0, 534: 0, 535: 0, 536: 0, 537: 0, 538: 0, 539: 0, 540: 0, 541: 0, 542: 0, 543: 0, 544: 0, 545: 0, 546: 0, 547: 0, 548: 0, 549: 0, 550: 0, 551: 0, 552: 0, 553: 0, 554: 0, 555: 0, 556: 0, 557: 0, 558: 0, 559: 0, 560: 0, 561: 0, 562: 0, 563: 0, 564: 0, 565: 0, 566: 0, 567: 0, 568: 7, 569: 0, 570: 0, 571: 15, 572: 2, 573: 10, 574: 1, 575: 0, 576: 0, 577: 0, 578: 0, 579: 0, 580: 0, 581: 0, 582: 0, 583: 0, 584: 0, 585: 0, 586: 0, 587: 0, 588: 0, 589: 0, 590: 0, 591: 0, 592: 0, 593: 0, 594: 0, 595: 0, 596: 0, 597: 0, 598: 0, 599: 0, 600: 0, 601: 0, 602: 0, 603: 0, 604: 0, 605: 0, 606: 0, 607: 0, 608: 0, 609: 0, 610: 0, 611: 0, 612: 0, 613: 0, 614: 0, 615: 9, 616: 0, 617: 0, 618: 5, 619: 0, 620: 0, 621: 5, 622: 0, 623: 0, 624: 0, 625: 0, 626: 0, 627: 0, 628: 0, 629: 0, 630: 0, 631: 0, 632: 0, 633: 0, 634: 0, 635: 0, 636: 0, 637: 0, 638: 0, 639: 0, 640: 0, 641: 0, 642: 0, 643: 0, 644: 0, 645: 0, 646: 0, 647: 0, 648: 0, 649: 0, 650: 0, 651: 0, 652: 0, 653: 0, 654: 0, 655: 0, 656: 0, 657: 0, 658: 0, 659: 0, 660: 0, 661: 0, 662: 0, 663: 9, 664: 5, 665: 2, 666: 16, 667: 7, 668: 8, 669: 0, 670: 0, 671: 0, 672: 0, 673: 0, 674: 0, 675: 0, 676: 0, 677: 0, 678: 0, 679: 0, 680: 0, 681: 0, 682: 0, 683: 0, 684: 0, 685: 0, 686: 0, 687: 0, 688: 0, 689: 0, 690: 0, 691: 0, 692: 0, 693: 0, 694: 0, 695: 0, 696: 0, 697: 0, 698: 0, 699: 0, 700: 0, 701: 0, 702: 0, 703: 0, 704: 0, 705: 0, 706: 0, 707: 0, 708: 0, 709: 0, 710: 13, 711: 14, 712: 16, 713: 3, 714: 12, 715: 15, 716: 6, 717: 0, 718: 0, 719: 0, 720: 0, 721: 0, 722: 0, 723: 0, 724: 0, 725: 0, 726: 0, 727: 0, 728: 0, 729: 0, 730: 0, 731: 0, 732: 0, 733: 0, 734: 0, 735: 0, 736: 0, 737: 0, 738: 0, 739: 0, 740: 0, 741: 0, 742: 0, 743: 0, 744: 0, 745: 0, 746: 0, 747: 0, 748: 0, 749: 0, 750: 0, 751: 0, 752: 0, 753: 0, 754: 0, 755: 0, 756: 0, 757: 2, 758: 12, 759: 17, 760: 16, 761: 10, 762: 0, 763: 4, 764: 7, 765: 0, 766: 0, 767: 0, 768: 0, 769: 0, 770: 0, 771: 0, 772: 0, 773: 0, 774: 0, 775: 0, 776: 0, 777: 0, 778: 0, 779: 0, 780: 0, 781: 0, 782: 0, 783: 0, 784: 0, 785: 0, 786: 0, 787: 0, 788: 0, 789: 0, 790: 0, 791: 0, 792: 0, 793: 0, 794: 0, 795: 0, 796: 0, 797: 0, 798: 0, 799: 0, 800: 0, 801: 0, 802: 0, 803: 5, 804: 14, 805: 4, 806: 2, 807: 13, 808: 13, 809: 10, 810: 6, 811: 2, 812: 0, 813: 0, 814: 0, 815: 0, 816: 0, 817: 0, 818: 0, 819: 0, 820: 0, 821: 0, 822: 0, 823: 0, 824: 0, 825: 0, 826: 0, 827: 0, 828: 0, 829: 0, 830: 0, 831: 0, 832: 0, 833: 0, 834: 0, 835: 0, 836: 0, 837: 0, 838: 0, 839: 0, 840: 0, 841: 0, 842: 0, 843: 0, 844: 0, 845: 0, 846: 0, 847: 0, 848: 0, 849: 0, 850: 18, 851: 24, 852: 10, 853: 11, 854: 21, 855: 12, 856: 12, 857: 17, 858: 10, 859: 0, 860: 0, 861: 0, 862: 0, 863: 0, 864: 0, 865: 0, 866: 0, 867: 0, 868: 0, 869: 0, 870: 0, 871: 0, 872: 0, 873: 0, 874: 0, 875: 0, 876: 0, 877: 0, 878: 0, 879: 0, 880: 0, 881: 0, 882: 0, 883: 0, 884: 0, 885: 0, 886: 0, 887: 0, 888: 0, 889: 0, 890: 0, 891: 0, 892: 0, 893: 0, 894: 0, 895: 0, 896: 0, 897: 10, 898: 13, 899: 11, 900: 6, 901: 36, 902: 9, 903: 10, 904: 11, 905: 14, 906: 0, 907: 0, 908: 0, 909: 0, 910: 0, 911: 0, 912: 0, 913: 0, 914: 0, 915: 0, 916: 0, 917: 0, 918: 0, 919: 0, 920: 0, 921: 0, 922: 0, 923: 0, 924: 0, 925: 0, 926: 0, 927: 0, 928: 0, 929: 0, 930: 0, 931: 0, 932: 0, 933: 0, 934: 0, 935: 0, 936: 0, 937: 0, 938: 0, 939: 0, 940: 0, 941: 0, 942: 0, 943: 0, 944: 0, 945: 22, 946: 1, 947: 12, 948: 10, 949: 16, 950: 15, 951: 10, 952: 19, 953: 20, 954: 15, 955: 0, 956: 0, 957: 0, 958: 0, 959: 0, 960: 0, 961: 0, 962: 0, 963: 0, 964: 0, 965: 0, 966: 0, 967: 0, 968: 0, 969: 0, 970: 0, 971: 0, 972: 0, 973: 0, 974: 0, 975: 0, 976: 0, 977: 0, 978: 0, 979: 0, 980: 0, 981: 0, 982: 0, 983: 0, 984: 0, 985: 0, 986: 0, 987: 0, 988: 0, 989: 0, 990: 0, 991: 7, 992: 18, 993: 11, 994: 6, 995: 9, 996: 13, 997: 12, 998: 6, 999: 3, 1000: 15, 1001: 18, 1002: 16, 1003: 0, 1004: 0, 1005: 0, 1006: 0, 1007: 0, 1008: 0, 1009: 0, 1010: 0, 1011: 0, 1012: 0, 1013: 0, 1014: 0, 1015: 0, 1016: 0, 1017: 0, 1018: 0, 1019: 0, 1020: 0, 1021: 0, 1022: 0, 1023: 0, 1024: 0, 1025: 0, 1026: 0, 1027: 0, 1028: 0, 1029: 0, 1030: 0, 1031: 0, 1032: 0, 1033: 0, 1034: 0, 1035: 0, 1036: 0, 1037: 0, 1038: 6, 1039: 16, 1040: 23, 1041: 11, 1042: 24, 1043: 22, 1044: 16, 1045: 0, 1046: 0, 1047: 6, 1048: 14, 1049: 30, 1050: 8, 1051: 0, 1052: 0, 1053: 0, 1054: 0, 1055: 0, 1056: 0, 1057: 0, 1058: 0, 1059: 0, 1060: 0, 1061: 0, 1062: 0, 1063: 0, 1064: 0, 1065: 0, 1066: 0, 1067: 0, 1068: 0, 1069: 0, 1070: 0, 1071: 0, 1072: 0, 1073: 0, 1074: 0, 1075: 0, 1076: 0, 1077: 0, 1078: 0, 1079: 0, 1080: 0, 1081: 0, 1082: 0, 1083: 0, 1084: 0, 1085: 1, 1086: 0, 1087: 22, 1088: 10, 1089: 18, 1090: 14, 1091: 18, 1092: 11, 1093: 0, 1094: 0, 1095: 1, 1096: 15, 1097: 20, 1098: 17, 1099: 5, 1100: 0, 1101: 0, 1102: 0, 1103: 0, 1104: 0, 1105: 0, 1106: 0, 1107: 0, 1108: 0, 1109: 0, 1110: 0, 1111: 0, 1112: 0, 1113: 0, 1114: 0, 1115: 0, 1116: 0, 1117: 0, 1118: 0, 1119: 0, 1120: 0, 1121: 0, 1122: 0, 1123: 0, 1124: 0, 1125: 0, 1126: 0, 1127: 0, 1128: 0, 1129: 0, 1130: 0, 1131: 0, 1132: 0, 1133: 0, 1134: 2, 1135: 6, 1136: 22, 1137: 2, 1138: 9, 1139: 10, 1140: 0, 1141: 5, 1142: 0, 1143: 19, 1144: 11, 1145: 17, 1146: 37, 1147: 11, 1148: 0, 1149: 0, 1150: 0, 1151: 0, 1152: 0, 1153: 0, 1154: 0, 1155: 0, 1156: 0, 1157: 0, 1158: 0, 1159: 0, 1160: 0, 1161: 0, 1162: 0, 1163: 0, 1164: 0, 1165: 0, 1166: 0, 1167: 0, 1168: 0, 1169: 0, 1170: 0, 1171: 0, 1172: 0, 1173: 0, 1174: 0, 1175: 0, 1176: 0, 1177: 0, 1178: 0, 1179: 0, 1180: 0, 1181: 0, 1182: 0, 1183: 9, 1184: 4, 1185: 27, 1186: 20, 1187: 6, 1188: 5, 1189: 1, 1190: 16, 1191: 9, 1192: 2, 1193: 23, 1194: 31, 1195: 17, 1196: 18, 1197: 21, 1198: 1, 1199: 0, 1200: 0, 1201: 0, 1202: 0, 1203: 0, 1204: 0, 1205: 0, 1206: 0, 1207: 0, 1208: 0, 1209: 0, 1210: 0, 1211: 0, 1212: 0, 1213: 0, 1214: 0, 1215: 0, 1216: 0, 1217: 0, 1218: 0, 1219: 0, 1220: 0, 1221: 0, 1222: 0, 1223: 0, 1224: 0, 1225: 0, 1226: 0, 1227: 0, 1228: 0, 1229: 0, 1230: 0, 1231: 6, 1232: 10, 1233: 20, 1234: 14, 1235: 16, 1236: 7, 1237: 10, 1238: 0, 1239: 0, 1240: 10, 1241: 14, 1242: 24, 1243: 28, 1244: 29, 1245: 19, 1246: 3, 1247: 0, 1248: 0, 1249: 0, 1250: 0, 1251: 0, 1252: 0, 1253: 0, 1254: 0, 1255: 0, 1256: 0, 1257: 0, 1258: 0, 1259: 0, 1260: 0, 1261: 0, 1262: 0, 1263: 0, 1264: 0, 1265: 0, 1266: 0, 1267: 0, 1268: 0, 1269: 0, 1270: 0, 1271: 0, 1272: 0, 1273: 0, 1274: 0, 1275: 0, 1276: 0, 1277: 0, 1278: 5, 1279: 7, 1280: 26, 1281: 25, 1282: 13, 1283: 20, 1284: 13, 1285: 0, 1286: 6, 1287: 12, 1288: 8, 1289: 30, 1290: 18, 1291: 36, 1292: 27, 1293: 18, 1294: 0, 1295: 0, 1296: 0, 1297: 0, 1298: 0, 1299: 0, 1300: 0, 1301: 0, 1302: 0, 1303: 0, 1304: 0, 1305: 0, 1306: 0, 1307: 0, 1308: 0, 1309: 0, 1310: 0, 1311: 0, 1312: 0, 1313: 0, 1314: 0, 1315: 0, 1316: 0, 1317: 0, 1318: 0, 1319: 0, 1320: 0, 1321: 0, 1322: 0, 1323: 0, 1324: 0, 1325: 13, 1326: 15, 1327: 15, 1328: 22, 1329: 19, 1330: 17, 1331: 0, 1332: 0, 1333: 27, 1334: 18, 1335: 19, 1336: 25, 1337: 18, 1338: 16, 1339: 27, 1340: 28, 1341: 0, 1342: 0, 1343: 0, 1344: 0, 1345: 0, 1346: 0, 1347: 0, 1348: 0, 1349: 0, 1350: 0, 1351: 0, 1352: 0, 1353: 0, 1354: 0, 1355: 0, 1356: 0, 1357: 0, 1358: 0, 1359: 0, 1360: 0, 1361: 0, 1362: 0, 1363: 0, 1364: 0, 1365: 0, 1366: 0, 1367: 0, 1368: 0, 1369: 0, 1370: 0, 1371: 0, 1372: 15, 1373: 8, 1374: 16, 1375: 23, 1376: 31, 1377: 15, 1378: 13, 1379: 7, 1380: 23, 1381: 24, 1382: 30, 1383: 15, 1384: 15, 1385: 17, 1386: 17, 1387: 29, 1388: 0, 1389: 0, 1390: 0, 1391: 0, 1392: 0, 1393: 0, 1394: 0, 1395: 0, 1396: 0, 1397: 0, 1398: 0, 1399: 0, 1400: 0, 1401: 0, 1402: 0, 1403: 0, 1404: 0, 1405: 0, 1406: 0, 1407: 0, 1408: 0, 1409: 0, 1410: 0, 1411: 0, 1412: 0, 1413: 0, 1414: 0, 1415: 0, 1416: 0, 1417: 0, 1418: 0, 1419: 22, 1420: 37, 1421: 31, 1422: 23, 1423: 32, 1424: 23, 1425: 18, 1426: 8, 1427: 9, 1428: 23, 1429: 32, 1430: 28, 1431: 6, 1432: 32, 1433: 14, 1434: 13, 1435: 0, 1436: 0, 1437: 0, 1438: 0, 1439: 0, 1440: 0, 1441: 0, 1442: 0, 1443: 0, 1444: 0, 1445: 0, 1446: 0, 1447: 0, 1448: 0, 1449: 0, 1450: 0, 1451: 0, 1452: 0, 1453: 0, 1454: 0, 1455: 0, 1456: 0, 1457: 0, 1458: 0, 1459: 0, 1460: 0, 1461: 0, 1462: 0, 1463: 0, 1464: 0, 1465: 0, 1466: 10, 1467: 22, 1468: 29, 1469: 20, 1470: 57, 1471: 39, 1472: 19, 1473: 46, 1474: 40, 1475: 44, 1476: 41, 1477: 28, 1478: 11, 1479: 28, 1480: 29, 1481: 15, 1482: 0, 1483: 0, 1484: 0, 1485: 0, 1486: 0, 1487: 0, 1488: 0, 1489: 0, 1490: 0, 1491: 0, 1492: 0, 1493: 0, 1494: 0, 1495: 0, 1496: 0, 1497: 0, 1498: 0, 1499: 0, 1500: 0, 1501: 0, 1502: 0, 1503: 0, 1504: 0, 1505: 0, 1506: 0, 1507: 0, 1508: 0, 1509: 0, 1510: 0, 1511: 2, 1512: 0, 1513: 4, 1514: 29, 1515: 14, 1516: 25, 1517: 14, 1518: 21, 1519: 8, 1520: 31, 1521: 36, 1522: 21, 1523: 33, 1524: 40, 1525: 32, 1526: 27, 1527: 33, 1528: 23, 1529: 0, 1530: 0, 1531: 0, 1532: 0, 1533: 0, 1534: 0, 1535: 0, 1536: 0, 1537: 0, 1538: 0, 1539: 0, 1540: 0, 1541: 0, 1542: 0, 1543: 0, 1544: 0, 1545: 0, 1546: 0, 1547: 0, 1548: 0, 1549: 0, 1550: 0, 1551: 0, 1552: 0, 1553: 0, 1554: 0, 1555: 0, 1556: 0, 1557: 0, 1558: 2, 1559: 0, 1560: 0, 1561: 10, 1562: 18, 1563: 28, 1564: 23, 1565: 16, 1566: 22, 1567: 17, 1568: 33, 1569: 29, 1570: 8, 1571: 19, 1572: 33, 1573: 26, 1574: 47, 1575: 5, 1576: 7, 1577: 0, 1578: 0, 1579: 0, 1580: 0, 1581: 0, 1582: 0, 1583: 0, 1584: 0, 1585: 0, 1586: 0, 1587: 0, 1588: 0, 1589: 0, 1590: 0, 1591: 0, 1592: 0, 1593: 0, 1594: 0, 1595: 0, 1596: 0, 1597: 0, 1598: 0, 1599: 0, 1600: 0, 1601: 0, 1602: 0, 1603: 0, 1604: 0, 1605: 0, 1606: 0, 1607: 3, 1608: 20, 1609: 34, 1610: 30, 1611: 22, 1612: 26, 1613: 34, 1614: 25, 1615: 18, 1616: 4, 1617: 20, 1618: 43, 1619: 43, 1620: 43, 1621: 19, 1622: 21, 1623: 7, 1624: 0, 1625: 0, 1626: 0, 1627: 0, 1628: 0, 1629: 0, 1630: 0, 1631: 0, 1632: 0, 1633: 0, 1634: 0, 1635: 0, 1636: 0, 1637: 0, 1638: 0, 1639: 0, 1640: 0, 1641: 0, 1642: 0, 1643: 0, 1644: 0, 1645: 0, 1646: 0, 1647: 0, 1648: 0, 1649: 0, 1650: 0, 1651: 0, 1652: 0, 1653: 0, 1654: 0, 1655: 39, 1656: 42, 1657: 39, 1658: 37, 1659: 13, 1660: 35, 1661: 28, 1662: 11, 1663: 6, 1664: 19, 1665: 54, 1666: 21, 1667: 35, 1668: 6, 1669: 20, 1670: 0, 1671: 0, 1672: 0, 1673: 0, 1674: 0, 1675: 0, 1676: 0, 1677: 0, 1678: 0, 1679: 0, 1680: 0, 1681: 0, 1682: 0, 1683: 0, 1684: 0, 1685: 0, 1686: 0, 1687: 0, 1688: 0, 1689: 0, 1690: 0, 1691: 0, 1692: 0, 1693: 0, 1694: 0, 1695: 0, 1696: 0, 1697: 0, 1698: 0, 1699: 0, 1700: 0, 1701: 6, 1702: 31, 1703: 15, 1704: 36, 1705: 46, 1706: 52, 1707: 25, 1708: 29, 1709: 47, 1710: 13, 1711: 56, 1712: 69, 1713: 29, 1714: 9, 1715: 4, 1716: 0, 1717: 0, 1718: 0, 1719: 0, 1720: 0, 1721: 0, 1722: 0, 1723: 0, 1724: 0, 1725: 0, 1726: 0, 1727: 0, 1728: 0, 1729: 0, 1730: 0, 1731: 0, 1732: 0, 1733: 0, 1734: 0, 1735: 0, 1736: 0, 1737: 0, 1738: 0, 1739: 0, 1740: 0, 1741: 0, 1742: 0, 1743: 0, 1744: 0, 1745: 0, 1746: 0, 1747: 0, 1748: 12, 1749: 32, 1750: 13, 1751: 9, 1752: 49, 1753: 36, 1754: 34, 1755: 35, 1756: 54, 1757: 39, 1758: 57, 1759: 40, 1760: 8, 1761: 0, 1762: 0, 1763: 0, 1764: 0, 1765: 0, 1766: 0, 1767: 0, 1768: 0, 1769: 0, 1770: 0, 1771: 0, 1772: 0, 1773: 0, 1774: 0, 1775: 0, 1776: 0, 1777: 0, 1778: 0, 1779: 0, 1780: 0, 1781: 0, 1782: 0, 1783: 0, 1784: 0, 1785: 0, 1786: 0, 1787: 0, 1788: 0, 1789: 0, 1790: 0, 1791: 0, 1792: 0, 1793: 0, 1794: 9, 1795: 28, 1796: 30, 1797: 8, 1798: 9, 1799: 39, 1800: 38, 1801: 42, 1802: 28, 1803: 45, 1804: 46, 1805: 52, 1806: 12, 1807: 0, 1808: 0, 1809: 0, 1810: 0, 1811: 0, 1812: 0, 1813: 0, 1814: 0, 1815: 0, 1816: 0, 1817: 0, 1818: 0, 1819: 0, 1820: 0, 1821: 0, 1822: 0, 1823: 0, 1824: 0, 1825: 0, 1826: 0, 1827: 0, 1828: 0, 1829: 0, 1830: 0, 1831: 0, 1832: 0, 1833: 0, 1834: 0, 1835: 0, 1836: 0, 1837: 0, 1838: 0, 1839: 2, 1840: 0, 1841: 15, 1842: 40, 1843: 24, 1844: 13, 1845: 16, 1846: 49, 1847: 30, 1848: 30, 1849: 35, 1850: 45, 1851: 47, 1852: 36, 1853: 2, 1854: 4, 1855: 1, 1856: 0, 1857: 0, 1858: 0, 1859: 0, 1860: 0, 1861: 0, 1862: 0, 1863: 0, 1864: 0, 1865: 0, 1866: 0, 1867: 0, 1868: 0, 1869: 0, 1870: 0, 1871: 0, 1872: 0, 1873: 0, 1874: 0, 1875: 0, 1876: 0, 1877: 0, 1878: 0, 1879: 0, 1880: 0, 1881: 0, 1882: 0, 1883: 0, 1884: 0, 1885: 0, 1886: 0, 1887: 0, 1888: 28, 1889: 26, 1890: 22, 1891: 28, 1892: 31, 1893: 26, 1894: 31, 1895: 30, 1896: 39, 1897: 48, 1898: 19, 1899: 4, 1900: 3, 1901: 1, 1902: 0, 1903: 0, 1904: 0, 1905: 0, 1906: 0, 1907: 0, 1908: 0, 1909: 0, 1910: 0, 1911: 0, 1912: 0, 1913: 0, 1914: 0, 1915: 0, 1916: 0, 1917: 0, 1918: 0, 1919: 0, 1920: 0, 1921: 0, 1922: 0, 1923: 0, 1924: 0, 1925: 0, 1926: 0, 1927: 0, 1928: 0, 1929: 0, 1930: 0, 1931: 0, 1932: 0, 1933: 0, 1934: 12, 1935: 21, 1936: 38, 1937: 24, 1938: 21, 1939: 19, 1940: 32, 1941: 23, 1942: 18, 1943: 18, 1944: 37, 1945: 29, 1946: 0, 1947: 0, 1948: 0, 1949: 0, 1950: 0, 1951: 0, 1952: 0, 1953: 0, 1954: 0, 1955: 0, 1956: 0, 1957: 0, 1958: 0, 1959: 0, 1960: 0, 1961: 0, 1962: 0, 1963: 0, 1964: 0, 1965: 0, 1966: 0, 1967: 0, 1968: 0, 1969: 0, 1970: 0, 1971: 0, 1972: 0, 1973: 0, 1974: 0, 1975: 0, 1976: 0, 1977: 0, 1978: 0, 1979: 0, 1980: 0, 1981: 20, 1982: 26, 1983: 17, 1984: 32, 1985: 22, 1986: 17, 1987: 30, 1988: 34, 1989: 18, 1990: 27, 1991: 22, 1992: 11, 1993: 0, 1994: 0, 1995: 0, 1996: 0, 1997: 0, 1998: 0, 1999: 0, 2000: 0, 2001: 0, 2002: 0, 2003: 0, 2004: 0, 2005: 0, 2006: 0, 2007: 0, 2008: 0, 2009: 0, 2010: 0, 2011: 0, 2012: 0, 2013: 0, 2014: 0, 2015: 0, 2016: 0, 2017: 0, 2018: 0, 2019: 0, 2020: 0, 2021: 0, 2022: 0, 2023: 0, 2024: 0, 2025: 0, 2026: 0, 2027: 0, 2028: 17, 2029: 10, 2030: 7, 2031: 20, 2032: 14, 2033: 30, 2034: 25, 2035: 19, 2036: 33, 2037: 23, 2038: 9, 2039: 1, 2040: 0, 2041: 0, 2042: 0, 2043: 0, 2044: 0, 2045: 0, 2046: 0, 2047: 0, 2048: 0, 2049: 0, 2050: 0, 2051: 0, 2052: 0, 2053: 0, 2054: 0, 2055: 0, 2056: 0, 2057: 0, 2058: 0, 2059: 0, 2060: 0, 2061: 0, 2062: 0, 2063: 0, 2064: 0, 2065: 0, 2066: 0, 2067: 0, 2068: 0, 2069: 0, 2070: 0, 2071: 0, 2072: 0, 2073: 0, 2074: 0, 2075: 9, 2076: 10, 2077: 12, 2078: 20, 2079: 12, 2080: 17, 2081: 20, 2082: 20, 2083: 32, 2084: 8, 2085: 16, 2086: 0, 2087: 0, 2088: 0, 2089: 0, 2090: 0, 2091: 0, 2092: 0, 2093: 0, 2094: 0, 2095: 0, 2096: 0, 2097: 0, 2098: 0, 2099: 0, 2100: 0, 2101: 0, 2102: 0, 2103: 0, 2104: 0, 2105: 0, 2106: 0, 2107: 0, 2108: 0, 2109: 0, 2110: 0, 2111: 0, 2112: 0, 2113: 0, 2114: 0, 2115: 0, 2116: 0, 2117: 0, 2118: 0, 2119: 0, 2120: 0, 2121: 0, 2122: 17, 2123: 17, 2124: 16, 2125: 29, 2126: 22, 2127: 26, 2128: 23, 2129: 34, 2130: 10, 2131: 14, 2132: 11, 2133: 0, 2134: 0, 2135: 0, 2136: 0, 2137: 0, 2138: 0, 2139: 0, 2140: 0, 2141: 0, 2142: 0, 2143: 0, 2144: 0, 2145: 0, 2146: 0, 2147: 0, 2148: 0, 2149: 0, 2150: 0, 2151: 0, 2152: 0, 2153: 0, 2154: 0, 2155: 0, 2156: 0, 2157: 0, 2158: 0, 2159: 0, 2160: 0, 2161: 0, 2162: 0, 2163: 0, 2164: 0, 2165: 0, 2166: 0, 2167: 0, 2168: 0, 2169: 6, 2170: 12, 2171: 4, 2172: 8, 2173: 11, 2174: 16, 2175: 16, 2176: 35, 2177: 18, 2178: 19, 2179: 0, 2180: 0, 2181: 0, 2182: 0, 2183: 0, 2184: 0, 2185: 0, 2186: 0, 2187: 0, 2188: 0, 2189: 0, 2190: 0, 2191: 0, 2192: 0, 2193: 0, 2194: 0, 2195: 0, 2196: 0, 2197: 0, 2198: 0, 2199: 0, 2200: 0, 2201: 0, 2202: 0, 2203: 0, 2204: 0, 2205: 0, 2206: 0, 2207: 0, 2208: 0, 2209: 0, 2210: 0, 2211: 0, 2212: 0, 2213: 0, 2214: 0, 2215: 0, 2216: 9, 2217: 18, 2218: 9, 2219: 0, 2220: 1, 2221: 0, 2222: 13, 2223: 16, 2224: 17, 2225: 1, 2226: 0, 2227: 0, 2228: 0, 2229: 0, 2230: 0, 2231: 0, 2232: 0, 2233: 0, 2234: 0, 2235: 0, 2236: 0, 2237: 0, 2238: 0, 2239: 0, 2240: 0, 2241: 0, 2242: 0, 2243: 0, 2244: 0, 2245: 0, 2246: 0, 2247: 0, 2248: 0, 2249: 0, 2250: 0, 2251: 0, 2252: 0, 2253: 0, 2254: 0, 2255: 0, 2256: 0, 2257: 0, 2258: 0, 2259: 0, 2260: 0, 2261: 0, 2262: 0, 2263: 15, 2264: 13, 2265: 12, 2266: 5, 2267: 0, 2268: 0, 2269: 8, 2270: 16, 2271: 0, 2272: 0, 2273: 0, 2274: 0, 2275: 0, 2276: 0, 2277: 0, 2278: 0, 2279: 0, 2280: 0, 2281: 0, 2282: 0, 2283: 0, 2284: 0, 2285: 0, 2286: 0, 2287: 0, 2288: 0, 2289: 0, 2290: 0, 2291: 0, 2292: 0, 2293: 0, 2294: 0, 2295: 0, 2296: 0, 2297: 0, 2298: 0, 2299: 0, 2300: 0, 2301: 0, 2302: 0, 2303: 0, 2304: 0, 2305: 0, 2306: 0, 2307: 0, 2308: 0, 2309: 0, 2310: 0, 2311: 8, 2312: 7, 2313: 10, 2314: 2, 2315: 16, 2316: 10, 2317: 4, 2318: 0, 2319: 0, 2320: 0, 2321: 0, 2322: 0, 2323: 0, 2324: 0, 2325: 0, 2326: 0, 2327: 0, 2328: 0, 2329: 0, 2330: 0, 2331: 0, 2332: 0, 2333: 0, 2334: 0, 2335: 0, 2336: 0, 2337: 0, 2338: 0, 2339: 0, 2340: 0, 2341: 0, 2342: 0, 2343: 0, 2344: 0, 2345: 0, 2346: 0, 2347: 0, 2348: 0, 2349: 0, 2350: 0, 2351: 0, 2352: 0, 2353: 0, 2354: 0, 2355: 0, 2356: 0, 2357: 0, 2358: 16, 2359: 17, 2360: 3, 2361: 20, 2362: 13, 2363: 37, 2364: 0, 2365: 0, 2366: 0, 2367: 0, 2368: 0, 2369: 0, 2370: 0, 2371: 0, 2372: 0, 2373: 0, 2374: 0, 2375: 0, 2376: 0, 2377: 0, 2378: 0, 2379: 0, 2380: 0, 2381: 0, 2382: 0, 2383: 0, 2384: 0, 2385: 0, 2386: 0, 2387: 0, 2388: 0, 2389: 0, 2390: 0, 2391: 0, 2392: 0, 2393: 0, 2394: 0, 2395: 0, 2396: 0, 2397: 0, 2398: 0, 2399: 0, 2400: 0, 2401: 0, 2402: 0, 2403: 0, 2404: 0, 2405: 12, 2406: 5, 2407: 14, 2408: 25, 2409: 22, 2410: 19, 2411: 0, 2412: 0, 2413: 0, 2414: 0, 2415: 0, 2416: 0, 2417: 0, 2418: 0, 2419: 0, 2420: 0, 2421: 0, 2422: 0, 2423: 0, 2424: 0, 2425: 0, 2426: 0, 2427: 0, 2428: 0, 2429: 0, 2430: 0, 2431: 0, 2432: 0, 2433: 0, 2434: 0, 2435: 0, 2436: 0, 2437: 0, 2438: 0, 2439: 0, 2440: 0, 2441: 0, 2442: 0, 2443: 0, 2444: 0, 2445: 0, 2446: 0, 2447: 0, 2448: 0, 2449: 0, 2450: 0, 2451: 4, 2452: 0, 2453: 2, 2454: 24, 2455: 10, 2456: 18, 2457: 3, 2458: 0, 2459: 0, 2460: 0, 2461: 0, 2462: 0, 2463: 0, 2464: 0, 2465: 0, 2466: 0, 2467: 0, 2468: 0, 2469: 0, 2470: 0, 2471: 0, 2472: 0, 2473: 0, 2474: 0, 2475: 0, 2476: 0, 2477: 0, 2478: 0, 2479: 0, 2480: 0, 2481: 0, 2482: 0, 2483: 0, 2484: 0, 2485: 0, 2486: 0, 2487: 0, 2488: 0, 2489: 0, 2490: 0, 2491: 0, 2492: 0, 2493: 0, 2494: 0, 2495: 0, 2496: 0, 2497: 0, 2498: 2, 2499: 0, 2500: 6, 2501: 35, 2502: 10, 2503: 0, 2504: 0, 2505: 0, 2506: 0, 2507: 0, 2508: 0, 2509: 0, 2510: 0, 2511: 0, 2512: 0, 2513: 0, 2514: 0, 2515: 0, 2516: 0, 2517: 0, 2518: 0, 2519: 0, 2520: 0, 2521: 0, 2522: 0, 2523: 0, 2524: 0, 2525: 0, 2526: 0, 2527: 0, 2528: 0, 2529: 0, 2530: 0, 2531: 0, 2532: 0, 2533: 0, 2534: 0, 2535: 0, 2536: 0, 2537: 0, 2538: 0, 2539: 0, 2540: 0, 2541: 0, 2542: 0, 2543: 0, 2544: 0, 2545: 6, 2546: 0, 2547: 11, 2548: 11, 2549: 0, 2550: 0, 2551: 0, 2552: 0, 2553: 0, 2554: 0, 2555: 0, 2556: 0, 2557: 0, 2558: 0, 2559: 0, 2560: 0, 2561: 0, 2562: 0, 2563: 0, 2564: 0, 2565: 0, 2566: 0, 2567: 0, 2568: 0, 2569: 0, 2570: 0, 2571: 0, 2572: 0, 2573: 0, 2574: 0, 2575: 0, 2576: 0, 2577: 0, 2578: 0, 2579: 0, 2580: 0, 2581: 0, 2582: 0, 2583: 0, 2584: 0, 2585: 0, 2586: 0, 2587: 0, 2588: 0, 2589: 0, 2590: 0, 2591: 0, 2592: 1, 2593: 12, 2594: 21, 2595: 0, 2596: 0, 2597: 0, 2598: 0, 2599: 0, 2600: 0, 2601: 0, 2602: 0, 2603: 0, 2604: 0, 2605: 0, 2606: 0, 2607: 0, 2608: 0, 2609: 0, 2610: 0, 2611: 0, 2612: 0, 2613: 0, 2614: 0, 2615: 0, 2616: 0, 2617: 0, 2618: 0, 2619: 0, 2620: 0, 2621: 0, 2622: 0, 2623: 0, 2624: 0, 2625: 0, 2626: 0, 2627: 0, 2628: 0, 2629: 0, 2630: 0, 2631: 0, 2632: 0, 2633: 0, 2634: 0, 2635: 0, 2636: 0, 2637: 0, 2638: 0, 2639: 0, 2640: 2, 2641: 12, 2642: 0, 2643: 0, 2644: 0, 2645: 0, 2646: 0, 2647: 0, 2648: 0, 2649: 0, 2650: 0, 2651: 0, 2652: 0, 2653: 0, 2654: 0, 2655: 0, 2656: 0, 2657: 0, 2658: 0, 2659: 0, 2660: 0, 2661: 0, 2662: 0, 2663: 0, 2664: 0, 2665: 0, 2666: 0, 2667: 0, 2668: 0, 2669: 0, 2670: 0, 2671: 0, 2672: 0, 2673: 0, 2674: 0, 2675: 0, 2676: 0, 2677: 0, 2678: 0, 2679: 0, 2680: 0, 2681: 0, 2682: 0, 2683: 0, 2684: 0, 2685: 0, 2686: 0, 2687: 0, 2688: 0, 2689: 0, 2690: 0, 2691: 0, 2692: 0, 2693: 0, 2694: 0, 2695: 0, 2696: 0, 2697: 0, 2698: 0, 2699: 0, 2700: 0, 2701: 0, 2702: 0, 2703: 0, 2704: 0, 2705: 0, 2706: 0, 2707: 0, 2708: 0, 2709: 0, 2710: 0, 2711: 0, 2712: 0, 2713: 0, 2714: 0, 2715: 0, 2716: 0, 2717: 0, 2718: 0, 2719: 0, 2720: 0, 2721: 0, 2722: 0, 2723: 0, 2724: 0, 2725: 0, 2726: 0, 2727: 0, 2728: 0, 2729: 0, 2730: 0, 2731: 0, 2732: 0, 2733: 0, 2734: 0, 2735: 0, 2736: 0, 2737: 0, 2738: 0, 2739: 0, 2740: 0, 2741: 0, 2742: 0, 2743: 0, 2744: 0, 2745: 0, 2746: 0, 2747: 0, 2748: 0, 2749: 0, 2750: 0, 2751: 0, 2752: 0, 2753: 0, 2754: 0, 2755: 0, 2756: 0, 2757: 0, 2758: 0, 2759: 0, 2760: 0, 2761: 0, 2762: 0, 2763: 0, 2764: 0, 2765: 0, 2766: 0, 2767: 0, 2768: 0, 2769: 0, 2770: 0, 2771: 0, 2772: 0}
    Dict={'Count':CountData}
    ExitList=RetrunLatLonGrid(GridUTMpath=PathFileGridUTM,CountData=Dict,Letter=Letter,Number=Number)
    # print(ExitList.keys())
    # b=input("Halt")
    GeograpJSON=CreateGridObjProperties(DictCoords=ExitList,EPSGname="4326",Name=Agency,Table=Dict)
    # print(GeograpJSON)
    WriteToJsonFile(Text=GeograpJSON,Path=PathFileGridExit)


if __name__ == "__main__":

    PathFileGridUTM=r"/mnt/e/GitHub/CAMMM-Tool_1.3/SampleData/TESSSSt3.geojson"
    PathStopsGeojson=r"/mnt/e/GitHub/CAMMM-Tool_1.3/EXAMPLES_GEOJSON/Temp.geojson"
    # PathStopsGeojson=r"/mnt/e/GitHub/CAMMM-Tool_1.3/EXAMPLES_GEOJSON/stm_arrets_sig_32618.shp"
    PathFileGridExit=r"/mnt/e/GitHub/CAMMM-Tool_1.3/SampleData/NewGrid.geojson"
    PathTrip="/mnt/e/GitHub/CAMMM-Tool_1.3/SampleData/MTL_gtfs_RAW/trips.txt"
    PathShape="/mnt/e/GitHub/CAMMM-Tool_1.3/SampleData/MTL_gtfs_RAW/shapes.txt"
    Pathroute="/mnt/e/GitHub/CAMMM-Tool_1.3/SampleData/MTL_gtfs_RAW/routes.txt"
    PathStopsCSV="/mnt/e/GitHub/CAMMM-Tool_1.3/SampleData/MTL_gtfs_RAW/stops.txt"

    TransformStopsCsvToGeoJson(PathStopsCSV,PathStopsGeojson,Agency="STM")
    
    GetStopDensity(PathFileGridUTM=PathFileGridUTM,PathStops=PathStopsGeojson,PathFileGridExit=PathFileGridExit,PathTrip=PathTrip,PathShape=PathShape,Pathroute=Pathroute,Agency="STM")
    print("..........fin.............")

