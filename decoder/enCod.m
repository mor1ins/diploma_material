% Title: enCod.m
% BitSeq = enCod(NumSeq,n) establishes a code book for decoding.
%
% NumSeq-- an integer number that has values 0~4. Indicate the
% kind of the number sequence used.
% 0- main number sequence.
% 1~4- secondary number sequence set A1, A2, A3, A4.
% n— has the value 5, 6 or 8. n=5 indicates encoding SDS, n=6 or 8
% indicate encoding PDS using 6×6 array or 8×8 array.
% BitSeq— the output.
function BitSeq = enCod(NumSeq, n)
    switch NumSeq
        case 0
            NS =
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1,
            0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1];
        case 4
            NS =
            [0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, 2, 0, 0, 2, 0, 1, 0, 0, 0, 1, 1, 2, 0, 0, 0, 1, 2, 0, 0, 2, 1, 0, 0, 0, 2, 1, 1, 2, 0,
            1, 0, 1, 0, 0, 1, 2, 1, 0, 0, 1, 0, 0, 2, 2, 0, 0, 0, 2, 2, 1, 0, 2, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 2, 0, 1, 1
            , 1, 1, 0, 0, 2, 0, 2, 0, 1, 2, 0, 2, 2, 0, 1, 0, 2, 1, 0, 1, 2, 1, 1, 0, 1, 1, 1, 2, 2, 0, 0, 1, 0, 1, 2, 2, 2, 0, 0, 2, 2,
            2, 0, 1, 2, 1, 2, 0, 2, 0, 0, 1, 2, 2, 0, 1, 1, 2, 1, 0, 2, 1, 1, 0, 2, 0, 2, 1, 2, 0, 0, 1, 1, 0, 2, 1, 2, 1, 0, 1, 0, 2, 2
            , 0, 2, 1, 0, 2, 2, 1, 1, 1, 2, 0, 2, 1, 1, 1, 0, 2, 2, 2, 2, 0, 2, 0, 2, 2, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 2, 2, 2, 1, 0, 0,
            2, 1, 2, 2, 1, 0, 1, 1, 2, 2, 1, 1, 2, 1, 2, 2, 2, 2, 1, 2, 0, 1, 2, 2, 1, 2, 2, 0, 2, 2, 2, 1, 1];
        case 2
            NS =
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 2, 0, 0, 0, 1,
            2, 0, 1, 0, 1, 2, 1, 0, 0, 0, 2, 1, 1, 1, 0, 1, 1, 1, 0, 2, 1, 0, 0, 1, 2, 1, 2, 1, 0, 1, 0, 2, 0, 1, 1, 0, 2, 0, 0, 1, 0, 2
            , 1, 2, 0, 0, 0, 2, 2, 0, 0, 1, 1, 2, 0, 2, 0, 0, 2, 0, 2, 0, 1, 2, 0, 0, 2, 2, 1, 1, 0, 0, 2, 1, 0, 1, 1, 2, 1, 0, 2, 0, 2,
            2, 1, 0, 0, 2, 2, 2, 1, 0, 1, 2, 2, 0, 0, 2, 1, 2, 2, 1, 1, 1, 1, 1, 2, 0, 0, 1, 2, 2, 1, 2, 0, 1, 1, 1, 2, 1, 1, 2, 0, 1, 2
            , 1, 1, 1, 2, 2, 0, 2, 2, 0, 1, 1, 2, 2, 2, 2, 1, 2, 1, 2, 2, 0, 1, 2, 2, 2, 0, 2, 0, 2, 1, 1, 2, 2, 1, 0, 2, 2, 0, 2, 1, 0,
            2, 1, 1, 0, 2, 2, 2, 2, 0, 1, 0, 2, 2, 1, 2, 2, 2, 1, 1, 2, 1, 2, 0, 2, 2, 2];
        case 3
            NS = [0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1];
        case 1
            NS =
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 1, 0, 0, 1, 0, 1, 0, 0, 2, 0, 0, 0, 1, 1, 0, 0, 0, 1, 2, 0, 0, 1, 0, 2, 0, 0, 2, 0, 2,
            0, 1, 1, 0, 1, 0, 1, 1, 0, 2, 0, 1, 2, 0, 1, 0, 1, 2, 0, 2, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 2, 1, 0, 1, 0, 2, 1, 1, 0, 0
            , 1, 2, 1, 0, 1, 1, 2, 0, 0, 0, 2, 1, 0, 2, 0, 2, 1, 1, 1, 0, 0, 2, 1, 2, 0, 1, 1, 1, 2, 0, 2, 0, 0, 1, 1, 2, 1, 0, 0, 0, 2,
            2, 0, 1, 0, 2, 2, 0, 0, 1, 2, 2, 0, 2, 0, 2, 2, 1, 0, 1, 2, 1, 2, 1, 0, 2, 1, 2, 1, 1, 0, 2, 2, 1, 2, 1, 2, 0, 2, 2, 0, 2, 2
            , 2, 0, 1, 1, 2, 2, 1, 1, 0, 1, 2, 2, 2, 2, 1, 2, 0, 0, 2, 2, 1, 1, 2, 1, 2, 2, 1, 0, 2, 2, 2, 2, 2, 0, 2, 1, 2, 2, 2, 1, 1,
            1, 2, 1, 1, 2, 0, 1, 2, 2, 1, 2, 2, 0, 1, 2, 1, 1, 1, 1, 2, 2, 2, 0, 0, 2, 1, 1, 2, 2];
    end
    SL = length(NS);
    bitseq = zeros(SL, n);
    BitSeq = zeros(SL, n);
    for i = 1:SL
     
        for j = 1:n
            if i + j - 1 <= SL
                bitseq(i, j) = NS(i + j - 1);
            else
                bitseq(i, j) = NS(i + j - 1 - SL);
             
            end
         
        end
     
    end
    BitSeq = cellstr(int2str(bitseq));
 
 