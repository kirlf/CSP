# Fast Fourier transform et al.
## M.Sc. Vladimir Fadeev, M.Sc. Zlata Fadeeva
### Kazan, 2019

Small python examples of the Fast Fourier Transform aplying.

![](https://hsto.org/getpro/habr/post_images/c2e/6c4/40f/c2e6c440f11f538840bf0c4931cb7b8b.jpg)

### FFT - basic example

Briefly **[Fourier transform](https://en.wikipedia.org/wiki/Fourier_transform)** can be described as a signal that allows you to transmit a signal from the time domain to the frequency domain \(and vice versa when using the inverse Fourier transform \),

[**Discrete Fourier Transform**](https://en.wikipedia.org/wiki/Discrete_Fourier_transform) (DFT) can be executed (simplified) as [Fourier Transform](https://habr.com/ru/post/196374/) over discrete signals.

[**Fast Fourier Transform**](https://en.wikipedia.org/wiki/Fast_Fourier_transform) \(FFT\) is a method for calculating the results of the DFT time series \(discrete data samples\).

The FFT calculates the DFT and gives exactly the same result. the most important difference is that the FFT is much faster.

``` python
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

w_1 = 30
w_2 = 50
a = 1.1
b = 0.6
t = np.array([i for i in range(300)])/1000
t = t[1:]
x = a*np.cos(2*np.pi*w_1*t) + b*np.sin(2*np.pi*w_2*t)

FFT = np.fft.fft(x)
amps = np.abs(FFT) / (len(FFT) / 2)
fs = 1 / (t[1]-t[0])
f = fs*np.array([i for i in range(int(len(x)))]) / len(x)

plt.subplots(1, 1, figsize=(6, 4), dpi=150)
plt.stem(f[:50], amps[:50])
plt.ylabel('Magnitude of the FFT')
plt.xlabel('Frequencies (Hz)')
plt.grid(True)
plt.show()
```

<img src="https://raw.githubusercontent.com/kirlf/CSP/master/Different/DSP/FFT.PNG" width="500" >

### Gibs effect

``` python
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

Nsub = 100 # number of subsequences

w_1 = 20 # frequency of the 1st component of the signal (Hz)
w_2 = 40 # frequency of the 2nd component of the signal (Hz)

a = 1.1 # magnitude of the 1st component of the signal
b = 0.6 # magnitude of the 2nd component of the signal

t = np.array([i for i in range(1,301)])/1000 # time samples (s)
fs = 1 / (t[1]-t[0]) # sampling frequency (Hz)

x = a*np.cos(2*np.pi*w_1*t) + b*np.sin(2*np.pi*w_2*t) # considered signal

N = [len(x)-10, len(x), len(x)+10]
fig, ax = plt.subplots(len(N), 1, constrained_layout=True,\
                       figsize=(6, 7), dpi=250)

for idx, item in enumerate(N):
    FFT = np.fft.fft(x, n=item)
    amps = np.abs(FFT) / (len(FFT) / 2)
    ax[idx].stem(f[:20], amps[:20])
    ax[idx].grid(True)
    ax[idx].set_ylabel('Magnitude of the FFT')
plt.xlabel('Frequencies (Hz)')
plt.show()
```

![](https://upload.wikimedia.org/wikipedia/commons/c/c9/FFT_py.png)

### Periodogram - power spectrum estimation (with different windows)

**Power** harmonics can also be evaluated. For this, the [**periodogram method**](https://en.wikipedia.org/wiki/Periodogram) can be considered as one of the simplest methods. In signal processing, the periodogram is an estimate of the spectral density of the signal, or the spectrum itself.

The term was coined by Arthur Schuster in 1898. Today, the periodogram is an integral part of more complex methods. This is the most common tool for studying the amplitude and frequency characteristics of FIR filters and window functions. FFT spectrum analyzers are also implemented as a time series of periodograms.

``` python
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

w_1 = 40 # frequency of the 1st component of the signal (Hz)
w_2 = 60 # frequency of the 2nd component of the signal (Hz)

a = 0.5 # magnitude of the 1st component of the signal
b = 1.0 # magnitude of the 2nd component of the signal

t = np.array([i for i in range(1,301)])/1000 # time samples (s)
fs = 1 / (t[1]-t[0]) # sampling frequency (Hz)

x = a*np.cos(2*np.pi*w_1*t) + b*np.sin(2*np.pi*w_2*t) # considered signal
n = .2*np.random.randn(len(t)) # white Gaussian noise
y = x + n

windows = [None,'hamming']
plt.subplots(1, 1, figsize=(6, 4), dpi=250)

for window in windows:
    if window == None:
        label = 'rect'
    else:
        label = window
    f, Pxx_den = signal.periodogram(y, fs=fs, scaling='spectrum', nfft=2048, window=window)
    plt.semilogy(f[1:200], Pxx_den[1:200], label=label)

plt.subplots(1, 1, figsize=(6, 4), dpi=250)
plt.ylabel('Spectrum')
plt.xlabel('Frequencies (Hz)')
plt.title('Periodogram')
plt.grid(True)
plt.show()
```
![](https://upload.wikimedia.org/wikipedia/commons/5/58/Periodogram_windows.png)

### Bartlett's method - averaged periodogram

In the examples above, we considered the cases of the evaluation of the spectral characteristics of only one implementation. However, having on hand some array of experiments or a sequence long enough to divide it into some subsequences, we can apply one of the simplest methods of noise leveling - averaging.

The periodogram averaging method - **the Bartlett method** - is a consistent estimate of the power spectrum.
We also recommend that you familiarize yourself with the [**welch**] method (https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.signal.welch.html) of the **scipy** library.

``` python
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

Nsub = 100 # number of subsequences

w_1 = 30 # frequency of the 1st component of the signal (Hz)
w_2 = 40 # frequency of the 2nd component of the signal (Hz)

a = 0.7 # magnitude of the 1st component of the signal
b = 0.4 # magnitude of the 2nd component of the signal

t = np.array([i for i in range(1,301)])/1000 # time samples (s)
fs = 1 / (t[1]-t[0]) # sampling frequency (Hz)

x = a*np.cos(2*np.pi*w_1*t) + b*np.sin(2*np.pi*w_2*t) # considered signal

y_mat = np.dot(np.ones((Nsub, 1)), x.reshape((1, len(x)))) # assume that subsequences are identical

Pxx = np.empty((Nsub, int((2048/2)+1)))
for i in range(np.shape(y_mat)[0]):
    y_mat[i,:] = y_mat[i,:] # + 2*np.random.randn(len(t))
    f, Pxx[i,:] = signal.periodogram(y_mat[i,:],nfft=2048,\
                                     fs=fs, scaling='spectrum')
Pxx_bart = np.mean(Pxx, axis=0)

plt.subplots(1, 1, figsize=(6, 4), dpi=250)
plt.semilogy(f[1:150], Pxx_bart[1:150], '-')#, linewidth=2, color='b')
plt.ylabel('Spectrum')
plt.xlabel('Frequencies (Hz)')
plt.title('Bartlett\'s method')
plt.grid(True)
plt.show()
```
![](https://raw.githubusercontent.com/kirlf/CSP/master/Different/DSP/Bartlett.PNG)
