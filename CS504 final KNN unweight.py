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
    """
    #basic I/O
    print("123")    
    print(1+1)
    print('this is test \'s sdadas')   # 'is special character
    print  ("dsfsdfsdfsf" + os.getcwd())
    print ('line 7'+'=' * 10)
    counter=0
    counter+=1
    print (counter)
    test=['x','y']
    food=['a','b','c',test]
    print(food[3][1])
    for i in range(1,10):
        print(i)
        print('s')

    foo(50,20)
    
    #change data to int
    print(int("101", 16))
    print(int("101", 10))
    print(int("101", 8))
    print(int("101", 2))
    print(int(22.01))
    print(int(32.56))
    print(int(float("11.0")))
    print(int(float("36.9")))
    print(int(float("33.4")))
    """
    """
    # test sub function
    x=[2,3,0,0,5]
    y=[3,4,0,1,0]
    sum=distance(x, y)
    print(sum)
    """
    """
    #print all data we read
    for y in range(len(data)):
        print(data[y])
    print(data[1][3])
    """
    
    """
    #dictionary test
    mydict = dict(a=1, b=2, c=3)
    listd=[1,3,4]
    x=5
    #print(type(listd[0]),type(x))
    mydict[listd[2]]=listd[0]
    keylist=mydict.keys()
    #print(keylist)
    #keylist=sorted(keylist, key=lambda x:x[1],reverse=True)
    s = [(k, mydict[k]) for k in sorted(mydict, key=mydict.get, reverse=True)]
    #for key in keylist:
     #   print ("%s: %s %s" % (key, mydict[key]))
    print(s)
    """
    
    """
    pathProg ="D:/cs504 final data set"
    os.chdir(pathProg)
    f =open('distace2.csv','r')
    distace=[]
    #testList=[0 for x in range(user)]
    for row in csv.reader(f):        
        distace.append(row)
    f.close()
    """
    #print(round(5.25,1))
    tStart = time.time()
    readdata()
    tEnd = time.time()
    print("It cost %f sec" % (tEnd - tStart))
    #window will automatically add change line when line is end, this fuction as well so need to give new line variable = ""
    #file = open(pathProg + '\exportExample.csv', 'w',newline='')  
    #svCursor = csv.writer(file) #write csv
    #svCursor.writerow()
    
    # initialize path ,usernumer and movie  number.
