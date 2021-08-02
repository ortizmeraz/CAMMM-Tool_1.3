# import Calculations
# import math
# import decimal
# decimal.getcontext().prec = 10





# Base1=[11565.251,418765.782]
# Base2=[26548.125,886547.348]

# BaseOhCoords=[11565.251,418765.782,26548.125,886547.348]
# ListCoords=[]
# Tup1Coord=[]
# for i in range(1000000):
#    ListCoords.append(BaseOhCoords) 
#    Tup1Coord.append((Base1,Base2))
# # print(Tup1Coord)

# print("Start C")
# for Di in ListCoords:
#     F=Calculations.CalcDistance(Di[0],Di[1],Di[2],Di[3])

# print("End C")


# print("Start Python")
# for ge in Tup1Coord:
#     G=Distance(P1=ge[0],P2=ge[1])

# print("End Python")

# B=Distance(P1=(0.0,0.0),P2=(10.0,10.0))
# print("Calculation on P",B)

# F=Calculations.CalcDistance(0.0,0.0,10.0,10.0)
# print("Calculation on C",F)

# G= Calculations.SumTest(11.11111,22.22222)
# print(G)

# s1=decimal.Decimal(11.11)
# s2=decimal.Decimal(22.22)

# G= Calculations.SumTest(11.11,22.22)
# print("C def",G)


# G1= Calculations.SumTest(s1,s2)
# print("decimal.Decimal",G1)

# G2=11.11+22.22
# print("Bare metal",G2)


import pyproj
import utm
import datetime 

def ConvertToUTM(lat,lon):
    import warnings
    warnings.filterwarnings("ignore")
    Zone=int((float(lon)/6)+31)
    if float(lat)>0:
        Val_EPSG="epsg:326"+str(Zone)
    elif float(lat)<0:
        Val_EPSG="epsg:325"+str(Zone)
    proj_wgs84 = pyproj.Proj(init="epsg:4326")
    proj_utm = pyproj.Proj(init=str(Val_EPSG))
    x, y = pyproj.transform(proj_wgs84, proj_utm, lon, lat)
    # print("proj_wgs84",type(proj_wgs84))
    # print("proj_utm",type(proj_utm))
    # print("X",type(x))
    # print("Y",type(y))
    # print("Val_EPSG",type(Val_EPSG))
    return x,y,Val_EPSG

# print("************************************************"*3)
# ct1 = datetime.datetime.now()
# print("Start time:-", ct1)
# x,y,Val_EPSG=ConvertToUTM(lat=51.2562,lon=37.5468)
# print("x,y,Val_EPSG",x,y,Val_EPSG)
# ct2 = datetime.datetime.now()
# print("current time:-", ct2)
# print("Delta",ct2-ct1)

# print("************************************************"*3)


# ct1 = datetime.datetime.now()
# print("Start time:-", ct1)
# CoordUtm=utm.from_latlon(51.2562, 37.5468)
# print("CoordUtm",CoordUtm)
# ct2 = datetime.datetime.now()
# print("current time:-", ct2)
# print("Delta",ct2-ct1)

# if CoordUtm[0]==x:
#     print("X Is the same")

# if CoordUtm[1]==y:
#     print("Y Is the same")


# print(CoordUtm[0],x,CoordUtm[0]-x)
# print(CoordUtm[1],y,CoordUtm[1]-y)

# print(utm.to_latlon(CoordUtm[0], CoordUtm[1], CoordUtm[2], CoordUtm[3]))


CoordUtm=list(utm.from_latlon(51.2562, 37.5468))
print(CoordUtm,type(CoordUtm))
