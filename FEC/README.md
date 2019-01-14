### Summary

1. Convolutional codes

1.1 [Introduction](https://github.com/kirlf/CSP/blob/master/FEC/Convolutional%20codes%20intro.md)

1.2 [Modeling in MatLab](https://github.com/kirlf/CSP/blob/master/FEC/Convolutional%20codes%20modeling.md)

### Preface

The main idea of the channel codes can be formulated as following thesises:
- We need to increase **noise immunity** of our signal;
- We add **redundant bits** for error detection and error correction;
- We use some algorithms (coding schemes) for this;
- Coding schemes can be simple or complicated and are used for different purposes, e.g. error detection, error correction in small SNR, error correction in large SNR  etc.

![mainidea](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/FECmainidea.png)

Actually, encoding algorithms **separate** code words adding redundancy (kind of **diversity** in time domain). 
![examp1](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/FECexamp1.png)

As how much farther certain algorithm separates code words is so much stronger noise immunity.

For the binary codes minimum distance between the all code words named **Hamming distance**.

![examp2](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/FECexamp2.png)

As larger certain algorithm provides **dmin**  is so much stronger noise immunity [1, p.23].

Firstly, the channel codes can be classified by error detection and error correction capabolities:
![class1](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/harq.png)

Secondly, they can be classified as block and continious codes:
![class2](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/BlockCont.png)

Redundancy of the channel coding schemes influences (decreases) bit rate. Actually, it is the cost for the noiseless increasing.
**Net bit** rate concept is usually used:

![net](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/nebitrate.png)

### Reference

[1] Moon, Todd K. "Error correction coding." Mathematical Methods and Algorithms. Jhon Wiley and Son (2005).
