#!/usr/bin/env python
# coding: utf-8

# # MIMO Channel Capacity
# ### M.Sc. Vladimir Fadeev
# #### Kazan, 2018


import numpy as np
from numpy import linalg as LA
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt


def waterpouring(Mt, SNR_dB, H_chan):
    SNR = 10**(SNR_dB/10)
    r = LA.matrix_rank(H_chan)
    H_sq = np.dot(H_chan,np.matrix(H_chan, dtype=complex).H)
    lambdas = LA.eigvals(H_sq) 
    lambdas = np.sort(lambdas)[::-1]
    p = 1;
    gammas = np.zeros((r,1))
    flag = True
    while flag == True:
        lambdas_r_p_1 = lambdas[0:(r-p+1)]
        inv_lambdas_sum =  np.sum(1/lambdas_r_p_1)
        mu = ( Mt / (r - p + 1) ) * ( 1 + (1/SNR) * inv_lambdas_sum)
        for idx, item in enumerate(lambdas_r_p_1):
            gammas[idx] = mu - (Mt/(SNR*item))
        if gammas[r-p] < 0: #due to Python starts from 0
            gammas[r-p] = 0 #due to Python starts from 0
            p = p + 1
        else:
            flag = False
    res = []
    for gamma in gammas:
        res.append(float(gamma))
    return np.array(res)

#Test
Mt = 3
SNR_db = 10
H_chan = np.array([[1,0,2],[0,1,0], [0,1,0]], dtype = float)
gammas = waterpouring(Mt, SNR_db, H_chan)
print('Rank of the matrix: '+str(LA.matrix_rank(H_chan)))
print('Gammas:\n'+str(gammas))


# Short comparison


def openloop_capacity(H_chan, SNR_dB):
    SNR = 10**(SNR_dB/10)
    Mt = np.shape(H_chan)[1]
    H_sq = np.dot(H_chan,np.matrix(H_chan, dtype=complex).H)
    lambdas = LA.eigvals(H_sq) 
    lambdas = np.sort(lambdas)[::-1]
    c = 0
    for eig in lambdas:
        c = c + np.log2(1 + SNR*eig/Mt)
    return np.real(c)

Mr = 4
Mt = 4
H_chan = (np.random.randn(Mr,Mt) + 1j*np.random.randn(Mr, Mt))/np.sqrt(2) #Rayleigh flat fading
c = openloop_capacity(H_chan, 10)
print(c)   


def closedloop_capacity(H_chan, SNR_dB):
    SNR = 10**(SNR_dB/10)
    Mt = np.shape(H_chan)[1]
    H_sq = np.dot(H_chan,np.matrix(H_chan, dtype=complex).H)
    lambdas = LA.eigvals(H_sq) 
    lambdas = np.real(np.sort(lambdas))[::-1]
    c = 0
    gammas = waterpouring(Mt, SNR_dB, H_chan)
    for idx, item in enumerate(lambdas):
        c = c + np.log2(1+ SNR*item*gammas[idx]/Mt)
    return np.real(c)

c = closedloop_capacity(H_chan, 10)
print(c)  



Mr = 4
Mt = 4
counter = 1000
SNR_dBs = [i for i in range(1, 21)]
C_open = np.empty((len(SNR_dBs), counter))
C_closed = np.empty((len(SNR_dBs), counter))

for c in range(counter):
    H_chan = (np.random.randn(Mr,Mt) + 1j*np.random.randn(Mr, Mt))/np.sqrt(2)
    for idx, SNR_dB in enumerate(SNR_dBs):
        C_open[idx, c] = openloop_capacity(H_chan, SNR_dB)
        C_closed[idx, c] = closedloop_capacity(H_chan, SNR_dB)
    
C_open_erg = np.mean(C_open, axis=1)
C_closed_erg = np.mean(C_closed, axis=1)


fig = plt.figure(figsize=(10, 5), dpi=300)
plt.plot(SNR_dBs, C_open_erg, label='Channel Unknown (CU)')
plt.plot(SNR_dBs, C_closed_erg, label='Channel Known (CK)')
plt.title("Ergodic Capacity")
plt.xlabel('SNR (dB)')
plt.ylabel('Capacity (bps/Hz)')
plt.legend()
plt.grid()
plt.show()


# # Reference
# 
# 1. Paulraj, Arogyaswami, Rohit Nabar, and Dhananjay Gore. 
# Introduction to space-time wireless communications. Cambridge university press, 2003.

# # Suggested literature
# 
# 1. Haykin S. Communication systems. – John Wiley & Sons, 2008. - p.366-368
