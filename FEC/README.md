### Summary

1. Convolutional codes

    1.1. [Introduction](https://github.com/kirlf/CSP/blob/master/FEC/Convolutional%20codes%20intro.md)

    1.2. [Modeling in MatLab](https://github.com/kirlf/CSP/blob/master/FEC/Convolutional%20codes%20modeling.md)
    
    1.3. [Extensions of the convolutional codes idea](https://github.com/kirlf/CSP/blob/master/FEC/Conv%20codes%20idea%20extensions.md)
    
    1.4. [Python tutorial: Convolutional encoder](https://github.com/kirlf/CSP/blob/master/FEC/Convolutional_encoder.ipynb)

### Preface

#### Main idea
The main idea of the channel codes can be formulated as following thesises:
- We need to increase **noise immunity** of our signal;
- We add **redundant bits** for error detection and error correction;
- We use some algorithms (coding schemes) for this;
- Coding schemes can be simple or complicated and are used for different purposes, e.g. error detection, error correction in small SNR, error correction in large SNR  etc.

![mainidea](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/FECmainidea.png)

Actually, encoding algorithms **separate** code words adding redundancy (kind of **diversity** in time domain). 
![examp1](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/FECexamp1.png)

As how much farther certain algorithm separates code words is so much stronger noise immunity.

#### Minimum distance
Minimum distance between all of the code words is named **Hamming distance** in case of binary codes .
<img src="https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/FECexamp2.png" alt="examp2" width="400"/>

As larger certain algorithm provides **dmin**  is so much stronger noise immunity [1, p.23].

#### Classification
Firstly, the channel codes can be classified by error detection and error correction capabilities:
![class1](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/harq.png)

Secondly, they can be classified as block and continious codes:
![class2](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/BlockCont.png)

To decode block codes the syndrome decoding is frequently used:

![syndr](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/syndrome.png)

#### Net bit rate
Redundancy of the channel coding schemes influences (decreases) bit rate. Actually, it is the cost for the noiseless increasing.
**Net bit** rate concept is usually used:

<img src="https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/nebitrate.png" alt="net" width="500"/>

To change the code rate (k/n) of the block code dimensions of the Generator matrix can be changed:
![blockcoderate](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/coderateblock.png)

To change the coderate of the continuous code, e.g. convolutional code, **puncturing** procedure is frequently used:

![punct](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/punct.png)

Seems little bit tricky, however it really works in real systems. On the receiver side nulls are inserted according to puncturing pattern usually ("depuncturing" or "insert zeros").

> Implementation of the "puncturing" and "isert zeros" functions in python 3.5 can be obtained by the [following link](https://github.com/kirlf/CSP/blob/master/FEC/functions/Puncturing-Depuncturing.ipynb)

#### Interleaving
To increase separation in time domain and avoid bursty destortions **interleaving** procedure is also frequently used:

<img src="https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/interleaving.png" alt="interleaving" width="700"/>

The most popular applications of the interleaving are concatenated codes (RSCC, Turbo codes etc.).

### Reference

[1] Moon, Todd K. "Error correction coding." Mathematical Methods and Algorithms. Jhon Wiley and Son (2005).
