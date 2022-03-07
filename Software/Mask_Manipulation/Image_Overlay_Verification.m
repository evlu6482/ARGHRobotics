%{
Script for the verificatoin of mask output of maskrcnn, 
can be used to recombine an image and a mask and superimpose one on top of another
%}
%% 
clc
close all
clear all
 %read in image and mask data
image=imread('Images\realsense.jpeg');
M1=csvread('Masks\Mask_0');
I=rgb2gray(image);%convert image to greyscale


%enter color values for edge
r=0;
g=128;
b=0;

[x,y]=size(M1);%find size of matricies


EdgeMask=GetEdges(M1);



for i=1:x
   for j=1:y
     if M1(i,j)~= 1  %If pixel in image is not in the mask, color pixel grey 
        image(i,j,:)= I(i,j,:);
     end  
     
     if EdgeMask(i,j)==1 % color the edge pixels of mask green
         image(i,j,2)= 225;
     end
   end
end

% %% plotting
% figure()
% imshow(EdgeMask)
% figure()
% hold on 
% imshow(I)
% imshow(image)
% hold off

%% plotting

figure()

imshow(EdgeMask)

hold on

 

ax=gca

hold on

[y,x]=find(EdgeMask);

ellipse=fit_ellipse(x,y,ax)

figure()

hold on

 

 

imshow(I)

imshow(image)

 

ax=gca

hold on

[y,x]=find(EdgeMask);

ellipse=fit_ellipse(x,y,ax)

hold off

 