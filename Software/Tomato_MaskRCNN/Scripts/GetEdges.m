function EdgeMask=GetEdges(Mask)
%function for extracting the edge pixels associated with a mask
%Created By: Collin Rasbid 1/12/2022
%input: any binary mask
%output: binary mask of edge points

%extract mask dimensions
[x,y]=size(Mask);

%{
    Cases:
   * edge of array i=0, j=0 or i=x j=y and mask is present
   * mask has any open "air" in adjacent index (Mask==0) 
        - check x+-1 y+-1
%}

EdgeMask=zeros(x,y); %initialize edge mask

for i=1:x
    for j=1:y
        if (i==0 || j==0) 
           if Mask==1
            EdgeMask(i,j)=1;
           end
           
        elseif (i==x || j==y) 
           if Mask==1
            EdgeMask(i,j)=1;
           end 
           
        elseif Mask(i,j)==1 && ( (Mask(i-1,j)==0) ||  (Mask(i+1,j)==0) )
             EdgeMask(i,j)=1;
            
        elseif Mask(i,j)==1 && ( (Mask(i,j-1)==0) ||  (Mask(i,j+1)==0) )
            EdgeMask(i,j)=1;
        end 
        
    end
    
end

end