def readdata():
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
        try:
            arraytest[int(data[y][0],10)][int(data[y][1],10)]=data[y][2]  #10 means decimal
        except:#if there has anything overflow, it will show at below
            print("the fault is %s %s" %(data[y][0], data[y][1]))
    
    #for x in range(len(userDistance)):
    
    """ test function
    print(arraytest[0][1])
    scoreMovie=["1","2","3"]
    userlist=whoScoreMovie(arraytest,scoreMovie)
    print(userlist)
    """
    
    #read the test data set to decide which distance i should caculate
    f =open('ratings_test_10.csv','r')
    dataTest=[]
    #testList=[0 for x in range(user)]
    testList=[[] for x in range(user)]     # two dimention list to record the test set movie scored by user  [user][the movies they score]
    for row in csv.reader(f):              
        dataTest.append(row)
    f.close()
    
    #testList[int(dataTest[0][0],10)].append("x")
    #print(testList[int(dataTest[0][0],10)])
    
    for x in range(len(dataTest)):
       testList[int(dataTest[x][0],10)].append(dataTest[x][1])       # appand all movie number from test data set
       
    """
    for x in range(len(testList)):
        print("movie %d %s" %(x,testList[x]))
    """

    
    predictScroe=[9999.99 for x in range(len(dataTest))]   #store the predict result
    predictCounter=0
    #caculate distance beging
    for x in range(user):    
        #for y in range(x+1,671):  used to caculat
        for s in range(len(testList[x])):
            testSetList=whoScoreMovie(arraytest,testList[x][s])    #input a train dataset and movie, output who score that movie in test set
            #print(testList[x][s],testSetList)
            dicUserScor={}
            for y in range(len(testSetList)):# find the distance between user x and the user who score movie i                
                if testSetList[y]: 
                    if x<=testSetList[y]:#we just need to caculate upper triangle user in distance matrix.
                        if userDistance[x][testSetList[y]] ==9999:# user x id<= user y id as normal
                            userDistance[x][testSetList[y]]= distance(arraytest[x],arraytest[testSetList[y]])
                        
                        #tmpdata.append(userDistance[x][testSetList[y]])
                    if x>testSetList[y]:
                        if userDistance[testSetList[y]][x] ==9999:#user x id> user y id exchange their position
                            userDistance[testSetList[y]][x]= distance(arraytest[x],arraytest[testSetList[y]])
                    
                    #tmpdata.append(userDistance[testSetList[y]][x])
                    #build dictionary to sort the distance
                    if x<=testSetList[y]: 
                        dicUserScor[testSetList[y]]=userDistance[x][testSetList[y]]
                    if x>testSetList[y]:
                        dicUserScor[testSetList[y]]=userDistance[testSetList[y]][x]
                        
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
                #d=sort[counterk-1][1]
                #=====================caculate weight end
            else:
                counterk=K
                #d=sort[K-1][1]
                
            for count in range(counterk):
                try:
                    #caculate weight beg
                    #if(count!=0):
                     #   weight= (sort[K-1][1]-sort[count][1])/(sort[K-1][1]-sort[0][1])
                    #else:
                     #   weight=1
                    #caculate weight end
                    sum=float(arraytest[sort[count][0]][int(testList[x][s],10)])+sum
                    #sumd=weight*d+sumd
                except:
                    print(sort[count][0],int(testList[x][s],10))
                    print(count,x,s)
                #print(sort[count][1])
            #unweight    
            #predictScroe[predictCounter]=round(sum/counterk,1)
            #weight
            try:
                predictScroe[predictCounter]=round(sum/counterk,1)
            except:
                print(weight,d)
            #print(predictScroe[predictCounter])
            predictCounter=predictCounter+1
            #print(x,testList[x][s],sort)    
                   
        #print("=======================") 
           
    Solution=[[] for listcout in range(len(predictScroe))]                    
    for zz in range(len(predictScroe)):
        try:
            Solution[zz].extend(dataTest[zz][0:3])
            Solution[zz].append(predictScroe[zz])
        except:
            print(zz,len(predictScroe),len(dataTest),predictCounter)
            
    file = open(pathProg + '/rating_pre_k10_uw.csv', 'w',newline='')  
    svCursor = csv.writer(file) #write csv
    for y in range(len(Solution)):
        svCursor.writerow(Solution[y])
    
    file.close()
    """
    Solution[0].extend(dataTest[0][0:3])
    Solution[0].append(predictScroe[0])
    print(dataTest[0][0:3])
    print(Solution)
    """
    #print(Solution[0])
    #appen the predict value after test set 
    """       
    file = open(pathProg + '\distace3.csv', 'w',newline='')  
    svCursor = csv.writer(file) #write csv
    for y in range(len(userDistance)):
        svCursor.writerow(userDistance[y])
    
    file.close()
    file = open(pathProg + '\exportExample3.csv', 'w',newline='')  
    svCursor = csv.writer(file) #write csv
    for y in range(len(arraytest)):
        svCursor.writerow(arraytest[y])
    
    file.close()
    """
    
    #for y in range(len(arraytest)):
        #for x in range(len(arraytest[y])):
            #if(arraytest[y][x]!=0):
               # print("%d,%d"%(y,x))
    
    #print("the result is'\n")
    #print(arraytest[1][30])
    #print(arraytest[0])
    #for x in range(len(data)):
     #   if(arraytest[data[x][2]]>0):
      #      for y in range(len(data)):
       #         if(data[y][2]>0):
    #print(arraytest)
    
    #for z in range(0,100):
     #   for y in range(0,100):
      #      arraytest[z][y]=-1
    

def foo(v1,v2):
    vt=v1+v2
    if(vt<50):
        print("foo")
    elif(vt<100):
        print("bar")
    else:
        print("big")
        
    return vt
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