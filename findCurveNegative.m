%This is used to find the cells in the grid that has
%shown negative change in elevation.

%It gives  the plot of the area having negative change




%reading "predtm" and "postdtm":
post_data=xlsread("postdtm.xlsx");
pre_data=xlsread("predtm.xlsx");

%variable storing change in elevation
data=pre_data-post_data;

%Steps to find the negative cell unit:
data=data/10000;
data2=floor(data);
for c=1:40
    for d=1:40
        if data2(c,d) == -1
            data2(c,d)=100;
        end
    end
end

%plotting the data
image(data2)
colormap(jet)
axis equal




