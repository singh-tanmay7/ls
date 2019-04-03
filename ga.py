import numpy as np
import array 
import openpyxl 

from openpyxl import *



#matrix_x variable is for entering the width of matrix
matrix_x=40

#matrix_y variable is for entering the height of matrix
matrix_y=40

#importin predtm and postdtm
predtm= load_workbook(filename='D:\Study\sem 4\scope\matlb_landslide\postdtm.xlsx')
postdtm= load_workbook(filename='D:\Study\sem 4\scope\matlb_landslide\predtm.xlsx')


#azimuth
az=135

a1=100

ar=np.arange(0,40)
arx=np.arange(0,matrix_x)
ary=np.arange(0,matrix_y)

postimg=hillshade(postdtm,ary,arx,'azimuth',az,'altitude',al)

pcsumxy=matrix_y*matrix_x-3

generations=int(20)

populations=int(30)

delta = np.zeros(matrix_x,matrix_y,populations)
for i in range(0,populations):
	delta[:,:,i]=np.random.rand(matrix_y,matrix_x)*range*2-range

for i in range(0,generations):
	# now_generations_count=i         
    pctime=0

    # pc variable refers to the probability of crossover
    pc=0.8
    if (pc > np.random.rand(1)):
    
        # pcrandnew1 variable and pcrandnew2 variable are the places for new chromosomes
        pcrandnew1=21
        pcrandnew2=22
        

        # each crossover supplies two new chromosomes
        for j in range(18,20):
            delta[:,:,i]=np.random.rand(matrix_y,matrix_x)*range*2-range 

        #each crossover produces two new chromosomes
        while(pctime < 5):

                pcrandbest1=round(rand(1)*(19))
                pcrandbest2=round(rand(1)*(19))

                pcrandpoint1=1+round(rand(1)*(pcsumxy))
                pcrandpoint2=1+round(rand(1)*(pcsumxy))

                selecttemp1=delta[:,:,pcrandbest1] 
                selecttemp2=delta[:,:,pcrandbest2]

                selecttemp1=np.transpose(selecttemp1) 
                selecttemp2=np.transpose(selecttemp2)

                if (pcrandpoint1 > pcrandpoint2):
                    pctemp = pcrandpoint2
                    pcrandpoint2 = pcrandpoint1
                    pcrandpoint1 = pctemp
                
            
                for j in range(pcrandpoint1,pcrandpoint2):    
                    pctemp=selecttemp1[j]                  
                    selecttemp1[j]=selecttemp2[j]
                    selecttemp2[j]=pctemp  

                delta[:,:,pcrandnew1]=np.reshape(selecttemp1,matrix_y,matrix_x)
                delta[:,:,pcrandnew2]=np.reshape(selecttemp2,matrix_y,matrix_x)

                pcrandnew1=pcrandnew1+2
                pcrandnew2=pcrandnew2+2
                pctime=(pctime+1)
        


    pmtime=0

    #pm variable refers to the probability of mutation
    pm=0.06
    
    for j in range(1,18):
        t[j]=np.random.rand(1)
  
        if(pm > t(j)):
            pmx=1+round(np.random.rand(1)*(matrix_x-1))
            pmy=1+round(np.random.rand(1)*(matrix_y-1))  
          
            pmvolue=delta[pmy,pmx,j]+(np.random.rand(1)*range*2-range)

            while (abs(pmvolue) > range):
                pmvolue=delta[pmy,pmx,j]+(np.random.rand(1)*range*2-range)
            
            delta[pmy,pmx,j]=pmvolue
           
       
    for j in range(0,populations):
        shadow[:,:,j]=hillshade(predtm+delta[:,:,j],ary,arx,'azimuth',az,'altitude',al) 
   

    #calculates fitness function
    for j in range(0,populations):
        F[j]=corr2(shadow[:,:,j],postimg)  

    [orderF,indexF]=sort(F)
    
    for j in range(0,populations):
        delta_temp[:,:,j]=delta[:,:,indexF(populations+1-j)]
        shadow_temp[:,:,j]=shadow[:,:,indexF(populations+1-j)] 
 
    for j in range(0,populations):
        delta[:,:,j]=delta_temp[:,:,j]
        shadow[:,:,j]=shadow_temp[:,:,j] 

    best[i]=max(F)


bestrange=delta[:,:,1]

#filter
fun=np.median(x)
bestdtm=predtm+bestrange
bestrange_filter=nlfilter(bestdtm,[12,12],fun)

	
for y in range(0,matrix_y):
    for x in range(0,matrix_x):
        if (bestrange_filter[y,x]==0):
            bestrange_filter[y,x]=bestdtm[y,x]

for y in range(3,matrix_y-3):
    for x in range(3,matrix_x-3):
        end_bestrange[y-3,x-3]=bestrange[y,x]

for y in range (3,matrix_y-3):
    for x in range(3,matrix_x-3):
        end_filter[y-3,x-3]=bestrange_filter[y,x]

for y in range (3,matrix_y-3):
    for x in range (3,matrix_x-3):
        end_predtm[y-3,x-3]=predtm[y,x]

for y in range (3,matrix_y-3):
    for x in range (3,matrix_x-3):
        end_postdtm[y-3,x-3]=postdtm[y,x]

X_estimate=end_filter[17,:]
X_predtm=end_predtm[17,:]
X_postdtm=end_postdtm[17,:]

Y_estimate=end_filter[:,17]  
Y_predtm=end_predtm[:,17]
Y_postdtm=end_postdtm[:,17]

truedepth_del=0
truedepth_add=0
estimatedepth_del=0
estimatedepth_add=0   

for y in range(0,matrix_y-6):      
    for x in range(0,matrix_x-6):
        if (end_predtm(y,x) > end_postdtm(y,x)):
            truedepth=end_predtm(y,x)-end_postdtm(y,x)
            truedepth_del=truedepth+truedepth_del 
        if (end_predtm(y,x) < end_postdtm(y,x)):
            truedepth=end_postdtm(y,x)-end_predtm(y,x)
            truedepth_add=truedepth+truedepth_add 

volume_true_del=((truedepth_del))
volume_true_add=((truedepth_add))


for y in range(0,matrix_y-6):
    for x in range(0,matrix_x-6):
        if (end_predtm(y,x) > end_filter(y,x)):
            estimatedepth=end_predtm(y,x)-end_filter(y,x)
            estimatedepth_del=estimatedepth+estimatedepth_del
 
        if (end_predtm(y,x) < end_filter(y,x)):
            estimatedepth=end_filter(y,x)-end_predtm(y,x)
            estimatedepth_add=estimatedepth+estimatedepth_add

volume_estimate_del=((estimatedepth_del))
volume_estimate_add=((estimatedepth_add))


#output result
figure(1)


best_h=hillshade(predtm+bestrange,ar,ar,'azimuth',az,'altitude',al)
new_h=hillshade(postdtm,ar,ar,'azimuth',az,'altitude',al)
subplot[3,1,1]
imshow(mat2gray(postimg)) 
title('post-event remote sensing image (A)')
subplot[3,1,2]
imshow(mat2gray(best_h)) 
title('estimate result shadow image (B)')
subplot[3,1,3]
imshow(mat2gray(new_h)) 
title('post-event DTM shadow image (C)')



	

