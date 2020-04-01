% Title: PDScoeff.m
% [a1,a2,a3,a4] = PDScoeff(PDS) converts the primary difference sequence PDS into % sequences a1, a2, a3 and a4.
function [a1,a2,a3,a4] = PDScoeff(PDS)
[r,c] = size(PDS);
a1= zeros(r,c);a2= zeros(r,c);a3= zeros(r,c);a4= zeros(r,c);
for i = 1:r for j = 1:c
if PDS(i,j)>=5 && PDS(i,j)<= 58%PDS(i,j)>=5 && PDS(i,j)<= 58 if PDS(i,j)>=41 % 5+2*18
a4(i,j) = 2;
elseif PDS(i,j)>=23 % 5+1*18
a4(i,j) = 1;
else
a4(i,j) = 0;
end
PDS(i,j) = PDS(i,j) - a4(i,j)*18 -5; if PDS(i,j)>= 9 % 1*9
a3(i,j) = 1;
else
a3(i,j) = 0;
end
PDS(i,j) = PDS(i,j)-a3(i,j)*9; if PDS(i,j) >= 6 % 2*3
a2(i,j) = 2;
elseif PDS(i,j) >= 3 %1*3
a2(i,j) = 1;
else
a2(i,j) = 0;
end
82
PDS(i,j)= PDS(i,j)-a2(i,j)*3;
a1(i,j) = PDS(i,j);
else % which means the element of PDS does not belong to [5,58] a1(i,j) = 8;
a2(i,j) = 8; a3(i,j) = 8; a4(i,j) = 8;
end
end end

