import csv 
import jenkspy 
import statistics
import numpy as np


cpdef QuantilesBareFile(str Path, int Classess):
    cdef count
    count=0
    cdef list Data=[]
    cdef list breaks=[]

    with open(Path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        # print("csv_reader",type(csv_reader),len(list(csv_reader)))
        for line in csv_reader:
            count+=1
            # print(line[-1])
            if count==1:
                pass
            else:
                Data.append(int(line[-1]))
            # if count==100:
            #     break

    breaks= statistics.quantiles(Data,n=Classess)
    return breaks



cpdef NaturalBreaksNumpyFile(str Path, int Classess):
    cdef int count
    cdef list Data=[]
    cdef list breaks=[]

    count=0
    
    with open(Path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        # print("csv_reader",type(csv_reader),len(list(csv_reader)))
        # a = np.arange(len(list(csv_reader)))
        # print(a)
        for line in csv_reader:
            count+=1
            # print(line[-1])
            if count==1:
                pass
            else:
                Data.append(int(line[-1]))
            # if count==100:
            #     break
        Array=np.array(Data)

    breaks = jenkspy.jenks_breaks(Array, nb_class=Classess)
    return breaks




cpdef NaturalBreaksNumpyList(list Data, int Classess):
    cdef int count
    cdef list Data=[]
    cdef list breaks=[]

    Array=np.array(Data)
    breaks = jenkspy.jenks_breaks(Array, nb_class=Classess)
    return breaks


