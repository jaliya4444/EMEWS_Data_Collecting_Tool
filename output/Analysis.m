clear all;
close all;

signal=csvread('a5.csv');
time=signal(:,4);
amplitude=signal(:,5);

amplitude=amplitude-mean(amplitude);

for i=1:length(time)-1
    diffs(i)=time(i+1)-time(i);
end
avgDiff=mean(diffs);
cuttoff_calculated=1/(avgDiff*10^(-6));
fs=cuttoff_calculated

figure('Name','Orginal Signal')
plot(time, amplitude)
title('Orginal Signal')
xlabel('Time (s)')
ylabel('Amplitude (V)')