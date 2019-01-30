# OFDM Frame Generator 
## (MATLAB tutorial)
### M.Sc. Vladimir Fadeev
#### Kazan, 2017

## Preface

Hello, everyone!

The material presented below is primarily intended for students of **GRIAT-CSP** \(KNRTU-KAI named after A.Tupolev\). However, everyone can join the discussion, or write to me, if you know how to make this small tutorial more interesting and useful. You are welcome!

This tutorial aims to show the opportunities of modeling without different **GUI** \(Graphical User Interface\), such as **MatLab Simulink**, for example.

The author does not deny that for certain purposes it is more convenient to use the  **Simulink**, however, he is deeply convinced that the solutions made with the help of programming languages are more manageable, faster \(in terms of speed of processing\) and elegant.

The way of modeling of the **OFDM** signal generator based on the MATLAB language features will be presented in this tutorial. 
This approach will rely entirely on MATLAB's matrices magic and if after that you will still consider Simulink as a simpler solution - [*well, nobody is perfect*](https://www.youtube.com/watch?v=CYUfPTeE0DM).

So, all the words are said, tune in to a serious mood, let's go!

M.Sc. Vladimir Fadeev

vladimir\_fadeev1993@mail.ru

## Introduction

Before we start I would recomend you to learn basic stuff about OFDM and its applications in LTE by professor Andreas Mitschele-Thiel's [lectures](https://www.tu-ilmenau.de/en/integrated-communication-systems-group/teaching/master-studies/?lecture_id=27).

> Additionally, you can learn more by IEEE standarts and papers \(e.g. [this](http://ieeexplore.ieee.org/document/5766559/) and [this](http://ieeexplore.ieee.org/document/4459272/) - God, bless Alexandra Elbakyan!\).

We should mention that we don't consider cyclic prefix and preamble in this work, because we believe that to add this items to your research projects wont be a difficult task  after this tutorial.

Let us predefine our techinical task. Assume that we have:

* fixed number of subcarriers, 
* fixed length of the OFDM frame and 
* we should to add one null to the middle and couples of nulls to the begining and the end of the frame;
* information symbols are modulated by pi/4-QPSK \( or 4-QAM \). 

Fortunatelly, syntax of MatLab is not so difficult for understanding and there is no necessity to explain it for a long time. Briefly, we can note that :

* comments can be added after '%' symbol, 
* semicolon \(';'\) in the end of the row \(line\) is not necessary and only doesn't allow displaying of the result,
* tabulation is also not necessary, but it always is a good taste, 
* indexes in MatLab begin from **1** \(unlike **Python** or **C** where indexec begin from **0**\);
* needed help you can obtain via **F1** hotkey or from the [official MathWorks site](https://ch.mathworks.com/solutions/dsp.html).

## Modeling

We guess more fruitful to see it in the example. Click the **Create new script** bottom and start to print:

```Octave
clear all; close all; clc

M = 4; % e.g. QPSK 
bits = log2(M); % bits per modulation symbol

frame_len = 32; % the length of our OFDM frame
message = randi([0 1], 16*bits, 1); % binary information symbols
num_inf_ind = 16; % number of subcarriers (information symbols, actually) in the frame
num_pilots = frame_len - num_inf_ind - 5; % number of pilots
pilots = [1;j;-1;-j]; % what kind of pilots we use
nulls = [1,2,frame_len/2,frame_len-1,frame_len]; %indexes of nulls

if M >= 16
	info_symbols = qammod(message, M, pi/4);
else
	info_symbols = pskmod(message, M, pi/4);
end 
```

Ok, we have defined number of information symbols, nulls and have calculated number of pilots. However, indexes \(positions\) of subcariers and pilots haven't been defined yet. Of course, for simple examples it works to define that explisetly:

```Octave
inf_ind_1 = (floor(linspace(4,14,num_inf_ind/2))).'; 
inf_ind_2 = (floor(linspace(18,29,num_inf_ind/2))).';
inf_ind = [inf_ind_1;inf_ind_2]; % simple concatenation
```
However, for the real projects we have to use frames with a lot of elements \(256 , 512 e.t.c.\) and therefore more useful to construct index vectors automaticaly.

