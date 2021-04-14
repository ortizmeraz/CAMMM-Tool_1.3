import openpyxl
from openpyxl import load_workbook



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
    DataSet={}
    # RowVal=RowVal+1
    ListofRows=CreateListRows(NumRecords)
    DictColumns=GetColumns()
    for row in ListofRows:
        DataSet[row]={}
        for column in DictColumns.keys():
            Cell=DictColumns[column]+str(row)
            # print(Cell,end="\t")
            print(Cell,WorkSheet[Cell].value,end="\t")
            DataSet[row][DictColumns[column]]=WorkSheet[Cell].value
        print()






def OpenFile(Data):
    PathExcel="E:\GitHub\CAMMM-Web-Tool-1\DatabaseCitys.xlsx"
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
