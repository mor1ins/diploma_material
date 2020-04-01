% Title: Gridestab.m
%
% [averx,avery,~,~] = Gridestab(recX,recY,x,y) reconstructs the virtual raster
% lines and returns the coordinates averx and avery of the raster lines.


function [averx, avery, deltax, deltay] = Gridestab(recX, recY, x, y)
    plot(x(:, :), y(:, :), 'r*'); axis square
    hh = axis;
    [M, N] = size(x);
    averx = zeros(1, M);
    deltax = zeros(1, M - 1);
    hold on;
    for i = 1:M
        count = 0;
        sum = 0;
        for j = 1:N
            if recX(j, i) == 0
                sum = sum + x(j, i);
                count = count + 1;
            end
        end
        averx(i) = sum / count;
        plot([averx(i), averx(i)], [hh(3), hh(4)], 'b'); axis square
    end
    for i = 1:M - 1
        deltax(i) = averx(i + 1) - averx(i);
    end
    avery = zeros(1, N);
    deltay = zeros(1, N - 1);
    for j = 1:N
        count = 0;
        sum = 0;
        for i = 1:M
            if recY(j, i) == 0
                sum = sum + y(j, i);
                count = count + 1;
            end
        end
        avery(j) = sum / count;
        plot([hh(1), hh(2)], [avery(j), avery(j)], 'b'); axis square
    end
    for j = 1:N - 1
        deltay(j) = avery(j + 1) - avery(j);
    end
    hold off
