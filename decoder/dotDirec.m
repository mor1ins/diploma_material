% Title: dotDirec.m
% [recX,recY,xSpace,ySpace] = dotDirec(x,y) analyzes the x-coordinates and
% y-coordinates of the centroids and assign offset direction indicators recX and % recY to each dot. xSpace and ySpace are two arrays used to record the spacings % of the columns and rows respectively.
function [recX, recY, xSpace, ySpace] = dotDirec(x, y) 
    [N, M] = size(x);
    recX = zeros([N, M]);
    recY = recX;
    xSpace = zeros(1, M); ySpace = zeros(N, 1); xt1 = zeros(1, M); xt2 = zeros(1, M); 
    yt1 = zeros(N, 1); yt2 = zeros(N, 1);
    
    for i = 1:M
        xt1(i) = min(x(:, i));
        xt2(i) = max(x(:, i)); xSpace(i) = xt2(i) - xt1(i);
    end
    for i = 1:M
        for j = 1:N
            x_m1 = abs((x(j, i) / xt1(i)) - 1);
            x_m2 = abs((x(j, i) / xt2(i)) - 1);
            x_mm = min([x_m1, x_m2]);
            if xSpace(i) > 2 / 3 * max(xSpace)

                xt3 = (xt2(i) - xt1(i)) / 3 + xt1(i);
                xt4 = 2 * (xt2(i) - xt1(i)) / 3 + xt1(i);
                if x(j, i) >= xt1(i) && x(j, i) < xt3
                    recX(j, i) = - 1;
                elseif x(j, i) >= xt3 && x(j, i) < xt4
                    recX(j, i) = 0;
                elseif x(j, i) >= xt4 && x(j, i) <= xt2(i)
                    recX(j, i) = 1;
                else
                    switch x_mm
                        case x_m1
                            recX(j, i) = - 1;
                        case x_m2
                            recX(j, i) = 1;
                    end
                end
            elseif xSpace(i) < 1 / 3 * max(xSpace)
                recX(j, i) = 3;
            else
                xt5 = 0.5 * (xt1(i) + xt2(i));
                if x(j, i) >= xt1(i) && x(j, i) < xt5
                    recX(j, i) = - 2;
                elseif x(j, i) >= xt5 && x(j, i) < xt2(i)
                    recX(j, i) = 2;
                else
                    switch x_mm
                        case x_m1
                            recX(j, i) = - 2;
                        case x_m2
                            recX(j, i) = 2;
                    end
                end
            end
        end
    end
    for j = 1:N
        yt1(j) = min(y(j, :));
        yt2(j) = max(y(j, :));
        ySpace(j) = yt2(j) - yt1(j);
    end

    for j = 1:N
        for i = 1:M
            y_m1 = abs((y(j, i) / yt1(j)) - 1);
            y_m2 = abs((y(j, i) / yt2(j)) - 1);
            y_mm = min([y_m1, y_m2]);

            if ySpace(j) > 2 / 3 * max(ySpace)

                yt3 = (yt2(j) - yt1(j)) / 3 + yt1(j);
                yt4 = 2 * (yt2(j) - yt1(j)) / 3 + yt1(j);
                if y(j, i) >= yt1(j) && y(j, i) < yt3
                    recY(j, i) = - 1;
                elseif y(j, i) >= yt3 && y(j, i) < yt4
                    recY(j, i) = 0;
                elseif y(j, i) >= yt4 && y(j, i) <= yt2(j)
                    recY(j, i) = 1;
                else
                    switch y_mm
                        case y_m1
                            recY(j, i) = - 1;
                        case y_m2
                            recY(j, i) = 1;
                    end
                end
            elseif ySpace(i) < 1 / 3 * max(ySpace)
                recY(j, i) = 3;

            else
                yt5 = 0.5 * (yt1(j) + yt2(j));
                if y(j, i) >= yt1(j) && y(j, i) < yt5
                    recY(j, i) = - 2;
                elseif y(j, i) >= yt5 && x(j, i) < yt2(j)
                    recY(j, i) = 2;
                else

                    switch y_mm
                        case y_m1
                            recY(j, i) = - 2;
                        case y_m2
                            recY(j, i) = 2;
                    end
                end
            end
        end
    end
    xismatched = zeros(N, M);
    wrongcolumn = zeros(1, M);
    x_replace = 225;
    k = 1;
    for i = 1:M
        if isempty(find(recX(:, i) == 0))
            wrongcolumn(k) = i;
            k = k + 1;
        end
    end

    for i = 1:M
        if wrongcolumn(i) ~= 0
            t = wrongcolumn(i);

            for j = 1:N
                if (recY(j, t) == - 1) || (recY(j, t) == 1)
                    x_replace = recX(j, t);
                    xismatched(j, t) = 1;
                else
                    xismatched(j, t) = 0;
                end

                if recX(j, t) == x_replace
                    recX(j, t) = 0;
                elseif recX(j, t) > 0
                    recX(j, t) = 1;
                else
                    recX(j, t) = - 1;
                end
            end

        end
    end
    yismatched = zeros(N, M);
    wrongrow = zeros(N, 1);
    y_replace = 225;
    l = 1;
    for j = 1:N
        if isempty(find(recY(j, :) == 0))
            wrongrow(l) = j;
            l = l + 1;
        end
    end
    for j = 1:N
        if wrongrow(j) ~= 0
            s = wrongrow(j);

            for i = 1:M
                if (recX(s, i) == - 1) || (recX(s, i) == 1)
                    y_replace = recY(s, i);
                    yismatched(s, i) = 1;
                else
                    yismatched(s, i) = 0;
                end

                if recY(s, i) == y_replace
                    recY(s, i) = 0;
                elseif recY(s, i) > 0
                    recY(s, i) = 1;

                else
                    recY(s, i) = - 1;
                end
            end

        end
    end
