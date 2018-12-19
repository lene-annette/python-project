import numpy as np

def perceptron(input, weights):
    ''' 
    Sum up all the products of weight values and color values.
    It then uses the activate function to return either 1 or -1 according
    to if the dot product is positive or negative. It takes the following arguments:

        - input: An array of RGB color data.
        - weights: An array with the weights that corresponds to the category that is tested for.
    '''
    dot_product = np.dot(input, weights)
    # The following line does the same as the above line, however it is slower:
    # dot_product = sum([i * w for i, w in zip(input, weights)])
    output = activate(dot_product)
    return output

def activate(num):
    '''Determine the output that the perceptron produces.'''
    # Turn a sum over 0 into 1, and below 0 into -1.
    if num > 0:
        return 1
    return -1
