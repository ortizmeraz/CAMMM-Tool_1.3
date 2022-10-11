import os
import time

def Main(PathBusStop:str,PathMetroStation:str):
    ListOfUsedBusStops=[]
    PathBase='F:/OneDrive - Concordia University - Canada/RA-CAMMM/HubProccesing'

    BaseMetro=r'E:\\GitHub\\CAMMM-Tool_1.3\\SampleData\\GIS_Data\\Montreal_Metro_Sample.gpkg|layername=Montreal_Metro_Sample'

    BaseBuses=r'E:\\GitHub\\CAMMM-Tool_1.3\\SampleData\\GIS_Data\\Montreal_Bus_Sample.gpkg|layername=Montreal_Bus_Sample'


    UsedStops=[]
    NodeCollection={}
    BusesToUSe=[]

    BusStops_layer=QgsVectorLayer(PathBusStop,"ogr")
    print(BusStops_layer)
    for i in BusStops_layer.getFeatures():
        # print(dir(i))
        # print(type(i.attributes()))
        # print(i.attributes()[2])
        BusesToUSe.append(i.attributes()[2])

    # print(PathMetroStation)
    # b=input('.................................')

    MetroStation_layer=QgsVectorLayer(PathMetroStation,"ogr")
    for i in MetroStation_layer.getFeatures():
        PathTempMetro=PathBase+'/Operational/Metro_'+str(i.attributes()[2])+'.gpkg'
        PathTempBuffermetro=PathBase+'/Operational/Buffer_Metro_'+str(i.attributes()[2])+'.gpkg'
        PathTempClip=PathBase+'/Operational/SelectionBusStops_Metro_'+str(i.attributes()[2])+'.gpkg'
        PathTempDist=PathBase+'/Operational/DistanceBusStops_Metro_'+str(i.attributes()[2])+'.gpkg'

        #################################################################
        #################################################################
        print("StopCode:",i.attributes()[2])
        print("Extract by attribute")
        paramsExtract={'INPUT':BaseMetro,
        'FIELD':'StopCode',
        'OPERATOR':0,
        'VALUE':str(i.attributes()[2]),
        'OUTPUT':PathTempMetro}
        processing.run("native:extractbyattribute", paramsExtract)

        print("buffer")
        paramsBuf= {'INPUT':PathTempMetro,
        'DISTANCE':DistanceCat['BufferMetro'],
        'SEGMENTS':5,
        'END_CAP_STYLE':0,
        'JOIN_STYLE':0,
        'MITER_LIMIT':2,
        'DISSOLVE':False,
        'OUTPUT':PathTempBuffermetro}
        processing.run("native:buffer", paramsBuf)

        print("clip")
        paramsClip={'INPUT':PathBusStop,
        'OVERLAY':PathTempBuffermetro,
        'OUTPUT':PathTempClip}
        processing.run("native:clip", paramsClip)

        print("Distances")
        paramsDist={'INPUT':PathTempClip,
        'HUBS':PathTempMetro,
        'FIELD':'StopCode',
        'UNIT':0,
        'OUTPUT':PathTempDist}
        processing.run("qgis:distancetonearesthubpoints",paramsDist)

        Distances=QgsVectorLayer(PathTempDist,"ogr")

        if str(i.attributes()[2]) not in NodeCollection:
            NodeCollection[str(i.attributes()[2])]=[]


        for j in Distances.getFeatures():
            print(j.attributes()[23])
            if int(j.attributes()[23]) < DistanceCat['DistanceMetro']:
                print("Eureka!!!!!!!!!!")
                UsedStops.append(str(j.attributes()[2]))
                NodeCollection[str(i.attributes()[2])].append({'StopCode':str(j.attributes()[2]),'Distance':int(j.attributes()[23])})
        
    
        # time.sleep(2)
        # print("Remove")
        # os.remove(PathTempMetro)
        # os.remove(PathTempBuffermetro)
        # os.remove(PathTempClip)
        # os.remove(PathTempDist)


    # print(NodeCollection)
    for BS in BusesToUSe:
        if BS not in UsedStops:
            PathTempBuses=PathBase+'/Operational/BusStop_'+BS+'.gpkg'
            PathTempBufferBuses=PathBase+'/Operational/BusStop_Buffer_'+BS+'.gpkg'
            PathTempClipBuses=PathBase+'/Operational/BusStop_Clip_'+BS+'.gpkg'
            PathTempDistBuses=PathBase+'/Operational/BusStop_Dist_'+BS+'.gpkg'
            ###########################################################
            ###########################################################
            print(BS)
            print("StopCode:",BS)
            print("Extract by attribute")
            paramsExtract={'INPUT':BaseBuses,
            'FIELD':'StopCode',
            'OPERATOR':0,
            'VALUE':BS,
            'OUTPUT':PathTempBuses}
            processing.run("native:extractbyattribute", paramsExtract)

            print("buffer")
            paramsBuf= {'INPUT':PathTempBuses,
            'DISTANCE':DistanceCat['BufferBus'],
            'SEGMENTS':5,
            'END_CAP_STYLE':0,
            'JOIN_STYLE':0,
            'MITER_LIMIT':2,
            'DISSOLVE':False,
            'OUTPUT':PathTempBufferBuses}
            processing.run("native:buffer", paramsBuf)

            print("clip")
            paramsClip={'INPUT':PathBusStop,
            'OVERLAY':PathTempBufferBuses,
            'OUTPUT':PathTempClipBuses}
            processing.run("native:clip", paramsClip)

            print("Distances")
            paramsDist={'INPUT':PathTempClipBuses,
            'HUBS':PathTempBuses,
            'FIELD':'StopCode',
            'UNIT':0,
            'OUTPUT':PathTempDistBuses}
            processing.run("qgis:distancetonearesthubpoints",paramsDist)


            Distances=QgsVectorLayer(PathTempDistBuses,"ogr")

            if BS not in NodeCollection:
                NodeCollection[BS]=[]

            for j in Distances.getFeatures():
                print(j.attributes()[23])
                if int(j.attributes()[23]) < DistanceCat['DistanceBusStop']:
                    print("Eureka!!!!!!!!!!")
                    if int(j.attributes()[23])!=0:
                    # UsedStops.append(str(j.attributes()[2]))
                        NodeCollection[BS].append({'StopCode':str(j.attributes()[2]),'Distance':int(j.attributes()[23])})
        


        else:
            print(BS,"Used Bus Stop")
    print(NodeCollection)

    print(".........fin..........")



