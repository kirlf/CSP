# Task 3: Write and learn (Python, NumPy)

**Tutor**: M.Sc. Vladimir Fadeev

**Form of reports**: Jupyter notebook based generated HTML file.

# Introduction

Yes, MatLab is very popular tool among communication systems engineers, hower it has several serious disadvantages:
- MatLab is not free;
- MATLAB language depends on MatLab/Octave that makes it less flexible than "true" programming languages;
- Most of block are "black boxes" (source code is not available).

This facts is good motivation to learn another popular programming language - **Python**.

Python is:
- one of central tools for Machine Learning and Deep Learning;
- used in web and communication applications;
- used as flexible way to automitize routines

and therefore it has a dig and supportive community. 

Moreover, a lot of Python based solutions are open-source (and therefore free).

# Task

Today you will try to approximate histogram of Poisson process. Why Poisson? Because it is simple and also used in communications.

Distributed by Poisson random process can be described by the following formula: 

<p align="center"><img align="center" src="https://i.upmath.me/svg/%20f(k%2C%20%5Clambda)%20%3D%20%5Cfrac%7B%5Clambda%5Ek%20e%5E%7B-%5Clambda%7D%7D%7Bk!%7D%20%5Cqquad(1)%20" alt=" f(k, \lambda) = \frac{\lambda^k e^{-\lambda}}{k!} \qquad(1) " /></p>

where <img src="https://i.upmath.me/svg/k%20%5Cgeq%200" alt="k \geq 0" /> is the integer value, and <img src="https://i.upmath.me/svg/%5Clambda" alt="\lambda" /> is the intensity parametr.

Try to select optimal parameters with which some approximation error will be minimal. For example, mean-squared error: 

<p align="center"><img align="center" src="https://i.upmath.me/svg/%20MSE%20%3D%20%5Cfrac%7B1%7D%7BN%7D%5Csum_%7Bi%3D0%7D%5E%7BN-1%7D(a_i%20-%20b_i)%5E2%20%5Cqquad(2)" alt=" MSE = \frac{1}{N}\sum_{i=0}^{N-1}(a_i - b_i)^2 \qquad(2)" /></p>

where <img src="https://i.upmath.me/svg/a_i" alt="a_i" /> and <img src="https://i.upmath.me/svg/b_i" alt="b_i" /> is <img src="https://i.upmath.me/svg/i" alt="i" />-th items of sequence (length of the sequence is  <img src="https://i.upmath.me/svg/N" alt="N" />).

Use the following libraries during this practice:

```python
import math
import numpy as np
import matplotlib.pyplot as plt
```

Use the following teplate as the reference:

```python
class FitPoisson:
    def __init__(self):
        self.lambd = None
    
    def __MSE(self, a, b):
        # Write your code here.
        return mse

    def __poisson(self, lambd, k):
        f = [lambd**ki*np.exp(-lambd) / math.factorial(ki) for ki in k]
        return np.array(f)  

    def fit_poisson(self, count, bins, max_lambda=100):
        
        '''
        inputs:
          count (array): 
              values of the histogram bins that should be approximated
          bins (array): 
              edges of the histogram bins that should be approximated
          max_lambda (int): 
              maximum value of the lambda for searching
        outputs:
          lambda_opt (int):
              optimal lambda
          f_norm (array):
              normalized distribution with optimal lambda
          k (array):
              the array of the k's
        '''

        lambdas = [lmbd for lmbd in range(1, max_lambda)] # range of lambdas

        # Select non-zero values of bins:
        non_zero_count = count[np.nonzero(count)]

        start = int(np.min(bins)) # the first edge of bins 
        stop = len(non_zero_count) + start # the last required edge of bins

        k = np.array([i for i in range(start, stop)],\
                  dtype=float)
                  
        e = [] #list for errors
        for lambd in lambdas:
            # Call the method self.__poisson and assign the result to the variable (e.g. f)
            # Calculate MSE between normlized Poisson value (e.g. f) and non-zero values of bins. 
            # Append this to list of errors. Use the following approach for normalization:
            #   f*np.max(non_zero_count) / np.max(f) 

        lambda_opt = lambdas[np.argmin(e)] # optimal lambda
        # Find optimal Poisson curve (e.g. f_opt).
        # Normalize this.

        return lambda_opt, f_norm, k
```

To generate the input use the following expression:

```python
p_mean = 30
a = np.random.poisson(p_mean, size=100000) # generate the random process with Poisson distribution
count, bins, ignored = plt.hist(a, bins='fd', density=1)
plt.show()
```

After that run approximation:

``` python
lambd, f, k = FitPoisson().fit_poisson(count, bins)
```

And check your results:

```python
print('Mean: '+str(lambd))
count, bins, ignored = plt.hist(a, bins='fd', density=1)
plt.plot(k, f)
plt.hist(a, bins='fd', density=1)
plt.show()
```

Good luck!

### Hints

- Download [Anaconda](https://www.anaconda.com/) to work with Jupyter notebooks. 
- Or use online solutions (e.g. https://jupyter.org/try), but remember that they can interrupt the session (save your results periodically). 
