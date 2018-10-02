
import scipy
from scipy import signal
import scipy.io.wavfile
import pyaudio
import wave
import sys
import numpy as np
import numpy.linalg as nplg
import matplotlib.pyplot as plt
import pickle as pic
import scipy.fftpack as spf
import struct

def AnalisisDirectMDCT(input, N, h): #the input signal, number of subbands, window function
    L =2*N
    H = np.zeros((N,L)) #skeleton for analisis H matrix
    pr = (L+len(input)-1) #lengh (number of coloumn) of signal after convolution
    Analysis_Mat = np.zeros((N,pr)) #skeleton for matrix after convolution
    print('Analisis...')
    #analisis
    for k in range(N): #rows
        for n in range(L): #coloumns
            H[k,n] = h[n]*np.cos((np.pi/N)*(k+0.5)*(n+0.5-(N/2))) #analisis H matrix
        Analysis_Mat[k,:] = np.convolve(input,H[k,:]) #convolution
    d, c = Analysis_Mat.shape
    e = c - L + 1 #length (number of rows) of signal after convolution without last 255
    MatCut = Analysis_Mat[:,0:e]
    print('Downsampling...')
    #downsampling
    iter128 = e/N #number of rows that sould be stay after downsampling
    cutmat = int(np.floor(iter128)*N) #number of rows that sould follow to downsampln block (cut rows that are not fold to N)
    Analis = np.zeros((N,iter128)) #skeleton for signal after downsampling
    Post_Fin_Mat = MatCut[:,0:cutmat]#input for downsampling block
    for j in range(iter128):
        Analis[:,j] = Post_Fin_Mat[:,0+j*N] #downsampling (it may be more simple without loop,of course)
    print('Successfully!')
    return Analis, H, iter128

# The part of the perceptual model was developed by Prof. Dr.-Ing. Schuller's examples mostly.
def freq2bark(f):
        Brk = 6. * np.arcsinh(f/600.)                                                 
        return Brk

def mapping2barkmat(sample_rate, bark_sub, N):
  step_barks = 24.0/(bark_sub-1)
  f = np.arange(N) * sample_rate / (2 * N)
  binbarks = freq2bark(f)
  W = np.zeros((bark_sub, N))
  for i in xrange(bark_sub):
     W[i, 0:N] = (np.round(binbarks/step_barks)== i)
  return W

def mapping2bark(mX,W,N):
  mXbark = (np.dot(W, np.abs(mX)**2.0))**(0.5)
  return mXbark

def spreadingfunctionmat(maxfreq,bark_sub,alpha):
        fbdb=7.5     # Upper slope of spreading function
        fbbdb=26.0   # Lower slope of spreading function   
        maxbark=freq2bark(maxfreq)
        spreadingfunctionBarkdB=np.zeros(2*bark_sub)
        
        #Spreading functions for all bark scale bands in a matrix:
        spreadingfuncmatrix=np.zeros((bark_sub,bark_sub))
        for k in range(bark_sub):
            fadB= 14.5+(k/2)+5 # Simultaneous masking for tones at Bark band 12
            #upper slope, fbdB attenuation per Bark, over maxbark Bark (full frequency range), with fadB dB simultaneous masking:
            spreadingfunctionBarkdB[0:bark_sub]=np.linspace(-maxbark*fbdb,-2.5,bark_sub)-fadB
            #lower slope fbbdb attenuation per Bark, over maxbark Bark (full frequency range):
            spreadingfunctionBarkdB[bark_sub:2*bark_sub]=np.linspace(0,-maxbark*fbbdb,bark_sub)-fadB
            #Convert from dB to "voltage" and include alpha exponent
            spreadingfunctionBarkVoltage=10.0**(spreadingfunctionBarkdB/20.0*alpha)

            spreadingfuncmatrix[:,k]=spreadingfunctionBarkVoltage[(bark_sub-k):(2*bark_sub-k)]
	return spreadingfuncmatrix

