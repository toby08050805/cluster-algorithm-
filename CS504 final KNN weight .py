#dsfsfsdfsdf
# -*- coding: UTF-8 -*-
import os
import csv
from array import array
from sre_compile import isstring
from _operator import invert
from ctypes.wintypes import CHAR
import time


def main():
   
    tStart = time.time()
    KNN()
    tEnd = time.time()
    print("It cost %f sec" % (tEnd - tStart))
    #window will automatically add change line when line is end, this fuction as well so need to give new line variable = ""
    #file = open(pathProg + '\exportExample.csv', 'w',newline='')  
    #svCursor = csv.writer(file) #write csv
    #svCursor.writerow()
    
    # initialize path ,usernumer and movie  number.
def KNN():
    distancallCount=0
    viewdistance=0
    tmpcounterk=0
    user=670+1
    movie=9065+1
    K= 10
    pathProg ="D:/cs504 final data set"
    os.chdir(pathProg)
    #read data from training data set
    f =open('ratings_training_90.csv','r')
    data=[]
    for row in csv.reader(f):        
        data.append(row)
    f.close()
    
    
    arraytest= [[0 for x in range(0,movie)] for y in range(0,user)] #declare 2 dimentions [user][movie]array and initial valuse are 0  
    userDistance=[[9999 for x in range(0,user)] for y in range(0,user)] #declare users distance ,initial valu is 9999
    
    
    #create a score and user matrix
    for y in range(len(data)):
        arraytest[int(data[y][0],10)][int(data[y][1],10)]=data[y][2]  #10 means decimal
        
    
    #read the test data set to decide which distance i should caculate
    f =open('ratings_test_10.csv','r')
    dataTest=[]
    #testList=[0 for x in range(user)]
    testList=[[] for x in range(user)]     # two dimention list to record the test set movie scored by user  [user][the movies they score]
    for row in csv.reader(f):              
        dataTest.append(row)
    f.close()

    for x in range(len(dataTest)):
       testList[int(dataTest[x][0],10)].append(dataTest[x][1])       # appand all movie number from test data set
  
    predictScroe=[9999.99 for x in range(len(dataTest))]   #store the predict result
    predictCounter=0
    #caculate distance beging
    for x in range(user):    
        for s in range(len(testList[x])):
            testSetList=whoScoreMovie(arraytest,testList[x][s])    #input a train dataset and movie, output who score that movie in test set
            #print(testList[x][s],testSetList)
            dicUserScor={}
            for y in range(len(testSetList)):# find the distance between user x and the user who score movie i                
                if testSetList[y]: 
                    if x<=testSetList[y]:#we just need to caculate upper triangle user in distance matrix.
                        if userDistance[x][testSetList[y]] ==9999:# user x id<= user y id as normal
                            userDistance[x][testSetList[y]]= distance(arraytest[x],arraytest[testSetList[y]])
                            distancallCount=distancallCount+1
                        #tmpdata.append(userDistance[x][testSetList[y]])
                    if x>testSetList[y]:
                        if userDistance[testSetList[y]][x] ==9999:#user x id> user y id exchange their position
                            userDistance[testSetList[y]][x]= distance(arraytest[x],arraytest[testSetList[y]])
                            distancallCount=distancallCount+1
                    #tmpdata.append(userDistance[testSetList[y]][x])
                    #build dictionary to sort the distance
                    if x<=testSetList[y]: 
                        dicUserScor[testSetList[y]]=userDistance[x][testSetList[y]]
                        viewdistance=viewdistance+1
                    if x>testSetList[y]:
                        dicUserScor[testSetList[y]]=userDistance[testSetList[y]][x]
                        viewdistance=viewdistance+1
                        
                #sorted(tmpdata)
                #print(tmpdata)
                #sorting
            
            sort = [(k, dicUserScor[k]) for k in sorted(dicUserScor, key=dicUserScor.get)]
            
            #=====================caculate weight beg
            
            
            #=====================caculate weight end
            sum=0
            sumd=0
            
            if(K>len(sort)):
                counterk=len(sort)
                #=====================caculate weight beg
                d=sort[counterk-1][1]
                #=====================caculate weight end
            else:
                counterk=K
                d=sort[K-1][1]
                
            for count in range(counterk):
                #count mean the # of close customer                    #caculate weight beg
                if(count!=0):  #the nearest recaord weight is 1
                    weight= (sort[counterk-1][1]-sort[count][1])/(sort[counterk-1][1]-sort[0][1])
                else:
                    weight=1
                #caculate weight end
                    
                sum=float(arraytest[sort[count][0]][int(testList[x][s],10)])*weight*d+sum
                    #sum=float(arraytest[sort[1][0]][int(testList[14][37],10)])*weight*d+sum
                sumd=weight*d+sumd
            predictScroe[predictCounter]=round(sum/sumd,1)
            predictCounter=predictCounter+1
            tmpcounterk=tmpcounterk+counterk
    Solution=[[] for listcout in range(len(predictScroe))]                    
    for zz in range(len(predictScroe)):        
        Solution[zz].extend(dataTest[zz][0:3])
        Solution[zz].append(predictScroe[zz])    
    file = open(pathProg + '/rating_pre_k5_w.csv', 'w',newline='')  
    svCursor = csv.writer(file) #write csv
    for y in range(len(Solution)):
        svCursor.writerow(Solution[y])
    
    file.close()
    print(K,distancallCount,viewdistance,tmpcounterk)
def distance(u1, u2):      #caculate Euclidean Distance
    if len(u1)!= len(u2):
        print("two vector must at same length")
        return -1
    else:
        sum=0
        for x in range(0,len(u1)):
            if(float(u1[x])!=0 or float(u2[x]!=0)):
                u3=(float(u1[x])-float(u2[x]))**2
                sum=sum+u3
            #print(sum)
        sum=sum**0.5 
        #print("the sum is %d" %(sum))
        return sum
    
    

def whoScoreMovie(traindata,scoreMovie):
    userList=[0 for x in range(671)]
    users=[]
    
    #for y in range(len(scoreMovie)):
    for x in range(len(traindata)):
        if float(traindata[x][int(scoreMovie,10)])>0:
                #print(scoreMovie,float(traindata[x][int(scoreMovie,10)]),x)
            users.append(x)
                #userList[x]=1
    
    #for x in range(len(userList)):
     #   if userList[x]==1:
      #      users.append(x)
    #print(users)       
    return users
    
if __name__=='__main__':
    main()