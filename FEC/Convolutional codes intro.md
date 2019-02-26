
# Convolutional codes basics 

### Summary

   1.1. Introduction

   1.2. [Modeling in MatLab](https://github.com/kirlf/CSP/blob/master/FEC/Convolutional%20codes%20modeling.md)
    
   1.3. [Extensions of the convolutional codes idea](https://github.com/kirlf/CSP/blob/master/FEC/Conv%20codes%20idea%20extensions.md)

# Introduction

## Encoding
[Convolutional codes](https://en.wikipedia.org/wiki/Convolutional_code) are kind of continuous [error-correcting codes](https://github.com/kirlf/CSP/tree/master/FEC). They can be easily described via the polynomial structure, that can be also mapped into the shift-registers representation, e.g.:

![shiftregs](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/shift_regs.png)
>Fig. 1.1.1. Example of shift-register structure (m1 and m2 are the constrain lengths (memory length)).

> **NOTE THAT**:
>
> All of the math operations should be done by modulo 2.


In practice, polynomial structures are selected from the reference books. Searching of the optimal structure of the convolutional codes is the scientific research item. This relates to the chance to construct [catastrophic](https://www.mathworks.com/help/comm/ref/iscatastrophic.html) convolutional code.  

Moreover, the following classification can be applied:
<img src="https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/syst-nonsyst.png" alt="SysNonSys" width="600"/>

Non-systematic convolutional codes are more popular due to better noise immunity. It relates to the [**free distance**](  https://www.mathworks.com/help/comm/ug/bit-error-rate-ber.html#brck0zf) of the convolutional code \[1, p. 508\].

Additionally, convolutional codes can be devided into two groups: recursive and non-recursive:

![recnonrec](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/recnonrec.png)

> Fig. 1.1.2. Two state recurcive (a) and nonrecursive (b) encoder \[2\].

Not so much different in BER performance:

![recBER](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/recnonrecber.png)

> Fig. 1.1.3. BER performance of recursive and non-recursive codes. 

However, this type of CC is implemented in Turbo convolutional codes due to interleaving properties.

The name of convolutional codes directly relates to the discrete [convolution](https://en.wikipedia.org/wiki/Convolution): encoding can be done via this math routine.

<img src="https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/convformula.png" alt="formula" width="400"/>

Where *y* is the code word, *x* is the initial message and *h* is the generator branch, *L* is the constrain length, *j* is the number of branch and *i* is the number of message bit that should be encoded. [For example](http://web.mit.edu/6.02/www/f2010/handouts/lectures/L8.pdf), for the (7, \[177, 133\]) structure the branches are:

<img src="https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/gensexamp.png" alt="branches" width="400"/>

> See the example of encoding based on the shift-registers in our Puthon tutorial:
>
> [Jupyter notebook](https://github.com/kirlf/CSP/blob/master/FEC/Convolutional_encoder.ipynb)
>
> [RISE slides](https://www.dropbox.com/s/no7rbkjtc0b2ky4/Convolutional_codes.slides.html?dl=0)

Actually, the encoding procedure can be represented as the work with the [Trellis structures](https://www.gaussianwaves.com/tag/trellis-diagram/) that simplifies all of the routines to the transactions beatween the some predefined states with the predefined outputs.

> Good illustrations by [M. Sc. Dipl.-Ing. (FH) Marko Hennhöfer](http://www5.tu-ilmenau.de/nt/de/private_home/hennhoefer/index.html):
>
> [Trellis diagram and shift-registers](https://github.com/kirlf/CSP/blob/master/FEC/assets/trellis1.jpg)
>
> [State diagram (compact form of the Trellis)](https://github.com/kirlf/CSP/blob/master/FEC/assets/trellis2.jpg)
>
> [Tail bits (termination of the Trellis)](https://github.com/kirlf/CSP/blob/master/FEC/assets/trellis3.jpg)

## Decoding
[Viterbi algorithm](http://www.scholarpedia.org/article/Viterbi_algorithm) (one of the **MLE** – Maximum Likelihood Estimation -  algorithms) is usually used for decoding. Viterbi algorithm also use the [Trellis structures](https://www.gaussianwaves.com/tag/trellis-diagram/) for the decoding. 

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

>Fig. 1.1.4. Comparison of QPSK with and without convolutional codes (7, [175 133]) (AWGN).

Moreover, if you choose the larger constrain length (use more delaying memory blocks), your encoder (and decoder) becomes more sophisticated (exponentially). However, coding algorithm becomes more strong (more available combinations, code words), hence, the length of the constrain length influences you BER performance. 

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

>Fig. 1.1.5. Comparison of the different structures of the convolutional codes (QPSK, AWGN).

The MATLAB modeling of the transmission of the encoded message is presented below. 

### References

\[1\] Moon, Todd K. "Error correction coding." Mathematical Methods and Algorithms. Jhon Wiley and Son (2005).

\[2\] Benedetto, Sergio, and Guido Montorsi. "Role of recursive convolutional codes in turbo codes." Electronics Letters 31.11 (1995): 858-859.

### Suggested literature

\[1\] Francis, Michael. "Viterbi Decoder Block Decoding-Trellis Termination and Tail Biting." Xilinx XAPP551 v2. 0, DD (2005): 1-21.

\[2\] Chen, Qingchun, Wai Ho Mow, and Pingzhi Fan. "Some new results on recursive convolutional codes and their applications." Information Theory Workshop, 2006. ITW'06 Chengdu. IEEE. IEEE, 2006.

\[3\] Fiebig, U-C., and Patrick Robertson. "Soft-decision and erasure decoding in fast frequency-hopping systems with convolutional, turbo, and Reed-Solomon codes." IEEE Transactions on Communications 47.11 (1999): 1646-1654.

\[4\] Bhaskar, Vidhyacharan, and Laurie L. Joiner. "Performance of punctured convolutional codes in asynchronous CDMA communications under perfect phase-tracking conditions." Computers & Electrical Engineering 30.8 (2004): 573-592.

### Suggested literature (in Russian):

\[1\] Хлынов, А. А. "ИССЛЕДОВАНИЕ ПРИНЦИПОВ РЕАЛИЗАЦИИ LDPC КОДЕКА НА ПЛИС." Фундаментальные проблемы радиоэлектронного приборостроения 12.6 (2012): 150-156.

\[2\] Банкет, В. Л. "Сигнально-кодовые конструкции в телекоммуникационных системах." О.: Феникс (2009).

\[3\] Никитин, Г. И. "ББК 32.811. 4 Н62.“

\[4\] Колесник В. Д., Полтырев Г. Ш. Курс теории информации. – " Наука," Глав. ред. физико-математической лит-ры, 1982.

\[5\] Нгок Д. К. Исследование методов поиска оптимальных сверточных и перфорированных сверточных кодов : дис. – Диссертация на соискание ученой степени кандидата технических наук. СПб.: ЛЭТИ, 2014.

### Afterwords

The following Wikipedia articles were contributed based on this page:
* [Convolutional code](https://en.wikipedia.org/wiki/Convolutional_code)

