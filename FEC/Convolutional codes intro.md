
# Convolutional codes basics 

## Introduction

[Convolutional codes](https://en.wikipedia.org/wiki/Convolutional_code) are kind of continuous error-correcting codes. They can be easily described via the polynomial structure, that can be also mapped into the shift-registers representation, e.g.:

![shiftregs](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/shift_regs.png)

In practice, polynomial structures are selected from the reference books. Searching of the optimal structure of the convolutional codes is the scientific research item. This relates to chance to construct [catastrophic](https://www.mathworks.com/help/comm/ref/iscatastrophic.html) convolutional code structure.  

Moreover, the following classification can be applied:
![SysNonSys](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/syst-nonsyst.png)

Non-systematic convolutional codes are more popular due to better noise immunity.

The name of convolutional codes directly relates to the convolution: encoding can be done via this math routine.

> See more in our Puthon tutorial:
>
> [Jupyter notebook](https://github.com/kirlf/CSP/blob/master/FEC/Convolutional_encoder.ipynb)
>
> [RISE slides](https://www.dropbox.com/s/gt3bsjy7yw5fmse/Convolutional_codes.slides.html?dl=0)

Convolutional **decoders** can make either **hard** or **soft** decision. What does it mean? That means differrent type of encoders' inputs: zeros and ones (hard descision) or [log-likelihood ratios](https://www.mathworks.com/help/comm/ug/digital-modulation.html#brc6yjx) (soft descision). The soft descion is more preferable due to BER (bit-error ratio) performance:



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
