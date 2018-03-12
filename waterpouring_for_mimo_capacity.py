'''
By Paulraj, Arogyaswami, Rohit Nabar, and Dhananjay Gore. 
Introduction to space-time wireless communications. Cambridge university press, 2003. – p. 68-69
'''

import numpy as np
from numpy import linalg as LA

def waterporing(Mt, SNR_dB, H_chan):
	SNR = 10**(np.log10(SNR_dB)/10)
	r = LA.matrix_rank(H_chan)
	H_sq = np.dot(H_chan,np.matrix(H_chan).H)
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
	return gammas

# Testing
Mt = 4
SNR_db = 10
H_chan = np.array([[1,0,2],[0,1,0], [0,1,0]], dtype = np.float)
gammas = waterporing(Mt, SNR_db, H_chan)

print(gammas)
