% Title: CENTROIDS.m
% CENTROIDS is the main script.
% It calls a number of functions to do incline-correction reconstruct the virtual
% raster lines and decoding.
% clean up the work space
clc; clear all;
disp('Running centroids.m...'); % Message sent to command window.
  [FileName, PathName] = uigetfile({
          '*.bmp;*.tif;*.jpg;*.gif;*.png', 'Images(* .bmp, * .tif, * .jpg, * .gif, * .png)';
          '*.bmp', 'BMP Image(*.bmp)'; ...
          '*.tif', 'Tiff Image(*.tif)'; ...
          '*.jpg', 'JPEG Image (*.jpg)'; ...
          '*.gif', 'GIF (*.gif)'; ...
          '*.png', 'PNG (*.png)'; ...
          '*.*', 'All Files (*.*)'
      }, ...
      'Select an Image');
if isequal(FileName, 0)
    disp('User selected Cancel')
else
    FullFileName = fullfile(PathName, FileName);
end
OI = imread(FullFileName);
OI = flipud(OI);
figure
% imshow(OI);
[numofBlobs, centroids] = GetCentroids(OI);
% }

% Since centroids is a N×2 array, it's not easy and instinct to utilize
% its data, we set two new N×N arrays x and y to store x-coordinates and
% y-coordinates of the centroids separately.
N = sqrt(numofBlobs);
xt = zeros(N);
yt = zeros(N);
for n = 1:N
    for m = 1:N
        xt(m, n) = centroids(m + (n - 1) * N, 1);
        yt(m, n) = centroids(m + (n - 1) * N, 2);
    end
end

[temp, index] = sort(yt, 'descend');
% create y matrix

y = temp;

% create x matrix
x = zeros(N);
for m = 1:N
    for n = 1:N
        x(n, m) = xt(index(n, m), m);
    end
end

% obtain the offset indicators recX and recY
% obtain the spacing in x and y directions
[recX, recY, xSpace, ySpace] = dotDirec(x, y);
[averx, avery, ~, ~] = Gridestab(recX, recY, x, y);
for i = 1:N
    for j = 1:N
        if abs(recX(j, i)) + abs(recY(j, i)) ~= 1
            if abs(x(j, i) - averx(i)) > abs(y(j, i) - avery(j))
                recY(j, i) = 0;
                recX(j, i) = sign(x(j, i) - averx(i));
            else
                recY(j, i) = sign(y(j, i) - avery(j));
                recX(j, i) = 0;
            end
        end
    end
end
MarkVal_x = zeros(N);
MarkVal_y = zeros(N);
% calculate the mark value
for i = 1:N ^ 2
    if recX(i) == - 1 && recY(i) == 0
        MarkVal_x(i) = 3;
    elseif recX(i) == 1 && recY(i) == 0
        MarkVal_x(i) = 1;
    elseif recX(i) == 0 && recY(i) == - 1
        MarkVal_y(i) = 4;
    elseif recX(i) == 0 && recY(i) == 1
        MarkVal_y(i) = 2;
    else
     
    end
end
MarkVal = MarkVal_x + MarkVal_y;
% using mark value to determine x, y codes.
xcode = zeros(N); ycode = zeros(N);
for j = 1:N
    for i = 1:N
        switch MarkVal(j, i)
         
            case 1
                xcode(j, i) = 0;
                ycode(j, i) = 1;
            case 2
                xcode(j, i) = 0;
                ycode(j, i) = 0;
            case 3
                xcode(j, i) = 1;
                ycode(j, i) = 0;
            case 4
                xcode(j, i) = 1;
                ycode(j, i) = 1;
            otherwise
                % when error occurs
                xcode(j, i) = 3;
                ycode(j, i) = 3;
        end
    end
 
end
% find the pixel coordinates of the centroid of the object
[objectX, objectY] = getcent
objectR = 0;
objectC = 0;
for i = 1:N - 1
    if objectX >= averx(i) && objectX <= averx(i + 1)
        objectC = i + (objectX - averx(i)) / (averx(i + 1) - averx(i));
    end
end
for j = 1:N - 1
    if objectY <= avery(j) && objectY >= avery(j + 1)
        objectR = j + (objectY - avery(j)) / (avery(j + 1) - avery(j));
    end
end
% establish the code book as a reference for decoding
BitSeq = enCod(0, 6);
PaSeq_1SDS = enCod(1, 5);
PaSeq_2SDS = enCod(2, 5);
PaSeq_3SDS = enCod(3, 5);
PaSeq_4SDS = enCod(4, 5);
% decoding..
% obtain the PDS
[PVy, PDSy] = deCody(ycode, BitSeq, 6);
[PVx, PDSx] = deCodx(xcode, BitSeq, 6);
% convert PDS into SDS in x direction
[a1x, a2x, a3x, a4x] = PDScoeff(PDSx);
% obtain the place numbers in SDS in x direction
[p1x, ~] = deCodx(a1x, PaSeq_1SDS, 5);
[p2x, ~] = deCodx(a2x, PaSeq_2SDS, 5);
[p3x, ~] = deCodx(a3x, PaSeq_3SDS, 5);
[p4x, ~] = deCodx(a4x, PaSeq_4SDS, 5);
% convert PDS into SDS in y direction
[a1y, a2y, a3y, a4y] = PDScoeff(PDSy);

% obtain the place numbers in SDS in y direction
[p1y, ~] = deCody(a1y, PaSeq_1SDS, 5);
[p2y, ~] = deCody(a2y, PaSeq_2SDS, 5);
[p3y, ~] = deCody(a3y, PaSeq_3SDS, 5);
[p4y, ~] = deCody(a4y, PaSeq_4SDS, 5);
% obtain the place numbers in PDS if needed
% Px = Place_PDS(xcode,1);
% Py = Place_PDS(ycode,2);
% obtain the place numbers of the ROI
Bx = [p1x(1, 1), p2x(1, 1), p3x(1, 1), p4x(1, 1)];
By = [p1y(1, 1), p2y(1, 1), p3y(1, 1), p4y(1, 1)];
% the place numbers of the first column and the first row
% provided as a reference when establish Table 5-10 and Table 5-11
Ax = [32, 57, 12, 96];
Ay = [224, 19, 4, 155];

% obtain the coordinates in columns and rows of the ROI.
X = DetCor(Ax, Bx);
Y = DetCor(Ay, By);

% obtain the coordinates in columns and rows of the object.
objectC = X + objectC - 1;
objectR = Y + objectR - 1;
Coordinate = [objectC, objectR];