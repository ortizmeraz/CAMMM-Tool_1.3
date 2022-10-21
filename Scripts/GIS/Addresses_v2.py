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



def Main(PathNodes):
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
        Type=record[9]
        FiD=record[0]



    params= {'INPUT':'/home/omar/CAMMM/Nodes/Nodes_Full_UTM.gpkg',
    'FIELD':'fid',
    'OPERATOR':0,
    'VALUE':str(FiD),
    'OUTPUT':'/home/omar/CAMMM/Porcessing/Node/Node_'+FullNum(x=int(FiD),TotalX=R)+'.gpkg'}
    processing.run("native:extractbyattribute",params)


    processing.run("native:buffer", {'INPUT':'/home/omar/CAMMM/Porcessing/Node/Node_'+FullNum(x=int(FiD),TotalX=R)+'.gpkg',
    'DISTANCE':BufferSize[Type],
    'SEGMENTS':5,
    'END_CAP_STYLE':0,
    'JOIN_STYLE':0,'MITER_LIMIT':2,
    'DISSOLVE':False,
    'OUTPUT':'/home/omar/CAMMM/Porcessing/Buffer/Buffer_'+FullNum(x=int(FiD),TotalX=R)+'.gpkg'})



    processing.run("native:clip", {'INPUT':'/home/omar/CAMMM/Addresses/Addresses.gpkg',
    'OVERLAY':'/home/omar/CAMMM/Porcessing/Buffer/Buffer_'+FullNum(x=int(FiD),TotalX=R)+'.gpkg',
    'OUTPUT':'/home/omar/CAMMM/Porcessing/Clip/Clip_'+FullNum(x=int(FiD),TotalX=R)+'.gpkg'})

    params={'INPUT':'/home/omar/CAMMM/Streets/Streets.gpkg',
    'STRATEGY':0,
    'DIRECTION_FIELD':'',
    'VALUE_FORWARD':'',
    'VALUE_BACKWARD':'',
    'VALUE_BOTH':'',
    'DEFAULT_DIRECTION':2,
    'SPEED_FIELD':'',
    'DEFAULT_SPEED':50,
    'TOLERANCE':0,
    'START_POINTS':'/home/omar/CAMMM/Porcessing/Clip/Clip_'+FullNum(x=int(FiD),
    TotalX=R)+'.gpkg',
    'END_POINT':'602837.308377,5040905.975071 [EPSG:32618]',
    'OUTPUT':'/home/omar/CAMMM/Porcessing/Distances/Dist_Addresses_'+FullNum(x=int(FiD),TotalX=R)+'.gpkg'}
    processing.run("native:shortestpathlayertopoint", params)



BasePath=r"/home/omar/CAMMM/Nodes/Nodes_Full_UTM.gpkg"
Main(PathNodes=BasePath)