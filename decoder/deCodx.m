% Title: deCodx.m
% [PosVal,DS] = deCodx(code, BitSeq, n)decodes the code in the x direction % n— has the value 5, 6 or 8. n=5 indicates encoding SDS, n=6 or 8
% indicate encoding PDS using 6×6 array or 8×8 array.
function [PosVal,DS] = deCodx(code, BitSeq, n) [r_code,c_code] = size(code);
switch n
case 8
r_codeT = floor(r_code/n); % number of vertical bit sequences of x-code. c_codeT = c_code;
bla = blanks(c_codeT*(n+2*(n-1)));
bla = zeros(r_codeT,length(bla));
case 6
r_codeT = floor(r_code/n); % number of vertical bit sequences of x-code. c_codeT = c_code;
bla = blanks(c_codeT*(n+2*(n-1)));
bla = zeros(r_codeT,length(bla)); % build a temporary array to contain the
codes.
case 5
c_codeT = floor(c_code/n);
r_codeT = r_code;
bla = blanks(c_codeT*(n+2*(n-1))); bla = zeros(r_codeT,length(bla));
otherwise
disp('n must be 5 or 6 or 8') end
PosVal = zeros(r_codeT,c_codeT);
DS = zeros(r_codeT,c_codeT-1); %Primary Difference Sequence
switch n
   case 8
       for
i = 1: r_codeT
code8 = char(int2str(code(1+(i-1)*n:i*n,:)')); [r8,c8] = size(code8);
for j = 1:r8
bla(i, 1+(j-1)*c8:j*c8) = code8(j,:);
case 6 for
i = 1: r_codeT
code6 = char(int2str(code(1+(i-1)*n:i*n,:)')); [r6,c6] = size(code6);
for j = 1:r6
bla(i, 1+(j-1)*c6:j*c6) = code6(j,:);
end end
end end
79
case 5
for i = 1: r_codeT
code5 = char(int2str(code(:,1+(i-1)*n:i*n))); [~,c5] = size(code5);
bla(:,1+(i-1)*c5:i*c5) = code5;
end end
bla = char(bla);
for i = 1:r_codeT for j = 1:c_codeT
end end
switch n
   case 6
       for
i = 1:r_codeT
for j = 1:c_codeT-1
DS(i,j) = mod((PosVal(i,j+1)-PosVal(i,j)),63);
case 8 for
i = 1:r_codeT
for j = 1:c_codeT-1
DS(i,j) = mod((PosVal(i,j+1)-PosVal(i,j)),63);
for
k = 1:length(BitSeq)
if isequal(bla(i,1+(j-1)*n+2*(n-1)*(j-1):j*n+2*(n-1)*j),BitSeq{k})
PosVal(i,j) = k-1;
end end
end end
end end
otherwise
DS = [];
end

