import numpy as np
from GLCM import *
import csv
import math

if __name__ == '__main__':
    X = np.loadtxt("test.txt", dtype={'names': (
        'Contrast', 'Energy', 'Homogenity', 'Correlation'), 'formats': (np.float, np.float, np.float, np.float)})
    Y = open("test.txt", 'r')
    image = cv2.imread(
        "jerukknn/datatest.jpeg")
    # print image
    # print map(float, Y)
    with open("test.txt") as f:
        floats = csv.reader(f, delimiter=' ')
        kontras = []
        energy = []
        homogenity = []
        korelasi = []
        label = []
        for row in floats:
            kontras.append(float(row[0]))
            energy.append(float(row[1]))
            homogenity.append(float(row[2]))
            korelasi.append(float(row[3]))
            label.append(int(row[4]))
    distance = []
    # print kontras
    # print floats
    X.reshape(-1, 1)
    # print X.shape
    # print X[0].contrast
    # for ()
    imageglcm = GLCM(image, 0, 1)
    for row in range(len(kontras)):
        distance.append(math.sqrt(pow((rgb2gs(imageglcm.kontras) - kontras[row]), 2) + pow((rgb2gs(imageglcm.energy) - energy[row]), 2) + pow(
            (rgb2gs(imageglcm.homogenity) - homogenity[row]), 2) + pow((rgb2gs(imageglcm.korelasion) - korelasi[row]), 2)))
    print "distance : " + str(distance)

    rank = sorted(range(len(distance)), key=lambda k: distance[k])
    print "rank : " + str(rank)

    k = 2
    knn = []
    for trasi in range(k):
        knn.append(rank.index(trasi))
    print "knn : "+ str(knn)
    klas1 = []
    klas2 = []
    for x in range(len(knn)):
        if label[rank[x]] == 0:
            klas1.append(rank[knn[x]])
        if label[rank[x]] == 1 :
            klas2.append(rank[knn[x]])
    print "klas 1 : " + str(klas1)
    print "klas 2 : " + str(klas2)
    klas1dis=0
    klas2dis=0
    if len(klas1) == len(klas2):
        for x in range(len(klas1)):
            klas1dis+=distance[klas1[x]]
            klas2dis+=distance[klas2[x]]
        print "kelas : " + str(0 if klas1dis> klas2dis else 1)
    else:
        print "Kelas : " + str(0 if len(klas1) > len(klas2) else 1)
