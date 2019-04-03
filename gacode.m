% We modified the binary code of (Wang, 2007) to make it a real-coded GA method 
% that uses two-point crossover and mutation,and used the function by (Hebeler, 2007) to produce the hillshade image.
%
% -----------------------------------References----------------------------------------
% Hebeler, F., (2007, 07 May), Hillshade, from http://www.mathworks.com/matlabcentral/fileexchange/14863-hillshade.
% Wang, J.-D., 2007. Neural network and fuzzy control theory entry application (chinese book). The QuanHua Book Company, 12-23 pp.
% -------------------------------------------------------------------------------------
%


clear;
close;

% use tic command to start the recording time
tic;

% matrix_x variable is for entering the width of matrix
matrix_x=40;

% matrix_y variable is for entering the height of matrix
matrix_y=40;

% predtm variable refers to pre-event elevation
predtm=xlsread('predtm.xlsx');

% postdtm variable refers to post-event elevation
postdtm=xlsread('postdtm.xlsx');

% az variable refers to azimuth
az=135;

% al variable refers to altitude
al=100;

% posting variable is post-event satellite image
postimg=hillshade(postdtm,1:matrix_y,1:matrix_x,'azimuth',az,'altitude',al);

% pcsumxy variable is temporary variable of crossover
pcsumxy=matrix_y*matrix_x-3;

generations=600000;

populations=30;

% range variable is the maximum value of estimating terrain change (¡µh)
range=100;

% initial population has 30 chromosomes (random numbers are scattered within the matrix with positive and negative numbers)
for i=1:1:populations
    delta(:,:,i)=rand(matrix_y,matrix_x)*range*2-range;
end

for i=1:1:generations

    now_generations_count=i
         
    pctime=0;

    % pc variable refers to the probability of crossover
    pc=0.8;

    if pc > rand(1)
    
        % pcrandnew1 variable and pcrandnew2 variable are the places for new chromosomes
        pcrandnew1=21;
        pcrandnew2=22;
        
        % each crossover supplies two new chromosomes
        for j=19:1:20
            delta(:,:,j)=rand(matrix_y,matrix_x)*range*2-range;
        end

        % each crossover produces two new chromosomes
        while pctime < 5

                pcrandbest1=1+round(rand(1)*(19));
                pcrandbest2=1+round(rand(1)*(19));

                pcrandpoint1=2+round(rand(1)*(pcsumxy));
                pcrandpoint2=2+round(rand(1)*(pcsumxy));

                selecttemp1=delta(:,:,pcrandbest1); 
                selecttemp2=delta(:,:,pcrandbest2);

                selecttemp1=selecttemp1(:)'; 
                selecttemp2=selecttemp2(:)';

                if pcrandpoint1 > pcrandpoint2
                    pctemp = pcrandpoint2;
                    pcrandpoint2 = pcrandpoint1;
                    pcrandpoint1 = pctemp;
                end
            
                for j = pcrandpoint1:1:pcrandpoint2    
                    pctemp=selecttemp1(j);                  
                    selecttemp1(j)=selecttemp2(j);
                    selecttemp2(j)=pctemp;
                end  

                delta(:,:,pcrandnew1)=reshape(selecttemp1,matrix_y,matrix_x);
                delta(:,:,pcrandnew2)=reshape(selecttemp2,matrix_y,matrix_x);

                pcrandnew1=pcrandnew1+2;
                pcrandnew2=pcrandnew2+2;

            pctime=pctime+1;
        end
    end

    pmtime=0;

    % pm variable refers to the probability of mutation
    pm=0.06;
    
    for j=2:1:18

        t(j)=rand(1);
  
        if pm > t(j)   

            pmx=1+round(rand(1)*(matrix_x-1));
            pmy=1+round(rand(1)*(matrix_y-1));   
          
            pmvolue=delta(pmy,pmx,j)+(rand(1)*range*2-range);

            while abs(pmvolue) > range
                pmvolue=delta(pmy,pmx,j)+(rand(1)*range*2-range);
            end

            delta(pmy,pmx,j)=pmvolue;
           
        end
    end  

    for j=1:1:populations
        shadow(:,:,j)=hillshade(predtm+delta(:,:,j),1:matrix_y,1:matrix_x,'azimuth',az,'altitude',al); 
    end

    % calculates fitness function
    for j=1:1:populations
        F(j)=corr2(shadow(:,:,j),postimg); 
    end

    [orderF,indexF]=sort(F);
    
    for j=1:1:populations
        delta_temp(:,:,j)=delta(:,:,indexF(populations+1-j));
        shadow_temp(:,:,j)=shadow(:,:,indexF(populations+1-j)); 
    end
 
    for j=1:1:populations
        delta(:,:,j)=delta_temp(:,:,j);
        shadow(:,:,j)=shadow_temp(:,:,j); 
    end

    best(i)=max(F);