def maskingThresholdBark(mXbark,spreadingfuncmatrix,alpha): 
  mTbark=np.dot(spreadingfuncmatrix, mXbark**alpha)
  #apply the inverse exponent to the result:
  mTbark=mTbark**(1.0/alpha)
  return mTbark

def mappingfrombarkmat(W,N):
  W_inv= np.dot(np.diag((1.0/np.sum(W,1))**0.5), W[:,0:N+1]).T
  return W_inv  

def nan2zero(N, bark_sub, W_inv):
    for i in range(N):
        for j in range(bark_sub):
            if np.isnan(W_inv[i, j]):
                W_inv[i, j] = 0
    return W_inv

def mappingfrombark(masking_threshold,W_inv):
  lin_treshold = np.dot(W_inv, masking_threshold)
  return lin_treshold

def quantstep(x):
    n = np.log2(abs(x))
    n = np.floor(n)
    for i in np.arange(n.size):
        if n[i]<0:
            n[i]=0
    return n

#quantizing
def quant(examp,q):
    max_range = max(examp)
    min_range = min(examp)
    qfin = (float(abs(max_range))+float(abs(min_range)))/(2**q)
    ind0 = np.round(examp/qfin)    #quant
    ind = np.array(tuple(ind0), dtype = float)
    return ind

#dequantizing
def dequant(examp,q):
    max_range = max(examp)
    min_range = min(examp)
    qfin = (float(abs(max_range))+float(abs(min_range)))/(2**q)
    ind0 = examp*qfin    #dequant
    return ind0
    
def SynthesisDirectMDCT(input, N, H, q):
    L = 2*N
    a, b = input.shape    # number of rows and collumns of input 
    print('Upsampling...')
    #upsampling
    upsamp = np.zeros((a,b*N)) #skeleton for signal that should be after upsampling
    for i in range(b):
        upsamp[:,0+N*i] = input[:,i]
    print('Synthesis...')
    m,n= upsamp.shape
    #synthesis
    R = L + n - 1 #legth of signal (number o rows) that should be after convolution 
    Final = np.zeros((N,R)) #skeleton for signal that should be after convolution 
    G = (np.fliplr(H))/(N/2) #Synthesis matrix
    for k in range(N):
        Final[k,:] = np.convolve(upsamp[k,:], G[k,:]) #convolution
    c,d = Final.shape
    e  = d-L+1
    FinalCut = Final[:,0:e]
    
    #normalization
    FinPreNorm = np.zeros((1,e)) #skeleton for signal after sum of all subbands
    maxprenorm = np.zeros((1,e)) #skeleton for array of maximum of each subband
    Norm = np.zeros((N,e))
    for k in range(N):
        if q[k] <= 0:
            q[k] = 1
        Norm[k,:] = FinalCut[k,:]/2**(q[k]-1)
    for r in range(e):
        FinPreNorm[:,r] = np.sum(Norm[:,r])#sum of all subbands 
    print('Successfully!')
    return FinPreNorm, G

#Create the function of encoding
def encframewk(f):
    #create the empty file bin
    n = open('C:\Python27\Seminar1\encoded_huf.bin', 'r+')
    #q_bin = open('C:\Python27\Seminar1\q_bin.bin', 'wb')
    #serialization
    n.write(f)
    #du = pic.dump(f, n, pic.HIGHEST_PROTOCOL)
    #q_file = pic.dump(q, q_bin, pic.HIGHEST_PROTOCOL)
    return 

#Create the function of decoding
def decframewk(d):
    #decoding file
    w = pic.load(d)
    #q_step = pic.load(q_bin)
    #saving the decoding file in wav
    www = scipy.io.wavfile.write('C:\Python27\Seminar1\decoded_huf.wav',44100, w)
    return www
    
def decode(encoded, decodebook):
    decodebook_val = decodebook.values()
    decodebook_keys = decodebook.keys()
    symb =''
    decoded = []
    for bit in encoded:
        symb += bit
        for dec_key in range(len(decodebook_val)):
            if decodebook_keys[dec_key] == symb:
                decoded.append(decodebook_val[dec_key])
                symb = ''
                break
    return decoded
