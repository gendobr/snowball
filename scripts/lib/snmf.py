import numpy
import random


def gradient_descent(wwcovar, p_max, parameters):
    """
    symmetric nonnegative matrix factorization
    projected gradient descent
    """
    # parameters['eta'] = 0.1
    # parameters['beta'] = 0.9
    # parameters['beta2'] = 1.001
    # parameters['maxError'] = 1e-10

    # 'maxIterations':1000
    if 'maxIterations' in parameters:
        max_iterations = int(parameters['maxIterations'])
    else:
        max_iterations = 200
    # ================= SNMF = BEGIN ===========================================
    # SNMF dimensions
    # print Pmax, len(wwcovarReduced)
    # return
    n_words = len(wwcovar)
    n_topics = p_max
    print('gradient_descent', n_words, n_topics)

    # ranges
    x1range = range(0, n_words)
    x2range = range(0, n_topics)

    if 'H' in parameters:
        h = parameters['H']
    else:
        h = __initial_random_values(n_words, n_topics)

    d1 = -1
    d2 = -1
    cnt = 1
    for iteration in range(0, max_iterations):

        diff = h.dot(h.T) - wwcovar
        # print diff

        grad = diff.dot(h)
        # print grad
        max_grad = 0
        for x1 in x1range:
            for x2 in x2range:
                if max_grad < abs(grad[x1][x2]):
                    max_grad = abs(grad[x1][x2])

        d = parameters['eta'] / max_grad
        # d=eta
        for x1 in x1range:
            for x2 in x2range:
                h[x1][x2] = h[x1][x2] - d * grad[x1][x2]
                if h[x1][x2] < 0:
                    h[x1][x2] = 0

        if d2 > d1:
            parameters['eta'] = parameters['eta'] * parameters['beta']
        else:
            parameters['eta'] = parameters['eta'] * parameters['beta2']
        # print H
        if d2 > d1:
            parameters['eta'] = parameters['eta'] * parameters['beta']
        else:
            parameters['eta'] = parameters['eta'] * parameters['beta2']

        error = numpy.linalg.norm(diff, ord='fro')
        d1 = d2
        d2 = error

        if cnt >= 10:
            print((iteration,  ' eta=', parameters['eta'], "error=", error, " sparsity=", sparsity(h)))
            cnt = 1
        else:
            cnt = cnt + 1

        if parameters['maxError'] > error:
            # if parameters['maxError'] > parameters['eta']:
            break

    print("error=", numpy.linalg.norm(h.dot(h.T) - wwcovar, ord='fro'))
    return h


def sparse_gradient_descent(wwcovar, p_max, parameters):
    """
    sparse symmetric nonnegative matrix factorization
    projected gradient descent
    :param wwcovar:
    :param p_max:
    :param parameters:
    :return:
    """
    # parameters['eta'] = 0.1
    # parameters['beta'] = 0.9
    # parameters['beta2'] = 1.001
    # parameters['maxError'] = 1e-10
    # parameters['lambda'] =

    # 'maxIterations':1000
    if 'maxIterations' in parameters:
        max_iterations = int(parameters['maxIterations'])
    else:
        max_iterations = 200
    # ================= SNMF = BEGIN ===========================================
    # SNMF dimensions
    # print Pmax, len(wwcovarReduced)
    # return
    n_words = len(wwcovar)
    n_topics = p_max
    print('sparse_gradient_descent', n_words, n_topics)

    # ranges
    words_range = range(0, n_words)
    topics_range = range(0, n_topics)

    if 'H' in parameters:
        h = parameters['H']
    else:
        h = __initial_random_values(n_words, n_topics)

    d1 = -1
    d2 = -1
    cnt = 1
    L = float(parameters['lambda'])

    avg_error = 0

    for iteration in range(0, max_iterations):

        diff = h.dot(h.T) - wwcovar
        # print diff

        grad = diff.dot(h)
        # print grad
        max_grad = 0
        for x1 in words_range:
            for x2 in topics_range:
                if max_grad < abs(grad[x1][x2]):
                    max_grad = abs(grad[x1][x2])

        if max_grad < parameters['maxError']:
            break

        d = parameters['eta'] / max_grad
        # d=eta
        for x1 in words_range:
            for x2 in topics_range:
                h[x1][x2] = h[x1][x2] - d * (grad[x1][x2]+L)
                if h[x1][x2] < 0:
                    h[x1][x2] = 0

        if d2 > d1:
            parameters['eta'] = parameters['eta'] * parameters['beta']
        else:
            parameters['eta'] = parameters['eta'] * parameters['beta2']

        error = numpy.linalg.norm(diff, ord='fro')
        d1 = d2
        d2 = error

        if cnt >= 10:
            print(iteration, ' eta=', parameters['eta'], "error=", error, " sparsity=", sparsity(h))
            cnt = 1
        else:
            cnt = cnt + 1

        if parameters['maxError'] > abs(error - avg_error):
            break

        avg_error = 0.9 * avg_error + 0.1 * error

    print("error=", numpy.linalg.norm(h.dot(h.T) - wwcovar, ord='fro'))

    return h


