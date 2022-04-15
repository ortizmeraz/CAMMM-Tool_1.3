import math
import decimal
decimal.getcontext().prec = 10


class PlotingData:
    def __init__(self, ShapeFiles, Titles):
        self.ShapeFiles = ShapeFiles
        self.Titles = Titles

class Paths:
    def __init__(self,ProcessFolder):
        self.ProcessFolder=ProcessFolder

    def TempoFolder():
        return r"E:\\OneDrive - Concordia University - Canada\\RA-CAMM\\Software\\CAMMM-Soft-Tools\\Operational\\"

class DataBucket:
    def __init__(self,name):
        self.name


class BusStop:
    def __init__(self,Id="",CoordX=0,CoordY=0,Epsg="",Routes=[],Cluster=[],SuperNode=0):
        self.Id=Id
        self.CoordX=CoordX
        self.CoordY=CoordY
        self.Epsg=Epsg
        self.Routes=[]
        self.Cluster=[]
        self.SuperNode=SuperNode

class Station:
    def __init__(self,Id="",CoordX=0,CoordY=0,Epsg="",Routes=[],Cluster=[],System=[]):
        self.Id=Id
        self.CoordX=CoordX
        self.CoordY=CoordY
        self.Epsg=""
        self.Routes=[]
        self.Cluster=[]
        self.System=[]

class ClassDataCentroid(DataBucket):
    def __init__(self, ShapeFiles, Titles,CityArea,Ratio,):
        self.ShapeFiles=ShapeFiles
        self.Titles=Titles
        self.CityArea=CityArea
        self.Ratio=Ratio
       


class CentroidData(PlotingData):
    def __init__(self, ShapeFiles, Titles):
        super().__init__(ShapeFiles, Titles)
        self.graduationyear = 2019

class Coord:
    def __init__(self,X,Y):
        self.X = X
        self.Y = Y
        

class Station(Coord):
    def __init__(self,Id,Type,Lines,Coords,RawDirectConections,RawIndirectConnections):
        self.Id = Id
        self.Type = Type
        self.Lines = Lines
        self.Coords = Coords
        self.RawDirectConections = RawDirectConections
        self.RawIndirectConnections = RawIndirectConnections
        
class Line():
    def __init__(self,Type,Name,NumberStations,AverageStationDistance,Lenght,ConectingLines):
        self.Type
        self.Name
        self.NumberStations
        self.AverageStationDistance
        self.Lenght
        self.ConectingLines


class  CriteriaData():
    def __init__(self,MinDistMask,MaxDistMask,NameFieldLines,NameFieldStop,NeigbourDistance,AdjacentDistance):
        self.MinDistMask
        self.MaxDistMask
        self.NameFieldLines
        self.NameFieldStop
        self.NeigbourDistance
        self.AdjacentDistance

# B12345=BusStop(Id=1,Lines="2",Coords=Coord(X=10,Y=20))


class Street:
    def __init__(self,Name="",CoordXA=0,CoordYA=0,CoordXB=0,CoordYB=0,Segments=[]):
        self.Name=Name
        self.CoordXA=CoordXA
        self.CoordYA=CoordYA
        self.CoordXB=CoordXB
        self.CoordYB=CoordYB
        self.Segments=[]



class Segment:
    import math
    def __init__(self, CoordXA=0,CoordXB=0,CoordYA=0,CoordYB=0):
        self.CoordXA=CoordXA
        self.CoordXB=CoordXB
        self.CoordYA=CoordYA
        self.CoordYB=CoordYB
    def Dist(self):
        return math.sqrt(((self.CoordXB-self.CoordXA)**2)+((self.CoordYB-self.CoordYA)**2))
    def M(self):
        return (self.CoordYB-self.CoordYA)/(self.CoordXB-self.CoordXA)
    def B(self):
        return self.CoordYB-((self.CoordYB-self.CoordYA)/(self.CoordXB-self.CoordXA)*self.CoordXB)

class Point:
    """ Create a new Point, at coordinates x, y """

    def __init__(self, x=0, y=0):
        """ Create a new point at x, y """
        self.x = x
        self.y = y

    def distance_from_origin(self):
        """ Compute my distance from the origin """
        return ((self.x ** 2) + (self.y ** 2)) ** 0.5

    
if __name__ == "__main__":

    # D=Segment(64355340,54353100,1014254,105424860)
    D=Segment()
    D.CoordXA=64355340
    D.CoordXB=54353100
    D.CoordYA=1014254
    D.CoordYB=105424860
    print("Dist:",D.Dist())
    print("M:",D.M())
    print("B:",D.B())
    Dict={}
    Dict[D]=0
    # St=StreetSegment
    # St.CoordX0=0
    # St.CoordX1=10
    # St.CoordY0=0
    # St.CoordY1=10
    # print(St.DistancePoints())
    # St.CalcDist()
    # # St.Dist=0
    # print(St.Dist)
    # P=Point(10,10)
    # print(P.distance_from_origin())
    # print(Paths.TempoFolder())

# class Street():
#     def __init__(self,Name,Segments):