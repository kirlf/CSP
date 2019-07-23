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



### Reference

[1] Moon, Todd K. "Error correction coding." Mathematical Methods and Algorithms. Jhon Wiley and Son (2005).

[2] Eberspächer J. et al. GSM-architecture, protocols and services. – John Wiley & Sons, 2008. - p. 97

[3] 3rd Generation Partnership Project (September 2012). ["3GGP TS45.001: Technical Specification Group GSM/EDGE Radio Access Network; Physical layer on the radio path; General description"](https://portal.3gpp.org/desktopmodules/Specifications/SpecificationDetails.aspx?specificationId=2705). Retrieved 2013-07-20.
