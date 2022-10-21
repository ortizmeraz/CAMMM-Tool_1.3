

def FullNum(x:int,TotalX:int)->str:
    StrTot=str(TotalX)
    Top=1
    Exit=str(x)
    for i in StrTot:
        Top*=10
    Diff=Top-x
    for i in str(Diff):
        Exit='0'+Exit
    return (Exit)



def Main(PathNodes,ProcPath):
    BufferSize={"Cluster":400,"Hub":800}
    NodeLayers=QgsVectorLayer(PathNodes,"ogr")

    R=0
    for i in NodeLayers.getFeatures():
        R+=1

    Count=0
    Stopper=False
    for i in NodeLayers.getFeatures():
        Count+=1
        if Stopper:
            if Count>10:
                break

        record=i.attributes()
        print(record)
        print(record[9])
        FiD=record[0]

        print("extractbyattribute")
        paramsExtract={'INPUT':'C:\\Users\\Omar\\Desktop\\CAMMMM\\NewNodes\\Montreal_Nodes.gpkg|layername=Montreal_Nodes',
        'FIELD':'fid',
        'OPERATOR':0,
        'VALUE':'1',
        'OUTPUT':'C:/Users/Omar/Desktop/CAMMMM/Processing/TempNode/Node'+FullNum(x=int(FiD),TotalX=R)+'.gpkg'}

        processing.run("native:extractbyattribute", paramsExtract)
        # break

        print("Creation of the buffer")
        paramsExtract={'INPUT':'C:/Users/Omar/Desktop/CAMMMM/Processing/TempNode/Node'+FullNum(x=int(FiD),TotalX=R)+'.gpkg',
        'DISTANCE':100,
        'SEGMENTS':5,
        'END_CAP_STYLE':0,
        'JOIN_STYLE':0,
        'MITER_LIMIT':2,
        'DISSOLVE':False,
        'OUTPUT':'C:/Users/Omar/Desktop/CAMMMM/Processing/Buffer/Buffer_'+FullNum(x=int(FiD),TotalX=R)+'.gpkg'}
        processing.run("native:buffer", paramsExtract)


        print("Clipp of services")
        paramExtract={'INPUT':'C:/Users/Omar/Desktop/CAMMMM/Services_wCat_UTMwgs84/Services_wCat_UTMwgs84.shp',
        'OVERLAY':'C:/Users/Omar/Desktop/CAMMMM/Processing/Buffer/Buffer_'+FullNum(x=int(FiD),TotalX=R)+'.gpkg',
        'OUTPUT':'C:/Users/Omar/Desktop/CAMMMM/Processing/Clip/Clip_'+FullNum(x=int(FiD),TotalX=R)+'.gpkg'}
        processing.run("native:clip",paramExtract )

        geom = i.geometry()
        PX=geom.asPoint().x()
        PY=geom.asPoint().y()
        Coords=str(PX)+','+str(PY)+' [EPSG:32618]'
        print(PX,PY)

        paramsExtract= {'INPUT':'C:/Users/Omar/Desktop/CAMMMM/Streets/MontrealStreeets.gpkg',
        'STRATEGY':0,
        'DIRECTION_FIELD':'',
        'VALUE_FORWARD':'',
        'VALUE_BACKWARD':'','VALUE_BOTH':'',
        'DEFAULT_DIRECTION':2,'SPEED_FIELD':'',
        'DEFAULT_SPEED':50,
        'TOLERANCE':0,
        'START_POINT':str(PX)+','+str(PY)+' [EPSG:32618]',
        'END_POINTS':'C:/Users/Omar/Desktop/CAMMMM/Processing/Clip/Clip_'+FullNum(x=int(FiD),TotalX=R)+'.gpkg',
        'OUTPUT':'C:/Users/Omar/Desktop/CAMMMM/Processing/DIstances/Services_Node_'+FullNum(x=int(FiD),TotalX=R)+'.gpkg'}

        processing.run("native:shortestpathpointtolayer",paramsExtract)


BasePath=r"C:\Users\Omar\Desktop\CAMMMM\NewNodes\Montreal_Nodes.gpkg"
ProcFolderPath=r"C:/Users/Omar/Desktop/CAMMMM/Processing"
Main(PathNodes=BasePath,ProcPath=ProcFolderPath)