# Convolutional codes basics

## Summary

## Reed-Solomon Convolutional concatenated (RSCC) codes

Very popular option of the FEC in the satellite communication systems.
![RSCC](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/rsc.png)
Fig. 1.3.1. Deep-space concatenated coding system. \[1, p. 433\]

It relates to the [deep-space communication standard](https://ipnpr.jpl.nasa.gov/progress_report/42-63/63H.PDF) that allows to achieve sufficiently high BER performance.

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
Fig. 1.3.2. Bit error rate curves for several codes with rates near 1/6: k ¼ 1784 and k¼ 8920 turbo codes and the (n ¼ 255, k¼ 223) Reed–Solomon code concatenated with a constraint length N ¼ 15, rate 1/6 convolutional code. \[3\]





## Turbo convolutional codes


## References

\[1\] J. Hagenauer, E. Offer, and L. Papke, Reed Solomon Codes and Their Applications. New York IEEE Press, 1994
\[2\] Ebert, P. M., and S. Y. Tong. "Convolutional Reed‐Solomon Codes." Bell Labs Technical Journal 48.3 (1969): 729-742.
\[3\] Andrews, Kenneth S., et al. "The development of turbo and LDPC codes for deep-space applications." Proceedings of the IEEE 95.11 (2007): 2142-2156.