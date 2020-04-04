% Title: GetCentroids.m
%
% [numofBlobs, centroids] = GetCentroids(OI) uses binary image information
% contained in OI to determine the number of blobs, numofBlobs in the original
% image, locate the coordinates (pixels) of the centroids of each blob and save
% them in a array called centroids.


function [numofBlobs, centroids] = GetCentroids(OI)
    % Maximize the figure window.
    set(gcf, 'Position', get(0, 'ScreenSize'));
    % Thresholding the image
    thres = 100; % Set a threshold value for binarize the image
    % BW = OI < thres; % Store the obtained binary image into an array 'BW'
    BW = OI > thres;
    % Find the coordinates of centroids of each blob
    % Calculate all properties of the binary image
    blobMeasurements = regionprops(BW, 'centroid');
    % Put the coordinates into an array 'centorids'
    centroids = cat(1, blobMeasurements.Centroid);
    % Plot the centroids on the binary image
    % imagesc(BW); colormap(gray(256)); title('Centroids of each blob'); axis square;
    % imshow(BW)
    [~, numofBlobs] = bwlabel(BW, 8);
    % hold on
    plot(centroids(:, 1), centroids(:, 2), '.'); 
    axis square
    % hold off
