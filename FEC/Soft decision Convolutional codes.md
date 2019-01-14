
# Convolutional codes basics 

## Introduction

[Convolutional codes](https://en.wikipedia.org/wiki/Convolutional_code) are kind of continuous error-correcting codes. They can be easily described via the polynomial structure, that can be also mapped into shift-registers representation, e.g.:

![shiftregs](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/shift_regs.png)

In practice, polynomial structures are selected from the reference books. Searching of the optimal structure of the convolutional codes is the scientific research item. This relates to chance to construct [catastrophic](https://www.mathworks.com/help/comm/ref/iscatastrophic.html) convolutional code structure.  

Moreover, the following classification can be applied:
![SysNonSys](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/syst-nonsyst.png)

``` octave
clear all
close all
clc

EbNo = 0:7;
lens = 5:9;
gens = [[35 23]; [51 73]; [171 133]; [371 247]; [753 561]];

for g = 1: length(gens)
   spect =  distspec(poly2trellis(lens(g), gens(g,:)), 7);
   ber(:, g) = bercoding(EbNo,'conv','soft',1/2,spect);
end

semilogy(EbNo, ber,'LineWidth', 1.5)
hold on
legend('(5,[35 23])','(6,[51 73])','(7,[171 133])','(8,[371 247])','(9,[753 561])','location','best')
grid on
xlabel('Eb/No (dB)')
ylabel('Bit Error Rate')
```



![LLR](https://i2.wp.com/www.gaussianwaves.com/gaussianwaves/wp-content/uploads/2012/07/PDF_of_BPSK_symbols.png?ssl=1)

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
        reset(demods);
    
        % Viterbi decode the demodulated data
        dataSoft = step(decoders, rxDataSoft);
        
        %reset(decoderh);
        reset(decoders);
        
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
trellis = poly2trellis(7,[171 133]);
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
>Fig. 1. Convolutional codes with 1/2 code rate and constrain length 7 (Soft descision, 4-QAM / QPSK / OQPSK)


So, the curves are sufficiently matched. Let us continue to use considered model.

## Punctured convolutional codes

Usually, to obtain needed code rate convolutional encoded message should be punctured, e.g.:

![punct](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/punct.png)

Seems little bit tricky, however it really works in real systems. On the receiver side nulls are inserted according to puncturing pattern usually ("depuncturing" or "insert zeros").

Implementation of the "puncturing" and "isert zeros" functions in python 3.5 can be obtained by the [following link](https://github.com/kirlf/CSP/blob/master/FEC/functions/Puncturing-Depuncturing.ipynb).

MATLAB simulation:

``` octave
clear; close all; clc
rng default
M = 4;                 % Modulation order
k = log2(M);            % Bits per symbol
EbNoVec = (0:15)';       % Eb/No values (dB)
numSymPerFrame = 300000;   % Number of QAM symbols per frame

modul = comm.RectangularQAMModulator(M, 'BitInput', true);
berEstSoft = zeros(size(EbNoVec)); 


trellis = poly2trellis(7,[171 133]);
tbl = 32;
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
        reset(encoders);

        % QAM modulate
        txSig = step(modul, dataEnc);

        % Pass through AWGN channel
        rxSig = awgn(txSig, snrdB, 'measured');
        
        % Demodulate the noisy signal using hard decision (bit) and
        % soft decision (approximate LLR) approaches.
        
        demods = comm.RectangularQAMDemodulator(M, 'BitOutput', true, ...
        'DecisionMethod', 'Approximate log-likelihood ratio', 'VarianceSource', 'Property', 'Variance', noiseVar);
        rxDataSoft = step(demods, rxSig);
        reset(demods);
    
        % Viterbi decode the demodulated data
        dataSoft = step(decoders, rxDataSoft);
        
        %reset(decoderh);
        reset(decoders);
        
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
EbNoVec = (0:8)';
trellis = poly2trellis(7,[171 133]);
spect = distspec(trellis, 7);
soft_bertool = bercoding(EbNoVec,'conv','soft',1/2,spect); % BER bound

figure(1)
semilogy(EbNoVec, soft_bertool.','-o',EbNoVec,berEstSoft(1:9).','-o', 'LineWidth', 1.5)
grid on
hold on
legend('1/2 (theory)','3/4 (simulation)','location','best')
grid on
xlabel('Eb/No (dB)')
ylabel('Bit Error Rate')
```
![Punct](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/Soft34.png). 
>Fig. 2. Convolutional codes with 1/2 and 3/4 code rates (and constrain length 7, Soft descision, 4-QAM / QPSK / OQPSK)

The 2 dB difference can be noted. Actually, it is the price for the higher data rate.

## Flat fading channel

More realistic case is the case of the [fading channel](https://github.com/kirlf/CSP/blob/master/Channels/RicianFlatFading.ipynb). Let us test capabilities of the soft decison  convolutional codes in two fadiing states:
1. Rician factor *K = 4.0* (relatively light Rician flat fading);
2. Rician factor *K = 0* (Rayleigh (no line-of-sight component) flat fading).

Additionally, we are plotting the AWGN curve from the previous simulation as the no fading case.

``` octave
clear; close all; clc
rng default
M = 4;                 % Modulation order
k = log2(M);            % Bits per symbol
EbNoVec = (0:15)';       % Eb/No values (dB)
numSymPerFrame = 300000;   % Number of QAM symbols per frame
K = 4; %K=0 means Rayleigh fading;

modul = comm.RectangularQAMModulator(M, 'BitInput', true);
berEstSoft = zeros(size(EbNoVec)); 


trellis = poly2trellis(7,[171 133]);
tbl = 32;
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
        reset(encoders);

        % QAM modulate
        txSig = step(modul, dataEnc);

        % Fading
        r = sqrt( K/(K+1))...
            + sqrt( 1/(K+1))*(1/sqrt(2))*(randn(size(txSig)) + 1j*randn(size(txSig)));
        ric_msg = txSig.*r; % Rician flat fading


        % Pass through AWGN channel
        rxSig = awgn(ric_msg, snrdB, 'measured');

        % Zero-forcing equalization
        noisy_mod = rxSig ./ r; %

        % Demodulate the noisy signal using hard decision (bit) and
        % soft decision (approximate LLR) approaches.
        demods = comm.RectangularQAMDemodulator(M, 'BitOutput', true, ...
        'DecisionMethod', 'Approximate log-likelihood ratio', 'VarianceSource', 'Property', 'Variance', noiseVar);
        rxDataSoft = step(demods, noisy_mod);
        reset(demods);
    
        % Viterbi decode the demodulated data
        dataSoft = step(decoders, rxDataSoft);
        
        %reset(decoderh);
        reset(decoders);
        
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
```

![fading](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/34SoftFading.png)

To sum up, we are noting that convolutional codes require more amount of redundacy to satisfy quality requirements, especially in real fading channels.
