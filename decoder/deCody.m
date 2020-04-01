% Title: deCody.m
% [PosVal,DS] = deCody(code, BitSeq, n)decodes the code in the y direction
% n— has the value 5, 6 or 8. n=5 indicates encoding SDS, n=6 or 8
% indicate encoding PDS using 6×6 array or 8×8 array.
function [PosVal, DS] = deCody(code, BitSeq, n)
    [r_code, c_code] = size(code);
    switch n
        case 8
            c_codeT = floor(c_code / n); % number of vertical bit sequences of x-code.
            r_codeT = r_code;
            bla = blanks(c_codeT * (n + 2 * (n - 1)));
         
            bla = zeros(r_codeT, length(bla)); % build a temporary array to contain the codes.
        case 6
            c_codeT = floor(c_code / n); % number of vertical bit sequences of x-code.
            r_codeT = r_code;
            bla = blanks(c_codeT * (n + 2 * (n - 1)));
            bla = zeros(r_codeT, length(bla)); % build a temporary array to contain the codes.
        case 5
            r_codeT = floor(r_code / n);
            c_codeT = c_code;
            bla = blanks(c_codeT * (n + 2 * (n - 1)));
            bla = zeros(r_codeT, length(bla));
         
        otherwise
            disp('n must be 5 or 6.')
    end
    PosVal = zeros(r_codeT, c_codeT);
    DS = zeros(r_codeT - 1, c_codeT); % Primary Difference Sequence
    switch n
        case 8
            for i = 1: c_codeT
                code8 = char(int2str(code(:, 1 + (i - 1) * n:i * n)));
                [~, c8] = size(code8);
             
                bla(:, 1 + (i - 1) * c8:i * c8) = code8;
             
            end
     
        case 6
          for i = 1: c_codeT
              code6 = char(int2str(code(:, 1 + (i - 1) * n:i * n)));
              [~, c6] = size(code6);
           
              bla(:, 1 + (i - 1) * c6:i * c6) = code6;
           
          end
       
          case 5
            for i = 1: r_codeT
                code5 = char(int2str(code(1 + (i - 1) * n:i * n, :)'));
                [r5, c5] = size(code5);
                for j = 1:r5
                    bla(i, 1 + (j - 1) * c5:j * c5) = code5(j, :);
                end
            end
         
        end
        bla = char(bla);
        for i = 1:r_codeT
            for j = 1:c_codeT
                for k = 1:length(BitSeq)
                    if isequal(bla(i, 1 + (j - 1) * n + 2 * (n - 1) * (j - 1):j * n + 2 * (n - 1) * j), BitSeq{k})
                        PosVal(i, j) = k - 1;
                    end
                end
            end
        end
        switch n
            case 8
                for i = 1:r_codeT - 1
                    for j = 1:c_codeT
                        DS(i, j) = mod((PosVal(i + 1, j) - PosVal(i, j)), 63);
                        % DS(i,j) = mod(abs((PosVal(i,j+1)-PosVal(i,j))),63);
                    end
                end
         
            case 6
              for i = 1:r_codeT - 1
                  for j = 1:c_codeT
                      DS(i, j) = mod((PosVal(i + 1, j) - PosVal(i, j)), 63);
                      % DS(i,j) = mod(abs((PosVal(i,j+1)-PosVal(i,j))),63);
                  end
              end
            otherwise
              DS = [];
        end
       
       