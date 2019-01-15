# Convolutional codes basics

## Summary

## Reed-Solomon Convolutional concatenated (RSCC) codes

Very popular option of the FEC in the satellite communication systems.
![RSCC](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/rsc.png)
Fig. 1.3.1. Deep-space concatenated coding system. \[1, p. 433\]

It relates to the [deep-space communication standard](https://ipnpr.jpl.nasa.gov/progress_report/42-63/63H.PDF) that allows to achieve sufficiently high BER performance.

### Little bit more about Reed-Solomon codes

Reed-Solomon (RS) codes is the type of [cyclic codes](https://en.wikipedia.org/wiki/Cyclic_code), i.e. a block codes, where the circular
shifts of each code word gives another code word. Moreover, RS codes can be defined as the specific, **non-binary** case of the [Bose–Chaudhuri–Hocquenghem (BCH)](https://en.wikipedia.org/wiki/BCH_code) codes. Syndrome decoding is used:

![syndr](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/syndrome.png)

Frequently are measured in symbols (bytes, blocks). 

![RScoderate](https://raw.githubusercontent.com/kirlf/CSP/master/FEC/assets/RScoderate.png)




## Turbo convolutional codes


## References

\[1\] J. Hagenauer, E. Offer, and L. Papke, Reed Solomon Codes and Their Applications. New York IEEE Press, 1994
