import ast



def main(data):
    NewDict={}
    NewOrder=[]
    UsedStops=[]
    KeyList=list(data.keys())

    for num in range(31,-1,-1):
        # print("Num",num)
        for key in data.keys():
            List=data[key]
            # print(key,List,len(List))
            if len(List)==num:
                # print("\t hey")
                NewOrder.append(key)

    for idx,stop in enumerate(NewOrder):
        ###############################################################################
        ##### Variable declaration
        LocalPrint=True
        #######################
        LocalOrder=[]


        ###############################################################################
        ##### Presentation of the data
        LocalPrint=True
        #######################
        if LocalPrint: print("\n"*3)
        if LocalPrint: print("········································\n"*3)
        if LocalPrint: print(idx,"/",len(NewOrder))
        if LocalPrint: print("Stop:",stop,"---",len(data[stop]))
        if LocalPrint: print("\t",data[stop],len(data[stop]))
        
        if stop in UsedStops:
            if LocalPrint: print("\nSkip because it has been used")
            continue
        ###############################################################################
        ##### Variable declaration
        LocalPrint=True
        #######################

        ###############################################################################
        ########    METRO STATION
        ###############################################################################
        ##### Variable declaration
        LocalPrint=True
        #######################

        if int(stop) <100:
            # print (stop)
            LocalPrint=True
            LocalOrder.append(stop)
            if LocalPrint: print("METRO:\t",stop,data[stop],len(data[stop]))
            for substop in data[stop]:
                LocalOrder.append(substop['StopCode'])
                if LocalPrint: print(substop)
                # UsedStops.append(substop['StopCode'])
            print("Local Order:",LocalOrder)
            NewDict[stop]={"Data":LocalOrder,"Type":"Hub"}
            # b=input('.................................')
            # if LocalPrint: print("UsedStops ",UsedStops)
            continue


        ###############################################################################
        ##### Checking Quality
        if len(data[stop])==0:
            # NewDict[stop]=[stop]
            NewDict[stop]={"Data":[stop],"Type":"Cluster"}


        
        ###############################################################################
        ########    BUS STOPS
        ###############################################################################
        ##### Listing stage
        LocalPrint=False
        #######################
        print("Start Order")

        OldOrder=[]
        for substop in data[stop]:
            OldOrder.append(substop['StopCode'])
            if LocalPrint: print()
            if LocalPrint: print(substop)
            if LocalPrint: print("\t",substop['StopCode'])
            if LocalPrint: print(len(data[substop['StopCode']]),"-",data[substop['StopCode']])
            if LocalPrint: print()
            if LocalPrint: print("\tEnter ranking")
        ###############################################################################
        ##### Sorting stage
        LocalPrint=False
        #######################
        if LocalPrint: print("OldOrder",OldOrder)

        # if substop in NewOrder:

        print(OldOrder,len(OldOrder))
        # b=input('.................................')
        if len(OldOrder)==0:
            StartRange=0
        else:
            StartRange=len(OldOrder)
        for rank in range(StartRange+1,0,-1):
            if LocalPrint: print("\t","+",rank)
            for substop in OldOrder:
                if rank == len(data[substop]):
                    if LocalPrint: print("\t"*2+"Sub Stop",substop,len(data[substop]))
                    LocalOrder.append(substop)
                else:
                    if LocalPrint: print()
        if LocalPrint: print(LocalOrder)
        if LocalPrint: 
            for substop in LocalOrder:
                print(substop,len(data[substop]))
        ###############################################################################
        ##### Expansion stage
        LocalPrint=True
        #######################
        CompleteLocalOrder=[]
        for stp in LocalOrder:
            CompleteLocalOrder.append(stp)
        if LocalPrint: print("Local Order       ",LocalOrder)
        if LocalPrint: print("CompleteLocalOrder",CompleteLocalOrder)
        if LocalPrint: print("Local Order",LocalOrder)
        for substop in LocalOrder:
            if LocalPrint: print("\t",substop)
            for subcheck in data[substop]:
                if LocalPrint: print(subcheck,end="")

                if subcheck['StopCode'] in LocalOrder or subcheck['StopCode']==stop:
                    if LocalPrint: print("\t"*2+"Mirrored")
                else:
                    if LocalPrint: print("\t"*2+"Expand")
                    if LocalPrint: print("\tNested:",subcheck['StopCode'],data[subcheck['StopCode']])
                    for NestedStop in data[subcheck['StopCode']]:
                        print("Nested Stop",NestedStop['StopCode'])
                        if NestedStop['StopCode'] not in CompleteLocalOrder:
                            if LocalPrint: print("CompleteLocalOrder+",CompleteLocalOrder,NestedStop['StopCode'])
                            CompleteLocalOrder.append(NestedStop['StopCode'])
                            if LocalPrint: print("\t"*2,"NEW ADDITON·····························································································")
                            if LocalPrint: print("CompleteLocalOrder+",CompleteLocalOrder,NestedStop['StopCode'])
        CompleteLocalOrder.append(stop)
        for stp in CompleteLocalOrder:
            UsedStops.append(stp)
        # NewDict[stop]=CompleteLocalOrder
        NewDict[stop]={"Data":CompleteLocalOrder,"Type":"Cluster"}

        print(stop)
        print(NewDict[stop])
        if LocalPrint: print("Local Order       ",LocalOrder,len(LocalOrder))
        if LocalPrint: print("CompleteLocalOrder",CompleteLocalOrder,len(CompleteLocalOrder))
        # if stop =='54160': print("HEEEEEEEEEEEEEEEEEEEEEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE\n"*10)
        for stop in NewDict.keys():
            print(stop,NewDict[stop])
        # b=input('...Stop..............................')

        # for stop in List:
        #     StCd=stop['StopCode']
        #     print(StCd,type(StCd))
        #     if StCd in KeyList:
        #         print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("End of procesing")
    for stop in NewDict.keys():
        print(stop,NewDict[stop])

    Path=r'E:\GitHub\CAMMM-Tool_1.3\SampleData\GIS_Data\NodeList.txt'
    f = open(Path, 'w')
    f.write(str(NewDict))
    f.close()


def ReadDict(Path,ShowData=False):
    with open(Path) as f:
        Lines = f.readlines()
        # for line in Lines:
        #     print(line)
    f.close()
    ExitData=ast.literal_eval(Lines[0])
    if ShowData: print(ExitData,type(ExitData))
    return ExitData


DataPath=r"E:\GitHub\CAMMM-Tool_1.3\SampleData\GIS_Data\ExitDict2.txt"

NodeData=ReadDict(Path=DataPath)
main(data=NodeData)
# print(data)
