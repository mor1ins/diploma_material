% Script: Rigtpart.m
% Purpose: process the right part of an experimental image to obtain the exact
% ratio, ratio2_exp, of the distances A and B.
% A is the distance between the point on the thimble which coincides with the axial % line to the lower graduation.
% B is the distance between the lower graduation and the higher graduation.
% Input: ‘*****.jpg’ – the experimental image.
% Output: ratio2_exp -- the ratio as describe above.
clc;clear all;
BW = imread('25973.jpg'); % A typical experimental image
[r,c] = size(BW); BW =BW>100;
[n,~] = hist(BW); n = n(10,:);
% Filter out unnecessary parts
for i= 1:c
if n(i)<20
n(i) = 0;
end end
% Locate the ranges of lower graduation, higher graduation and the axial line.
py=zeros(2,3); j = 0;
for i = 1:c-1
if n(i)~=0 && n(i+1)==0 py(2,j+1) = i;
j = j+1;
end end
j =
for
0;
i = 1:c-1
if n(i)==0 && n(i+1)~=0
py(1,j+1) = i+1; j = j+1;
72
end end
% Find the means for lower graduation, higher graduation and the axial line. % Use the means to represent the positions of each line.
% Calculate the ratio using the means.
pymean = mean(py);
ratio2_exp = (pymean(2)-pymean(1))/(pymean(3)-pymean(1));
% Plot the intensity histogram
histo = bar(n)
