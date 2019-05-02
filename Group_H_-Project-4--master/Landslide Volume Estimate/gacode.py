import numpy as np
import array 
from hillshade import hillshade
import math
import pandas as pd
import imageio
import csv


from openpyxl import *

def corr2(x,y):
    meanx=np.mean(x)*np.ones(x.shape)
    meany=np.mean(y)*np.ones(y.shape)
    x=np.subtract(x,meanx)
    y=np.subtract(y,meany)
    dividend=np.sum(np.multiply(x,y))
    divisor=math.sqrt(np.sum(np.square(x))*np.sum(np.square(y)))
    result=dividend/divisor
    return result


def gacode(post,pre,az,al):
    #matrix_x variable is for entering the width of matrix
    matrix_x=40

    #matrix_y variable is for entering the height of matrix
    matrix_y=40

    #importin predtm and postdtm
    #predtm= load_workbook(filename='D:\Study\sem 4\scope\matlb_landslide\postdtm.xlsx')
    #postdtm= load_workbook(filename='D:\Study\sem 4\scope\matlb_landslide\predtm.xlsx')
    predtm = pd.read_excel(pre,header=None,index_col=None)
    predtm.as_matrix()
    postdtm = pd.read_excel(post,header=None,index_col=None)
    postdtm.as_matrix()

    #azimuth
    if az==-1:
        az=135
    if int(al)==-1:
        al=100

    ar=np.arange(0,40)
    arx=np.arange(0,matrix_x)
    ary=np.arange(0,matrix_y)

    postimg=hillshade(postdtm,az,al,-1)

    pcsumxy=matrix_y*matrix_x-3

    generations=int(100000)

    populations=int(30)

    rang = int(100)

    delta = np.zeros((matrix_x,matrix_y,populations))
    for i in range(0,populations):
        delta[:,:,i]=np.random.rand(matrix_y,matrix_x)*rang*2-rang
    best=np.zeros(generations)
    for i in range(0,generations):
        # now_generations_count=i         
        pctime=0

        # pc variable refers to the probability of crossover
        pc=0.8
        if (pc > np.random.rand()):
        
            # pcrandnew1 variable and pcrandnew2 variable are the places for new chromosomes
            pcrandnew1=20
            pcrandnew2=21
            

            # each crossover supplies two new chromosomes
            for j in range(18,20):
                delta[:,:,j]=np.random.rand(matrix_y,matrix_x)*rang*2-rang 

            #each crossover produces two new chromosomes
            while(pctime < 5):

                    pcrandbest1=round(np.random.rand()*(19))
                    pcrandbest2=round(np.random.rand()*(19))

                    pcrandpoint1=1+round(np.random.rand()*(pcsumxy))
                    pcrandpoint2=1+round(np.random.rand()*(pcsumxy))

                    selecttemp1=delta[:,:,pcrandbest1] 
                    selecttemp2=delta[:,:,pcrandbest2]

                    selecttemp3=np.zeros((matrix_x*matrix_y,))
                    selecttemp4=np.zeros((matrix_x*matrix_y,))

                    j=0
                    for k in range(0,matrix_x*matrix_y,matrix_x):
                        blk1=selecttemp1[j]
                        blk2=selecttemp2[j]
                        selecttemp3[k:k+matrix_x]=np.asarray(blk1)
                        selecttemp4[k:k+matrix_x]=np.asarray(blk2)
                        j=j+1


                    selecttemp1=np.transpose(selecttemp3) 
                    selecttemp2=np.transpose(selecttemp4)

                    if (pcrandpoint1 > pcrandpoint2):
                        pctemp = pcrandpoint2
                        pcrandpoint2 = pcrandpoint1
                        pcrandpoint1 = pctemp
                    
                
                    for j in range(pcrandpoint1,pcrandpoint2+1):    
                        pctemp=selecttemp1[j]                  
                        selecttemp1[j]=selecttemp2[j]
                        selecttemp2[j]=pctemp  

                    delta[:,:,pcrandnew1]=np.reshape(selecttemp1,(matrix_y,matrix_x))
                    delta[:,:,pcrandnew2]=np.reshape(selecttemp2,(matrix_y,matrix_x))

                    pcrandnew1=pcrandnew1+2
                    pcrandnew2=pcrandnew2+2
                    pctime=(pctime+1)
            


        pmtime=0

        #pm variable refers to the probability of mutation
        pm=0.06
        t=np.zeros(18)
        for j in range(1,18):
            t[j]=np.random.rand()
    
            if(pm > t[j]):
                pmx=round(np.random.rand()*(matrix_x-1))
                pmy=round(np.random.rand()*(matrix_y-1))  
            
                pmvolue=delta[pmy,pmx,j]+(np.random.rand()*rang*2-rang)

                while (abs(pmvolue) > rang):
                    pmvolue=delta[pmy,pmx,j]+(np.random.rand(1)*rang*2-rang)
                
                delta[pmy,pmx,j]=pmvolue
        
        shadow = np.zeros((matrix_x,matrix_y,populations))
        for j in range(0,populations):
            shadow[:,:,j]=hillshade(np.add(predtm,delta[:,:,j]),az,al,-1) 
    
        F=np.zeros(populations)
        #calculates fitness function
        for j in range(0,populations):
            F[j]=corr2(shadow[:,:,j],postimg)  

        indexF=np.argsort(F)
        
        delta_temp=np.zeros((matrix_x,matrix_y,populations))
        shadow_temp=np.zeros((matrix_x,matrix_y,populations))
        for j in range(0,populations):
            delta_temp[:,:,j]=delta[:,:,indexF[populations-j-1]]
            shadow_temp[:,:,j]=shadow[:,:,indexF[populations-j-1]] 
    
        for j in range(0,populations):
            delta[:,:,j]=delta_temp[:,:,j]
            shadow[:,:,j]=shadow_temp[:,:,j] 

        
        best[i]=np.max(F)


    bestrange=delta[:,:,1]

    #filter
    bestdtm=np.add(predtm,bestrange)
    print(bestdtm.shape)

    bestrange_filter=np.zeros(bestdtm.shape)
    for i in range(0,bestdtm.shape[0],12):
        for j in range(0,bestdtm.shape[1],12):
            block=bestdtm.iloc[i:i+12,j:j+12]
            bestrange_filter[i:i+12,j:j+12]=np.median(block)*np.ones(block.shape)


        
    for y in range(0,matrix_y):
        for x in range(0,matrix_x):
            if (bestrange_filter[y,x]==0):
                bestrange_filter[y,x]=bestdtm[y,x]

    end_predtm=np.zeros((matrix_y-6,matrix_x-6))
    end_postdtm=np.zeros((matrix_y-6,matrix_x-6))
    end_filter=np.zeros((matrix_y-6,matrix_x-6))
    end_bestrange=np.zeros((matrix_y-6,matrix_x-6))
    for y in range(3,matrix_y-3):
        for x in range(3,matrix_x-3):
            end_bestrange[y-3,x-3]=bestrange[y,x]

    for y in range (3,matrix_y-3):
        for x in range(3,matrix_x-3):
            end_filter[y-3,x-3]=bestrange_filter[y,x]

    for y in range (3,matrix_y-3):
        for x in range (3,matrix_x-3):
            end_predtm[y-3,x-3]=predtm.iloc[y,x]

    for y in range (3,matrix_y-3):
        for x in range (3,matrix_x-3):
            end_postdtm[y-3,x-3]=postdtm.iloc[y,x]

    X_estimate=end_filter[16,:]
    X_predtm=end_predtm[16,:]
    X_postdtm=end_postdtm[16,:]

    Y_estimate=end_filter[:,16]  
    Y_predtm=end_predtm[:,16]
    Y_postdtm=end_postdtm[:,16]

    truedepth_del=0
    truedepth_add=0
    estimatedepth_del=0
    estimatedepth_add=0   

    for y in range(0,matrix_y-6):      
        for x in range(0,matrix_x-6):
            if (end_predtm[y,x] > end_postdtm[y,x]):
                truedepth=end_predtm[y,x]-end_postdtm[y,x]
                truedepth_del=truedepth+truedepth_del 
            if (end_predtm[y,x] < end_postdtm[y,x]):
                truedepth=end_postdtm[y,x]-end_predtm[y,x]
                truedepth_add=truedepth+truedepth_add 

    volume_true_del=((truedepth_del))
    volume_true_add=((truedepth_add))


    for y in range(0,matrix_y-6):
        for x in range(0,matrix_x-6):
            if (end_predtm[y,x] > end_filter[y,x]):
                estimatedepth=end_predtm[y,x]-end_filter[y,x]
                estimatedepth_del=estimatedepth+estimatedepth_del
    
            if (end_predtm[y,x] < end_filter[y,x]):
                estimatedepth=end_filter[y,x]-end_predtm[y,x]
                estimatedepth_add=estimatedepth+estimatedepth_add

    volume_estimate_del=((estimatedepth_del))
    volume_estimate_add=((estimatedepth_add))


    #output result

    best_h=hillshade(np.add(predtm,bestrange),az,al,-1)
    new_h=hillshade(postdtm,az,al,-1)
    #convert postimg,best_h,new_h to img and show
    '''
    img1 = PIL.Image.fromarray(postimg)
    img2 = PIL.Image.fromarray(best_h)
    img3 = PIL.Image.fromarray(new_h)
    cv2.imshow("post-event remote sensing image",img1)
    cv2.imshow("estimate result shadow image",img2)
    cv2.imshow("post-event DTM shadow image",img3)
    '''
    imageio.imwrite("post-eventDTM.png",new_h)
    imageio.imwrite("estimate-result.png",best_h)

    error=(abs(volume_true_del-volume_estimate_del)/volume_true_del)*100
    row=[generations,volume_estimate_del,error]
    change=predtm-postdtm

    with open('data.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)
    csvFile.close()
    return(volume_estimate_del,error,change)
