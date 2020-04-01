% Title: DetCor.m
% X = DetCor(A,B) determines the coordinates of the dots in columns and rows. % A = (p1r,p2r,p3r,p4r) is the reference unique 4-number combination.
% B = (p1,p2,p3,p4) is the 4-number combination of the interested region. function X = DetCor(A,B)
a = zeros(4,1000);
% establish a table
for i = 1:1000
a(1,i) = mod(A(1)+i-1,236); a(2,i) = mod(A(2)+i-1,233); a(3,i) = mod(A(3)+i-1,31); a(4,i) = mod(A(4)+i-1,241);
end
% output the result.
flag = 0; for i=1:1000
if a(4,i) == B(4) && a(3,i)== B(3) && a(2,i) == B(2) && a(1,i) == B(1) X = i;
flag =1;
if flag == 0
disp('no match found') X = 0;
end

