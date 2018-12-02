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

### Summary

1. [Convolutional codes](https://github.com/kirlf/CSP/blob/master/FEC/Soft%20decision%20Convolutional%20codes.md)

### Reference

[1] Moon, Todd K. "Error correction coding." Mathematical Methods and Algorithms. Jhon Wiley and Son (2005).





 
