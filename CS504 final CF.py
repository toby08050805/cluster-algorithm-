#dsfsfsdfsdf
# -*- coding: UTF-8 -*-
import os
import csv
from array import array
from sre_compile import isstring
from _operator import invert
from ctypes.wintypes import CHAR
import time
from testpyson import whoScoreMovie
from multiprocessing.connection import answer_challenge


def main():
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
    tmpcounter=0
    K= 3
    pathProg ="D:/cs504 final data set"
    os.chdir(pathProg)
    #read data from training data set
    f =open('ratings_training_80.csv','r')
    data=[]
    for row in csv.reader(f):        
        data.append(row)
    f.close()
    
    
    arraytest= [[0 for x in range(0,movie)] for y in range(0,user)] #declare 2 dimentions [user][movie]array and initial valuse are 0  
    userDistance=[[9999 for x in range(0,user)] for y in range(0,user)] #declare users distance ,initial valu is 9999
    itemDistance=[[9999 for x in range(0,movie)] for y in range(0,movie)] #declare users distance ,initial valu is 9999
    userMeanScore= [0 for x in range(user)]
    userScoreSum=0
    datacount=0
    trainList=[[]for x in range(user)]
    #create a score and user matrix
    for y in range(len(data)):
        #new add
        trainList[int(data[y][0],10)].append(data[y][1])       # appand all movie number from test data set
        try:
            arraytest[int(data[y][0],10)][int(data[y][1],10)]=data[y][2]  #10 means decimal
        except:#if there has anything overflow, it will show at below
            print("the fault is %s %s" %(data[y][0], data[y][1]))
        userScoreSum=userScoreSum+float(data[y][2])
        datacount+=1
        if y!=len(data)-1:
            if data[y][0]!= data[y+1][0] :   #means next iteration will run diff user so need to caculate meAN
                userMeanScore[int(data[y][0],10)]=userScoreSum/datacount
                userScoreSum=0
                datacount=0
                #print(userMeanScore)
        else:
            userMeanScore[int(data[y][0],10)]=userScoreSum/datacount
            userScoreSum=0
            datacount=0
            #print(userMeanScore)
            
    
    
    
    #read the test data set to decide which distance i should caculate
    f =open('ratings_test_20.csv','r')
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
     
    
    predictScroe=[9999.99 for x in range(len(dataTest))]   #store the predict result
    predictCounter=0
    solution=[[] for x in range(len(dataTest))]
    solutionCounter=0
    #caculate distance beging
    
    for x in range(user):    
        #for y in range(x+1,671):  used to caculat
        #for s in range(2):# find predict movie
        for s in range(len(testList[x])):# find predict movie
            testSetList=whoScoreMovie(arraytest,testList[x][s])    #input a train dataset and movie, output who score that movie in test set
            #print(testList[x][s],testSetList)
            dicUserScor=[]
            for y in range(len(trainList[x])):#find the distance between need predict movie and and x user score movies             
                if len(testSetList)>0: 
                    if int(trainList[x][y],10)<=int(testList[x][s],10):#we just need to caculate upper triangle user in distance matrix.    
                        if itemDistance[int(trainList[x][y],10)][int(testList[x][s],10)] ==9999:# user x id<= user y id as normal
                            itemDistance[int(trainList[x][y],10)][int(testList[x][s],10)]= sim(testList[x][s],trainList[x][y], arraytest,userMeanScore,testSetList,x)
                
                        
                        #tmpdata.append(userDistance[x][testSetList[y]])
                    if int(trainList[x][y],10)>int(testList[x][s],10):
                        if itemDistance[int(trainList[x][y],10)][int(testList[x][s],10)] ==9999:# user x id<= user y id as normal
                            itemDistance[int(testList[x][s],10)][int(trainList[x][y],10)]= sim(testList[x][s],trainList[x][y], arraytest,userMeanScore,testSetList,x)
                    
                    #tmpdata.append(userDistance[testSetList[y]][x])
                    #build dictionary to sort the distance
                    
                    if int(trainList[x][y],10)<=int(testList[x][s],10):#we just need to caculate upper triangle user in distance matrix.  
                        if itemDistance[int(trainList[x][y],10)][int(testList[x][s],10)]>0:
                            dicUserScor.append([trainList[x][y],itemDistance[int(trainList[x][y],10)][int(testList[x][s],10)]])
                        #else:
                         #   print([trainList[x][y],itemDistance[int(trainList[x][y],10)][int(testList[x][s],10)]])
                    if int(trainList[x][y],10)>int(testList[x][s],10):#we just need to caculate upper triangle user in distance matrix.
                        if itemDistance[int(testList[x][s],10)][int(trainList[x][y],10)]>0:
                            dicUserScor.append([trainList[x][y],itemDistance[int(testList[x][s],10)][int(trainList[x][y],10)]])
                        #else:
                         #   print([trainList[x][y],itemDistance[int(testList[x][s],10)][int(trainList[x][y],10)]])
                    
                #sorted(tmpdata)
                #print(tmpdata)
                #sorting
                tmpcounter=tmpcounter+1
            #print(dicUserScor)
            
            
            movieScore=0
            simSum=0
            for count in range(len(dicUserScor)):
                movieScore= movieScore+float(arraytest[x][int(dicUserScor[count][0],10)])*dicUserScor[count][1]
                simSum=dicUserScor[count][1]+simSum
            try:  #in some situation all sim are less than 0
                if simSum==0:
                    predictScroe=0
                    #print(testList[x],user,trainList[x][y])
                else:
                    predictScore=round(movieScore/simSum,1)
            except:
                print(testList[x],x,len(dicUserScor))
            solution[solutionCounter].extend(dataTest[solutionCounter][0:3])
            solution[solutionCounter].append(predictScore)
            solutionCounter=solutionCounter+1
            #print(solution)
            #print(answer)
                    
           
            
    file = open(pathProg + '/rating_pre_cf20.csv', 'w',newline='')  
    svCursor = csv.writer(file) #write csv
    for y in range(len(solution)):
        svCursor.writerow(solution[y])
    
    file.close()
    print(tmpcounter)
    

    
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
def sim(item1,item2,traindata,usermean,ScoreMovie,predictuser):
    differenceI=0
    differenceJ=0
    sumI=0
    sumJ=0
    sumdiff=0
    item1= int(item1,10)
    item2= int(item2,10)
    meantmpI=[]
    meantmpJ=[]
    traindatatmpI=[]
    traindatatmpJ=[]
    #print(type(item1),type(traindata[0][0]),type(usermean[0]),type(ScoreMovie[0]))
    #print(item1,item2,usermean,whoScoreMovie,predictuser)
    
    for userCounter in range(len(ScoreMovie)):
        if float(traindata[ScoreMovie[userCounter]][item2])==0:
            continue  #ignore users who are not score movie J
        #else:
            #print(float(traindata[ScoreMovie[userCounter]][item2]),ScoreMovie[userCounter], item2)
        differenceI=float(traindata[ScoreMovie[userCounter]][item1])-float(usermean[ScoreMovie[userCounter]])
        #meantmpI.append(usermean[ScoreMovie[userCounter]])
        #traindatatmpI.append(traindata[ScoreMovie[userCounter]][item1])
        #if differenceI==0:
        #    print("I")
         #   print(ScoreMovie[userCounter],usermean[ScoreMovie[userCounter]],traindata[ScoreMovie[userCounter]][item1],float(usermean[ScoreMovie[userCounter]]),item1)
        differenceJ=float(traindata[ScoreMovie[userCounter]][item2])-float(usermean[ScoreMovie[userCounter]])
        #meantmpJ.append(usermean[ScoreMovie[userCounter]])
        #traindatatmpJ.append(traindata[ScoreMovie[userCounter]][item2])
        #if differenceJ==0:
         #   print("J")
          #  print(ScoreMovie[userCounter],usermean[ScoreMovie[userCounter]],traindata[ScoreMovie[userCounter]][item2],float(usermean[ScoreMovie[userCounter]]),item2)
        
            
        sumI=sumI+(differenceI*differenceI)
        sumJ=sumJ+(differenceJ*differenceJ)
        sumdiff=sumdiff+differenceI*differenceJ
    try:
        if(sumI==0 or sumJ==0):
            answer=-999
        else:    
            answer=sumdiff/((sumI*sumJ)**0.5)
        
    except:
        print(ScoreMovie)
        print(item1,item2,predictuser)
        print(meantmpI)
        print(traindatatmpI)
        print(meantmpJ)
        print(traindatatmpJ)
        
        
         
    #print("%d %d:sumi is %d, sumj is %d sumdiff is %d answer:%f"%(item1,item2,sumI,sumJ,sumdiff,answer))
    
    #return sumdiff/((sumI*sumJ)**0.5)
    return answer  
      
if __name__=='__main__':
    main()