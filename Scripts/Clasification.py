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
    

def CalculateRotatedGrid(Angle,Distnace,StartX,StartY,NumCellX,NumCellY):
    for iY in range(NumCellY):
        print("\n\n\nY:",iY)
        DiY=iY+1
        for iX in range(0,NumCellX):
            DiX=iX+1
            print("X:",iX,end="\t")
            # Q1 coords
            XDistnace=StartX+(DiX*Distnace)
            YDistnace=StartY+(DiY*Distnace)

    RAngle=math.radians(Angle)
    XDistnace=Distnace+StartX
    YDistnace=Distnace+StartY
    xR=(XDistnace*math.cos(RAngle))+(YDistnace*math.sin(RAngle))
    yR=((-1*XDistnace)*math.sin(RAngle))+(YDistnace*math.cos(RAngle))

    print(xR,yR)



#   Q4  Q3
#   Q1  Q2
#
# Path=r"D:\GitHub\CAMMM-Tool_1.3\SampleData\Random\SampleData.csv"
# Lists=chunkIt(Path, 5)
# QuantilesBare(Path)
# print("chunkIt",Lists)

# Break=QuantilesBare(Path)
# print("QuantilesBare",Break)
CalculateRotatedGrid(Angle=45,Distnace=500,StartX=0,StartY=0,NumCellX=10,NumCellY=10)

print("..........fin.............")

