% Title: FindPoint.m
%
% This function is not written by the author of this thesis. It is found on a
% Matlab learner’s forum on the internet.
%
% Point = FindPoint(xy0, xy)Find nearest points of one given point in 4 quadrants.
function Point = FindPoint(xy0, xy)
    Point = cell(1, 4);
    x = xy0(:, 1) - xy(1);
    y = xy0(:, 2) - xy(2);

    % 1st quadrant
    id1 = (x > 0 & y >= 0);
    Point{1} = subfun(id1, x, y, xy0);

    % 2nd quadrant
    id2 = (x <= 0 & y > 0);
    Point{2} = subfun(id2, x, y, xy0);

    % 3rd quadrant
    id3 = (x < 0 & y <= 0);
    Point{3} = subfun(id3, x, y, xy0);

    % 4th quadrant
    id4 = (x >= 0 & y < 0);
    Point{4} = subfun(id4, x, y, xy0);
end

function xyPoint = subfun(id,x,y,xy0) % find the nearest point
    xyPoint = [];
    x1 = x(id);
    if ~isempty(x1)
        y1 = y(id);
        distance = x1.^2 + y1.^2;
        xy0_1 = xy0(id,:);
        xyPoint = xy0_1(find(distance == min(distance)),:);
    end
end
