#!/usr/bin/python3

'''
Developed by 
Paulraj, Arogyaswami, Rohit Nabar, and Dhananjay Gore. 
Introduction to space-time wireless communications. Cambridge university press, 2003. - p.40
'''

import numpy as np 

Mr = 2 # Number of receive antennas
Mt = 2 # Number of transmitt antennas
L = 1000 # Number of snapshots

# Channel matrix
H = (np.random.randn(Mr,Mt,L) + 1j*np.random.randn(Mr, Mt, L))/np.sqrt(2); #Rayleigh flat fading

## Let us divide main formula and avereging to two loops for better representation

# Spatial correlation
R = np.zeros((Mr*Mr, Mt*Mt, L), dtype = 'complex');
for i in range(L):
	R[:,:,i] = np.dot(H[:,:,i].reshape((Mr*Mt, 1)), np.matrix(H[:,:,i].reshape((Mr*Mt, 1))).H); # R = vec(H)*vec(H)'

# Expected value
RR = np.zeros((Mr*Mr, Mt*Mt), dtype = 'complex');
for i in range(L):
	RR = RR + R[:,:,i];

RR = (RR/L) # R = E{vec(H)*vec(H)'}

print(RR)


'''
MATLAB / Octave example 

Mr = 2; % Number of receive antennas
Mt = 2; % Number of transmitt antennas
L = 1000; % Number of snapshots

% Channel matrix
H = (randn(Mr,Mt,L) + 1j*randn(Mr, Mt, L))./sqrt(2); %Rayleigh flat fading

% Spatial correlation
for i = 1:L
    R(:,:,i) = reshape(H(:,:,i), Mr*Mt, 1)*reshape(H(:,:,i), Mr*Mt, 1)'; % R = vec(H)*vec(H)'
end

% Expected value
RR = zeros(Mr*Mr, Mt*Mt);
for i = 1:L
    RR = RR + R(:,:,i);
end

RR = (RR./L) % R = E{vec(H)*vec(H)'}

'''