end

% use toc command to end the recording time
toc;

% runtime variable refers to the calculating time by the program
runtime=toc;

% bestrange variable is the best result of estimating elevation change
bestrange=delta(:,:,1);

% filter
fun=@(x)median(x(:));
bestdtm=predtm+bestrange;
bestrange_filter=nlfilter(bestdtm,[12,12],fun);

for y=1:1:matrix_y
    for x=1:1:matrix_x
        if bestrange_filter(y,x)==0
            bestrange_filter(y,x)=bestdtm(y,x);
        end
    end
end

for y=4:1:matrix_y-3
    for x=4:1:matrix_x-3
        end_bestrange(y-3,x-3)=bestrange(y,x);
    end
end

for y=4:1:matrix_y-3
    for x=4:1:matrix_x-3
        end_filter(y-3,x-3)=bestrange_filter(y,x);
    end
end

for y=4:1:matrix_y-3
    for x=4:1:matrix_x-3
        end_predtm(y-3,x-3)=predtm(y,x);
    end
end

for y=4:1:matrix_y-3
    for x=4:1:matrix_x-3
        end_postdtm(y-3,x-3)=postdtm(y,x);
    end
end

X_estimate=end_filter(17,:);
X_predtm=end_predtm(17,:);
X_postdtm=end_postdtm(17,:);

Y_estimate=end_filter(:,17);  
Y_predtm=end_predtm(:,17);
Y_postdtm=end_postdtm(:,17);

truedepth_del=0;
truedepth_add=0;
estimatedepth_del=0;
estimatedepth_add=0;

for y=1:1:matrix_y-6      
    for x=1:1:matrix_x-6
        if end_predtm(y,x) > end_postdtm(y,x)
            truedepth=end_predtm(y,x)-end_postdtm(y,x);
            truedepth_del=truedepth+truedepth_del;
        end 
        if end_predtm(y,x) < end_postdtm(y,x)
            truedepth=end_postdtm(y,x)-end_predtm(y,x);
            truedepth_add=truedepth+truedepth_add;
        end 
    end
end
volume_true_del=((truedepth_del));
volume_true_add=((truedepth_add));

for y=1:1:matrix_y-6
    for x=1:1:matrix_x-6
        if end_predtm(y,x) > end_filter(y,x)
            estimatedepth=end_predtm(y,x)-end_filter(y,x);
            estimatedepth_del=estimatedepth+estimatedepth_del;
        end 
        if end_predtm(y,x) < end_filter(y,x)
            estimatedepth=end_filter(y,x)-end_predtm(y,x);
            estimatedepth_add=estimatedepth+estimatedepth_add;
        end 
    end
end
volume_estimate_del=((estimatedepth_del));
volume_estimate_add=((estimatedepth_add));

% output result
figure(1);
best_h=hillshade(predtm+bestrange,1:40,1:40,'azimuth',az,'altitude',al);
new_h=hillshade(postdtm,1:40,1:40,'azimuth',az,'altitude',al);
subplot(3,1,1);
imshow(mat2gray(postimg)); 
title('post-event remote sensing image (A)');
subplot(3,1,2);
imshow(mat2gray(best_h)); 
title('estimate result shadow image (B)');
subplot(3,1,3);
imshow(mat2gray(new_h)); 
title('post-event DTM shadow image (C)');








