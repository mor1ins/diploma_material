% Title: getcent.m
%
% [X,Y] = getcent find the centroid coordinates in pixels for the object.


function [X, Y] = getcent
    clc; clear all;
    disp('Running program, please wait...'); % Message sent to command window.
    [FileName, PathName] = uigetfile({
            '*.bmp;*.tif;*.jpg;*.gif;*.png', 'Images(* .bmp, * .tif, * .jpg, * .gif, * .png)';
            '*.bmp', 'BMP Image(*.bmp)'; ...
            '*.tif', 'Tiff Image(*.tif)'; ...
            '*.jpg', 'JPEG Image (*.jpg)'; ...
            '*.gif', 'GIF (*.gif)'; ...
            '*.png', 'PNG (*.png)'; ...
            '*.*', 'All Files (*.*)'
        }, ...
        'Select an Image' ...
    );

    if isequal(FileName, 0)
        disp('User selected Cancel')
    else
        FullFileName = fullfile(PathName, FileName);
    end

    OI3 = imread(FullFileName);
    OI3 = flipud(OI3);
    figure
    [numofBlobs, centroids] = GetCentroids(OI3);
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

    X = x;
    Y = y;
