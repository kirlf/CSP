# Channel codes

## Main idea
The main idea of the channel codes can be formulated as following thesises:
- We need to increase **noise immunity** of our signal;
- We add **redundant bits** for error detection and error correction;
- We use some algorithms (coding schemes) for this;
- Coding schemes can be simple or complicated and are used for different purposes, e.g. error detection, error correction in small SNR, error correction in large SNR  etc.

![mainidea](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/FECmainidea1.png)

Actually, encoding algorithms **separate** code words adding redundancy (kind of **diversity** in time domain). 
![examp1](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/FECexamp1.png)

As how much farther certain algorithm separates code words is so much stronger noise immunity.

## Minimum distance
Minimum distance between all of the code words is named **Hamming distance** in case of binary codes .
<img src="https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/FECexamp2.png" alt="examp2" width="400"/>

As larger certain algorithm provides **dmin**  is so much stronger noise immunity [1, p.23].

## Classification
Firstly, the channel codes can be classified by error detection and [error correction](https://en.wikipedia.org/wiki/Error_correction_code) capabilities:
![class1](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/harq.png)

Secondly, they can be classified as block and continious codes:
![class2](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/BlockCont.png)

To decode block codes the syndrome decoding is frequently used:

![syndr](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/syndrome.png)

## Net bit rate
Redundancy of the channel coding schemes influences (decreases) bit rate. Actually, it is the cost for the noiseless increasing.
**Net bit** rate concept is usually used:

<img src="https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/nebitrate.png" alt="net" width="500"/>

To change the code rate (k/n) of the block code dimensions of the Generator matrix can be changed:
![blockcoderate](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/coderateblock.png)

To change the coderate of the continuous code, e.g. [convolutional code](https://github.com/kirlf/CSP/blob/master/FEC/Convolutional%20codes%20intro.md), **puncturing** procedure is frequently used:

![punct](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/punct.png)

Seems little bit tricky, however it really works in real systems. On the receiver side nulls are inserted according to puncturing pattern usually ("depuncturing" or "insert zeros").

> Implementation of the "puncturing" and "insert zeros" functions in python 3.5 can be obtained by the [following link](https://github.com/kirlf/CSP/blob/master/FEC/functions/Puncturing-Depuncturing.ipynb)

## History of FEC in mobile communications

### 2G: GSM, GPRS, EDGE

Both error correction and error detection techniques are used in [**GSM**](http://www.scholarpedia.org/article/Global_system_for_mobile_communications_(GSM)) (fig. 1).

![](https://habrastorage.org/webt/fi/vt/rg/fivtrgot1jque5tipk_52ttp8rm.png)

*Fig.1. Stages of channel coding in GSM [2]*

Let us count main blocks:

- **Block encoder** and **Parity check** - error detection part
- **Convol. encoder** and **Convol. decoder** - error correction part
- **Interleaving** and **Deinterleaving** - code words separation increasing

<details> 
  <summary>*The illustration of the interleaving procedure idea.</summary>
   To increase separation in time domain and avoid bursty destortions interleaving procedure is also frequently used:
   <img src="https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/interleaving1.png" width="700"/>
</details>

The same picture in **GPRS** due to the same RAN (Radio Access Network).

![](https://raw.githubusercontent.com/kirlf/CSP/master/Different/assets/gsm_gprs.PNG)

*Fig. 2. The illustration of the GSM and GPRS network architectures. Source: https://www.tu-ilmenau.de/fileadmin/public/iks/files/lehre/UMTS/03_CCS-2G-ws18_19.pdf*

The code rate 1/3 is used in EDGE [3]. 

### Reference

[1] Moon, Todd K. "Error correction coding." Mathematical Methods and Algorithms. Jhon Wiley and Son (2005).

[2] Eberspächer J. et al. GSM-architecture, protocols and services. – John Wiley & Sons, 2008. - p. 97

[3] 3rd Generation Partnership Project (September 2012). ["3GGP TS45.001: Technical Specification Group GSM/EDGE Radio Access Network; Physical layer on the radio path; General description"](https://portal.3gpp.org/desktopmodules/Specifications/SpecificationDetails.aspx?specificationId=2705). Retrieved 2013-07-20.
