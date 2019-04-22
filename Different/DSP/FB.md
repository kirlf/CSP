# Filter Banks: a part of MP3 
## M.Sc. Vladimir Fadeev
### Kazan, 2019

## Introduction

I think there is no visitor to this page who would not hear about the MP3 standard (MPEG-1 Layer III), so I don't see any sense in the long introduction. The format is known largely due to its compactness and rather good (in terms of indifferent to lossless formats) quality. Nowadays, it is very outdated, but it still exists in the players of some music lovers, and on online music sites (perhaps more now in the form of its reincarnation - the AAC format).

How was the balance between size and quality found? If in brief, then:
1. the application of filter banks;
2. the application of the psycho-acoustic (perceptual) model in the process of compression of non-information (irrelevance);
3. the use of [entropy coding](https://github.com/kirlf/CSP/blob/master/Different/Coding_Theory/README.md) in the process of getting rid of redundancy.

<img src = "https://pp.userapi.com/c844720/v844720150/bcd72/80VaKOi-hI8.jpg" width = "700">

In this seminar, filter banks will be considered (see slides **02 Filterbanks1, NobleID** and **03 FilterBanks2** by this [link](https://www.tu-ilmenau.de/mt/lehrveranstaltungen/lehre-fuer-master-mt/audio-coding/)).

## Main idea

In general, the idea can be described as follows: we have a line (comb, as they sometimes say) of parallel filters, each of which is consistently tuned to its own frequency. Frequencies are usually normalized from 0 to pi. Accordingly, the more filters we have at our disposal, the rarer (smoother) the transition step from frequency to frequency becomes, and therefore the more frequency variations we can analyze.

Filters in this context are, as a rule, everyone who has experienced signal processing known Fourier converters in one form or another: [FFT](https://github.com/kirlf/CSP/blob/master/Different/DSP/FFT.md), [DCT-IV](https://www.tu-ilmenau.de/fileadmin/media/mt/lehre/ma_mt/audiocoding/Lecture_WS2013_14/04_shl_Filterbanks1_NobleID_WS2013-14.pdf), [MDCT](https://www.tu-ilmenau.de/fileadmin/public/mt_ams/public/mt_ams/Audio_C.pl/aft/aft/aft_de/file/deal_ws2013_Noble/Lecture_WS2013_14/04_shl_Filterbanks1_NobleID_WS2013-14.pdf), [PQMF](https://www.tu-ilmenau.de/fileadmin/public/mt_ams/Audio_Coding/Vorlesung/WS_2016-17/07_shl_PQMF_MPEG1-2BC_WS2016-17.pdf), etc.

## Restrictions

You cannot select too many filters due to the pre-echo effect ![](https://pp.userapi.com/c845020/v845020283/b410a/6stmEn7NaXY.jpg)
- *reason: blocks too long (too many bands)*

## Types

There are several methods for using a filter comb. Consider the two most famous:
1. Direct application;
<img src = "https://pp.userapi.com/c845523/v845523283/b5477/mN4VMQzDnkE.jpg" width = "700">

2. Noble Identities.
<img src = "https://pp.userapi.com/c849424/v849424283/3f6aa/FC571JKPJ80.jpg" width = "700">

**Home task**: Explain what is the advantage of one method over another?

## Down-sampling и Up-sampling

In the process of applying parallel filters, we willy-nilly increase the number of samples, and accordingly, the playback frequency and the size of the file being processed. In order to avoid such consequences, two mirror procedures are applied:


<img src="https://pp.userapi.com/c824603/v824603630/17a383/-bKRpCkWCoo.jpg" width="700">
Up-sampling 
<img src="https://pp.userapi.com/c824603/v824603630/17a38c/XUmXKfiDRdg.jpg" width="700">

## Math description

In the framework of this work, we will consider the method of MDCT (Modified Discret Cosine Transform):

<p align="center" style="text-align: center;"><img align="center" src="https://tex.s2cms.ru/svg/%20h_k(L-1-n)%20%3D%20h(n)cos%5Cleft(%5Cfrac%7B%5Cpi%7D%7BN%7D(k%2B0.5)(n%2B0.5-%5Cfrac%7BN%7D%7B2%7D)%5Cright)%20" alt=" h_k(L-1-n) = h(n)cos\left(\frac{\pi}{N}(k+0.5)(n+0.5-\frac{N}{2})\right) " /></p>

where the index <img src="https://tex.s2cms.ru/svg/%20k%20" alt=" k " /> is the filter number from 0 to <img src="https://tex.s2cms.ru/svg/N-1" alt="N-1" /> (<img src="https://tex.s2cms.ru/svg/%20N%20" alt=" N " /> is the length of the filter), <img src="https://tex.s2cms.ru/svg/%20n%20" alt=" n " /> is the count number from 0 to <img src="https://tex.s2cms.ru/svg/%202N-1%20" alt=" 2N-1 " />, and <img src="https://tex.s2cms.ru/svg/%20h(n)%20" alt=" h(n) " /> is some window function. Note that the representation is given in the time domain. As a window function, select a sine window:


<p align="center" style="text-align: center;"><img align="center" src="https://tex.s2cms.ru/svg/%20h(n)%20%3D%20sin%5Cleft(%5Cfrac%7B%5Cpi%7D%7BL%7D(n%2B0.5)%5Cright)%20" alt=" h(n) = sin\left(\frac{\pi}{L}(n+0.5)\right) " /></p>

where <img src="https://tex.s2cms.ru/svg/%20L%20%3D%202N%20" alt=" L = 2N " /> is the window length.
As a rule, the same mathematical functions are used for analysis and synthesis.


## MDCT modeling

