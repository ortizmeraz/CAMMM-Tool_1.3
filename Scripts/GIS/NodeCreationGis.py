import os


def Main(PathBusStop:str,PathMetroStation:str):
    ListOfUsedBusStops=[]

    BaseMetro=r'E:\\GitHub\\CAMMM-Tool_1.3\\SampleData\\GIS_Data\\Montreal_Metro_Sample.gpkg|layername=Montreal_Metro_Sample'


    # BusStops_layer=QgsVectorLayer(PathBusStop,"ogr")
    # print(BusStops_layer)
    # for i in BusStops_layer.getFeatures():
    #     # print(dir(i))
    #     # print(type(i.attributes()))
    #     print(i.attributes()[0])

    # print(PathMetroStation)
    # b=input('.................................')

    MetroStation_layer=QgsVectorLayer(PathMetroStation,"ogr")
    for i in MetroStation_layer.getFeatures():
        PathTempMetro='F:/OneDrive - Concordia University - Canada/RA-CAMMM/HubProccesing/Operational/Metro_'+str(i.attributes()[2])+'.gpkg'
        PathTempBuffermetro='F:/OneDrive - Concordia University - Canada/RA-CAMMM/HubProccesing/Operational/Buffer_Metro_'+str(i.attributes()[2])+'.gpkg'
        PathTempClip='F:/OneDrive - Concordia University - Canada/RA-CAMMM/HubProccesing/Operational/SelectionBusStops_Metro_'+str(i.attributes()[2])+'.gpkg'
        PathTempDist='F:/OneDrive - Concordia University - Canada/RA-CAMMM/HubProccesing/Operational/DistanceBusStops_Metro_'+str(i.attributes()[2])+'.gpkg'

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
        'DISTANCE':Buffersize['Metro'],
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


        paramsDist={'INPUT':PathTempDist,
        'HUBS':PathTempMetro,
        'FIELD':'StopCode',
        'UNIT':0,
        'OUTPUT':PathTempDist}
        processing.run("qgis:distancetonearesthubpoints",)







# if __name__ == "__main__":
#     LocalPathBusStop="E:\GitHub\CAMMM-Tool_1.3\SampleData\GIS_Data\Montreal_Bus_Sample.gpkg"
#     LocalPathMetroStation=r"E:\GitHub\CAMMM-Tool_1.3\SampleData\GIS_Data\Montreal_Metro_Sample.gpkg"
#     Main(PathBusStop=LocalPathBusStop,PathMetroStation=LocalPathMetroStation)


LocalPathBusStop=r"E:\GitHub\CAMMM-Tool_1.3\SampleData\GIS_Data\Montreal_Bus_Sample.gpkg"
LocalPathMetroStation="E:\GitHub\CAMMM-Tool_1.3\SampleData\GIS_Data\Montreal_Metro_Sample.gpkg"


Buffersize={'Metro':160}
Main(PathBusStop=LocalPathBusStop,PathMetroStation=LocalPathMetroStation)


# ['__class__', '__delattr__', '__delitem__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__geo_interface__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'approximateMemoryUsage', 'attribute', 'attributeCount', 'attributes', 'clearGeometry', 'deleteAttribute', 'embeddedSymbol', 'fieldNameIndex', 'fields', 'geometry', 'hasGeometry', 'id', 'initAttributes', 'isValid', 'padAttributes', 'resizeAttributes', 'setAttribute', 'setAttributes', 'setEmbeddedSymbol', 'setFields', 'setGeometry', 'setId', 'setValid', 'staticMetaObject']