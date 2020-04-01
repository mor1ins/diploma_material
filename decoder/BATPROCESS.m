% File name: BATPROCESS.m
%
% BATPROCESS batch processes the binary images stored in a folder, dir_name,
% plotting intensity histogram to find the locations of the graduations on a sleeve.
% Then save the data into an excel file for establishing Table 3-3.
%
% Input:      dir_name        – location of the source images.
%             dir_name2       – location of the output images and excel file.
%
% Output:     xSpacing.xlsx   – file contain the spacing information of each reference image.
%             name.jpg        – intensity histogram of each reference image.


clc;
clear all;
dir_name = uigetdir('E:\EsoneruzA\Desktop\', 'Choose Source Folder');
if isequal(dir_name, 0)
    disp('invalid')
else
    tarFiles = dir(dir_name);
end
dir_name2 = uigetdir('E:\EsoneruzA\Desktop\', 'Choose Destination Folder');

filename = 'xSpacing.xlsx';
ffn = fullfile(dir_name2, filename);

px = zeros(numel(tarFiles) - 2, 20);
[rpx, cpx] = size(px);
xSpacing = zeros(rpx, cpx - 1);

for k = 3:numel(tarFiles)
    BW = imread(fullfile(dir_name, tarFiles(k).name));
    [r, c] = size(BW);
    % The name of the image file is specially named by its reading on the LCD screen.
    % This is very convenient when labeling each histogram.
    [~, name, ~] = fileparts(tarFiles(k).name);
    BW = BW > 100;
    [n, ~] = hist(BW);
    n = n(10, :);

    for i = 1:c
        if n(i) < 40 || (n(i) < 75 && i > 820) % Filter out unnecessary parts
            n(i) = 0;
        end
    end

    j = 0;
    for i = 1:c - 1 % Locate the position of peaks
        if n(i) ~= 0 && n(i + 1) == 0
            px(k - 2, j + 1) = i;
            j = j + 1;
        end
    end

    for i = 1:rpx
        for j = 1:cpx - 1
            if px(i, j + 1) ~= 0
                xSpacing(i, j) = px(i, j + 1) - px(i, j); % Calculate the values of spacings
            end
        end
    end

    histo = bar(n);
    str = ['0.' name];
    num1 = str2double(str);

    saveas(histo, [dir_name2, '\', name, '.jpg']); % Save histograms as jpeg images.
end

xlswrite(ffn, xSpacing, 'sheet1', 'A1'); % Save data into an excel document.
