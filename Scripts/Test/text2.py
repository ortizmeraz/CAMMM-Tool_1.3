Dict={}
Dict[2]= {'1': {'0': ['43', '42', '41', '40', '39', '38', '37', '36', '35', '34', '33', '32', '31', '30', '9999111', '29', '28', '27', '26', '25', '24', '23', '22', '21', '20', '19', '18'], '1': ['18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '9999111', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43']}, '2': {'0': ['65', '54', '53', '52', '51', '50', '9999492', '48', '47', '46', '36', '17', '16', '15', '14', '13', '12', '9999112', '10', '9', '8', '7', '6', '9999052', '4', '3', '2', '1', '66', '67', '68'], '1': ['68', '67', '66', '1', '2', '3', '4', '9999052', '6', '7', '8', '9', '10', '9999112', '12', '13', '14', '15', '16', '17', '36', '46', '47', '48', '9999492', '50', '51', '52', '53', '54', '65']}, '4': {'0': ['44', '45', '9999114'], '1': ['9999114', '45', '44']}, '5': {'0': ['9999495', '55', '56', '57', '58', '59', '60', '61', '9999055', '62', '63', '64'], '1': ['64', '63', '62', '9999055', '61', '60', '59', '58', '57', '56', '55', '9999495']}}


# for i,x in enumerate(Dict[2].keys()):
#     print(i,x,)
#     # print(i,x,Dict[2][x])
#     for j,y in enumerate(Dict[2][x].keys()):
#         print("\t",j,y,"-",len(Dict[2][x][y]),"-",Dict[2][x][y])

# Station Berri-UQAM        99      9999111-9999112-9999114
# Station Snowdon           98      9999495-9999492
# Station Jean-Talon        97      9999055-9999052
# Station Lionel-Groulx     36
GreenLine=['43', '42', '41', '40', '39', '38', '37', '36', '35', '34', '33', '32', '31', '30', '99', '29', '28', '27', '26', '25', '24', '23', '22', '21', '20', '19', '18']
# GreenLine Angrignon > Honoré-Beaugrand
OragnLine=['65', '54', '53', '52', '51', '50', '98', '48', '47', '46', '36', '17', '16', '15', '14', '13', '12', '99', '10', '9', '8', '7', '6', '97', '4', '3', '2', '1', '66', '67', '68']
# OragnLine Cote Vertu > Montmomercy
YelloLine=['44', '45', '99',]
# YelloLine Longueuil–Université-de-Sherbrooke > Berri UQAM
BlueLine=['98', '55', '56', '57', '58', '59', '60', '61', '97', '62', '63', '64']

# for s in GreenLine:
#     print("NodeData[",s,"]={'Line':['Green']}")

# for s in OragnLine:
#     print("NodeData[",s,"]={'Line':['Orange']}")

# for s in YelloLine:
#     print("NodeData[",s,"]={'Line':['Yellow']}")

# for s in BlueLine:
#     print("NodeData[",s,"]={'Line':['Blue']}")
# print("NodeData[99]={'Line':['Green','Orange','Yellow']}")
# print("NodeData[98]={'Line':['Orange','Blue']}")
# print("NodeData[97]={'Line':['Orange','Blue']}")
# print("NodeData[36]={'Line':['Green','Orange']}")

# def M(ListW):
#     for i,x in enumerate(ListW):
#         if x==ListW[-1]:
#             break
#         print([int(ListW[i]),int(ListW[i+1])],",")

# print("[")
# M(ListW=GreenLine)
# M(ListW=OragnLine)
# M(ListW=YelloLine)
# M(ListW=BlueLine)

print(len(GreenLine))
print(len(OragnLine))
print(len(YelloLine))
print(len(BlueLine))

# print("]")



