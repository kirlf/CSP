clear all; close all; clc

M = 4; % e.g. QPSK 
bits = log2(M); % bits per modulation symbol

frame_len = 32; % the length of our OFDM frame
message = randi([0 1], 16*bits, 1); % binary information symbols
num_inf_ind = 16; % number of subcarriers (information symbols, actually) in the frame
num_pilots = frame_len - num_inf_ind - 5; % number of pilots
pilots = [1;j;-1;-j]; % what kind of pilots we use
nulls = [1,2,frame_len/2,frame_len-1,frame_len]; %indexes of nulls

if M >= 16
	info_symbols = qammod(message, M, pi/4);
else
	info_symbols = pskmod(message, M, pi/4);
end 

inf_ind_1 = (floor(linspace(4,14,num_inf_ind/2))).'; 
inf_ind_2 = (floor(linspace(18,29,num_inf_ind/2))).';

inf_ind = [inf_ind_1;inf_ind_2]; % simple concatenation

% Of course, we can use only one linspace, 
% however in this case we have to check possition of null in the middle:
%inf_ind = (floor(linspace(3,29,num_inf_ind))).';
%for i = 1:length(inf_ind)
%    if inf_ind(i) == frame_len/2
%        inf_ind(i)  = inf_ind(i) + 1;
%        shift = 1;
%        while inf_ind(i) == inf_ind(i) + shift
%        inf_ind(i)  = inf_ind(i) + 1;
%        shift = shift + 1;
%        end
%    end
%end
% To sum up, I guess, using of two linspaces is more smart solution.

%For pilots we use other MatLab features:
inf_and_nulls = union(inf_ind, nulls); %concatenation and ascending sorting
pilot_indexes = setdiff(1:frame_len, inf_and_nulls); %numbers in range from 1 to frame length 
% that don't overlape with inf_and_nulls vector

% Well done! Now we have to sort our symbols by referent indexes. 
%For this example we will do it via the loop and conditions.

frame = zeros(frame_len, 1); %memory allocation 
% - this step is necessary for our example
% and preferable for other applications due to increasing of processing speed
pilot_pointer = 1; % pointer (not C pointer) to an index in the pilots vector - just a modeling tric
inf_pointer = 1; % pointer (not C pointer) to an index in the message vector - just a modeling tric

% "C-style" of the frame generation
for i = 1:length(frame)
    if (i ~= 1) && (i ~= 2) && (i ~= (length(frame)/2)) && (i ~= length(frame)) && (i ~= (length(frame)-1)) 
    % we know exactly where nulls should be and therefore we permit insertion into these positions
        if mod(inf_pointer, length(inf_ind)+1) == 0  % mod means modulo, second argument means order;
        	% it is equal to modulo-17 (length(inf_ind) = num_inf_ind) in our example
            inf_pointer = inf_pointer - 1; % this step is necessary to avoid 'segmentation fault' 
            % - out of band indexes
         end
        %% Message symbols insertion
        if i == inf_ind(inf_pointer) 
            frame(i) = info_symbols(inf_pointer) 
            inf_pointer = inf_pointer + 1
        %% Pilot symbols insertion 
        else
            frame(i) = pilots(pilot_pointer)
            pilot_pointer = pilot_pointer + 1
            if  mod(pilot_pointer,length(pilots)+1) == 0 %we are scaning pilots vector iteratively
                pilot_pointer = 1 %and switch to the begining when pilot vector ends
            end
        end
    end
end
% So, maybe, it's interesting to know how something can be done in classical way, 
% however more reasonable solution is using of the certain programming language opportunaties   
