import cv2
import numpy as np
import sys
import math


class GLCM:
    def __init__(self, image, dy, dx):
        self.image = image
        self.dy = dy
        self.dx = dx
        self.glcm = self.GLCMcount()
        self.kontras, self.meanI, self.meanJ, self.energy, self.homogenity = self.contrast()
        self.taoI, self.taoJ = self.tao()
        self.korelasion = self.correlation()

    def GLCMcount(self):
        height, width = self.image.shape[:2]
        glcm = np.zeros((256, 256, 3), np.double)
        x = 0
        for i in range(height):
            for j in range(width):
                if i + self.dy in range(height) and j + self.dx in range(width):
                    glcm[self.image[i, j, 0], self.image[i +
                                                         self.dy, j + self.dx, 0], 0] += 1
                    glcm[self.image[i, j, 1], self.image[i +
                                                         self.dy, j + self.dx, 1], 1] += 1
                    glcm[self.image[i, j, 2], self.image[i +
                                                         self.dy, j + self.dx, 2], 2] += 1
                    # print str(image[i,j,0]) + " " + str(image[i+dy,j+dx,0]) + "
                    # " + str(glcm[image[i,j,0],image[i+dy,j+dx,0],0])
                    x += 1
        glcm = glcm / x
        return glcm

    def contrast(self):
        contrast = np.zeros(3, np.float)
        meanI = np.zeros(3, np.float)
        meanJ = np.zeros(3, np.float)
        energy = np.zeros(3, np.float)
        homogenity = np.zeros(3, np.float)
        for i in range(256):
            for j in range(256):
                contrast[0] += pow(i - j, 2) * self.glcm[i, j, 0]
                contrast[1] += pow(i - j, 2) * self.glcm[i, j, 1]
                contrast[2] += pow(i - j, 2) * self.glcm[i, j, 2]
                meanI[0] += i * self.glcm[i, j, 0]
                meanI[1] += i * self.glcm[i, j, 1]
                meanI[2] += i * self.glcm[i, j, 2]
                meanJ[0] += j * self.glcm[i, j, 0]
                meanJ[1] += j * self.glcm[i, j, 1]
                meanJ[2] += j * self.glcm[i, j, 2]
                energy[0] += pow(self.glcm[i, j, 0], 2)
                energy[1] += pow(self.glcm[i, j, 1], 2)
                energy[2] += pow(self.glcm[i, j, 2], 2)
                homogenity[0] += self.glcm[i, j, 0] / (1 + abs(i - j))
                homogenity[1] += self.glcm[i, j, 1] / (1 + abs(i - j))
                homogenity[2] += self.glcm[i, j, 2] / (1 + abs(i - j))
        return contrast, meanI, meanJ, energy, homogenity

    def correlation(self):
        correlation = np.zeros(3, np.float)
        for i in range(256):
            for j in range(256):
                correlation[0] += ((i - self.meanI[0]) * (j - self.meanJ[0])
                                   * self.glcm[i, j, 0]) / (self.taoI[0] * self.taoJ[0])
                correlation[1] += ((i - self.meanI[1]) * (j - self.meanJ[1])
                                   * self.glcm[i, j, 1]) / (self.taoI[1] * self.taoJ[1])
                correlation[2] += ((i - self.meanI[2]) * (j - self.meanJ[2])
                                   * self.glcm[i, j, 2]) / (self.taoI[2] * self.taoJ[2])
                # print correlation;
        return correlation

    def tao(self):
        taoI = np.zeros(3, np.float)
        taoJ = np.zeros(3, np.float)
        for i in range(256):
            for j in range(256):
                taoI[0] += pow(i - self.meanI[0], 2) * self.glcm[i, j, 0]
                taoI[1] += pow(i - self.meanI[1], 2) * self.glcm[i, j, 1]
                taoI[2] += pow(i - self.meanI[2], 2) * self.glcm[i, j, 2]
                taoJ[0] += pow(j - self.meanJ[0], 2) * self.glcm[i, j, 0]
                taoJ[1] += pow(j - self.meanJ[1], 2) * self.glcm[i, j, 1]
                taoJ[2] += pow(j - self.meanJ[2], 2) * self.glcm[i, j, 2]
                # print str(taoJ[2])+" = "+ str(pow(j-meanJ[2],2)) + " x " + str(glcm[i,j,2])
        # print "taoi = "
        # print taoI
        # print "taoj = "
        # print taoJ
        for i in range(3):
            taoI[i] = math.sqrt(taoI[i])
            taoJ[i] = math.sqrt(taoJ[i])
        return taoI, taoJ

    def printglcm(self):

        print "meanI = " + str(rgb2gs(self.meanI))
        print "meanJ = " + str(rgb2gs(self.meanJ))
        print "taoI = " + str(rgb2gs(self.taoI))
        print "taoJ = " + str(rgb2gs(self.taoJ))
        print "kontras = " + str(rgb2gs(self.kontras))
        print "Energy = " + str(rgb2gs(self.energy))
        print "Homogenitas = " + str(rgb2gs(self.homogenity))
        print "Correlation = " + str(rgb2gs(self.korelasion))

    def writeglcm(self):
        with open("test.txt", "a") as myfile:
            myfile.write(str(rgb2gs(self.kontras)) + " " + str(rgb2gs(self.energy)) + " " +
                         str(rgb2gs(self.homogenity)) + " " + str(rgb2gs(self.korelasion)) + "\n")
        with open("type.txt", "a") as myfile:
            myfile.write(str(1) + ",\n")


def rgb2gs(rgb):
    val = 0.114 * (rgb[0]) + 0.587 * (rgb[1]) + 0.299 * (rgb[2])
    return val


if __name__ == '__main__':
    image = cv2.imread(sys.argv[1])
    glcm = GLCM(image, 0, 1)
    imglcm = glcm.glcm.astype(np.uint8)
    glcm.printglcm()
    glcm.writeglcm()

    # kontras, meanI, meanJ, energy, homogenity = contrast(glcm)
    # taoI, taoJ = tao(glcm, meanI, meanJ)
    # korelasion = correlation(glcm, meanI, meanJ, taoI, taoJ)
    # print "meanI = " + str(rgb2gs(glcm.meanI))
    # print "meanJ = " + str(rgb2gs(glcm.meanJ))
    # print "taoI = " + str(rgb2gs(glcm.taoI))
    # print "taoJ = " + str(rgb2gs(glcm.taoJ))
    # print "kontras = " + str(rgb2gs(glcm.kontras))
    # print "Energy = " + str(rgb2gs(glcm.energy))
    # print "Homogenitas = " + str(rgb2gs(glcm.homogenity))
    # print "Correlation = " + str(rgb2gs(glcm.korelasion))
    # print glcm

    # cv2.imshow("testing", imglcm)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
