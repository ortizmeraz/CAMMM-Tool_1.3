###### RUNN NOVEMBER 2022

#### Script 11




import ast


def main(data,ShowProcess:bool=False):
    NewDict={}
    NewOrder=[]
    UsedStops=[]
    KeyList=list(data.keys())

    if ShowProcess: print("Keys")
    if ShowProcess: print(KeyList)
    if ShowProcess: b=input('.................................')

    for key in data.keys():
        if int(key)>9999000:
            if ShowProcess: print("KEEEEEEEEEEEEEEEEEEy")
            if ShowProcess: print(key)


    if ShowProcess: print("End of checking")
    if ShowProcess: b=input('.................................')
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
        if ShowProcess: print("\n"*3)
        if ShowProcess: print("········································\n"*3)
        if ShowProcess: print(idx,"/",len(NewOrder))
        if ShowProcess: print("Stop:",stop,"---",len(data[stop]))
        if ShowProcess: print("\t",data[stop],len(data[stop]))
        
        if stop in UsedStops:
            if ShowProcess: print("\nSkip because it has been used")
            continue
        ###############################################################################
        ##### Variable declaration
        ShowProcess=True
        #######################

        ###############################################################################
        ########    METRO STATION
        ###############################################################################
        ##### Variable declaration
        ShowProcess=True
        #######################

        if int(stop) <100:
            # print (stop)
            ShowProcess=True
            LocalOrder.append(stop)
            if ShowProcess: print("METRO:\t",stop,data[stop],len(data[stop]))
            for substop in data[stop]:
                LocalOrder.append(substop['StopCode'])
                if ShowProcess: print(substop)
                # UsedStops.append(substop['StopCode'])
            print("Local Order:",LocalOrder)
            NewDict[stop]={"Data":LocalOrder,"Type":"Hub"}
            # b=input('.................................')
            # if ShowProcess: print("UsedStops ",UsedStops)
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
        ShowProcess=False
        #######################
        print("Start Order")

        OldOrder=[]
        for substop in data[stop]:
            OldOrder.append(substop['StopCode'])
            if ShowProcess: print()
            if ShowProcess: print(substop)
            if ShowProcess: print("\t",substop['StopCode'])
            if ShowProcess: print(len(data[substop['StopCode']]),"-",data[substop['StopCode']])
            if ShowProcess: print()
            if ShowProcess: print("\tEnter ranking")
        ###############################################################################
        ##### Sorting stage
        #######################
        if ShowProcess: print("OldOrder",OldOrder)

        # if substop in NewOrder:

        if ShowProcess: print(OldOrder,len(OldOrder))
        # b=input('.................................')
        if len(OldOrder)==0:
            StartRange=0
        else:
            StartRange=len(OldOrder)
        for rank in range(StartRange+1,0,-1):
            if ShowProcess: print("\t","+",rank)
            for substop in OldOrder:
                if rank == len(data[substop]):
                    if ShowProcess: print("\t"*2+"Sub Stop",substop,len(data[substop]))
                    LocalOrder.append(substop)
                else:
                    if ShowProcess: print()
        if ShowProcess: print(LocalOrder)
        if ShowProcess: 
            for substop in LocalOrder:
                if ShowProcess: print(substop,len(data[substop]))
        ###############################################################################
        ##### Expansion stage
        ShowProcess=True
        #######################
        CompleteLocalOrder=[]
        for stp in LocalOrder:
            CompleteLocalOrder.append(stp)
        if ShowProcess: print("Local Order       ",LocalOrder)
        if ShowProcess: print("CompleteLocalOrder",CompleteLocalOrder)
        if ShowProcess: print("Local Order",LocalOrder)
        for substop in LocalOrder:
            if ShowProcess: print("\t",substop)
            for subcheck in data[substop]:
                if ShowProcess: print(subcheck,end="")

                if subcheck['StopCode'] in LocalOrder or subcheck['StopCode']==stop:
                    if ShowProcess: print("\t"*2+"Mirrored")
                else:
                    if ShowProcess: print("\t"*2+"Expand")
                    if ShowProcess: print("\tNested:",subcheck['StopCode'],data[subcheck['StopCode']])
                    for NestedStop in data[subcheck['StopCode']]:
                        if ShowProcess:print("Nested Stop",NestedStop['StopCode'])
                        if NestedStop['StopCode'] not in CompleteLocalOrder:
                            if ShowProcess: print("CompleteLocalOrder+",CompleteLocalOrder,NestedStop['StopCode'])
                            CompleteLocalOrder.append(NestedStop['StopCode'])
                            if ShowProcess: print("\t"*2,"NEW ADDITON·····························································································")
                            if ShowProcess: print("CompleteLocalOrder+",CompleteLocalOrder,NestedStop['StopCode'])
        CompleteLocalOrder.append(stop)
        for stp in CompleteLocalOrder:
            UsedStops.append(stp)
        # NewDict[stop]=CompleteLocalOrder
        NewDict[stop]={"Data":CompleteLocalOrder,"Type":"Cluster"}

        print(stop)
        if ShowProcess: print(NewDict[stop])
        if ShowProcess: print("Local Order       ",LocalOrder,len(LocalOrder))
        if ShowProcess: print("CompleteLocalOrder",CompleteLocalOrder,len(CompleteLocalOrder))
        # if stop =='54160': print("HEEEEEEEEEEEEEEEEEEEEEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE\n"*10)
        for stop in NewDict.keys():
            if ShowProcess: print(stop,NewDict[stop])
        # b=input('...Stop..............................')

        # for stop in List:
        #     StCd=stop['StopCode']
        #     print(StCd,type(StCd))
        #     if StCd in KeyList:
        #         print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("End of procesing")
    for stop in NewDict.keys():
        print(stop,NewDict[stop])

    Path=r'F:\OneDrive - Concordia University - Canada\RA-CAMMM\Gis_Data\NodeList.txt'
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


DataPath=r'F:\OneDrive - Concordia University - Canada\RA-CAMMM\Gis_Data\DataToCreateNode.txt'

NodeData=ReadDict(Path=DataPath)
main(data=NodeData,ShowProcess=False)
# print(data)
