
import struct
import numpy as np
import math
import random
# import matplotlib.pyplot as plt

class Solution():
    def __init__(self):
        self.trainimgset=None
        self.trainimglab=None
        self.testimglab=None
        self.testimgset=None
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
            # print im

            lable=struct.unpack_from('>784B' ,buffer_lab, index_lab)
            index_lab+=1
            lableset.append(lable[0])

            # fig = plt.figure()
            # plotwindow = fig.add_subplot(111)
            # plt.imshow(im , cmap='gray')
            # plt.show()
        return imageset, lableset

    def readtrain(self,numread):
        self.imgfile='/Users/liuxiyun/Dropbox/250BHW/train-images.idx3-ubyte'
        self.labfile='/Users/liuxiyun/Dropbox/250BHW/train-labels.idx1-ubyte'
        self.trainimgset,self.trainimglab=self.readfile(self.imgfile,self.labfile,numread)# 2 is the number of image I want to read
        self.numTrainImg=len(self.trainimgset)
        return

    def readtest(self,numread):
        self.imgfile='/Users/liuxiyun/Dropbox/250BHW/t10k-images.idx3-ubyte'
        self.labfile='/Users/liuxiyun/Dropbox/250BHW/t10k-labels.idx1-ubyte'
        self.testimgset,self.testimglab=self.readfile(self.imgfile,self.labfile,numread)
        self.numTestImg=len(self.testimgset)
        return


    def l2distance(self,trainimg,testimg):#img is an 28*28array
        temp=0
        for i in range(28):
            for j in range(28):
                temp+=(trainimg[i][j]-testimg[i][j])**2
        return math.sqrt(temp)
    def findRandomSubset(self,numTS):
        self.readtrain(1000)
        self.readtest(10)
        self.subsetimg=[]
        self.numSubImg=numTS
        self.subsetlab=[]

        for i in range(numTS):
            x=random.randrange(0,1000,1)
            self.subsetimg.append(self.trainimgset[x])
            self.subsetlab.append(self.trainimglab[x])
            if i%50==0:
                print "Have found ",i," subset elements."
        # print len(self.subsetlab)
        return


    # def findsubset(self):
    #     self.readtrain()
    #     self.readtest()
    #     for n in range(self.numTrainImg):# n is the index of image in trainset
    #         nnSubindex=None # the index of the image in subset that has the shortest distance with training image n
    #         shortestDis=20000000 # the shortest distance between n th traning image and every imge from subset(for now)
    #         for m in range(self.numSubImg): # m is the index of image in subset
    #             l2distance=self.l2distance(self.trainimgset[n],self.subsetimg[m])
    #             if l2distance<shortestDis:
    #                 shortestDis=l2distance
    #                 nnSubindex=m
    #
    #         # if it is the first image OR nearest prototype from subset has a different label than n th training img.
    #         # Add it to subset
    #         if nnSubindex==None or self.trainimglab[n]!=self.subsetlab[nnSubindex]:
    #             self.subsetimg.append(self.trainimgset[n]) #Add it to subset
    #             self.subsetlab.append(self.trainimglab[n])
    #             self.numSubImg+=1
    #             # print 'add'
    #         if n%100==0:
    #             print 'In progress!',"Have done ",n
    #             print 'The subset for now is ', self.subsetlab
    #     print "The number of subset is", self.numSubImg
    #     # print self.trainimglab
    #     # print self.subsetlab
    #     return

    def match(self,numWannamatch):
        matchright=0
        for n in range(numWannamatch):
            nnSubindex=None # the index of the image in subset that has the shortest distance with training image n
            shortestDis=20000000
            for m in range(self.numSubImg): # m is the index of image in subset
                l2distance=self.l2distance(self.testimgset[n],self.subsetimg[m])
                #l2distance=self.l2distance(self.subsetimg[n],self.subsetimg[m])
                if l2distance<shortestDis:
                    shortestDis=l2distance
                    nnSubindex=m
            if self.subsetlab[nnSubindex]==self.testimglab[n]:
            #if self.subsetlab[nnSubindex]==self.subsetlab[n]:
                matchright+=1
            if n%5==0:
                print 'Have matched ',n, " testset elements, and ",matchright,' is correct'
        print "Haha I match ",numWannamatch,' and match right ', matchright
        # print '--------------'
        # print nnSubindex
        # print "I guess the lable is ",self.subsetlab[nnSubindex]
        # print "It should be ",self.testimglab[0]
        # return

c=Solution()
c.findRandomSubset(100)
c.match(10)

# 1000: Haha I match  1000  and match right  879

# 10000: Haha I match  100  and match right  95;
# 5000: Have matched  100  testset elements, and  98  is correct,Haha I match  200  and match right  190
#