def sparse_multiplicative(wwcovar, p_max, parameters):
    """
    sparse symmetric nonnegative matrix factorization
    projected gradient descent
    :param wwcovar:
    :param p_max:
    :param parameters:
    :return:
    """
    # parameters['eta'] = 0.1
    # parameters['beta'] = 0.9
    # parameters['beta2'] = 1.001
    # parameters['maxError'] = 1e-10
    # parameters['lambda'] =

    # 'maxIterations':1000
    if 'maxIterations' in parameters:
        max_iterations = int(parameters['maxIterations'])
    else:
        max_iterations = 200
    # ================= SNMF = BEGIN ===========================================
    # SNMF dimensions
    # print Pmax, len(wwcovarReduced)
    # return

    n_words = len(wwcovar)
    n_topics = p_max
    print(('sparse_multiplicative', 'n_words', n_words, 'n_topics', n_topics))

    # ranges
    words_range = range(0, n_words)
    topics_range = range(0, n_topics)

    if 'H' in parameters:
        h = parameters['H']
    else:
        h = __initial_random_values(n_words, n_topics)

    d1 = -1
    d2 = -1
    cnt = 1
    L = float(parameters['lambda']) * 0.25

    avg_error = 0

    _factor = numpy.zeros((n_words, n_topics))

    for iteration in range(0, max_iterations):

        for i_word in words_range:
            for i_topic in topics_range:
                _denominator = 0.000001  # regularization constant
                for p in topics_range:
                    for j in words_range:
                        _denominator += h[i_word][p] * h[j][p] * h[j][i_topic]
                _numerator = L
                for j in words_range:
                    _numerator += wwcovar[i_word][j] * h[j][i_topic]

                _factor[i_word][i_topic] = _numerator / _denominator
                # print(('i_word', i_word, 'i_topic', i_topic, 'factor', _factor[i_word][i_topic]))

        for i_word in words_range:
            for i_topic in topics_range:
                h[i_word][i_topic] = h[i_word][i_topic] * _factor[i_word][i_topic]

        diff = h.dot(h.T) - wwcovar
        # print diff

        if d2 > d1:
            parameters['eta'] = parameters['eta'] * parameters['beta']
        else:
            parameters['eta'] = parameters['eta'] * parameters['beta2']

        error = numpy.linalg.norm(diff, ord='fro')
        d1 = d2
        d2 = error

        if cnt >= 50:
            print(iteration, ' eta=', parameters['eta'], "error=", error, " sparsity=", sparsity(h))
            cnt = 1
        else:
            cnt = cnt + 1

        if parameters['maxError'] > abs(error - avg_error):
            break

        avg_error = 0.9 * avg_error + 0.1 * error

    print("avg_error=", avg_error)

    return h


def __initial_random_values(n_words, n_topics):
    h = numpy.zeros((n_words, n_topics))
    initial_value = 1.0 / (n_words * n_topics)
    words_range = range(0, n_words)
    topics_range = range(0, n_topics)
    for i_word in words_range:
        for i_topic in topics_range:
            h[i_word][i_topic] = initial_value * (1 + 0.01 * random.random())
    return h


def sparsity(h):
    n1 = len(h)
    n2 = len(h[0])
    n = n1 * n2
    l2 = 0
    l1 = 0
    for x1 in range(0, n1):
        for x2 in range(0, n2):
            l1 = l1 + h[x1][x2]
            l2 = l2 + h[x1][x2] * h[x1][x2]

    return numpy.sqrt(n) / (numpy.sqrt(n) - 1) - 1.0 / (numpy.sqrt(n) - 1) * l1 / numpy.sqrt(l2)