# if __name__ == "__main__":
#     LocalPathBusStop="E:\GitHub\CAMMM-Tool_1.3\SampleData\GIS_Data\Montreal_Bus_Sample.gpkg"
#     LocalPathMetroStation=r"E:\GitHub\CAMMM-Tool_1.3\SampleData\GIS_Data\Montreal_Metro_Sample.gpkg"
#     Main(PathBusStop=LocalPathBusStop,PathMetroStation=LocalPathMetroStation)


LocalPathBusStop=r"E:\GitHub\CAMMM-Tool_1.3\SampleData\GIS_Data\Montreal_Bus_Sample.gpkg"
LocalPathMetroStation="E:\GitHub\CAMMM-Tool_1.3\SampleData\GIS_Data\Montreal_Metro_Sample.gpkg"


DistanceCat={'BufferMetro':160,'DistanceMetro':150,'BufferBus':80,'DistanceBusStop':75}
Main(PathBusStop=LocalPathBusStop,PathMetroStation=LocalPathMetroStation)


# ['__class__', '__delattr__', '__delitem__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__geo_interface__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'approximateMemoryUsage', 'attribute', 'attributeCount', 'attributes', 'clearGeometry', 'deleteAttribute', 'embeddedSymbol', 'fieldNameIndex', 'fields', 'geometry', 'hasGeometry', 'id', 'initAttributes', 'isValid', 'padAttributes', 'resizeAttributes', 'setAttribute', 'setAttributes', 'setEmbeddedSymbol', 'setFields', 'setGeometry', 'setId', 'setValid', 'staticMetaObject']