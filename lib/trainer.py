import cv2
import numpy as np
import os
from tqdm import tqdm

from lib.perceptron import perceptron
import lib.utils as utils

def compute_weights(no_iterations, eta):
    '''
    Computes the weights for all categories using a number of iterations and a training rate.
    This function uses helper functions to read the training images from file, reshape them and then 
    finally use the `pla` function to compute the weights to be used by the perceptrons.
    It also writes the weights into a Python module, which is imported and used in another library file.
    '''
    forest_files = os.listdir(os.path.join('training_images', 'forest64'))
    forest_images = [utils.reshape(image) for image in get_training_images(forest_files, 'forest64')]

    urban_files = os.listdir(os.path.join('training_images', 'urban64'))
    urban_images = [utils.reshape(image) for image in get_training_images(urban_files, 'urban64')]

    water_files = os.listdir(os.path.join('training_images', 'water64'))
    water_images = [utils.reshape(image) for image in get_training_images(water_files, 'water64')]

    forest_training = get_training_data(forest_images, urban_images + water_images)
    urban_training = get_training_data(urban_images, forest_images + water_images)
    water_training = get_training_data(water_images, forest_images + urban_images)

    print('\nCalculating weights...')

    print('\nCalculating the weights for forest...')
    forest_weights = pla(forest_training, no_iterations, eta)

    print('\nCalculating the weights for urban...')
    urban_weights = pla(urban_training, no_iterations, eta)

    print('\nCalculating the weights for water...')
    water_weights = pla(water_training, no_iterations, eta)

    # Export the weights to a Python module.
    export_weights(forest_weights, urban_weights, water_weights, no_iterations, eta)

def get_training_images(image_list, folder):
    '''Returns all training images from a file name list and appends it to a list.'''
    images = []
    for filename in image_list:
        path = os.path.join('training_images', folder, filename)
        image = utils.read(path)
        images.append(image)
    return images

def get_training_data(right_array, wrong_array):
    '''
    Adds labels to the training data images depending on how the trainer should perceive them.
    It uses 1 for images to be considered correct and -1 for the opposite.
    '''
    training_data_list = []
    for image in right_array:
        training_data_list.append((image, 1))
    for image in wrong_array:
        training_data_list.append((image, -1))
    return training_data_list

def pla(training_data, no_iterations, eta):
    '''
    The training algorithm of the perceptron. It takes the following arguments:

        - training_data: An array of tuples, where the tuples 
                         are the image data and a label which 
                         indicates whether the image should be 
                         considered as 'right' or 'wrong' 
                         when used in training.

        - no_iterations: The number of times the training 
                         algorithm should pick an image from the 
                         training data and learn from it.
                         Note: A larger iterations number is 
                         preferred to a lower.

        - eta: The learning/training rate. 
               Note: A low value produces the most precise weights.

    Returns the computed weights for a given training data.
    '''
    # Initial_error.
    error = np.random.random()
    dim = len(training_data[0][0])
    # An array of random values between 0 and 1 is made to be used as
    # starting weights before the learning algorithm begins.
    weights =  np.random.random(dim)
    for i in tqdm(range(no_iterations)):
        inp_vec, expected_label = training_data[i % len(training_data)]
        perceptron_output = perceptron(inp_vec, weights)
        # Error is 0 if the perceptron predicts correctly and either -2 or 2 if it predicts wrongly.
        error = expected_label - perceptron_output
        # If an error is different from 0, the weights will be adjusted.
        weights += eta * error * inp_vec          
    return weights 

def export_weights(forest_weights, urban_weights, water_weights, no_iterations, eta):
    '''
    Exports the weights for all categories as well as the values of 
    iterations and training rate into one single Python module.
    '''
    try:
        print('\nCalculations finished successfully!')
        print('Exporting weights to module...')

        print('\nExporting the weights for forest to module...')
        forest_str = make_result(forest_weights)

        print('\nExporting the weights for urban to module...')
        urban_str = make_result(urban_weights)

        print('\nExporting the weights for water to module...')
        water_str = make_result(water_weights)

        module_txt = 'forest_weights = {} \nurban_weights = {} \nwater_weights = {} \niterations = {} \neta = {}'.format(forest_str, urban_str, water_str, no_iterations, eta)

        module_dir = 'modules'
        if not os.path.isdir(module_dir):
            os.makedirs(module_dir)
        with open(os.path.join(module_dir, 'weights.py'), 'w' ) as fp:
            fp.write(module_txt)
        print('\nWeight module created successfully!')  
    except Exception as _:
        print('\nWeight module failed to save!')

def make_result(weights):
    '''Turns the weights array into a string that can be written into a module file.'''
    result = '[ '
    for weight in tqdm(weights):
        result += str(weight) + ', '
    result += ' ]'
    return result
