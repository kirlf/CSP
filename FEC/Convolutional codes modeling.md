### Summary

   1.1. [Introduction](https://github.com/kirlf/CSP/blob/master/FEC/Convolutional%20codes%20intro.md)

   1.2. Modeling in MatLab
    
   1.3. [Extensions of the convolutional codes idea](https://github.com/kirlf/CSP/blob/master/FEC/Conv%20codes%20idea%20extensions.md)
    
# Modeling in MatLab
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

![Convolutional codes with 1/2 code rate and constrain length 7 (Soft descision, 4-QAM / QPSK / OQPSK)](https://raw.githubusercontent.com/kirlf/communication_stuff/master/FEC/assets/Soft%20conv.png
).
>Fig. 1.2.1. Convolutional codes with 1/2 code rate and constrain length 7 (Soft descision, 4-QAM / QPSK / OQPSK)


So, the curves are sufficiently matched. Let us continue to use considered model.

## Punctured convolutional codes

The options *'PuncturePatternSource'* should be defined as *'Property'* and *'PuncturePattern'* should be specified in the **ConvolutionalEncoder** and **ViterbiDecoder** blocks to apply the puncturing.

> Parameters were selected according to [Punctured Convolutional Coding](https://uk.mathworks.com/help/comm/ug/punctured-convolutional-coding-1.html) MathWorks example.

MATLAB simulation:

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
![Punct](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/Soft34.png). 
>Fig. 1.2.2. Convolutional codes with 1/2 and 3/4 code rates (constrain length 7, Soft descision, 4-QAM / QPSK / OQPSK)

The 1 dB difference can be noted. Actually, it is the price for the higher data rate.

## Convolutional codes in fading channel

[Rician channel model](https://nbviewer.jupyter.org/gist/kirlf/4328eb389b3ddc9a0c350eaed468f870) was used for the modeling.

``` octave
clear; close all; clc
rng default
M = 4;                 % Modulation order
k = log2(M);            % Bits per symbol
EbNoVec = (0:30)';       % Eb/No values (dB)
numSymPerFrame = 300000;   % Number of QAM symbols per frame

modul = comm.PSKModulator(M, 'BitInput', true);
berEstSoft = zeros(size(EbNoVec)); 

K = 4;
trellis = poly2trellis(7,[171 133]);
tbl = 96;
rate = 1/2;

spect = distspec(trellis);
encoders = comm.ConvolutionalEncoder(trellis);%,...
    %'PuncturePatternSource', 'Property', 'PuncturePattern', [1; 1; 0; 1; 0; 1]);
decoders = comm.ViterbiDecoder(trellis,'TracebackDepth',tbl,...
    'TerminationMethod','Continuous','InputFormat','Unquantized');%,...
    %'PuncturePatternSource', 'Property', 'PuncturePattern', [1; 1; 0; 1; 0; 1]);



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

        h = sqrt( K/(K+1)) +... 
        sqrt( 1/(K+1))*(1/sqrt(2))*(randn(size(txSig))...
         + 1j*randn(size(txSig))); 
        txSig = txSig.*h;
        % Pass through AWGN channel
        rxSig = awgn(txSig, snrdB, 'measured');
        rxSig = rxSig./h;
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
%soft_bertool = bercoding(EbNoVec,'conv','soft',1/2,spect); % BER bound
soft_bertool = berfading(EbNoVec, 'psk', M, 1, K);

figure(1)
semilogy(EbNoVec,soft_bertool,'b-o',EbNoVec,berEstSoft.','c-o', 'LineWidth', 1.5)
grid on
hold on
legend('uncoded (theory)','1/2 (simulation)','location','best')
grid on
xlabel('Eb/No (dB)')
ylabel('Bit Error Rate')
```
![fading](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/conv_fading.png)
>Fig. 1.2.3. Coded and uncoded cases in Rician flat fading (K = 4, constrain length 7, Soft descision, 4-QAM / QPSK / OQPSK)

So, the BER performace is still better in the coded case.

## Suggested literature:

1. Modestino, J., and Shou Mui. "Convolutional code performance in the Rician fading channel." IEEE Transactions on Communications 24.6 (1976): 592-606.

2. Chen, Yuh-Long, and Che-Ho Wei. "Performance evaluation of convolutional codes with MPSK on Rician fading channels." IEE Proceedings F-Communications, Radar and Signal Processing. Vol. 134. No. 2. IET, 1987.


