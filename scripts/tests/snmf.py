from lib.snmf import sparse_multiplicative, gradient_descent, sparse_gradient_descent
import time
import fire
import numpy
import configparser
import json


def main():
    # h0 = numpy.array([[0.25, 0.05], [0.4, 0.3]])
    h0 = numpy.array([[0.15, 0.05], [0.4, 0.2], [0.1, 0.1]])
    wwcovar = h0.dot(h0.T)
    p_max = 3
    params = {
            'maxIterations': 4000,
            'lambda': 0.00001,
            'eta': 0.1,
            'beta': 0.99,
            'beta2': 1.000,
            'maxError': 1e-7,
        }

    print('gradient_descent')
    h = gradient_descent(wwcovar, p_max,  params )
    print('h0=')
    print(h0)
    print('')
    print('original=')
    print(wwcovar)
    print('')
    print('restored=')
    print(h.dot(h.T))
    print('')
    print('h=')
    print(h)
    print('')
    print('diff=')
    print(h.dot(h.T) - wwcovar)

    params['H'] = h
    print('sparse_multiplicative')
    h = sparse_multiplicative(wwcovar, p_max,  params )
    print('h0=')
    print(h0)
    print('')
    print('original=')
    print(wwcovar)
    print('')
    print('restored=')
    print(h.dot(h.T))
    print('')
    print('h=')
    print(h)
    print('')
    print('diff=')
    print(h.dot(h.T) - wwcovar)

    params['H'] = h
    print('sparse_gradient_descent')
    h = sparse_gradient_descent(wwcovar, p_max, params)
    print('h0=')
    print(h0)
    print('')
    print('original=')
    print(wwcovar)
    print('')
    print('restored=')
    print(h.dot(h.T))
    print('')
    print('h=')
    print(h)
    print('')
    print('diff=')
    print(h.dot(h.T) - wwcovar)


if __name__ == "__main__":
    t0 = time.time()
    fire.Fire(main)
    t1 = time.time()
    print("finished")
    print(("time", t1 - t0, ))
