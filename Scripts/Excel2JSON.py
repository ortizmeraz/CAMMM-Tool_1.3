import openpyxl
from openpyxl import load_workbook

def Example():
    Dict={"City": {
        "Montreal": {"name": "Montréal","NumTransportSystem": 3,"NumBusStops": 65666,"NumRailStations": 123,"NumMetroStations": 50,"NumBoroughs": 19,"AreaSqKm": 431.5,"PopulationMillion": 1.78,"DensityPersonSqKm": 4115,"DirectStyleURL": "ckmdts11g14q417pe6b2r7ytx","NodeStyleURL": "ckmduljdi15jd17pdh44qtoh8","DirectLayers": [    "montreal_D_CD",    "montreal_D_CL"],"NodeLayers": [    "montreal_N_CD",    "montreal_N_CL"],"Coords": [    -73.71,    45.53],"Zoom": 10.45},
        "Vienna": {"name": "Vienna","NumTransportSystem": 6,"NumBusStops": 78888,"NumRailStations": 456,"NumMetroStations": 35,"NumBoroughs": 20,"AreaSqKm": 414.6,"PopulationMillion": 1.8,"DensityPersonSqKm": 4341,"DirectStyleURL": "ckmdv9k6p0y6617qwpyikvpms","NodeStyleURL": "ckmdvdgrv16cx17pljoyexm36","DirectLayers": [    "vienna_D_CD",    "vienna_D_CL"],"NodeLayers": [    "vienna_N_CD",    "vienna_N_CL"],"Coords": [    16.39,    48.20],"Zoom": 11},
        "Barcelona": {"name": "Barcelona","NumTransportSystem": 6,"NumBusStops": 44444,"NumRailStations": 36,"NumMetroStations": 135,"NumBoroughs": 1,"AreaSqKm": 101.9,"PopulationMillion": 5.575,"DensityPersonSqKm": 54710,"DirectStyleURL": "ckmdvikhj16k118rv36unif4h","NodeStyleURL": "ckmdvr9px0yne17qw1abv6rqx","DirectLayers": [    "barcelona_D_CD",    "barcelona_D_CL",    "barcelona_D_EV"],"NodeLayers": [    "barcelona_N_CD",    "barcelona_N_CL",    "barcelona_N_EV"],"Coords": [    2.13,    41.38],"Zoom": 11.81},
        "Budapest": {"name": "Budapest","NumTransportSystem": 2,"NumBusStops": 3333333,"NumRailStations": 66,"NumMetroStations": 222,"NumBoroughs": 15,"AreaSqKm": 525.2,"PopulationMillion": 1.75,"DensityPersonSqKm": 3388,"DirectStyleURL": "ckmdvy9vn0yud17qwen6l9jj8","NodeStyleURL": "ckmdw5kz7171117pddh6zl0bj","DirectLayers": [    "budapest_D_CD",    "budapest_D_CL"],"NodeLayers": [    "budapest_N_CD",    "budapest_N_CL"],"Coords": [    19.12,    47.48],"Zoom": 10},
        "Quebec": {"name": "Quebec","NumTransportSystem": 4,"NumBusStops": 777777,"NumRailStations": 77,"NumMetroStations": 222,"NumBoroughs": 10,"AreaSqKm": 234.5,"PopulationMillion": 0.57,"DensityPersonSqKm": 1648,"DirectStyleURL": "ckmdwizn553xs17naq3j69fy6","NodeStyleURL": "ckmdwsyti17nu17pdw6orgej8","DirectLayers": [    "quebec_D_CD",    "quebec_D_CL"],"NodeLayers": [    "quebec_N_CD",    "quebec_N_CL"],"Coords": [    -71.26,    46.78],"Zoom": 11.3}
    }}
    return Dict

def ReadHowManyRecordsWeHave(WorkSheet):
    EmptyCell=False
    RowVal=2
    ListOhCities=[]
    while(EmptyCell==False):
        RowVal=RowVal+1
        if WorkSheet.cell(row=RowVal, column=1).value == None:
            print("Fin")
            EmptyCell=True
        else:
            Index=WorkSheet.cell(row=RowVal, column=1).value
            Name=WorkSheet.cell(row=RowVal, column=2).value
            ListOhCities.append(Index)
            print("***",Name,Index)
    return len(ListOhCities)


