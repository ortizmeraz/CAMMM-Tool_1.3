import csv 
import jenkspy 
import statistics
import numpy as np
import math
import datetime

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
    print("Min",min(Data))
    print("1 D",StDev)
    print("1 D",StDev*2)
    print("Max",max(Data))




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
    print("max",max(Data))
    print("Min",min(Data))

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
# print("QuantilesBare",Break)
GridCoords=CalculateRotatedGrid(Angle=45,Distnace=1,StartX=0,StartY=0,NumCellX=20,NumCellY=20)
print(type(GridCoords))
TextJSON=CreateGridObj(ListCoords=GridCoords)
print(TextJSON)
WriteToJsonFile(Text=TextJSON,Path=r"E:\GitHub\Test.geojson")
print("..........fin.............")

