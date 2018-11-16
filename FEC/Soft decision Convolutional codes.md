
# Soft decision Convolutional codes 

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

# Punctured convolutional codes

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
rate = 2/3;

spect = distspec(trellis);
%soft_bertool = bercoding(EbNoVec,'conv','soft',rate,spect); % BER bound
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
        %dataEnc = convenc(dataIn, trellis, [1; 1; 0; 1; 0; 1]);
        dataEnc = step(encoders, dataIn);
        reset(encoders);

        % QAM modulate
        %txSig = qammod(dataEnc,M);%'InputType','bit','UnitAveragePower',true);
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

EbNoVec = (0:8)';

trellis = poly2trellis(7,[171 133]);
tbl = 32;
rate = 1/2;

spect = distspec(trellis, 7);
soft_bertool = bercoding(EbNoVec,'conv','soft',1/2,spect); % BER bound

figure(1)
semilogy(EbNoVec, soft_bertool.','-o',EbNoVec,berEstSoft(1:9).','-o', 'LineWidth', 1.5)
grid on
hold on
legend('1/2 (theory)','2/3 (simulation)','location','best')
grid on
xlabel('Eb/No (dB)')
ylabel('Bit Error Rate')
```
