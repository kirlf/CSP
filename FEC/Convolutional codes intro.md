
# Convolutional codes basics 

### Summary

1. Convolutional codes

    1.1. [Introduction](https://github.com/kirlf/CSP/blob/master/FEC/Convolutional%20codes%20intro.md)

    1.2. [Modeling in MatLab](https://github.com/kirlf/CSP/blob/master/FEC/Convolutional%20codes%20modeling.md)
    
    1.3. [Extensions of the convolutional codes idea](https://github.com/kirlf/CSP/blob/master/FEC/Conv%20codes%20idea%20extensions.md)
    
    1.4. [Python tutorial: Convolutional encoder](https://github.com/kirlf/CSP/blob/master/FEC/Convolutional_encoder.ipynb)

# Introduction

[Convolutional codes](https://en.wikipedia.org/wiki/Convolutional_code) are kind of continuous error-correcting codes. They can be easily described via the polynomial structure, that can be also mapped into the shift-registers representation, e.g.:

![shiftregs](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/shift_regs.png)

In practice, polynomial structures are selected from the reference books. Searching of the optimal structure of the convolutional codes is the scientific research item. This relates to the chance to construct [catastrophic](https://www.mathworks.com/help/comm/ref/iscatastrophic.html) convolutional code.  

Moreover, the following classification can be applied:
<img src="https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/syst-nonsyst.png" alt="SysNonSys" width="600"/>

Non-systematic convolutional codes are more popular due to better noise immunity. It relates to the [**free distance**](  https://www.mathworks.com/help/comm/ug/bit-error-rate-ber.html#brck0zf) of the convolutional code \[1, p. 508\].

The name of convolutional codes directly relates to the convolution: encoding can be done via this math routine.

> See more in our Puthon tutorial:
>
> [Jupyter notebook](https://github.com/kirlf/CSP/blob/master/FEC/Convolutional_encoder.ipynb)
>
> [RISE slides](https://www.dropbox.com/s/gt3bsjy7yw5fmse/Convolutional_codes.slides.html?dl=0)

[Viterbi algorithm](http://www.scholarpedia.org/article/Viterbi_algorithm) (one of the **MLE** – Maximum Likelihood Estimation -  algorithms) is usually used for decoding. Viterbi algorithm use the [Trellis structures](https://www.gaussianwaves.com/tag/trellis-diagram/) for the decoding. 

Convolutional **decoders** can make either **hard** or **soft** decision. What does it mean? That means differrent type of encoders' inputs: zeros and ones (hard descision) or [log-likelihood ratios](https://www.mathworks.com/help/comm/ug/digital-modulation.html#brc6yjx) (soft descision). The soft descion is more preferable due to BER (bit-error ratio) performance:

``` octave
clear all 
close all 
clc 

EbNo = 0:7; 
spect = distspec(poly2trellis(7,[171 133]),7) 
ber_h = bercoding(EbNo,'conv','hard',1/2,spect); 
ber_s = bercoding(EbNo,'conv','soft',1/2,spect); 
ber_u = berawgn(EbNo,'psk',4,'nondiff'); 

figure(1) 
semilogy(EbNo, ber_h, EbNo, ber_s,... 
EbNo, ber_u, 'LineWidth', 1.5) 
hold on 
legend('Hard','Soft','Uncoded','location','best') 
grid on 
xlabel('Eb/No (dB)') 
ylabel('Bit Error Rate') 
```
![hardsoft](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/softhard.png)

Fig. 1.1.1. Comparison of QPSK with and without convolutional codes (7, [175 133]) (AWGN).

If you choose the larger constrain length (use more delaying memory blocks), your encoder (and decoder) becomes more sophisticated (exponentially). However, coding algorithm becomes more strong (more available combinations, code words), hence, the length of the constrain length influences you BER performance. 

``` octave
clear all 
close all 
clc 

EbNo = 0:7; 
lens = 5:9; 
gens = [[35 23]; [51 73]; [171 133]; [371 247]; [753 561]]; 

for g = 1:length(gens) 
    spect = distspec(poly2trellis(lens(g), gens(g,:)),lens(g)) 
    ber_soft(:, g) = bercoding(EbNo,'conv','soft',1/2,spect); 
    ber_hard(:, g) = bercoding(EbNo,'conv','hard',1/2,spect); 
end 
ber_u = berawgn(EbNo,'psk',4,'nondiff').'; 

ber1 = [ber_soft ber_u]; 
ber2 = [ber_hard ber_u]; 

figure(1) 
semilogy(EbNo, ber1,'LineWidth', 1.5) 
hold on 
legend('Soft (5,[35 23])',... 
'Soft (6,[51 73])','Soft (7,[171 133])',... 
'Soft (8,[371 247])','Soft (9,[753 561])',... 
'Uncoded','location','best') 
grid on 
xlabel('Eb/No (dB)') 
ylabel('Bit Error Rate') 

figure(2) 
semilogy(EbNo, ber2,'LineWidth', 1.5) 
hold on 
legend('Hard (5,[35 23])',... 
'Hard (6,[51 73])','Hard (7,[171 133])',... 
'Hard (8,[371 247])','Hard (9,[753 561])',... 
'Uncoded','location','best') 
grid on 
xlabel('Eb/No (dB)') 
ylabel('Bit Error Rate') 
```
![lens](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/lenss.png)

Fig. 1.1.2. Comparison of the different structures of the convolutional codes (QPSK, AWGN).

The MATLAB modeling of the transmission of the encoded message is presented below. 

### Reference

[1] Moon, Todd K. "Error correction coding." Mathematical Methods and Algorithms. Jhon Wiley and Son (2005).
