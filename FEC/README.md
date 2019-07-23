# Channel codes

## Main idea
The main idea of the channel codes can be formulated as following thesises:
- We need to increase **noise immunity** of our signal;
- We add **redundant bits** for error detection and error correction;
- We use some algorithms (coding schemes) for this;
- Coding schemes can be simple or complicated and are used for different purposes, e.g. error detection, error correction in small SNR, error correction in large SNR  etc.

![mainidea](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/FECmainidea1.png)

Actually, encoding algorithms **separate** code words adding redundancy (kind of **diversity** in time domain). 
![examp1](https://camo.githubusercontent.com/ef8ed6eaef070a7747b65dfcc16cbbffe319a000/68747470733a2f2f686162726173746f726167652e6f72672f776562742f6e372f6f342f62732f6e376f34627366375f68746c76313067736174632d796f6a6272712e706e67)

As how much farther certain algorithm separates code words is so much stronger noise immunity.

## Minimum distance
Minimum distance between all of the code words is named **Hamming distance** in case of binary codes .
<img src="https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/FECexamp2.png" alt="examp2" width="400"/>

As larger certain algorithm provides **dmin**  is so much stronger noise immunity [1, p.23].

## Classification

Some classification is needed to talk about those or other implementations of the encoding and decoding algorithms.

First, the channel codes:
- can only [*detect*](https://en.wikipedia.org/wiki/Cyclic_redundancy_check) the presence of errors
- and they can also [*correct* errors](https://en.wikipedia.org/wiki/Error_correction_code).

Secondly, codes can be classified as **block** and **continuous**:
![class2](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/BlockCont.png)

<details>
  <summary>To decode block codes the syndrome decoding is frequently used. </summary>

![syndr](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/syndrome.png)

</details>

## Net bit rate
Redundancy of the channel coding schemes influences (decreases) bit rate. Actually, it is the cost for the noiseless increasing.
**Net bit** rate concept is usually used:

<img src="https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/nebitrate.png" alt="net" width="500"/>

<details> 
  <summary>How to change code rate of a block code?</summary>
To change the code rate (k/n) of the block code dimensions of the Generator matrix can be changed:
<img src="https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/coderateblock.png" />
</details>

<details> 
  <summary>How to change code rate of a continuous code?</summary>
To change the coderate of the continuous code, e.g. convolutional code, puncturing procedure is frequently used:

![punct](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/punct.png)

Seems little bit tricky, however it really works in real systems. On the receiver side nulls are inserted according to puncturing pattern usually ("depuncturing" or "insert zeros").

> Implementation of the "puncturing" and "insert zeros" functions in python 3.5 can be obtained by the [following link](https://github.com/kirlf/CSP/blob/master/FEC/functions/Puncturing-Depuncturing.ipynb)
</details>

## A short history of channel codes in mobile communications

### 2G: GSM, GPRS, EDGE

Both error correction and error detection techniques are used in [**GSM**](http://www.scholarpedia.org/article/Global_system_for_mobile_communications_(GSM)) (fig. 1).

![](https://habrastorage.org/webt/fi/vt/rg/fivtrgot1jque5tipk_52ttp8rm.png)

*Fig.1. Stages of channel coding in GSM [2]*

Let us count main blocks:

- **Block encoder** and **Parity check** - error detection part
- **Convol. encoder** and **Convol. decoder** - error correction part
- [**Interleaving** and **Deinterleaving**](https://upload.wikimedia.org/wikipedia/commons/6/62/Interleaving1.png) - code words separation increasing in time domain and to avoid bursty destortions

<details>
  <summary> The same picture in GPRS due to the same RAN (Radio Access Network). </summary>
  

![](https://raw.githubusercontent.com/kirlf/CSP/master/Different/assets/gsm_gprs.PNG)

*The illustration of the GSM and GPRS network architectures. Source: https://www.tu-ilmenau.de/fileadmin/public/iks/files/lehre/UMTS/03_CCS-2G-ws18_19.pdf*

</details>

The convolutional codes are still used in EDGE, but with the code rate 1/3 \[3\].

![](https://raw.githubusercontent.com/kirlf/CSP/master/Different/assets/EDGE_conv.PNG)

*Fig. 2. EGPRS coding and puncturing example (MCS-9: uncoded 8-PSK, two RLC blocks per 20 ms) \[4, p.50\]*

Actually, this air interface is used even in early releases of 3G networks.

### 3G: WCDMA-UMTS

The EDGE radio is used until Release 7.

![](https://raw.githubusercontent.com/kirlf/CSP/master/Different/assets/rel5_fec.PNG)

*Fig. 3. Channel coding and interleaving on the control channels. aGERAN Rel’5 terminology is used. This corresponds to a full-rate TCH \[4, p.430]*

Since Release 7 [EGPRS2](https://www.mpirical.com/glossary/egprs2-enhanced-general-packet-radio-service-phase-2) is used. This includes [**Turbo convolutional codes**](http://www.scholarpedia.org/article/Turbo_code).

The structure of the encoder can be represented as:

<img src="https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/TurboEncoder.png" alt="TurboEncoder" width="700"/>

*Fig. 4. Block scheme of Turbo convolutional encoder.*

Information in the input of the encoder is processed by blocks (chunks), the length of the block directly influences BER performance.

Turbo covolutional decoders use **MAP** (maximum a posteriori probability) algorithms unlike convolutional codes. For example, classical  **BCJR** (Bahl, Cocke, Jelinek and Raviv)\[5\]. More simple implementations such as **Log-MAP**, **MAX-Log-MAP** or **SOVA** of Turbo convolutional decoder are also exist \[6\]. 


### 4G: LTE, LTE-A

Turbo convolutional codes are still used in air interface of the 4G networks.

![Turbo](https://www.mathworks.com/help/examples/comm_product/win64/commpccc_04.png)

*Fig. 5. Code-Block Error Rate performance of the LTE Turbo codes. Source: ["Parallel Concatenated Convolutional Coding: Turbo Codes"(MathWorks)](https://www.mathworks.com/help/comm/examples/parallel-concatenated-convolutional-coding-turbo-codes.html)*

> Very interesting research can be found also in [\[7\]](https://publik.tuwien.ac.at/files/publik_262129.pdf) where capabilities of Turbo convolutional, LDPC and Polar codes are considered.

### Reference

[1] Moon, Todd K. "Error correction coding." Mathematical Methods and Algorithms. Jhon Wiley and Son (2005).

[2] Eberspächer J. et al. GSM-architecture, protocols and services. – John Wiley & Sons, 2008. - p. 97

[3] 3rd Generation Partnership Project (September 2012). ["3GGP TS45.001: Technical Specification Group GSM/EDGE Radio Access Network; Physical layer on the radio path; General description"](https://portal.3gpp.org/desktopmodules/Specifications/SpecificationDetails.aspx?specificationId=2705). Retrieved 2013-07-20.

[4] Halonen, Timo, Javier Romero, and Juan Melero, eds. GSM, GPRS and EDGE performance: evolution towards 3G/UMTS. John Wiley & Sons, 2004.

\[5\] Bahl, Lalit, et al. "Optimal decoding of linear codes for minimizing symbol error rate (corresp.)." IEEE Transactions on information theory 20.2 (1974): 284-287.

\[6\] Chatzigeorgiou, Ioannis Ap, and Clare Hall. Performance analysis and design of punctured turbo codes. Diss. Ph. D. dissertation, University of Cambridge, Cambridge, England, 2006.

\[7\] Tahir, Bashar, Stefan Schwarz, and Markus Rupp. "BER comparison between Convolutional, Turbo, LDPC, and Polar codes." Telecommunications (ICT), 2017 24th International Conference on. IEEE, 2017.
