#example_cython.pyx
import math

cpdef float CalcDistance(float P1x, float P1y, float P2x, float P2y):
    cdef float PX
    cdef float PY
    PX=(P2x-P1x)*(P2x-P1x)
    PY=(P2y-P1y)*(P2y-P1y)
	
    return math.sqrt(PX+PY)
   

cpdef float SumTest(float A, float B):
    cdef float Sum
    Sum = A + B
    return Sum


cpdef float MultTest(float A, float B):
    cdef float Sum
    Sum = A * B
    return Sum
