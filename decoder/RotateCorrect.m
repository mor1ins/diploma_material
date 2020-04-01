% Title: RotateCorrect.m
% Purpose: Do incline-correction.
clc;
clear all;
[FileName,PathName] = uigetfile({'*.bmp;*.tif;*.jpg;*.gif;*.png','Images (*.bmp,*.tif,*.jpg,*.gif,*.png)';
'*.bmp', 'BMP Image(*.bmp)'; ... '*.tif','Tiff Image(*.tif)'; ... '*.jpg','JPEG Image (*.jpg)'; ... '*.gif','GIF (*.gif)'; ... '*.png','PNG (*.png)'; ...
'*.*', 'All Files (*.*)'}, ... 'Select an Image');
if isequal(FileName,0) disp('User selected Cancel')
else
FullFileName = fullfile(PathName, FileName);
end
OI = imread(FullFileName);
imshow(OI);
[numofBlobs, centroids] = GetCentroids(OI);
xy = [centroids(round(numofBlobs/2),1), centroids(round(numofBlobs/2),2)]; P = FindPoint(centroids,xy);
alphaSum = 0; for i=1:4
temp = P{i}-xy;
d = sqrt(temp(1)^2+temp(2)^2);
if temp(1)/d ~=0 && temp(2)/d ~=0 if mod(i,2)==0
asin(abs(temp(2))/d)
alpha = asin(abs(temp(2))/d);
else
asin(abs(temp(2))/d)
alpha = pi/2-asin(abs(temp(2))/d);
end
alphaSum = alphaSum + alpha;
else
 89
alphaSum = 0;
end end
alphaM = 0.25*alphaSum*180/pi;
sprintf('the rotated angle is: %.2f degrees',alphaM)
[FileName,PathName] = uigetfile({'*.bmp;*.tif;*.jpg;*.gif;*.png','Images (*.bmp,*.tif,*.jpg,*.gif,*.png)';
'*.bmp', 'BMP Image(*.bmp)'; ... '*.tif','Tiff Image(*.tif)'; ... '*.jpg','JPEG Image (*.jpg)'; ... '*.gif','GIF (*.gif)'; ... '*.png','PNG (*.png)'; ...
'*.*', 'All Files (*.*)'}, ... 'Select an Image');
if isequal(FileName,0) disp('User selected Cancel')
else
FullFileName = fullfile(PathName, FileName);
end
OI2 = imread(FullFileName); RI = imrotate(OI2,-alphaM); figure
imshow(RI);
