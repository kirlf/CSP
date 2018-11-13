<div @import url('//maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css'); .isa_info, .isa_success, .isa_warning, .isa_error { margin: 10px 0px; padding:12px; } .isa_info { color: #00529B; background-color: #BDE5F8; } .isa_success { color: #4F8A10; background-color: #DFF2BF; } .isa_warning { color: #9F6000; background-color: #FEEFB3; } .isa_error { color: #D8000C; background-color: #FFD2D2; } .isa_info i, .isa_success i, .isa_warning i, .isa_error i { margin:10px 22px; font-size:2em; vertical-align:middle; }</div>

# Soft decision Convolutional codes 

This code is developed by example of description of [**convenc**](https://de.mathworks.com/help/comm/ref/convenc.html) MatLab function. Corrections is done for **MatLab 2014a**.

<div class="isa_info">
    <i class="fa fa-info-circle"></i>
    Replace this text with your own text.
</div>

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
M = 4;                      % Modulation order
k = log2(M);                % Bits per symbol
numSymPerFrame = 100000;    % Number of QAM symbols per frame

modul = comm.RectangularQAMModulator(M, 'BitInput', true);
berEstSoft = zeros(size(EbNoVec)); 
soft_bertool = [0.500000000000000   0.0783896324670213...
    0.00710474393540032 0.000428949195656827 1.74024834281753e-05];
EbNoVec = (0:length(soft_bertool)-1)';  % Eb/No values (dB)

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

![Convolutional codes with 1/2 code rate and constrain length 7 (Soft descision, 4-QAM / QPSK / OQPSK)](https://raw.githubusercontent.com/kirlf/communication_stuff/master/FEC/assets/Soft%20conv.png
).
<center>Fig. 1. Convolutional codes with 1/2 code rate and constrain length 7 (Soft descision, 4-QAM / QPSK / OQPSK)</center>
