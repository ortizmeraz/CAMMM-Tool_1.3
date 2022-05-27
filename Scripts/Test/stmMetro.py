def GetMetroSTM():

    # Station Lionel-Groulx     36
    Nodes=[43, 42, 41, 40, 39, 38, 37, 35, 34, 33, 32, 31, 30, 99, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18,65, 54, 53, 52, 51, 50, 98, 48, 47, 46, 36, 17, 16, 15, 14, 13, 12,  10, 9, 8, 7, 6, 4, 3, 2, 1, 66, 67, 68,44, 45, 55, 56, 57, 58, 59, 60, 61, 97, 62, 63, 64]

    NodeData={}
    NodeData[43]={'Line':['Green']}
    NodeData[42]={'Line':['Green']}
    NodeData[41]={'Line':['Green']}
    NodeData[40]={'Line':['Green']}
    NodeData[39]={'Line':['Green']}
    NodeData[38]={'Line':['Green']}
    NodeData[37]={'Line':['Green']}
    NodeData[36]={'Line':['Green']}
    NodeData[35]={'Line':['Green']}
    NodeData[34]={'Line':['Green']}
    NodeData[33]={'Line':['Green']}
    NodeData[32]={'Line':['Green']}
    NodeData[31]={'Line':['Green']}
    NodeData[30]={'Line':['Green']}
    NodeData[99]={'Line':['Green']}
    NodeData[29]={'Line':['Green']}
    NodeData[28]={'Line':['Green']}
    NodeData[27]={'Line':['Green']}
    NodeData[26]={'Line':['Green']}
    NodeData[25]={'Line':['Green']}
    NodeData[24]={'Line':['Green']}
    NodeData[23]={'Line':['Green']}
    NodeData[22]={'Line':['Green']}
    NodeData[21]={'Line':['Green']}
    NodeData[20]={'Line':['Green']}
    NodeData[19]={'Line':['Green']}
    NodeData[18]={'Line':['Green']}
    NodeData[65]={'Line':['Orange']}
    NodeData[54]={'Line':['Orange']}
    NodeData[53]={'Line':['Orange']}
    NodeData[52]={'Line':['Orange']}
    NodeData[51]={'Line':['Orange']}
    NodeData[50]={'Line':['Orange']}
    NodeData[98]={'Line':['Orange']}
    NodeData[48]={'Line':['Orange']}
    NodeData[47]={'Line':['Orange']}
    NodeData[46]={'Line':['Orange']}
    NodeData[36]={'Line':['Orange']}
    NodeData[17]={'Line':['Orange']}
    NodeData[16]={'Line':['Orange']}
    NodeData[15]={'Line':['Orange']}
    NodeData[14]={'Line':['Orange']}
    NodeData[13]={'Line':['Orange']}
    NodeData[12]={'Line':['Orange']}
    NodeData[99]={'Line':['Orange']}
    NodeData[10]={'Line':['Orange']}
    NodeData[9]={'Line':['Orange']}
    NodeData[8]={'Line':['Orange']}
    NodeData[7]={'Line':['Orange']}
    NodeData[6]={'Line':['Orange']}
    NodeData[97]={'Line':['Orange']}
    NodeData[4]={'Line':['Orange']}
    NodeData[3]={'Line':['Orange']}
    NodeData[2]={'Line':['Orange']}
    NodeData[1]={'Line':['Orange']}
    NodeData[66]={'Line':['Orange']}
    NodeData[67]={'Line':['Orange']}
    NodeData[68]={'Line':['Orange']}
    NodeData[44]={'Line':['Yellow']}
    NodeData[45]={'Line':['Yellow']}
    NodeData[99]={'Line':['Yellow']}
    NodeData[98]={'Line':['Blue']}
    NodeData[55]={'Line':['Blue']}
    NodeData[56]={'Line':['Blue']}
    NodeData[57]={'Line':['Blue']}
    NodeData[58]={'Line':['Blue']}
    NodeData[59]={'Line':['Blue']}
    NodeData[60]={'Line':['Blue']}
    NodeData[61]={'Line':['Blue']}
    NodeData[97]={'Line':['Blue']}
    NodeData[62]={'Line':['Blue']}
    NodeData[63]={'Line':['Blue']}
    NodeData[64]={'Line':['Blue']}
    NodeData[99]={'Line':['Green','Orange','Yellow']}
    NodeData[98]={'Line':['Orange','Blue']}
    NodeData[97]={'Line':['Orange','Blue']}
    NodeData[36]={'Line':['Green','Orange']}


    CoordData=ReadCoords()

    for node in Nodes:
        NodeData[node]['Pos']=[int(CoordData[str(node)]['X']),int(CoordData[str(node)]['Y'])]



    Edges=[[43,42],[42,41],[41,40],[40,39],[39,38],[38,37],[37,36],[36,35],[35,34],[34,33],[33,32],[32,31],[31,30],[30,99],[99,29],[29,28],[28,27],[27,26],[26,25],[25,24],[24,23],[23,22],[22,21],[21,20],[20,19],[19,18],[65,54],[54,53],[53,52],[52,51],[51,50],[50,98],[98,48],[48,47],[47,46],[46,36],[36,17],[17,16],[16,15],[15,14],[14,13],[13,12],[12,99],[99,10],[10,9],[9,8],[8,7],[7,6],[6,97],[97,4],[4,3],[3,2],[2,1],[1,66],[66,67],[67,68],[44,45],[45,99],[98,55],[55,56],[56,57],[57,58],[58,59],[59,60],[60,61],[61,97],[97,62],[62,63],[63,64],]


    EdgeData={}
    EdgeData['time']={}
    EdgeData['time'][43, 42]=71.5
    EdgeData['time'][42, 41]=102.66666666666667
    EdgeData['time'][41, 40]=82.75
    EdgeData['time'][40, 39]=74.41666666666667
    EdgeData['time'][39, 38]=88.41666666666667
    EdgeData['time'][38, 37]=78.16666666666667
    EdgeData['time'][37, 36]=106.08333333333333
    EdgeData['time'][36, 35]=128.16666666666666
    EdgeData['time'][35, 34]=82.58333333333333
    EdgeData['time'][34, 33]=82.66666666666667
    EdgeData['time'][33, 32]=60.666666666666664
    EdgeData['time'][32, 31]=66.25
    EdgeData['time'][31, 30]=64.83333333333333
    EdgeData['time'][30, 99]=64.16666666666667
    EdgeData['time'][99, 29]=72.66666666666667
    EdgeData['time'][29, 28]=69.33333333333333
    EdgeData['time'][28, 27]=103.58333333333333
    EdgeData['time'][27, 26]=97.91666666666667
    EdgeData['time'][26, 25]=62.333333333333336
    EdgeData['time'][25, 24]=84.08333333333333
    EdgeData['time'][24, 23]=79.83333333333333
    EdgeData['time'][23, 22]=89.75
    EdgeData['time'][22, 21]=86.0
    EdgeData['time'][21, 20]=72.08333333333333
    EdgeData['time'][20, 19]=74.08333333333333
    EdgeData['time'][19, 18]=115.83333333333333
    EdgeData['time'][44, 45]=130.0
    EdgeData['time'][45, 99]=215.0
    EdgeData['time'][98, 55]=81.33333333333333
    EdgeData['time'][55, 56]=86.33333333333333
    EdgeData['time'][56, 57]=75.83333333333333
    EdgeData['time'][57, 58]=96.5
    EdgeData['time'][58, 59]=75.5
    EdgeData['time'][59, 60]=85.16666666666667
    EdgeData['time'][60, 61]=64.66666666666667
    EdgeData['time'][61, 97]=65.83333333333333
    EdgeData['time'][97, 62]=90.16666666666667
    EdgeData['time'][62, 63]=74.83333333333333
    EdgeData['time'][63, 64]=101.5
    EdgeData['time'][65, 54]=66.57142857142857
    EdgeData['time'][54, 53]=113.5
    EdgeData['time'][53, 52]=85.71428571428571
    EdgeData['time'][52, 51]=97.85714285714286
    EdgeData['time'][51, 50]=69.14285714285714
    EdgeData['time'][50, 98]=81.21428571428571
    EdgeData['time'][98, 48]=92.71428571428571
    EdgeData['time'][48, 47]=127.14285714285714
    EdgeData['time'][47, 46]=125.85714285714286
    EdgeData['time'][46, 36]=76.0
    EdgeData['time'][36, 17]=92.14285714285714
    EdgeData['time'][17, 16]=73.21428571428571
    EdgeData['time'][16, 15]=71.57142857142857
    EdgeData['time'][15, 14]=65.57142857142857
    EdgeData['time'][14, 13]=64.57142857142857
    EdgeData['time'][13, 12]=64.28571428571429
    EdgeData['time'][12, 99]=101.35714285714286
    EdgeData['time'][99, 10]=85.85714285714286
    EdgeData['time'][10, 9]=95.28571428571429
    EdgeData['time'][9, 8]=74.85714285714286
    EdgeData['time'][8, 7]=85.71428571428571
    EdgeData['time'][7, 6]=73.42857142857143
    EdgeData['time'][6, 97]=82.07142857142857
    EdgeData['time'][97, 4]=100.5
    EdgeData['time'][4, 3]=88.28571428571429
    EdgeData['time'][3, 2]=121.57142857142857
    EdgeData['time'][2, 1]=114.5
    EdgeData['time'][1, 66]=129.27272727272728
    EdgeData['time'][66, 67]=153.27272727272728
    EdgeData['time'][67, 68]=116.72727272727273





    return Nodes,NodeData,Edges,EdgeData
