%%% 
%
% by Bereket Abraham
% Senior Thesis, 3D Volemtric Display Tech
%

clc
clear
close all
warning off

file = 'faces.txt';
folder = 'run0';
testing = true;
universe = [480, 320, 500];
s = universe(3)/pi; % scale
fpi = 24;
fpr = 72;
frameset = zeros(universe(1),universe(2),fpi);
inc = 2*pi/fpr;
theta = 0;
img = 1;
p = 1;
data = dlmread(file, ',');
m = size(data);

for k=1:fpr     % for every rotation
    
    for i=1:m(1)    % for every face
        n = data(i,1:3);
        v1 = data(i,4:6);
        v2 = data(i,7:9);
        v3 = data(i,10:12);

        xmin = min(v1(1), v2(1));
        xmin = min(xmin, v3(1));
        xmax = max(v1(1), v2(1));
        xmax = max(xmax, v3(1));
        xrange = xmin:0.5:xmax;
        % xrange = linspace(xmin,xmax,100);
        ymin = min(v1(2), v2(2));
        ymin = min(ymin, v3(2));
        ymax = max(v1(2), v2(2));
        ymax = max(ymax, v3(2));
        yo = (ymin+ymax)/2;

        % equation of the plane
        % ax + by + cz + d = 0
        a = n(1);
        b = n(2);
        c = n(3);
        d = -n(1)*v1(1) - n(2)*v1(2) - n(3)*v1(3);

        % equation of the helix
        % z = s*(atan(y/x) + theta)

        for j=1:length(xrange)
            xo = xrange(j);
            e = 1/xo;
            f = a*xo + theta*c*s;
            g = c*s;

            % intersection of the plane and the helix
            % f + b*y + g*atan(e*y) = 0 = f(y)
            func = @(y)f + b*y + g*atan(e*y);
            % rootfind this equation
            yo = fzero(func,yo); % seed the next round
            % find z
            zo = -a*xo/c - b*yo/c - d/c;

            %%%%% check edge limits on (xo,yo,zo)
            % equation of a line
            %

            % within universe?
            xp = round(xo)+universe(1)/2;
            yp = round(yo)+universe(2)/2;
            if (xp < 1) || (xp > universe(1)) || (yp < 1) || (yp > universe(2))
                continue;
            end
            
            % add to image array
            frameset(xp, yp, p) = 1;
        end
    end
    
    theta = theta + inc;
    if (theta >= 2*pi)
        theta = 0;
    end
    
    if testing
        % save current img
        str = strcat(folder,'/frame',num2str(k),'.png');
        pix = 255* cat(3, frameset(:,:,p), frameset(:,:,p), frameset(:,:,p));
        imwrite(pix, str);
    end
    
    p = p + 1;
    if (p > fpi)
        str = strcat(folder,'/image',num2str(img),'.png');
        % multiplex images
        for q=1:universe(1)
            for w=1:universe(2)
                % check endianness, generalize
                rr = bin2dec(num2str(frameset(q,w,1:8)));
                gg = bin2dec(num2str(frameset(q,w,9:16)));
                bb = bin2dec(num2str(frameset(q,w,17:24)));
                frameset(q,w,1) = rr;
                frameset(q,w,2) = gg;
                frameset(q,w,3) = bb;
            end
        end
        imwrite(frameset(:,:,1:3), str);
        
        img = img + 1;
        p = 1;
        frameset = zeros(universe(1),universe(2),fpi);
    end
end

% create a movie
