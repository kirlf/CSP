### Summary
1. Convolutional codes

    1.1. [Introduction](https://github.com/kirlf/CSP/blob/master/FEC/Convolutional%20codes%20intro.md)

    1.2. [Modeling in MatLab](https://github.com/kirlf/CSP/blob/master/FEC/Convolutional%20codes%20modeling.md)
    
    1.3. [Extensions of the convolutional codes idea](https://github.com/kirlf/CSP/blob/master/FEC/Conv%20codes%20idea%20extensions.md)
    
    1.4. [Python tutorial: Convolutional encoder](https://nbviewer.jupyter.org/format/slides/gist/kirlf/a70a3e65b24c1c80db5874b7d4c0f184#/)

# Extensions of the convolutional codes idea

## Reed-Solomon Convolutional concatenated (RSCC) codes

Very popular option of the FEC in the satellite communication systems.
![RSCC](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/rsc.png)
>Fig. 1.3.1. Deep-space concatenated coding system. \[1, p. 433\]

It relates to the [deep-space communication standard](https://ipnpr.jpl.nasa.gov/progress_report/42-63/63H.PDF) that allows to achieve sufficiently high BER performance.

> You can read more about concatenated codes in [Scholarpedia](http://www.scholarpedia.org/article/Concatenated_codes#RS60), peer-reviewed open-access encyclopedia.

### Little bit more about Reed-Solomon codes

Reed-Solomon (RS) codes is the type of [cyclic codes](https://en.wikipedia.org/wiki/Cyclic_code), i.e. a block codes, where the circular
shifts of each code word gives another code word. Moreover, RS codes can be defined as the specific, **non-binary** case of the [Bose–Chaudhuri–Hocquenghem (BCH)](https://en.wikipedia.org/wiki/BCH_code) codes. 

Syndrome decoding is used. Frequently are measured in symbols (bytes, blocks). Code rate can be calculated as:

<img src="https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/RScoderate.png" alt="RScoderate" width="500"/>

Can correct **t** symbols. The BER performance has the step-like character:

![RSBER](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/rs.png)

>Fig. 1.3.2. Theoretical BER performance of the Reed-Solomon code (N=255, K=233, QPSK, AWGN).

> **See also**: 
>
> [MATLAB source code](https://en.wikipedia.org/wiki/Reed%E2%80%93Solomon_error_correction#History)
>
> [MatLab RS encoder](https://www.mathworks.com/help/comm/ref/comm.rsencoder-system-object.html)
>
>[MatLab RS decoder](https://www.mathworks.com/help/comm/ref/comm.rsdecoder-system-object.html)

### Outlooks of the RSCC

Very old technique [2]. The part of the DVB-S standard, however was replaced in [DVB-S2](https://en.wikipedia.org/wiki/DVB-S2):

![DVB-S2](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/DVB_S2fec.png)

Since 2000-s modern error correction schemes, such as Turbo codes, are used more widely in space communications \[3\].

<img src="https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/turbovsrsBER.png" alt="TurboRSCC" width="700"/>

> Fig. 1.3.3. Bit error rate curves for several codes with rates near 1/6: k=1784 and k=8920 turbo codes and the (n=255, k=223) Reed–Solomon code concatenated with a constraint length N=15, rate 1/6 convolutional code. \[3\]

RSCC codes have the comparable complexity with Turbo codes \[4\], however worse BER performance (fig. 1.3.3). 

## Turbo convolutional codes

[Turbo convolutional codes](http://www.scholarpedia.org/article/Turbo_code) are the part of the mobile communication (UMTS, CDMA2000, LTE), broadcast (DVB-RCS, DVB-RCT, DVB-SSP), deep space (CCSDS) and other standards.

The structure of the encoder can be represented as:

<img src="https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/TurboEncoder.png" alt="TurboEncoder" width="700"/>

> Fig. 1.3.4. Block scheme of Turbo convolutional encoder.

Information in the input of the encoder is processed by blocks (chunks), the length of the block directly influences BER performance.

> Very interesting research can be found also in [\[5\]](https://publik.tuwien.ac.at/files/publik_262129.pdf) where capabilities of Turbo convolutional, LDPC and Polar codes are considered.

Turbo covolutional decoders use **MAP** (maximum a posteriori probability) algorithms unlike convolutional codes. For example, classical  **BCJR** (Bahl, Cocke, Jelinek and Raviv)\[6\]. More simple implementations such as **Log-MAP**, **MAX-Log-MAP** or **SOVA** of Turbo convolutional decoder are also exist \[7\]. 

> **See also**:
>
> [Turbo encoder MatLab object](https://www.mathworks.com/help/comm/ref/comm.turboencoder-system-object.html)
> 
> [Turbo decoder MatLab object](https://www.mathworks.com/help/comm/ref/comm.turbodecoder-system-object.html)

One of the most popular alternative of the Turbo convolutional codes is the class of the Low Density Parity Check (LDPC) codes.


## References

\[1\] J. Hagenauer, E. Offer, and L. Papke, Reed Solomon Codes and Their Applications. New York IEEE Press, 1994

\[2\] Ebert, P. M., and S. Y. Tong. "Convolutional Reed‐Solomon Codes." Bell Labs Technical Journal 48.3 (1969): 729-742.

\[3\] Andrews, Kenneth S., et al. "The development of turbo and LDPC codes for deep-space applications." Proceedings of the IEEE 95.11 (2007): 2142-2156.

\[4\] Balaji, Pavithra, et al. "Evaluation of decoding trade-offs of concatenated RS convolutional codes and turbo codes via trellis." Signal Processing and Integrated Networks (SPIN), 2015 2nd International Conference on. IEEE, 2015.

\[5\] Tahir, Bashar, Stefan Schwarz, and Markus Rupp. "BER comparison between Convolutional, Turbo, LDPC, and Polar codes." Telecommunications (ICT), 2017 24th International Conference on. IEEE, 2017.

\[6\] Bahl, Lalit, et al. "Optimal decoding of linear codes for minimizing symbol error rate (corresp.)." IEEE Transactions on information theory 20.2 (1974): 284-287.

\[7\] Chatzigeorgiou, Ioannis Ap, and Clare Hall. Performance analysis and design of punctured turbo codes. Diss. Ph. D. dissertation, University of Cambridge, Cambridge, England, 2006.


## Suggested literature

### Turbo convolutional codes:
\[1\] Battail, Gérard. "A conceptual framework for understanding turbo codes." IEEE Journal on Selected Areas in Communications 16.2 (1998): 245-254.

\[2\] Brejza, Matthew F., et al. "20 years of turbo coding and energy-aware design guidelines for energy-constrained wireless applications." IEEE Communications Surveys & Tutorials 18.1 (2016): 8-28.

\[3\] [3GPP LTE Turbo Reference Design](https://www.altera.com/content/dam/altera-www/global/en_US/pdfs/literature/an/an505.pdf)

\[4\] Garzón-Bohórquez, Ronald, Charbel Abdel Nour, and Catherine Douillard. "Improving Turbo codes for 5G with parity puncture-constrained interleavers." Turbo Codes and Iterative Information Processing (ISTC), 2016 9th International Symposium on. IEEE, 2016.

### Quantum applications:

Another interesting application of the channel codes are the quantum communications. Note that, rules of quantum world influence coding theory. For example, recursive quantum CC are catastrophic and  quantum Turbo CC outperforms even quantum LDPC.

\[1\] Houshmand, Monireh, and Mark M. Wilde. "Recursive quantum convolutional encoders are catastrophic: A simple proof." IEEE Transactions on Information Theory 59.10 (2013): 6724-6731.

\[2\] Lai, Ching-Yi, Min-Hsiu Hsieh, and Hsiao-feng Lu. "On the MacWilliams identity for classical and quantum convolutional codes." IEEE Transactions on Communications 64.8 (2016): 3148-3159.

\[3\] Poulin, David, Jean-Pierre Tillich, and Harold Ollivier. "Quantum serial turbo codes." IEEE Transactions on Information Theory 55.6 (2009): 2776-2798.

\[4\] Wilde, Mark M., Min-Hsiu Hsieh, and Zunaira Babar. "Entanglement-assisted quantum turbo codes." IEEE Transactions on Information Theory 60.2 (2014): 1203-1222.

\[5\] Djordjevic, Ivan. Quantum information processing and quantum error correction: an engineering approach. Academic press, 2012.

\[6\] Lidar, Daniel A., and Todd A. Brun, eds. Quantum error correction. Cambridge University Press, 2013.

### Afterwords

The following Wikipedia articles were contributed based on this page:
* [Reed–Solomon error correction](https://en.wikipedia.org/wiki/Reed–Solomon_error_correction)
