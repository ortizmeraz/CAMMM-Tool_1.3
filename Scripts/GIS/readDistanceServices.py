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

layer = iface.activeLayer()
R=0

for i in layer.getFeatures():
    R+=1
print(R)

idx=0
for i in layer.getFeatures():
    idx+=1
    param={ 'DEFAULT_DIRECTION' : 2,
     'DEFAULT_SPEED' : 50,
     'DIRECTION_FIELD' : '',
     'END_POINTS' : 'F:\\OneDrive - Concordia University - Canada\\RA-CAMM\\Density Calculations\\NetworkAnalysis\\ClippedAddresses\\ClippedAddresses.gpkg|layername=ClippedAddresses',
     'INPUT' : 'F:\\OneDrive - Concordia University - Canada\\RA-CAMM\\Density Calculations\\NetworkAnalysis\\MontrealStreeets.gpkg|layername=MontrealStreeets',
     'OUTPUT' : 'F:/OneDrive - Concordia University - Canada/RA-CAMM/Density Calculations/NetworkAnalysis/SampleResults/Samp'+FullNum(x=idx,TotalX=R)+'.gpkg',
     'SPEED_FIELD' : '',
     'START_POINT' : '611589.809372, 5039940.392722 [EPSG:32618]',
     'STRATEGY' : 0,
     'TOLERANCE' : 0,
     'VALUE_BACKWARD' : '',
     'VALUE_BOTH' : '',
     'VALUE_FORWARD' : '' }
    print(param)

    
#processing.run("native:shortestpathpointtolayer",param)
##################################################################################################


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

layer = iface.activeLayer()
R=0

for i in layer.getFeatures():
    R+=1
print(R)

idx=0
for i in layer.getFeatures():
    idx+=1
    if idx < 10:
        geom = i.geometry()
        PX=geom.asPoint().x()
        PY=geom.asPoint().y()
        Coords=str(PX)+','+str(PY)+' [EPSG:32618]'
        # print(PX,PY)

        param={ 'DEFAULT_DIRECTION' : 2,
        'DEFAULT_SPEED' : 50,
        'DIRECTION_FIELD' : '',
        'END_POINTS' : 'F:\\OneDrive - Concordia University - Canada\\RA-CAMM\\Density Calculations\\NetworkAnalysis\\ClippedAddresses\\ClippedAddresses.gpkg',
        'INPUT' : 'F:\\OneDrive - Concordia University - Canada\\RA-CAMM\\Density Calculations\\NetworkAnalysis\\MontrealStreeets.gpkg',
        'OUTPUT' : 'F:/OneDrive - Concordia University - Canada/RA-CAMM/Density Calculations/NetworkAnalysis/SampleResults/Samp'+FullNum(x=idx,TotalX=R)+'.gpkg',
        'SPEED_FIELD' : '',
        'START_POINT' : Coords,
        'STRATEGY' : 0,
        'TOLERANCE' : 0,
        'VALUE_BACKWARD' : '',
        'VALUE_BOTH' : '',
        'VALUE_FORWARD' : '' }

        print(param)
        processing.run("native:shortestpathpointtolayer",param)
    else:
        break


##################################################################################################################################################################################
##################################################################################################################################################################################
##################################################################################################################################################################################
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



Buffersize={"N":400,"S":800}
layer = iface.activeLayer()
R=0

for i in layer.getFeatures():
    R+=1
print("Total Features",R)

