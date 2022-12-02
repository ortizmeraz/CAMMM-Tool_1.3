a=[1,2,3,4,5,6]
b=[11,11,22,33]

for i,j in zip(a,b,strict=True):
    print(i,j)