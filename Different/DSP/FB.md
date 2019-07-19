# Filter Banks: a part of MP3 
## M.Sc. Vladimir Fadeev
### Kazan, 2019

## Introduction

I believe there is no visitor who would not hear about the MP3 standard (MPEG-1 Layer III), so I don't see any sense in the long introduction. The format is known largely due to its compactness and rather good quality (in terms of indifferent to lossless formats). Nowadays, it is very outdated, but it still exists in the players of some music lovers, and on online music sites (perhaps more now in the form of its reincarnation - the AAC format).

How was the balance between size and quality found? In short:
1. the application of filter banks
2. the application of the psycho-acoustic (perceptual) model at the process of compression of non-information (irrelevance) data
3. the use of [entropy coding](https://github.com/kirlf/CSP/blob/master/Different/Coding_Theory/README.md) at the process of getting rid of redundancy.

<img src = "https://raw.githubusercontent.com/kirlf/CSP/master/Different/DSP/assets/codec_scheme.png" width = "700">

*Fig. 1. Structure of perceptual Audio Coders*

In this tutorial, filter banks will be considered (see slides **02 Filterbanks1, NobleID** and **03 FilterBanks2**  (TU Ilmenau) via the following [link](https://www.tu-ilmenau.de/mt/lehrveranstaltungen/lehre-fuer-master-mt/audio-coding/)).

## Main idea

In general, the main idea can be described as follows: we have a line of parallel filters, which are consistently tuned to their own frequency. Frequencies are usually normalized from 0 to pi. Accordingly, the more filters we have at our disposal, the rarer (smoother) the transition step from frequency to frequency becomes, and therefore more frequency variations can be analyzed.

Filters are Fourier converters in one form or another mostly: [FFT](https://github.com/kirlf/CSP/blob/master/Different/DSP/FFT.md), [DCT-IV](https://www.tu-ilmenau.de/fileadmin/media/mt/lehre/ma_mt/audiocoding/Lecture_WS2013_14/04_shl_Filterbanks1_NobleID_WS2013-14.pdf), [MDCT](https://www.tu-ilmenau.de/fileadmin/public/mt_ams/public/mt_ams/Audio_C.pl/aft/aft/aft_de/file/deal_ws2013_Noble/Lecture_WS2013_14/04_shl_Filterbanks1_NobleID_WS2013-14.pdf), [PQMF](https://www.tu-ilmenau.de/fileadmin/public/mt_ams/Audio_Coding/Vorlesung/WS_2016-17/07_shl_PQMF_MPEG1-2BC_WS2016-17.pdf), etc.

## Restrictions

Too large number of filters cannot be selected due to the pre-echo effect. 
![](https://raw.githubusercontent.com/kirlf/CSP/master/Different/DSP/assets/preecho.PNG)

*Fig. 2. In audio coding, Pre-echoes appear before transients. Reason: blocks too long (too many bands).*

## Types

There are several methods for using a filter bank. Consider the most famous:
1. Direct application

<img src = "https://raw.githubusercontent.com/kirlf/CSP/master/Different/DSP/assets/fb_scheme.PNG" width = "700">

*Fig. 3. Block scheme of the direct implementation of Filter Banks.*

2. [Noble Identities](https://www.tu-ilmenau.de/fileadmin/media/mt/lehre/ma_mt/audiocoding/Lecture_WS2013_14/04_shl_Filterbanks1_NobleID_WS2013-14.pdf)

**Home task**: Explain what is the advantage of one method over another?

## Down-sampling and Up-sampling

We willy-nilly increase the number of samples in the process of applying parallel filters, and therefore the playback frequency and the size of the file being increased. In order to avoid such consequences, two mirror procedures are applied:

1. The operation of "down-sampling" by factor N describes the process of keeping every N-th sample discarding the rest.

<img src="https://raw.githubusercontent.com/kirlf/CSP/master/Different/DSP/assets/downsampl.PNG" width="700">

*Fig. 4. Down-sampling procedure illustration.*

2. The operation of “up-sampling“ by factor N describes the insertion of N-1 zeros between every sample of the input. 

<img src="https://raw.githubusercontent.com/kirlf/CSP/master/Different/DSP/assets/upsampl.PNG" width="700">

*Fig. 5. Up-sampling procedure illustration.*

## Math description

We will consider the method of MDCT (Modified Discret Cosine Transform) during this tutorial:

<p align="center" style="text-align: center;"><img align="center" src="https://tex.s2cms.ru/svg/%20h_k(L-1-n)%20%3D%20h(n)cos%5Cleft(%5Cfrac%7B%5Cpi%7D%7BN%7D(k%2B0.5)(n%2B0.5-%5Cfrac%7BN%7D%7B2%7D)%5Cright)%20" alt=" h_k(L-1-n) = h(n)cos\left(\frac{\pi}{N}(k+0.5)(n+0.5-\frac{N}{2})\right) " /></p>

where the index <img src="https://tex.s2cms.ru/svg/%20k%20" alt=" k " /> is the filter number from 0 to <img src="https://tex.s2cms.ru/svg/N-1" alt="N-1" /> (<img src="https://tex.s2cms.ru/svg/%20N%20" alt=" N " /> is the length of the filter), <img src="https://tex.s2cms.ru/svg/%20n%20" alt=" n " /> is the count number from 0 to <img src="https://tex.s2cms.ru/svg/%202N-1%20" alt=" 2N-1 " />, and <img src="https://tex.s2cms.ru/svg/%20h(n)%20" alt=" h(n) " /> is some window function. Note that the representation is given in the time domain. As a window function, select a sine window:


<p align="center" style="text-align: center;"><img align="center" src="https://tex.s2cms.ru/svg/%20h(n)%20%3D%20sin%5Cleft(%5Cfrac%7B%5Cpi%7D%7BL%7D(n%2B0.5)%5Cright)%20" alt=" h(n) = sin\left(\frac{\pi}{L}(n+0.5)\right) " /></p>

where <img src="https://tex.s2cms.ru/svg/%20L%20%3D%202N%20" alt=" L = 2N " /> is the window length.
As a rule, the same mathematical functions are used for analysis and synthesis.


## MDCT modeling

``` python

import numpy as np
import matplotlib.pyplot as plt

N = 8 # number of subbands
L = 2*N # number of filters

# Window function:

h = np.zeros((L,1)) #skeleton for window function
for n in range(2*N-1):
    h[n] = np.sin((np.pi / (2 * N)) * (n + 0.5)) #window function
    
# Considered signal

w = [30, 100, 300]
a = [1.1, .5, .1]
x = 0

t = np.array([i for i in range(1,3001)])/1000
for idx in range(len(w)):
    x = x + a[idx]*np.sin(2*np.pi*w[idx]*t)
    
FFT = np.fft.fft(x)
amps = np.abs(FFT) / (len(FFT) / 2)
fs = 1 / (t[1]-t[0])
f = fs*np.array([i for i in range(int(len(x)))]) / len(x)

plt.subplots(1, 1, figsize=(6, 4), dpi=150)
plt.stem(f[:int(len(f)/2)], amps[:int(len(f)/2)])
plt.ylabel('Magnitude of the FFT')
plt.xlabel('Frequencies (Hz)')
plt.grid(True)
plt.show()
```

![](https://habrastorage.org/webt/8o/q-/pl/8oq-pluoy6zn53dsv1mpp2bx6zy.png)

Analysis:

``` python
H = np.zeros((N,L)) #skeleton for analisis H matrix
pr = (L+len(x)-1) #lengh (number of coloumn) of signal after convolution
Analysis_Mat = np.zeros((N,pr)) #skeleton for matrix after convolution
for k in range(N): #rows
    for n in range(L): #coloumns
        H[k,n] = h[n]*np.cos((np.pi/N)*(k+0.5)*(n+0.5-(N/2))) #analysis H matrix
    Analysis_Mat[k,:] = np.convolve(x,H[k,:]) #convolution
```

After applying the convolution operation, the size of our input sequence will naturally increase by 𝐿 − 1.

Down-sampling:

``` python
# Number of samles that sould be stay after downsampling:
M = int(Analysis_Mat.shape[1] / N) 
# Number of rows that sould follow to downsampln block (cut rows that are not fold to N)
cutmat = int(np.floor(M)*N) 

Analysis_Mat_DS = np.zeros((N, M))
Analysis_Mat = Analysis_Mat[:, :cutmat]

for k in range(N):
    Analysis_Mat_DS[k, :] = Analysis_Mat[k,::N]
```

Up-sampling:

``` python
Analysis_Mat_US = np.zeros((N, Analysis_Mat_DS.shape[1]*N)) 
for n in range(Analysis_Mat_DS.shape[1]):
    Analysis_Mat_US[:,0+N*n] = Analysis_Mat_DS[:, n]
```

Synthesis:

``` python
R = L + Analysis_Mat_US.shape[1] - 1 #legth of signal (number o rows) that should be after convolution 
Syntesis_Mat = np.zeros((N,R))  
G = (np.fliplr(H))/(N/2) #Synthesis matrix
for k in range(N):
    Syntesis_Mat[k,:] = np.convolve(Analysis_Mat_US[k,:], G[k,:]) #convolution
y = np.sum(Syntesis_Mat, axis=0)

FFT = np.fft.fft(y)
amps = np.abs(FFT) / (len(FFT) / 2)
fs = 1 / (t[1]-t[0])
f = fs*np.array([i for i in range(int(len(x)))]) / len(x)

plt.subplots(1, 1, figsize=(6, 4), dpi=150)
plt.stem(f[:int(len(f)/2)], amps[:int(len(f)/2)])
plt.ylabel('Magnitude of the FFT')
plt.xlabel('Frequencies (Hz)')
plt.grid(True)
plt.show()
```

![](https://habrastorage.org/webt/wc/uw/5w/wcuw5w5b5xrmb142mt8yg9ijbog.png)

Did additional harmonics appeare due to some mistake? Join the [discussion](https://dsp.stackexchange.com/questions/58822/why-do-additional-harmonics-arise-after-the-filter-bank).

## Is ideal reconstruction possible?

* Ideal filters are not realizable
* In the time domain they would mean a convolution of our signal with a Sinc function
* Sinc function is infinitely long and not causal, meaning it causes infinite delay
* We can not simply use a DFT or FFT to obtain an ideal filter in the frequency domain either
* Because the DFT also represents a filter bank, but a special type
* Its equivalent filters are far from perfect filters (hence we cannot make ideal filters with it), not good enough for our purposes
(audio coding and the ear), as we will see
* Don‘t use your eye (looking at waveforms) to guess what the ear might be hearing (quite different processing)

## Suggested literature

* [Filter Banks and Audio Coding](https://docviewer.yandex.ru/view/53198835/?*=DP70DW9fr34xVGKzc0e6JIeVai17InVybCI6InlhLWRpc2s6Ly8vZGlzay%2FQo9GH0LXQsdCwL9Cf0YDQvtC50LTQtdC90L3Ri9C5INC80LDRgtC10YDQuNCw0LsvR1JJQVQvSWxtZW5hdS9BdWRpb2NvZGluZy9Cb29rQXVkaW9Db2RpbmcucGRmIiwidGl0bGUiOiJCb29rQXVkaW9Db2RpbmcucGRmIiwidWlkIjoiNTMxOTg4MzUiLCJ5dSI6IjQyMDQ3NTkwNTE0OTQ0ODYxNzciLCJub2lmcmFtZSI6ZmFsc2UsInRzIjoxNTU1OTE5NzY5OTc1fQ%3D%3D) by Gerald Schuller and Karlheinz Brandenburg, 2018
* Bosi, Marina, and Richard E. Goldberg. Introduction to digital audio coding and standards. Vol. 721. Springer Science & Business Media, 2012.
