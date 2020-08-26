# Task 2: Write and learn (MatLab)

**Tutor**: M.Sc. Vladimir Fadeev

**Form of reports**: PDF file.

# Introduction

Ok, you have already read how a part of the communication system can be modeled during the first practice. It's time to try model whole system by your-self in MatLab! Let us begin from some basics: transmitter, channel, receiver.

# Task

Use the following block scheme as the reference:

<img src="https://raw.githubusercontent.com/kirlf/CSP/master/MIMO/assets/test-model.png" width="800" />

Use **QPSK** with **pi/4** phase rotation as the digital baseband modulation. For this:
1. Apply [pskmod](https://www.mathworks.com/help/comm/ref/pskmod.html) and [pskdemod](https://www.mathworks.com/help/comm/ref/pskdemod.html) MatLab functions;
2. After that write your own (or just writen in MATLAB) solution for modulator and demodulator.

Use the **Rayleigh flat fading** as the channel model. For AWGN use 11 Eb/No points (from 0 to 10 dB).

> See the following tutorial to obtain example of end-to-end communication system modeling (with code!) and required formulas.
>
> [Rician flat fading channel modeling](https://nbviewer.jupyter.org/github/kirlf/CSP/blob/master/MIMO/RicianFlatFadingMATLAB.ipynb)

For bit error ratio calculation use [biterr](https://www.mathworks.com/help/comm/ref/biterr.html) or write something like this by your-self.

Plot the resulting bit error ratio curves and verify your results by [berfading](https://www.mathworks.com/help/comm/ref/berfading.html) function.  

Good luck!

## Hints

1. Look at the following MatLab simulation to obtain example how your-own modem (modulator and demodulator) can be implemented:

[Fast QPSK implementation](https://www.mathworks.com/matlabcentral/fileexchange/72860-fast-qpsk-implementation?s_tid=prof_contriblnk)

2. It is OK to ask questions.