idx=0
for i in layer.getFeatures():
    idx+=1
    if idx in range(1000,2):
        SuperNode=i['SuperNode']
        print(SuperNode,Buffersize[SuperNode])

        print("extractbyattribute")
        paramsExtract={'INPUT':'F:\\OneDrive - Concordia University - Canada\\RA-CAMM\\Density Calculations\\NetworkAnalysis\\Montreal_Nodes.gpkg|layername=Montreal_Nodes',
        'FIELD':'fid',
        'OPERATOR':0,
        'VALUE':str(idx),
        'OUTPUT':'F:/OneDrive - Concordia University - Canada/RA-CAMM/Density Calculations/Service_Calculations/TempNode/Node'+FullNum(x=idx,TotalX=R)+'.gpkg'}
        processing.run("native:extractbyattribute", paramsExtract)


        print("buffer")
        paramsBuf= {'INPUT':'F:\\OneDrive - Concordia University - Canada\\RA-CAMM\\Density Calculations\\Service_Calculations\\TempNode\\Node'+FullNum(x=idx,TotalX=R)+'.gpkg',
        'DISTANCE':Buffersize[SuperNode],
        'SEGMENTS':5,
        'END_CAP_STYLE':0,
        'JOIN_STYLE':0,
        'MITER_LIMIT':2,
        'DISSOLVE':False,
        'OUTPUT':'F:\OneDrive - Concordia University - Canada\RA-CAMM\Density Calculations\Service_Calculations/TempBuff/Buffer'+FullNum(x=idx,TotalX=R)+'.gpkg'}
        processing.run("native:buffer", paramsBuf)


        print("clip")
        paramsClip={'INPUT':'F:/OneDrive - Concordia University - Canada/RA-CAMM/Density Calculations/Service/Services_wCat_UTMwgs84/Services_wCat_UTMwgs84.gpkg',
        'OVERLAY':'F:/OneDrive - Concordia University - Canada/RA-CAMM/Density Calculations/Service_Calculations/TempBuff/Buffer'+FullNum(x=idx,TotalX=R)+'.gpkg',
        'OUTPUT':'F:/OneDrive - Concordia University - Canada/RA-CAMM/Density Calculations/Service_Calculations/TempServices/TempServices'+FullNum(x=idx,TotalX=R)+'.gpkg'}
        processing.run("native:clip", paramsClip)


        geom = i.geometry()
        PX=geom.asPoint().x()
        PY=geom.asPoint().y()
        Coords=str(PX)+','+str(PY)+' [EPSG:32618]'
        print(PX,PY)

        param={ 'DEFAULT_DIRECTION' : 2,
        'DEFAULT_SPEED' : 50,
        'DIRECTION_FIELD' : '',
        'END_POINTS' : 'F:\\OneDrive - Concordia University - Canada\\RA-CAMM\\Density Calculations\\Service_Calculations\\TempServices\\TempServices'+FullNum(x=idx,TotalX=R)+'.gpkg',
        'INPUT' : 'F:\\OneDrive - Concordia University - Canada\\RA-CAMM\\Density Calculations\\NetworkAnalysis\\MontrealStreeets.gpkg',
        'OUTPUT' : 'E:/GitHub/CAMMM-Tool_1.3/Results/CSV_Results_Services/Montreal/Samp'+FullNum(x=idx,TotalX=R)+'.csv',
        'SPEED_FIELD' : '',
        'START_POINT' : Coords,
        'STRATEGY' : 0,
        'TOLERANCE' : 0,
        'VALUE_BACKWARD' : '',
        'VALUE_BOTH' : '',
        'VALUE_FORWARD' : '' }

        print(param)
        processing.run("native:shortestpathpointtolayer",param)


idx=0
for i in layer.getFeatures():
    idx+=1
    if idx > 10:

        Path='F:/OneDrive - Concordia University - Canada/RA-CAMM/Density Calculations/NetworkAnalysis/SampleCSV/Samp'+FullNum(x=idx,TotalX=R)+'.csv'
        print(Path)

        # Tablelayer = QgsProject.instance().mapLayersByName("myLayerName")[0]
        Name="Sample"+FullNum(x=idx,TotalX=R)
        SampleLayer = iface.addVectorLayer(Path, Name, 'ogr')
        for j in SampleLayer.getFeatures():
            print(j['fid'])
    else:
        break