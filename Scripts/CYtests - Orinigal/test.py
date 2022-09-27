# import Distance
import jenkspy


# F=Distance.NaturalBreaksNumpy(Path="/mnt/d/GitHub/CAMMM-Tool_1.3/SampleData/Random/SampleData.csv", Classess=5)
# print(F)


# G=Distance.QuantilesBare(Path="/mnt/d/GitHub/CAMMM-Tool_1.3/SampleData/Random/SampleData.csv", Classess=5)
# print(G)
arr=[498,48769,48576,4856,48,48,754,8794,869,48796,4,94,8964,685,418765,4,864,98,646,91,68,8498,4,684,84,986,49,641,684,98,4,9847,894,568,489,41,94,68,48576,46,84,894,894,984,98,49,9469,4,968,49,496,4,6584,9,49,7,41,8,7,48497,1895,96,4,87,5,87,65,8,4,4,486]

D=jenkspy.jenks_breaks(arr, nb_class=5)

print(D)
