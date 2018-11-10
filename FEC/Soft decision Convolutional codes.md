# Soft decision Convolutional codes 

This code is developed by example of description of [**convenc**](https://de.mathworks.com/help/comm/ref/convenc.html) MatLab function. Corrections is done for **MatLab 2014a**.

The main structural boxes for the simulation:
1) Message sourse;
2) M-QAM modulator (*M* is ajustible);
3) Convolutional encoder;
4) AWGN channel;
5) M-QAM demodulator with Approximate LLR (or Exact LLR) outputs;
6) Soft decision Viterbi decoder;
7) BER calculation.

``` octave
clear; close all; clc
rng default
M = 4;                      % Modulation order
k = log2(M);                % Bits per symbol
EbNoVec = (0:15)';          % Eb/No values (dB)
numSymPerFrame = 100000;    % Number of QAM symbols per frame

modul = comm.RectangularQAMModulator(M, 'BitInput', true);
berEstSoft = zeros(size(EbNoVec)); 
soft_bertool = [0.500000000000000   0.0783896324670213  0.00710474393540032 0.000428949195656827    1.74024834281753e-05    4.40336640596542e-07    5.60804795434027e-09    2.70206257989620e-11    3.57916979368945e-14    8.99739068685192e-18    2.74381467584029e-22    5.84276962481868e-28    4.35508062487951e-35    4.76970915173631e-44    2.57382887992327e-55    1.72927075040153e-69];

trellis = poly2trellis(7,[171 133]);
tbl = 32;
rate = 1/2;

decoders = comm.ViterbiDecoder(trellis,'TracebackDepth',tbl,'TerminationMethod','Continuous','InputFormat','Unquantized');


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
```

![https://raw.githubusercontent.com/kirlf/communication_stuff/master/FEC/assets/Soft%20conv.png](Convolutional codes with 1/2 code rate and constrain length 7 (Soft descision, 4-QAM / QPSK / OQPSK)).

