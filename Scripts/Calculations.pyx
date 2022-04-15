#example_cython.pyx
import math
import jenkspy 

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

cdef float MenFunc(list inList):
   return sum(inList)/len(inList)


cpdef float AveragCoords(list inListStops):
    cdef float Xav
    cdef float Yav
    cdef list XcoordList=[]
    cdef list YcoordList=[]
    for Stop in inListStops:
        XcoordList.append(Stop.CoordX)
        YcoordList.append(Stop.CoordY)
    Xav=MenFunc(inList=XcoordList)
    Yav=MenFunc(inList=YcoordList)
    return Xav,Yav

cpdef NaturalBreaksNumpyList(list Data, int Classess):
    cdef list breaks=[]
    breaks = jenkspy.jenks_breaks(Data, nb_class=Classess)
    return breaks



cpdef ListToText(list DATA):
    cdef str Text
    Text=""
    cdef str TextLine
    for line in DATA:
        TextLine=','.join(line)
        Text=Text+TextLine+"\n"
    return Text