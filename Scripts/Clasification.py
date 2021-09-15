import csv 
import jenkspy 
import statistics
import numpy as np
import math
import datetime
import utm

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


def RotatedCoords(XDistnace,YDistnace,RAngle):
    xR=(XDistnace*math.cos(RAngle))+(YDistnace*math.sin(RAngle))
    yR=((-1*XDistnace)*math.sin(RAngle))+(YDistnace*math.cos(RAngle))
    return xR,yR


def CalculateRotatedGrid(Angle,Distnace,StartX,StartY,NumCellX,NumCellY):
    RAngle=math.radians(Angle)
    GridList=[]
    # NumCellY+=1
    for iY in range(NumCellY):
        # print("\n\n\nY:",iY)
        DiY=iY+1
        for iX in range(0,NumCellX):
            DiX=iX+1
            # print("||X:",iX)
            # Q1 coords
            X1Distnace=StartX+(iX*Distnace)
            Y1Distnace=StartY+(iY*Distnace)
            # print(end="\t"*1)
            # print("Q1xD",X1Distnace,"Q1yD",Y1Distnace,end="\t")
            # Q2 coords
            X2Distnace=StartX+(DiX*Distnace)
            Y2Distnace=StartY+(iY*Distnace)
            # print("X:",iX,end="\t")
            # print(end="\t"*1)
            # print("Q2xD",X2Distnace,"Q2yD",Y2Distnace,end="\t")
            # Q3 coords
            X3Distnace=StartX+(DiX*Distnace)
            Y3Distnace=StartY+(DiY*Distnace)
            # print("X:",iX,end="\t")
            # print(end="\t"*1)
            # print("Q3xD",X3Distnace,"Q3yD",Y3Distnace,end="\t")
            # Q4 coords
            X4Distnace=StartX+(iX*Distnace)
            Y4Distnace=StartY+(DiY*Distnace)
            # print("X:",iX,end="\t")
            # print(end="\t"*1)
            # print("Q4xD",X4Distnace,"Q4yD",Y4Distnace,end="\t")
            
            X1Distnace=X1Distnace+StartX
            Y1Distnace=Y1Distnace+StartY
            X2Distnace=X2Distnace+StartX
            Y2Distnace=Y2Distnace+StartY
            X3Distnace=X3Distnace+StartX
            Y3Distnace=Y3Distnace+StartY
            X4Distnace=X4Distnace+StartX
            Y4Distnace=Y4Distnace+StartY


            x1R,y1R=RotatedCoords(XDistnace=X1Distnace,YDistnace=Y1Distnace,RAngle=RAngle)
            x2R,y2R=RotatedCoords(XDistnace=X2Distnace,YDistnace=Y2Distnace,RAngle=RAngle)
            x3R,y3R=RotatedCoords(XDistnace=X3Distnace,YDistnace=Y3Distnace,RAngle=RAngle)
            x4R,y4R=RotatedCoords(XDistnace=X4Distnace,YDistnace=Y4Distnace,RAngle=RAngle)

            # print(x1R,y1R,x2R,y2R,x3R,y3R,x4R,y4R)
            GridList.append([[x1R,y1R],[x2R,y2R],[x3R,y3R],[x4R,y4R]])
    return GridList
    

def CreateGridObj(ListCoords):
    Start="{    \"type\": \"FeatureCollection\",    \"features\": ["
    End="]}"
    Header="            ,\"geometry\": {                \"type\": \"Polygon\",                \"coordinates\": [                    [ "
    Footer="                ]            }        },"

    ExitText=""
    ExitText+=Start
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
    VectorList=[]
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
            # 'shape_pt_sequence':
            else:
                DataShapes[line[0]]={}
                DataShapes[line[0]][line[3]]={'shape_pt_lat':line[1],'shape_pt_lon':line[2]}
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
        print("Angle",Alfa)

    Here you have the angle, still need to get the heading


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

# Break=QuantilesBare(Path)
# # print("QuantilesBare",Break)
# GridCoords=CalculateRotatedGrid(Angle=45,Distnace=1,StartX=0,StartY=0,NumCellX=20,NumCellY=20)
# print(type(GridCoords))
# TextJSON=CreateGridObj(ListCoords=GridCoords)
# print(TextJSON)
# WriteToJsonFile(Text=TextJSON,Path=r"E:\GitHub\Test.geojson")


PathTrip="/mnt/d/GitHub/CAMMM-Tool_1.3/SampleData/MTL_gtfs_RAW/trips.txt"
PathShape="/mnt/d/GitHub/CAMMM-Tool_1.3/SampleData/MTL_gtfs_RAW/shapes.txt"
Pathroute="/mnt/d/GitHub/CAMMM-Tool_1.3/SampleData/MTL_gtfs_RAW/routes.txt"
GetAngle(PathShapes=PathShape,PathTrips=PathTrip,PathRoutes=Pathroute)
print("..........fin.............")