def CreateListRows(NumRecords):
    ListRows=[]
    for i in range(3,(NumRecords+3)):
        print("-----------",i)
        ListRows.append(i)
    return ListRows

def GetColumns():
    Columns={}
    Columns["City"]="A"
    Columns["name"]="B"
    Columns["NumTransportSystem"]="C"
    Columns["NumBusStops"]="D"
    Columns["NumRailStations"]="E"
    Columns["NumMetroStations"]="F"
    Columns["NumBoroughs"]="G"
    Columns["AreaSqKm"]="H"
    Columns["PopulationMillion"]="I"
    Columns["DensityPersonSqKm"]="J"
    Columns["DirectStyleURL"]="K"
    Columns["NodeStyleURL"]="L"
    Columns["DirectLayers"]="M"
    Columns["NodeLayers"]="N"
    Columns["Lat"]="O"
    Columns["Lon"]="P"
    Columns["Zoom"]="Q"
    return Columns



def ReadExcelTable(NumRecords,WorkSheet):
    DataSet={"City":{}}
    # RowVal=RowVal+1
    ListofRows=CreateListRows(NumRecords)
    DictColumns=GetColumns()
    for row in ListofRows:
        DataSet["City"][WorkSheet["A"+str(row)].value]={}
        # print(row,"\t",WorkSheet["A"+str(row)].value,"\t",end="\t")
        for column in DictColumns.keys():
            Cell=DictColumns[column]+str(row)
            # print(Cell,end="\t")
            # print(Cell,WorkSheet[Cell].value,end="\t")
            # print("CityKey",WorkSheet["A"+str(row)].value,end="\t")
            # print("DictColumns",column,end="\t")
            if DictColumns[column] == "M":
                Text=WorkSheet[Cell].value
                print("original text",Text)
                Text.replace("\"", '')
                print("new text",Text)
                ListLayers=Text.split(",")
                print("\n\nListLayers",ListLayers,type(ListLayers))
                print(WorkSheet["A"+str(row)].value,[column])
                DataSet["City"][WorkSheet["A"+str(row)].value][column]=ListLayers
                print("Stored data",DataSet["City"][WorkSheet["A"+str(row)].value][column])
                # b=input()
                # print(b)
            if DictColumns[column] == "O":
                Coords=[WorkSheet[Cell].value]
            if DictColumns[column]=="P":
                Coords.append(WorkSheet[Cell].value)
                DataSet["City"][WorkSheet["A"+str(row)].value]["Coords"]=Coords
            else:
                DataSet["City"][WorkSheet["A"+str(row)].value][column]=WorkSheet[Cell].value
        print()
    print(DataSet)
    print("set one....................................................")
    for key in DataSet["City"].keys():
        print ("key:",key)
        for CityKey in DataSet["City"][key].keys():
            print(CityKey,end=":")
        print()
    print()
    print("set two....................................................")
    for key in Example()["City"].keys(): 
        print ("key:",key)
        for CityKey in Example()["City"][key].keys():
            # print(CityKey,end=":")
            print("Sample",CityKey,Example()["City"][key][CityKey],type(Example()["City"][key][CityKey]))
            print("Data",CityKey,DataSet["City"][key][CityKey],type(DataSet["City"][key][CityKey]))
            print()







def OpenFile(Data):
    PathExcel=r"E:\GitHub\CAMMM-Web-Tool-1\DatabaseCitys.xlsx"
    wb = load_workbook(filename = PathExcel)
    print (wb.sheetnames, type(wb.sheetnames))
    sheets=list(wb.sheetnames)
    print(sheets)
    DataSheet=wb[sheets[0]]
    print(DataSheet)
    NumberOfRecordsInCode=ReadHowManyRecordsWeHave(WorkSheet=DataSheet)
    print("NumberOfRecordsInCode",NumberOfRecordsInCode)
    ReadExcelTable(NumRecords=NumberOfRecordsInCode,WorkSheet=DataSheet)


if __name__ == "__main__":
    Data={"Agency":"Agency A10",
    "Number_of_transport_systems":20,
    "Number_of_train_stations":340,
    "Number_of_metro_stations":2354,
    "Number_of_bus_stops":22486}
    OpenFile(Data=Data)
