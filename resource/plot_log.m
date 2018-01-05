function PlotCarlsonLog(logfile)
%PLOTCARLSONLOG Plot Carlson log file
%   PLOTCARLSONLOG(N) where N is the number of the log file to load
%
%   NOTE: see subsections below for generating analysis plots
%
%14 August 2017, Benjamin Shanahan.

% filename = sprintf('../log/archive/LOG_%02d.txt',n);
data     = csvread(logfile);    % load data

% extract all data
startIdx = 1;  % define this in post
timestamp   = data(startIdx:end,1);
state       = data(startIdx:end,2);
fusion      = data(startIdx:end,[3  4  5]);
compass     = data(startIdx:end,[6  7  8]);
accel       = data(startIdx:end,[9  10 11]);
gyro        = data(startIdx:end,[12 13 14]);

% plotting data
h = figure;
lbls = {};
hold on;
window = 100;  % smoothing Gaussian window size
% timeAxisLimits = [timestamp(1) timestamp(end)];
timeAxisLimits = [23 33];  % defined in post, I think this was flight -> apogee
prop = '.';  % plot line properties

%% Add rocket internal state to plot
plot(timestamp, state, prop);  lbls = [lbls; 'State'];

%% Plot Fused data (RTQF method)
% Raw
if true
    %     plot(timestamp, fusion(:,1), prop);  lbls = [lbls; 'Roll'];
    plot(timestamp, fusion(:,2), prop);  lbls = [lbls; 'Pitch'];
    %     plot(timestamp, fusion(:,3), prop);  lbls = [lbls; 'Yaw'];
end

%% Plot Acceleration (accelerometer)
% Raw
if true
    %     plot(timestamp, accel(:,1), prop);  lbls = [lbls; 'Accel X (G)'];
    %     plot(timestamp, accel(:,2), prop);  lbls = [lbls; 'Accel Y (G)'];
    plot(timestamp, accel(:,3), prop);  lbls = [lbls; 'Accel Z (G)'];
end
% % Smoothed
% if false
%     plot(timestamp, smsig(accel(:,1),window));  lbls = [lbls; 'Smoothed Accel X (G)'];
%     plot(timestamp, smsig(accel(:,2),window));  lbls = [lbls; 'Smoothed Accel Y (G)'];
%     plot(timestamp, smsig(accel(:,3),window));  lbls = [lbls; 'Smoothed Accel Z (G)'];
% end

%% Plot Magnetic Field (compass)
% Raw
if false
    %     plot(timestamp, compass(:,1), prop);  lbls = [lbls; 'Compass X (?)'];
    %     plot(timestamp, compass(:,2), prop);  lbls = [lbls; 'Compass Y (?)'];
    plot(timestamp, compass(:,3), prop);  lbls = [lbls; 'Compass Z (?)'];
end

%% Plot Angular Acceleration (gyroscope)
% Raw
if false
    %     plot(timestamp, gyro(:,1), prop);  lbls = [lbls; 'Gyro X (deg/s^2)'];
    %     plot(timestamp, gyro(:,2), prop);  lbls = [lbls; 'Gyro Y (deg/s^2)'];
    plot(timestamp, gyro(:,3), prop);  lbls = [lbls; 'Gyro Z (deg/s^2)'];
end
% % Smoothed
% if false
%     plot(timestamp, smsig(gyro(:,1),window));  lbls = [lbls; 'Gyro X (deg/s^2)'];
%     plot(timestamp, smsig(gyro(:,2),window));  lbls = [lbls; 'Gyro Y (deg/s^2)'];
%     plot(timestamp, smsig(gyro(:,3),window));  lbls = [lbls; 'Gyro Z (deg/s^2)'];
% end

%% continue
hold off;
legend(lbls);
xlim(timeAxisLimits);
xlabel('Time (s)');

    function sm = smsig(data,windowSize)
        %SMSIG Smooth data using Gaussian window
        %   SMSIG(DATA,WINDOWSIZE) Smooth inputted data via a Gaussian
        %   window function.
        %
        %21 April 2015, Benjamin Shanahan.
        
        if mod(windowSize, 2) ~= 0
            error('windowSize must be an even number.');
        end
        
        half = windowSize / 2;
        filt = gausswin(windowSize); % create filter
        filt = filt / sum(filt); % normalize
        sm_pre = conv(data, filt); % convolve w filter
        
        sm = sm_pre(half : (end - half)); % return 
    end

end