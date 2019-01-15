# Convolutional codes basics

## Summary

## Reed-Solomon Convolutional concatenated (RSCC) codes

Very popular option of the FEC in the satellite communication systems.
![RSCC](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/rsc.png)
Fig. 1.3.1. Deep-space concatenated coding system. \[1, p. 433\]

It relates to the [deep-space communication standard](https://ipnpr.jpl.nasa.gov/progress_report/42-63/63H.PDF) that allows to achieve sufficiently high BER performance.

> You can read more about concatenated codes in [Scholarpedia](http://www.scholarpedia.org/article/Concatenated_codes#RS60), peer-reviewed open-access encyclopedia.

### Little bit more about Reed-Solomon codes

Reed-Solomon (RS) codes is the type of [cyclic codes](https://en.wikipedia.org/wiki/Cyclic_code), i.e. a block codes, where the circular
shifts of each code word gives another code word. Moreover, RS codes can be defined as the specific, **non-binary** case of the [Bose–Chaudhuri–Hocquenghem (BCH)](https://en.wikipedia.org/wiki/BCH_code) codes. 

Syndrome decoding is used:

![syndr](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/syndrome.png)

Frequently are measured in symbols (bytes, blocks). Code rate can be calculated as:

![RScoderate](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/RScoderate.png)

Can correct **t** symbols. The BER performance has the step-like character:


> **Extra links**: 
>
> [MATLAB source code](https://en.wikipedia.org/wiki/Reed%E2%80%93Solomon_error_correction#History)
>
> [MatLab RS encoder](https://www.mathworks.com/help/comm/ref/comm.rsencoder-system-object.html)
>
>[MatLab RS decoder](https://www.mathworks.com/help/comm/ref/comm.rsdecoder-system-object.html)


### Little bit more about interleaving

![interleaving](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/interleaving.png)


### Outlooks of the RSCC

Very old technique [2]. The part of the DVB-S standard, however was replaced in [DVB-S2](https://en.wikipedia.org/wiki/DVB-S2):

![DVB-S2](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/DVB_S2fec.png)

Since 2000-s modern error correction schemes, such as Turbo codes, are used more widely in space communications \[3\].

![TurboRSCC](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/turbovsrsBER.png)
Fig. 1.3.2. Bit error rate curves for several codes with rates near 1/6: k=1784 and k=8920 turbo codes and the (n=255, k=223) Reed–Solomon code concatenated with a constraint length N=15, rate 1/6 convolutional code. \[3\]

RSCC codes have the comparable complexity with Turbo codes \[4\], however worse BER performance (fig. 1.3.2). 

## Turbo convolutional codes

[Turbo convolutional codes](http://www.scholarpedia.org/article/Turbo_code) are the part of the mobile communication (UMTS, CDMA2000, LTE), broadcast (DVB-RCS, DVB-RCT, DVB-SSP), deep space (CCSDS) and other standards.

The structure of the encoder can be represented as:

![TurboEncoder](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/TurboEncoder.png)

Information in the input of the encoder is processed by blocks (chunks), the length of the block directly influences BER performance.

> Very interesting research can be found also in [\[5\]](https://publik.tuwien.ac.at/files/publik_262129.pdf) where capabilities of Turbo convolutional, LDPC and Polar codes are considered.

Turbo covolutional decoders use **MAP** (maximum a posteriori probability) algorithms unlike convolutional codes. For example, classical  **BCJR** (Bahl, Cocke, Jelinek and Raviv)\[6\]. More simple implementations such as **Log-MAP**, **MAX-Log-MAP** or **SOVA** of Turbo convolutional decoder are also exist \[7\]. 

> **See also**:
>
> [Turbo encoder MatLab object](https://www.mathworks.com/help/comm/ref/comm.turboencoder-system-object.html)
> 
> [Turbo decoder MatLab object](https://www.mathworks.com/help/comm/ref/comm.turbodecoder-system-object.html)


## References

\[1\] J. Hagenauer, E. Offer, and L. Papke, Reed Solomon Codes and Their Applications. New York IEEE Press, 1994

\[2\] Ebert, P. M., and S. Y. Tong. "Convolutional Reed‐Solomon Codes." Bell Labs Technical Journal 48.3 (1969): 729-742.

\[3\] Andrews, Kenneth S., et al. "The development of turbo and LDPC codes for deep-space applications." Proceedings of the IEEE 95.11 (2007): 2142-2156.

\[4\] Balaji, Pavithra, et al. "Evaluation of decoding trade-offs of concatenated RS convolutional codes and turbo codes via trellis." Signal Processing and Integrated Networks (SPIN), 2015 2nd International Conference on. IEEE, 2015.

\[5\] Tahir, Bashar, Stefan Schwarz, and Markus Rupp. "BER comparison between Convolutional, Turbo, LDPC, and Polar codes." Telecommunications (ICT), 2017 24th International Conference on. IEEE, 2017.

\[6\] Bahl, Lalit, et al. "Optimal decoding of linear codes for minimizing symbol error rate (corresp.)." IEEE Transactions on information theory 20.2 (1974): 284-287.

\[7\] Chatzigeorgiou, Ioannis Ap, and Clare Hall. Performance analysis and design of punctured turbo codes. Diss. Ph. D. dissertation, University of Cambridge, Cambridge, England, 2006.


