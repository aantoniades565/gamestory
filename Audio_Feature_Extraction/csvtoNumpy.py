import csv
import numpy as np
x = np.array([])
confidences = np.array([])
with open("pitch2.csv", 'r') as myFile:
    lines = csv.reader(myFile)
    for l in lines:
        x = np.append(x, float(l[0]))
        confidences = np.append(confidences, float(l[1]))
thres = 0.1
c = 0
for i in range(len(x)):
    if confidences[i] < thres or x[i] <0:
        c+=1
        x[i] = 0
print(c)

#----------------------d1 Zero out--------------------------#
# a,b = 6388,7322
# b+=1
# x[a:b] = (b-a)*[0]
#
# a,b = 11312,12347
# b+=1
# x[a:b] = (b-a)*[0]
#
# a,b = 18819,22434
# b+=1
# x[a:b] = (b-a)*[0]
#
# a,b = 26225,27172
# b+=1
# x[a:b] = (b-a)*[0]
#
# a,b = 30199,31142
# b+=1
# x[a:b] = (b-a)*[0]
#
# start,end = 3944,34248
# x = x[start:(end+1)]
# print(len(x))
#
# np.save('pitch_processed_d1.npy', x)

# print(np.load('pitch_processed_d1.npy'))


#----------------------d2 Zero Out--------------------------#

delta = 58754
a,b = 61557,62555
a-= delta
b-= delta
b+=1
x[a:b] = (b-a)*[0]

a,b = 68690,69846
a-= delta
b-= delta
b+=1
x[a:b] = (b-a)*[0]

a,b = 73004,79102
a-= delta
b-= delta
b+=1
x[a:b] = (b-a)*[0]

np.save('pitch_processed_d2.npy', x)