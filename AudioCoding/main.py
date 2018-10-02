# Python 2.7
from functions import *
from HuffmanCodeBook import *

#Opening the file Track48.wav
print("Opening the file Track48.wav")
sample_rate, fil = scipy.io.wavfile.read('C:\Python27\Seminar1\Track48.wav')

elpsec = len(fil)/28
elp3sec=elpsec*5
middle = len(fil)/2
arr = []
arr = fil[middle:middle+elp3sec]
chan1 = arr[:,0]
chan2 = arr[:,1]

samples1 = np.array(list(chan1), dtype = np.float)
samples2 = np.array(list(chan2), dtype = float)
samples = np.array(list(fil), dtype = float)

N = 128 #subbands
L = 2*N
q = 8

#sampling frequency of audio signal sample rate
maxfreq=sample_rate/2
alpha=0.6  #Exponent for non-linear superposition of spreading functions
bark_sub =48  #number of subbands in the bark domain

h = np.zeros((L,1)) #skeleton for windowfunction
for n in range(2*N-1):
    h[n] = np.sin((np.pi / (2 * N)) * (n + 0.5)) #window function

###################Call functions###############################################
#AnalisisDirectMDCT
Analis, H, iter128 = AnalisisDirectMDCT(samples1, N, h)

#Constructing mapping matrix W
W = mapping2barkmat(sample_rate,bark_sub,N)
'''
plt.imshow(W)
plt.title('Matrix W as Image')
plt.show()
'''
W_inv = mappingfrombarkmat(W,N)
W_inv = nan2zero(N, bark_sub, W_inv)
'''
plt.imshow(W_inv)
plt.title('Matrix W_inv as Image')
plt.show()
'''
#Maps (warps) magnitude spectrum vector mX from MDCT to the Bark scale
mXbark = mapping2bark(Analis,W,N)

#computes a matrix with shifted spreading functions in each column, in the Bark scale.
spreadingfuncmatrix = spreadingfunctionmat(maxfreq,bark_sub,alpha)
'''
plt.imshow(spreadingfuncmatrix)
plt.title('Matrix spreadingfuncmatrix as Image')
plt.xlabel('Bark Domain Subbands')
plt.ylabel('Bark Domain Subbands')
plt.show()
plt.plot(spreadingfuncmatrix)
plt.title('Spreading mat plot')
plt.show()
'''
#Computes the masking threshold on the Bark scale with non-linear superposition
masking_threshold=maskingThresholdBark(mXbark,spreadingfuncmatrix,alpha)
'''
plt.plot(masking_threshold)
plt.title('Masking threshold plot')
plt.show()
'''
#masking_threshold in linear
lin_treshold = mappingfrombark(masking_threshold,W_inv)
all_treshold = np.mean(lin_treshold,1)
'''
plt.plot(all_treshold)
plt.title('threshold plot')
plt.show()
'''
#quantization step
q = np.empty(128)
step_size = (all_treshold*12)**0.5
#step_size = ((all_treshold**2)*12)**0.5
q = quantstep(step_size)
'''
plt.plot(q)
plt.title('quantization steps')
plt.show()
'''
#quantizing signal
quantfunc = np.zeros((N,iter128)) #skeleton for siglal after quantizing
for k in range(N):
    quantfunc[k,:] = quant(Analis[k,:], q[k]) #quantizing

#multiplexor
x,y = quantfunc.shape
#print(quantfunc.shape)
mux = np.zeros((1,x*y+N))
for k in range(N):
    mux[:,0+k*y:y+k*y] = quantfunc[k,:]

mux[0,x*y:x*y+N] = q
mux = mux[:,0:x*y]
mux = np.transpose(np.array(tuple(mux), dtype = int))
mux = mux.tolist()

mux1 = []
for h in mux:
    for l in h:
        mux1.append(l)
q = np.transpose(np.array(tuple(q), dtype = int))
q = q.tolist()

for h in q:
        mux1.append(h)
print(mux1[0:5])

#Huffman coding
codebook = huffman(mux1)
print(codebook)
encoded = ''#(len(arr))
#print(encoded.type)
for i in range(len(mux1)):
    encoded = encoded + codebook[mux1[i]]
print(encoded[0:15])

#encoding
encframewk(encoded)
print('The file was encoded by Huffman successfully')

d = open('C:\Python27\Seminar1\encoded_huf.bin', 'r+').readline()

#decodebook
decodebook = dict() #codebook.copy()
decodebook_val = codebook.values()
decodebook_keys = codebook.keys()
d4 = dict()
for h in range(len(decodebook_keys)):
    d4[h] = {decodebook_val[h]:decodebook_keys[h]}
    decodebook.update(d4[h])
print(decodebook)    
#call the function of decoding 
decoded = np.array(tuple(decode(d, decodebook)), dtype = float)
print('The file was decoded by Huffman successfully')
print(decoded[0:5])
#demuxiplexor
demux = np.zeros((x,y))
for k in range(N):
    demux[k,:] = decoded[0+k*y:y+k*y]
q_step = decoded[x*y:x*y+N]

#dequantizing
dequantfunc = np.zeros((N,iter128)) #skeleton for siglal after dequantizing
for k in range(N):
    dequantfunc[k,:] = dequant(demux[k,:], q_step[k]) #dequantizing

#SYNTHESIS
Sinthes, G = SynthesisDirectMDCT(dequantfunc, N, H, q) #SYNTHESIS

#reproducing the signal
CHANNELS =  1
RATE = sample_rate  #Sampling Rate in Hz

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paFloat32, #get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True)
#Reproduce file
audio = Sinthes.astype(np.float32).tostring()
stream.write(audio)

stream.stop_stream()
stream.close()
p.terminate()
print("File reproduced")


