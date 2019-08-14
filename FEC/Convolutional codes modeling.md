# Convolutional codes tutorial
### M. Sc. Vladimir Fadeev

## Motivation

Before we start, let us shortly describe why this topic should be learned.

Convolutional codes are the part of most of the mobile communication systems. For example, they are implemented in [**GSM**](http://www.scholarpedia.org/article/Global_system_for_mobile_communications_(GSM)), GPRS, EDGE and 3G networks (until Release 7) \[1\], \[2, p. 430\].

<img src="https://habrastorage.org/webt/fi/vt/rg/fivtrgot1jque5tipk_52ttp8rm.png" width="650" />

*Fig.1. Stages of channel coding in GSM \[3, p. 97\]. **Block encoder** and **Parity check** - error detection part. **Convol. encoder** and **Convol. decoder** - error correction part. [**Interleaving** and **Deinterleaving**](https://upload.wikimedia.org/wikipedia/commons/6/62/Interleaving1.png) - code words separation increasing in time domain and to avoid bursty destortions.* 

They are also included in [deep-space communication standartd](https://ipnpr.jpl.nasa.gov/progress_report/42-63/63H.PDF) in concatenation with Reed-Solomon codes. 

> See also: [Survey of modulation and coding schemes for application in CubeSat systems (afterwords)](https://github.com/kirlf/cubesats/blob/master/fec.md)

Moreover, the convolutional codes are the part of the [Turbo convolutional codes](http://www.scholarpedia.org/article/Turbo_codes) that are used in 3G, [4G](https://www.mathworks.com/help/comm/examples/parallel-concatenated-convolutional-coding-turbo-codes.html?searchHighlight=turbo%20codes&s_tid=doc_srchtitle) and modern space communication systems.

![](http://www.scholarpedia.org/w/images/thumb/2/25/Turbocode_fig4_v2.jpg/450px-Turbocode_fig4_v2.jpg)

*Fig.2. A turbo code with component codes 13, 15. Source: http://www.scholarpedia.org/article/Turbo_codes . Turbo codes get their name
because the decoder uses feedback, like a turbo engine.*

In other words, basics of convolutional codes are the **key** for understanding of the main ideas of the forward error correction in mobile communications. 

> You can also read more about convolutional codes and Turbo caodes (and other error detection and error correction schemes) in the corresponding teaching [slides by Atlanta RF company](https://www.atlantarf.com/Error_Control.php). 


## Encoding
Convolutional codes are kind of **continuous [error-correcting codes](https://en.wikipedia.org/wiki/Error_correction_code)**. 

<img src="https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/BlockCont.png" width="800" />

Moreover, the following classification can be applied:
<img src="https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/syst-nonsyst.png" alt="SysNonSys" width="600"/>

Non-systematic convolutional codes are more popular due to better noise immunity. It relates to the [**free distance**](  https://www.mathworks.com/help/comm/ug/bit-error-rate-ber.html#brck0zf) of the convolutional code \[4, p. 508\].

Additionally, convolutional codes can be devided into two groups: recursive and non-recursive:

![recnonrec](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/recnonrec.png)

> Fig. 1.1.2. Two state recurcive (a) and nonrecursive (b) encoder \[5\].

Not so much different in BER performance:

![recBER](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/recnonrecber.png)

> Fig. 1.1.3. BER performance of recursive and non-recursive codes. 

However, this type of CC is implemented in Turbo convolutional codes due to interleaving properties.

The name of convolutional codes directly relates to the discrete [convolution](https://en.wikipedia.org/wiki/Convolution): encoding can be done via this math routine.

<img src="https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/convformula.png" alt="formula" width="400"/>

Where *y* is the code word, *x* is the initial message and *h* is the generator branch, *L* is the constrain length, *j* is the number of branch and *i* is the number of message bit that should be encoded. [For example](http://web.mit.edu/6.02/www/f2010/handouts/lectures/L8.pdf), for the (7, \[177, 133\]) structure the branches are:

<img src="https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/gensexamp.png" alt="branches" width="400"/>

<details>
  <summary> They can be easily described via the polynomial structure, that can be also mapped into the shift-registers representation. </summary>
 
<img src="https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/shift_regs.png" width="600" />

*Example of shift-register structure (m1 and m2 are the constrain lengths (memory length)). All of the math operations should be done by modulo 2.*
</details>

Searching of the optimal structure of the convolutional codes is the scientific research item. This relates to the chance to construct [catastrophic](https://www.mathworks.com/help/comm/ref/iscatastrophic.html) convolutional code.  

> Use reference books to select polynomial with required code rate. 

In practice, the encoding procedure can be implemented as the work with the [Trellis structures](https://www.gaussianwaves.com/tag/trellis-diagram/) that simplifies all of the routines to the transactions beatween the some predefined states with the predefined outputs.

<details>
  <summary> Nice illustrations by M. Sc. Dipl.-Ing. (FH) Marko Hennhöfer </summary>

Source: http://www5.tu-ilmenau.de/nt/de/teachings/vorlesungen/itsc_master/folien/script.pdf
    
 
<img src="https://raw.githubusercontent.com/kirlf/CSP/master/Different/assets/trellis_illustration.png" width="600" />

</details>


## Decoding
[Viterbi algorithm](http://www.scholarpedia.org/article/Viterbi_algorithm) (one of the **MLE** – Maximum Likelihood Estimation -  algorithms) is usually used for decoding. Viterbi algorithm also use the [Trellis structures](https://www.gaussianwaves.com/tag/trellis-diagram/) for the decoding. 

![](https://i.pinimg.com/originals/ba/80/a3/ba80a3399d8a1b2ddc61dbb4ec37c513.jpg)

*Andrew J. Viterbi*

Convolutional **decoders** can make either **hard** or **soft** decision. What does it mean? That means differrent type of encoders' inputs: zeros and ones (hard descision) or [log-likelihood ratios](https://www.mathworks.com/help/comm/ug/digital-modulation.html#brc6yjx) (soft descision). The soft descion is more preferable due to BER (bit-error ratio) performance:

<details>
  <summary> MATLAB script. </summary>

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
</details>

![hardsoft](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/softhard.png)

>Fig. 1.1.4. Comparison of QPSK with and without convolutional codes (7, [175 133]) (AWGN).

Moreover, if you choose the larger constrain length (use more delaying memory blocks), your encoder (and decoder) becomes more sophisticated (exponentially). However, coding algorithm becomes more strong (more available combinations, code words), hence, the length of the constrain length influences you BER performance. 

<details>
    <summary> MATLAB script. </summary>

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
</details>

![lens](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/lenss.png)

>Fig. 1.1.5. Comparison of the different structures of the convolutional codes (QPSK, AWGN).

The MATLAB modeling of the transmission of the encoded message is presented below. 

## Modeling in MatLab
This code is developed by example of description of [**convenc**](https://de.mathworks.com/help/comm/ref/convenc.html) MatLab function. 

>**NOTE:** Corrections is done for **MatLab 2014a**.


The main structural blocks for the simulation:
1) Message sourse;
2) M-QAM modulator (*M* is ajustible);
3) Convolutional encoder;
4) AWGN channel;
5) M-QAM demodulator with Approximate LLR (or Exact LLR) outputs;
6) Soft decision Viterbi decoder;
7) BER calculation.

Theoretical values are generated via the **bertool** GUI.

<details>
  <summary> MATLAB script. </summary>
  
``` octave
clear; close all; clc
rng default
M = 4;                 % Modulation order
k = log2(M);            % Bits per symbol
EbNoVec = (0:4)';       % Eb/No values (dB)
numSymPerFrame = 100000;   % Number of QAM symbols per frame

modul = comm.RectangularQAMModulator(M, 'BitInput', true);
berEstSoft = zeros(size(EbNoVec)); 


trellis = poly2trellis(7,[171 133]);
tbl = 32;
rate = 1/2;

decoders = comm.ViterbiDecoder(trellis,'TracebackDepth',tbl,...
'TerminationMethod','Continuous','InputFormat','Unquantized');


for n = 1:length(EbNoVec)
    % Convert Eb/No to SNR
    snrdB = EbNoVec(n) + 10*log10(k*rate);
    % Noise variance calculation for unity average signal power.
    noiseVar = 10.^(-snrdB/10);
    % Reset the error and bit counters
    [numErrsSoft, numErrsHard, numBits] = deal(0);
    
    while numErrsSoft < 100 && numBits < 1e7
        % Generate binary data and convert to symbols
        dataIn = randi([0 1], numSymPerFrame*k, 1);
        
        % Convolutionally encode the data
        dataEnc = convenc(dataIn, trellis);
        
        % QAM modulate
        txSig = step(modul, dataEnc);

        % Pass through AWGN channel
        rxSig = awgn(txSig, snrdB, 'measured');
        
        % Demodulate the noisy signal using hard decision (bit) and
        % soft decision (approximate LLR) approaches.       
        demods = comm.RectangularQAMDemodulator(M, 'BitOutput', true, ...
        'DecisionMethod', 'Approximate log-likelihood ratio',...
        'VarianceSource', 'Property', 'Variance', noiseVar);
        rxDataSoft = step(demods, rxSig);
    
        % Viterbi decode the demodulated data
        dataSoft = step(decoders, rxDataSoft);
        
        % Calculate the number of bit errors in the frame. Adjust for the
        % decoding delay, which is equal to the traceback depth.
        numErrsInFrameSoft = biterr(dataIn(1:end-tbl), dataSoft(tbl+1:end));
        
        % Increment the error and bit counters
        numErrsSoft = numErrsSoft + numErrsInFrameSoft;
        numBits = numBits + numSymPerFrame*k;

    end
    
    % Estimate the BER for both methods
    berEstSoft(n) = numErrsSoft/numBits;
end

%% Theoretical curves
spect = distspec(trellis, 7);
soft_bertool = bercoding(EbNoVec,'conv','soft',1/2,spect); % BER bound

semilogy(EbNoVec, berEstSoft,'-*',EbNoVec, soft_bertool.','-o','LineWidth', 1.5)
hold on
legend('Soft','Soft(theory)','location','best')
grid
xlabel('Eb/No (dB)')
ylabel('Bit Error Rate')
```
</details>
    
![Convolutional codes with 1/2 code rate and constrain length 7 (Soft descision, 4-QAM / QPSK / OQPSK)](https://raw.githubusercontent.com/kirlf/communication_stuff/master/FEC/assets/Soft%20conv.png
).
>Fig. 1.2.1. Convolutional codes with 1/2 code rate and constrain length 7 (Soft descision, 4-QAM / QPSK / OQPSK)


So, the curves are sufficiently matched. Let us continue to use considered model.

## Punctured convolutional codes

To change the coderate of the continuous code, e.g. convolutional code, puncturing procedure is frequently used:

![punct](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/punct.png)

Seems little bit tricky, however it really works in real systems. On the receiver side nulls are inserted according to puncturing pattern usually ("depuncturing" or "insert zeros").

> Implementation of the "puncturing" and "insert zeros" functions in python 3.5 can be obtained by the [following link](https://github.com/kirlf/CSP/blob/master/FEC/functions/Puncturing-Depuncturing.ipynb)

The options *'PuncturePatternSource'* should be defined as *'Property'* and *'PuncturePattern'* should be specified in the **ConvolutionalEncoder** and **ViterbiDecoder** blocks to apply the puncturing in MatLab.

> Parameters were selected according to [Punctured Convolutional Coding](https://uk.mathworks.com/help/comm/ug/punctured-convolutional-coding-1.html) MathWorks example.

<details>
  <summary> MATLAB script. </summary>

``` octave
clear; close all; clc
rng default
M = 4;                 % Modulation order
k = log2(M);            % Bits per symbol
EbNoVec = (0:8)';       % Eb/No values (dB)
numSymPerFrame = 300000;   % Number of QAM symbols per frame

modul = comm.PSKModulator(M, 'BitInput', true);
berEstSoft = zeros(size(EbNoVec)); 


trellis = poly2trellis(7,[171 133]);
tbl = 96;
rate = 3/4;

spect = distspec(trellis);
encoders = comm.ConvolutionalEncoder(trellis,...
    'PuncturePatternSource', 'Property', 'PuncturePattern', [1; 1; 0; 1; 0; 1]);
decoders = comm.ViterbiDecoder(trellis,'TracebackDepth',tbl,...
    'TerminationMethod','Continuous','InputFormat','Unquantized',...
    'PuncturePatternSource', 'Property', 'PuncturePattern', [1; 1; 0; 1; 0; 1]);


for n = 1:length(EbNoVec)
    % Convert Eb/No to SNR
    snrdB = EbNoVec(n) + 10*log10(k*rate);
    % Noise variance calculation for unity average signal power.
    noiseVar = 10.^(-snrdB/10);
    % Reset the error and bit counters
    [numErrsSoft, numErrsHard, numBits] = deal(0);
    
    while numErrsSoft < 100 && numBits < 1e7
        % Generate binary data and convert to symbols
        dataIn = randi([0 1], numSymPerFrame*k, 1);
        
        % Convolutionally encode the data
        dataEnc = step(encoders, dataIn);

        % QAM modulate
        txSig = step(modul, dataEnc);

        % Pass through AWGN channel
        rxSig = awgn(txSig, snrdB, 'measured');
        
        % Demodulate the noisy signal using hard decision (bit) and
        % soft decision (approximate LLR) approaches.
        
        demods = comm.PSKDemodulator(M, 'BitOutput', true, ...
        'DecisionMethod', 'Approximate log-likelihood ratio', 'VarianceSource', 'Property', 'Variance', noiseVar);
        rxDataSoft = step(demods, rxSig);
    
        % Viterbi decode the demodulated data
        dataSoft = step(decoders, rxDataSoft);
               
        % Calculate the number of bit errors in the frame. Adjust for the
        % decoding delay, which is equal to the traceback depth.
        numErrsInFrameSoft = biterr(dataIn(1:end-tbl), dataSoft(tbl+1:end));
        
        % Increment the error and bit counters
        numErrsSoft = numErrsSoft + numErrsInFrameSoft;
        numBits = numBits + numSymPerFrame*k;

    end
    
    % Estimate the BER for both methods
    berEstSoft(n) = numErrsSoft/numBits;
end

%% Theoretical curves
spect = distspec(trellis, 7);
soft_bertool = bercoding(EbNoVec,'conv','soft',1/2,spect); % BER bound

figure(1)
semilogy(EbNoVec, soft_bertool.','-o',EbNoVec,berEstSoft.','-o', 'LineWidth', 1.5)
grid on
hold on
legend('1/2 (theory)','3/4 (simulation)','location','best')
grid on
xlabel('Eb/No (dB)')
ylabel('Bit Error Rate')
```
</details>

![Punct](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/Soft34.png). 
>Fig. 1.2.2. Convolutional codes with 1/2 and 3/4 code rates (constrain length 7, Soft descision, 4-QAM / QPSK / OQPSK)

The 1 dB difference can be noted. Actually, it is the price for the higher data rate.

### References

\[1\] 3rd Generation Partnership Project (September 2012). "3GGP TS45.001: Technical Specification Group GSM/EDGE Radio Access Network; Physical layer on the radio path; General description". Retrieved 2013-07-20.

\[2\] Halonen, Timo, Javier Romero, and Juan Melero, eds. GSM, GPRS and EDGE performance: evolution towards 3G/UMTS. John Wiley & Sons, 2004.

\[3\] Eberspächer J. et al. GSM-architecture, protocols and services. – John Wiley & Sons, 2008.

\[4\] Moon, Todd K. "Error correction coding." Mathematical Methods and Algorithms. Jhon Wiley and Son (2005).

\[5\] Benedetto, Sergio, and Guido Montorsi. "Role of recursive convolutional codes in turbo codes." Electronics Letters 31.11 (1995): 858-859.

### Suggested literature

- Francis, Michael. "Viterbi Decoder Block Decoding-Trellis Termination and Tail Biting." Xilinx XAPP551 v2. 0, DD (2005): 1-21.

- Chen, Qingchun, Wai Ho Mow, and Pingzhi Fan. "Some new results on recursive convolutional codes and their applications." Information Theory Workshop, 2006. ITW'06 Chengdu. IEEE. IEEE, 2006.

- Fiebig, U-C., and Patrick Robertson. "Soft-decision and erasure decoding in fast frequency-hopping systems with convolutional, turbo, and Reed-Solomon codes." IEEE Transactions on Communications 47.11 (1999): 1646-1654.

- Bhaskar, Vidhyacharan, and Laurie L. Joiner. "Performance of punctured convolutional codes in asynchronous CDMA communications under perfect phase-tracking conditions." Computers & Electrical Engineering 30.8 (2004): 573-592.

- Modestino, J., and Shou Mui. "Convolutional code performance in the Rician fading channel." IEEE Transactions on Communications 24.6 (1976): 592-606.

- Chen, Yuh-Long, and Che-Ho Wei. "Performance evaluation of convolutional codes with MPSK on Rician fading channels." IEE Proceedings F-Communications, Radar and Signal Processing. Vol. 134. No. 2. IET, 1987.

### Suggested literature (in Russian):

- Хлынов, А. А. "ИССЛЕДОВАНИЕ ПРИНЦИПОВ РЕАЛИЗАЦИИ LDPC КОДЕКА НА ПЛИС." Фундаментальные проблемы радиоэлектронного приборостроения 12.6 (2012): 150-156.

- Банкет, В. Л. "Сигнально-кодовые конструкции в телекоммуникационных системах." О.: Феникс (2009).

- Никитин, Г. И. "ББК 32.811. 4 Н62.“

- Колесник В. Д., Полтырев Г. Ш. Курс теории информации. – " Наука," Глав. ред. физико-математической лит-ры, 1982.

- Нгок Д. К. Исследование методов поиска оптимальных сверточных и перфорированных сверточных кодов : дис. – Диссертация на соискание ученой степени кандидата технических наук. СПб.: ЛЭТИ, 2014.

### Afterwords

The following Wikipedia articles were contributed based on this page:
* [Convolutional code](https://en.wikipedia.org/wiki/Convolutional_code)
