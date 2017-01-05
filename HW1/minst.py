__author__ = 'liuxiyun'
import struct
import numpy as np
import math
import matplotlib.pyplot as plt
import random
class Solution():
    def __init__(self):
        self.trainingImage=None
        self.trainingLabel=None
        self.testingLabel=None
        self.testingImage=None
        self.numTrainImg=0
        self.numTestImg=0
        self.subsetimg=[]
        self.numSubImg=0
        self.subsetlab=[]

    def readfile(self,imgfile,labfile,numImg):# help function

        binfile_img=open(imgfile,'rb')
        buffer_img=binfile_img.read()
        binfile_img.close()

        binfile_lab=open(labfile,'rb')
        buffer_lab=binfile_lab.read()
        binfile_img.close()

        imageset=[]
        lableset=[]
        index_img=16
        index_lab=8
        # magic, numImages , numRows , numColumns = struct.unpack_from('>IIII' , buffer_img , index_img)
        # index_img += struct.calcsize('>IIII')

        for i in range(numImg):
            im = struct.unpack_from('>784B' ,buffer_img, index_img)
            index_img += 784

            im = np.array(im)
            im = im.reshape(28,28)

            imageset.append(im)

            lable=struct.unpack_from('>784B' ,buffer_lab, index_lab)
            index_lab+=1
            lableset.append(lable[0])

            # fig = plt.figure()
            # plotwindow = fig.add_subplot(111)
            # plt.imshow(im , cmap='gray')
            # plt.show()
        return imageset, lableset

    def readtrain(self):
        self.imgfile='/Users/liuxiyun/Dropbox/250BHW/train-images.idx3-ubyte'
        self.labfile='/Users/liuxiyun/Dropbox/250BHW/train-labels.idx1-ubyte'
        self.trainingImage,self.trainingLabel=self.readfile(self.imgfile,self.labfile,55000)# 2 is the number of image I want to read
        self.numTrainImg=len(self.trainingImage)
        return

    def readtest(self):
        self.imgfile='/Users/liuxiyun/Dropbox/250BHW/t10k-images.idx3-ubyte'
        self.labfile='/Users/liuxiyun/Dropbox/250BHW/t10k-labels.idx1-ubyte'
        self.testingImage,self.testingLabel=self.readfile(self.imgfile,self.labfile,3000)
        self.numTestImg=len(self.testingImage)
        return

    def l2distance(self,trainimg,testimg):#img is an 28*28array
        temp=0
        for i in range(28):
            for j in range(28):
                temp+=(trainimg[i][j]-testimg[i][j])**2
        return math.sqrt(temp)

    def findsubset(self,numNeed):
        self.readtrain()
        self.readtest()
        for n in range(self.numTrainImg):# n is the index of image in trainset
            nnSubindex=None # the index of the image in subset that has the shortest distance with training image n
            shortestDis=20000000 # the shortest distance between n th traning image and every imge from subset(for now)
            for m in range(self.numSubImg): # m is the index of image in subset
                l2distance=self.l2distance(self.trainingImage[n],self.subsetimg[m])
                if l2distance<shortestDis:
                    shortestDis=l2distance
                    nnSubindex=m


            # if it is the first image OR nearest prototype from subset has a different label than n th training img.
            # Add it to subset
            if nnSubindex==None or self.trainingLabel[n]!=self.subsetlab[nnSubindex]:
                self.subsetimg.append(self.trainingImage[n]) #Add it to subset
                self.subsetlab.append(self.trainingLabel[n])
                self.numSubImg+=1
                # print 'add'
            if self.numSubImg==numNeed:
                print "Need randomly find subset element"
                break
            if n%100==0:
                print "Have done ",n," Training set element"
                print self.numSubImg,' subset elements for now are found '
                print "--------------------------------------"
        self.findRandomSubset(numNeed-self.numSubImg)
        print "The number of subset is", self.numSubImg
        # print self.trainimglab
        # print self.subsetlab
        return

    def findRandomSubset(self,numNeed):
        self.readtrain()
        self.readtest()

        for i in range(numNeed):
            x=random.randrange(0,55000,1)
            self.subsetimg.append(self.trainingImage[x])
            self.subsetlab.append(self.trainingLabel[x])
            self.numSubImg+=1
        # print len(self.subsetlab)
        return

    def match(self,numWannamatch):
        matchright=0
        for n in range(numWannamatch):
            nnSubindex=None # the index of the image in subset that has the shortest distance with training image n
            shortestDis=20000000
            for m in range(self.numSubImg): # m is the index of image in subset
                l2distance=self.l2distance(self.testingImage[n],self.subsetimg[m])
                #l2distance=self.l2distance(self.subsetimg[n],self.subsetimg[m])
                if l2distance<shortestDis:
                    shortestDis=l2distance
                    nnSubindex=m
            if self.subsetlab[nnSubindex]==self.testingLabel[n]:
            #if self.subsetlab[nnSubindex]==self.subsetlab[n]:
                matchright+=1
            if n%100==0:
                print 'Have matched ',n, " testset elements, and ",matchright,' is correct'
        print "Haha I match ",numWannamatch,' and match right ', matchright
        # print '--------------'
        # print nnSubindex
        # print "I guess the lable is ",self.subsetlab[nnSubindex]
        # print "It should be ",self.testimglab[0]
        # returnf
#
# c=Solution()
# c.findsubset(1000)
# c.match(1000)

# 5000TS: The number of subset is 755
# Haha I match  300  and match right  254

# 1000TS: The number of subset is 228
# Haha I match  1000  and match right  777

# I found 1000subset, Haha I match  1000  and match right  860
