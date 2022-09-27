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
print(R)

idx=0
for i in layer.getFeatures():
    idx+=1
    if idx in range(3500,60000):
        SuperNode=i['SuperNode']
        print(SuperNode,Buffersize[SuperNode])

        paramsExtract={'INPUT':'F:\\OneDrive - Concordia University - Canada\\RA-CAMM\\Density Calculations\\NetworkAnalysis\\Montreal_Nodes.gpkg|layername=Montreal_Nodes',
        'FIELD':'fid',
        'OPERATOR':0,
        'VALUE':str(idx),
        'OUTPUT':'F:/OneDrive - Concordia University - Canada/RA-CAMM/Density Calculations/NetworkAnalysis/SampleResults/TempNode/Node'+FullNum(x=idx,TotalX=R)+'.gpkg'}
        processing.run("native:extractbyattribute", paramsExtract)

        paramsBuf= {'INPUT':'F:\\OneDrive - Concordia University - Canada\\RA-CAMM\\Density Calculations\\NetworkAnalysis\\SampleResults\\TempNode\\Node'+FullNum(x=idx,TotalX=R)+'.gpkg',
        'DISTANCE':Buffersize[SuperNode],
        'SEGMENTS':5,
        'END_CAP_STYLE':0,
        'JOIN_STYLE':0,
        'MITER_LIMIT':2,
        'DISSOLVE':False,
        'OUTPUT':'F:/OneDrive - Concordia University - Canada/RA-CAMM/Density Calculations/NetworkAnalysis/SampleResults/TempBuff/Buffer'+FullNum(x=idx,TotalX=R)+'.gpkg'}
        processing.run("native:buffer", paramsBuf)

        paramAddress= {'INPUT':'F:\\OneDrive - Concordia University - Canada\\RA-CAMM\\Density Calculations\\Addresses\\Montreal_Addresses_32618.gpkg',
        'OVERLAY':'F:/OneDrive - Concordia University - Canada/RA-CAMM/Density Calculations/NetworkAnalysis/SampleResults/TempBuff/Buffer'+FullNum(x=idx,TotalX=R)+'.gpkg',
        'OUTPUT':'F:/OneDrive - Concordia University - Canada/RA-CAMM/Density Calculations/NetworkAnalysis/SampleResults/TempAddresses/TempAddresses'+FullNum(x=idx,TotalX=R)+'.gpkg'}
        processing.run("native:clip", paramAddress)

        geom = i.geometry()
        PX=geom.asPoint().x()
        PY=geom.asPoint().y()
        Coords=str(PX)+','+str(PY)+' [EPSG:32618]'
        # print(PX,PY)

        param={ 'DEFAULT_DIRECTION' : 2,
        'DEFAULT_SPEED' : 50,
        'DIRECTION_FIELD' : '',
        'END_POINTS' : 'F:\\OneDrive - Concordia University - Canada\\RA-CAMM\\Density Calculations\\NetworkAnalysis\\SampleResults\\TempAddresses\\TempAddresses'+FullNum(x=idx,TotalX=R)+'.gpkg',
        'INPUT' : 'F:\\OneDrive - Concordia University - Canada\\RA-CAMM\\Density Calculations\\NetworkAnalysis\\MontrealStreeets.gpkg',
        'OUTPUT' : 'E:/GitHub/CAMMM-Tool_1.3/Results/CSV Montreal/Samp'+FullNum(x=idx,TotalX=R)+'.csv',
        'SPEED_FIELD' : '',
        'START_POINT' : Coords,
        'STRATEGY' : 0,
        'TOLERANCE' : 0,
        'VALUE_BACKWARD' : '',
        'VALUE_BOTH' : '',
        'VALUE_FORWARD' : '' }

        print(param)
        processing.run("native:shortestpathpointtolayer",param)

