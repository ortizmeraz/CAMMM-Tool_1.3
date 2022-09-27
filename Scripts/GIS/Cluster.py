import utm
import json



Path="/mnt/g/Downloads/pointsOfInterest.geojson"
PathExit="/mnt/g/Downloads/pointsOfInterestSquares.txt"
# for t in List:
#     text=t
#     f.write(text)
Buffer=5
# print(data[0][1])
# print(type(data[0][1]))




def Write2File(LLC1,LLC5,LLC2,LLC3,LLC4):
    Text="    \'geometry\': {"
    Text+="        \'type\': \'Polygon\',"
    Text+="    \'coordinates\': "
    Text+="        ["
    Text+="            ["
    Text+="                ["+str(LLC1[0])+", "+str(LLC1[1])+"],"
    Text+="                ["+str(LLC2[0])+", "+str(LLC2[1])+"],"
    Text+="                ["+str(LLC3[0])+", "+str(LLC3[1])+"],"
    Text+="                ["+str(LLC4[0])+", "+str(LLC4[1])+"],"
    Text+="                ["+str(LLC5[0])+", "+str(LLC5[1])+"],"

    Text+="            ]"
    Text+="        ]"
    Text+="                }\n"
    return Text

def ProcessData(data):
    for i in data[0][1]:
        print(type(i),"\n")
        print(i.keys(),"\n")
        print(i['geometry']['coordinates'])
        print(type(i['geometry']['coordinates']))
        cc=i['geometry']['coordinates']
        UTM=utm.from_latlon(cc[0], cc[1])
        print("UTM:",UTM)


        C1=[UTM[0]+(Buffer*0),UTM[1]+(Buffer*1),UTM[2],UTM[3]]
        C5=C1
        C2=[UTM[0]+(Buffer*1),UTM[1]+(Buffer*1),UTM[2],UTM[3]]

        C3=[UTM[0]+(Buffer*0),UTM[1]+(Buffer*-1),UTM[2],UTM[3]]
        
        C4=[UTM[0]+(Buffer*-1),UTM[1]+(Buffer*-1),UTM[2],UTM[3]]

        # print("C1",C1)
        LLC1=utm.to_latlon(C1[0],C1[1],C1[2],C1[3])
        LLC5=utm.to_latlon(C1[0],C1[1],C1[2],C1[3])
        # print(LLC1)

        # print("C2",C2)
        LLC2=utm.to_latlon(C1[0],C1[1],C1[2],C1[3])
        # print()

        # print("C3",C3)
        LLC3=utm.to_latlon(C1[0],C1[1],C1[2],C1[3])
        # print(LLC3)

        # print("C4",C4)
        LLC4=utm.to_latlon(C1[0],C1[1],C1[2],C1[3])
        # print(LLC4)
        Text=Write2File(LLC1,LLC5,LLC2,LLC3,LLC4)
        f.write(Text)




with open(Path) as f:
    data = list(json.load(f).items())
f = open(PathExit, 'w')
ProcessData(data)
f.close()