def ReadCoords():
    import csv
    Data={}
    HeadKey={}
    Path="/mnt/e/GitHub/CAMMM-Tool_1.3/Scripts/Test/GISdata/MetroStops.csv"
    with open(Path,encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        headers = next(csv_reader, None)
        # print(headers)
        for i,x in enumerate(headers):
            # print(i,x)
            HeadKey[i]=x
        # print(csv_reader)
        for idx,row in enumerate(csv_reader):
            # print(idx,row)
            Data[row[1]]={}
            for i,x in enumerate(row):
                Data[row[1]][HeadKey[i]]=x
    # for i,x in enumerate(Data.keys()):
    #     print(i,x,Data[x])
    return Data

if __name__=="__main__":
    Nodes,NodeData,Edges,EdgeData=GetMetroSTM()

    print("Nodes",len(Nodes))
    print("NodeData",len(NodeData))
    print("Edges",len(Edges))
    print("EdgeData",len(EdgeData))


    ReadCoords()

    CoordData=ReadCoords()

    # print(Nodes)

    # for i,x in enumerate(Nodes):
    #     print(i,x,CoordData[str(x)]['X'],CoordData[str(x)]['Y'])

    # for key in CoordData.keys():
    #     print(key,type(key))

    for node in Nodes:
        print(node,NodeData[node])

    # for i,x in enumerate(Nodes):
    #     print(i,x,NodeData[x])

