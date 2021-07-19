import Calculations
import math
import decimal
decimal.getcontext().prec = 10



def Distance(P1,P2):
    PX=math.pow(decimal.Decimal(P2[0])-decimal.Decimal(P1[0]),2)
    PY=math.pow(decimal.Decimal(P2[1])-decimal.Decimal(P1[1]),2)
    # print("X2:",P2[0],"X1:",P1[0],"D:",math.sqrt(PX+PY))
    # print("Y2:",P2[1],"y1:",P1[1])
    # print()
    return math.sqrt(PX+PY)

Base1=[11565.251,418765.782]
Base2=[26548.125,886547.348]

BaseOhCoords=[11565.251,418765.782,26548.125,886547.348]
ListCoords=[]
Tup1Coord=[]
for i in range(1000000):
   ListCoords.append(BaseOhCoords) 
   Tup1Coord.append((Base1,Base2))
# print(Tup1Coord)

print("Start C")
for Di in ListCoords:
    F=Calculations.CalcDistance(Di[0],Di[1],Di[2],Di[3])

print("End C")


print("Start Python")
for ge in Tup1Coord:
    G=Distance(P1=ge[0],P2=ge[1])

print("End Python")

# B=Distance(P1=(0.0,0.0),P2=(10.0,10.0))
# print("Calculation on P",B)

# F=Calculations.CalcDistance(0.0,0.0,10.0,10.0)
# print("Calculation on C",F)

# G= Calculations.SumTest(11.11111,22.22222)
# print(G)

# s1=decimal.Decimal(11.11)
# s2=decimal.Decimal(22.22)

# G= Calculations.SumTest(11.11,22.22)
# print("C def",G)


# G1= Calculations.SumTest(s1,s2)
# print("decimal.Decimal",G1)

# G2=11.11+22.22
# print("Bare metal",G2)

