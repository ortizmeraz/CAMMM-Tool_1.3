#example_cython.pyx
import math
import pyproj


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


cpdef float ConvertToUTM(float lat,float lon):
    print("lat",lat,type(lat))
    print("lon",lon,type(lon))
    cdef float x
    cdef float y
    cdef str Val_EPSG = "epsg:32"

    cdef int Zone
    cdef str TextZone

    import warnings
    warnings.filterwarnings("ignore")
    Zone=int((float(lon)/6)+31)
    TextZone=str(Zone)
    if float(lat)>0:
        Val_EPSG=Val_EPSG+"6"+TextZone
    elif float(lat)<0:
        Val_EPSG=Val_EPSG+"5"+TextZone
    print ("Val_EPSG",Val_EPSG)

    proj_wgs84 = pyproj.Proj(init="epsg:4326")
    proj_utm = pyproj.Proj(init=str(Val_EPSG))
    print("Projections ready")
    x, y = pyproj.transform(proj_wgs84, proj_utm, lon, lat)

    return x,y,Val_EPSG