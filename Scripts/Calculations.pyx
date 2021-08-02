#example_cython.pyx
import math

cpdef float CalcDistance(float P1x, float P1y, float P2x, float P2y):
    cdef float PX
    cdef float PY
    PX=(P2x-P1x)*(P2x-P1x)
    PY=(P2y-P1y)*(P2y-P1y)
	
    return math.sqrt(PX+PY)
   

cpdef float GetMediumPoint(float P1x, float P1y, float P2x, float P2y):

    cdef float P3x
    cdef float P3y

    P3x=(P1x+P2x)/2
    P3y=(P1y+P2y)/2
    
    return P3x,P3y


cpdef float SumTest(float A, float B):
    cdef float Sum
    Sum = A + B
    return Sum


cpdef float MultTest(float A, float B):
    cdef float Sum
    Sum = A * B
    return Sum



cpdef float AveragCoords(list inListStops):
    float Xav
    float Yav
    list XcoordList=[]
    list YcoordList=[]
    for Stop in inListStops:
        XcoordList.append(Stop.CoordX)
        YcoordList.append(Stop.CoordY)
    Xav=MenFunc(inList=XcoordList)
    Yav=MenFunc(inList=YcoordList)
    return Xav,Yav


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
                # Dist=Distance(P1=P1,P2=P2)
                Dist=Calculations.CalcDistance(P1[0],P1[1],P2[0],P2[1])

                ListDistance.append(Dist)
    return sum(ListDistance)/len(ListDistance),len(ListDistance)
