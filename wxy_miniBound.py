#!/usr/bin/env python
#coding=utf-8

import numpy as np
#import matplotlib as mpl
#from matplotlib import cm
import matplotlib.pyplot as plt
import math
import os
#import pylab as pl
from pathlib import Path

class Distance():
    def __init__(self):
        self.path = os.getcwd();

    def getElementinfo(self):

        infile = open(os.getcwd() + "/POSCAR")
        string = infile.readline()  # poscar name

        string = infile.readline()
        latticeConstant = float(string)  # latticeConstant

        latticeVec = np.array([]) # lattice vector
        for i in range(0, 3):
            string = infile.readline()
            temp = np.array([float(s0)*latticeConstant for s0 in string.split()])
            if (latticeVec.size == 0):  # if latticeVec is empty
                latticeVec = temp
            else:
                latticeVec = np.vstack([latticeVec, temp])

        # elements
        elementName = os.popen("sed -n 6p POSCAR").readline().split()
        string = infile.readline()
        string = infile.readline()
        elementAmount = np.array([int(s0) for s0 in string.split()])

        # coordinate
        string = infile.readline() # jump labe "Direct"
        coordinate = np.array([])
        for i in range(0, sum(elementAmount)):
            string = infile.readline()
            temp = np.array([float(s0) for s0 in string.split()])
            if (coordinate.size == 0):
                coordinate = temp
            else:
                coordinate = np.vstack([coordinate, temp])

        # change fraction to Descartes
        for i in range(0, coordinate.shape[0]):  #  witch line
            temp = 0
            for j in range(0, coordinate.shape[1]):  #  witch colume
                temp += coordinate[i][j]*latticeVec[j]*latticeConstant  #  Descartes row vector
            coordinate[i] = temp
        
        return elementName, elementAmount, coordinate

    def calculateDistance(self):
        miniDist = []
        dist = []
        elementName, elementAmount, coordinate = self.getElementinfo()
        for i in range(0, elementAmount[0]):
            for j in range(elementAmount[0] + elementAmount[1], sum(elementAmount)):
                tmp = coordinate[i] - coordinate[j]
                dist.append(math.sqrt(math.pow(tmp[0], 2) + math.pow(tmp[1], 2) + math.pow(tmp[2], 2)))
                #print i, j, coordinate[i], coordinate[j], dist  #Debug
        #print("mini bond of", elementName[0] + "-" + elementName[2], "is", min(dist)) 
        miniDist.append(min(dist))

        dist = []
        elementName, elementAmount, coordinate = self.getElementinfo()
        for i in range(elementAmount[0], elementAmount[0] + elementAmount[1]):
            for j in range(elementAmount[0] + elementAmount[1], sum(elementAmount)):
                tmp = coordinate[i] - coordinate[j]
                dist.append(math.sqrt(math.pow(tmp[0], 2) + math.pow(tmp[1], 2) + math.pow(tmp[2], 2)))
                #print i, j, coordinate[i], coordinate[j], dist  #Debug
        #print("mini bond of", elementName[1] + "-" + elementName[2], "is", min(dist)) 
        miniDist.append(min(dist))

        return miniDist

    def calculateALL(self):
        rootDir = os.getcwd()
        fileDirs = os.listdir(rootDir)
        #print(fileDirs)  #Debug

        MiniDistData = open("MiniDistData.dat",'w')
        for file in fileDirs:
            if os.path.exists(rootDir + '/' + file + '/band/POSCAR'):
                os.chdir(rootDir + '/' + file + '/band')
                #print(os.getcwd())
                for n in self.calculateDistance():
                    MiniDistData.write(str(n) + ' ')
                #MiniDistData.write('\n')
                Gap = os.popen('cp ~/scripts/cbvb.x ./; ./cbvb.x')
                #for line in Gap.readlines():
                #    print(line)
                #print(Gap.readline())
                MiniDistData.write(str(Gap.readline().split()[2]))
                MiniDistData.write('\n')
                
        MiniDistData.close()
        os.chdir('../../')

    def plotALL(self):
        #print(os.getcwd())
        #os.chdir('../../')
        #print(os.getcwd())
        datafile = 'MiniDistData.dat'
        x = []
        y = []
        z = []
        f = open(datafile)
        # read data
        for line in f:
            line = line.strip('\n')
            line = line.split(' ')

            x.append(float(line[2]))
            y.append(float(line[0]))
            z.append(float(line[1]))

        f.close
        
        ax1 = plt.subplot(121)
        ax1.scatter(x, y, marker='o', label='Ag-S bond distance')
        plt.ylim(2.5, 2.7)
        plt.xlim(0, 1.0)
        plt.legend()

        ax2 = plt.subplot(122)        
        ax2.scatter(x, z, marker='o',color='r', label='Bi-S bond distance')
        plt.ylim(2.3, 2.7)
        plt.xlim(0, 1.0)
        plt.legend()

        plt.savefig('atomDist.jpg')

        plt.show()



        

    
#print(Distance().calculateDistance())
Distance().calculateALL()
Distance().plotALL()


