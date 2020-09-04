#!/usr/bin/env python2
# encoding: UTF-8


import numpy


# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

# The Jensen–Shannon divergence (JSD) M + 1 ( A ) × M + 1 ( A ) → [ 0 , ∞ ) {\displaystyle M_{+}^{1}(A)\times M_{+}^{1}(A)\rightarrow [0,\infty {})} M_{+}^{1}(A)\times M_{+}^{1}(A)\rightarrow [0,\infty {}) is a symmetrized and smoothed version of the Kullback–Leibler divergence D ( P ∥ Q ) {\displaystyle D(P\parallel Q)} D(P\parallel Q). It is defined by
# J S D ( P ∥ Q ) = 1 2 D ( P ∥ M ) + 1 2 D ( Q ∥ M ) {\displaystyle {\rm {JSD}}(P\parallel Q)={\frac {1}{2}}D(P\parallel M)+{\frac {1}{2}}D(Q\parallel M)} {{\rm {JSD}}}(P\parallel Q)={\frac {1}{2}}D(P\parallel M)+{\frac {1}{2}}D(Q\parallel M)
# where M = 1 2 ( P + Q ) {\displaystyle M={\frac {1}{2}}(P+Q)} M={\frac {1}{2}}(P+Q)
def js_divergence(v1, v2):
    # symmetric KL - divergence
    v0 = [0.5 * (v1[i] + v2[i]) for i in range(0, len(v1))]
    s = 0
    for i in range(0, len(v1)):
        s = s + (v1[i] + 0.000000000001) * numpy.log((v1[i] + 0.000001) / (v0[i] + 0.000001))
        # abs(v1[i]-v2[i])
    for i in range(0, len(v1)):
        s = s + (v2[i] + 0.000000000001) * numpy.log((v2[i] + 0.000001) / (v0[i] + 0.000001))
    return s * 0.5


# simple KL - divergence
def kl_divergence(v1, v2):
    s = 0
    for i in range(0, len(v1)):
        s = s + (v1[i] + 0.000000000001) * numpy.log((v1[i] + 0.000001) / (v2[i] + 0.000001))
    return s


# symmetric KL - divergence
def skl_divergence(v1, v2):
    s = 0
    for i in range(0, len(v1)):
        s = s + (v1[i] + 0.000000000001) * numpy.log((v1[i] + 0.000001) / (v2[i] + 0.000001))
        # abs(v1[i]-v2[i])
    for i in range(0, len(v1)):
        s = s + (v2[i] + 0.000000000001) * numpy.log((v2[i] + 0.000001) / (v1[i] + 0.000001))
    return s * 0.5


# S2JSD measure
# https://pdfs.semanticscholar.org/77b1/9a491e14697bd87e56b0bd7fa1d6c8e9f857.pdf
def s2jsd_divergence(v1, v2):
    s = 0
    for i in range(0, len(v1)):
        s = s + (v1[i] + 0.000001) * numpy.log(2 * (v1[i] + 0.000001) / (v1[i] + v2[i] + 0.000002))

    for i in range(0, len(v1)):
        s = s + (v2[i] + 0.000001) * numpy.log(2 * (v2[i] + 0.000001) / (v1[i] + v2[i] + 0.000002))
    return numpy.sqrt(s)


# https://en.wikipedia.org/wiki/Hellinger_distance
def hellinger_distance(v1, v2):
    s = 0
    for i in range(0, len(v1)):
        d = numpy.sqrt(v1[i]) - numpy.sqrt(v2[i])
        s = s + d * d
    return numpy.sqrt(0.5 * s)
