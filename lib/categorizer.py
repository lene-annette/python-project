import cv2
import numpy as np
import os
import scipy.spatial as sp
from tqdm import tqdm

from lib.colors64 import color_list as colors64
from modules.weights import forest_weights, urban_weights, water_weights
from lib.perceptron import perceptron
import lib.utils as utils

def categorize_image(image_list):
    '''
    Runs through a list of images and determines which 
    category an image is predicted to belong to.
    '''
    dir_path = 'categorized'
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)

    # Create the color tree to be used when converting images into 64 colors.
    tree = create_tree(colors64)

    print('Determining the category for each image...')
    for filename in tqdm(image_list):
        categories_found = 0

        image_location = os.path.join('images', filename)
        image = utils.read(image_location)

        # Resize image to a fixed size of 400x300.
        resized_image = utils.resize(image, 400, 300)

        # Converting image into 64 colors.
        new_image = query_tree(resized_image, tree)
        
        # Reshaping image to be used in the perceptrons.
        test_image = utils.reshape(new_image)

        categories_found += predict(image, filename, 'forest', test_image, forest_weights)
        categories_found += predict(image, filename, 'urban', test_image, urban_weights)
        categories_found += predict(image, filename, 'water', test_image, water_weights)

        # This will check if any matching category has been found for the image.
        # Otherwise, the image will be saved in a folder called 'others'.
        if (categories_found == 0):
            new_dir_path = os.path.join(dir_path, 'others') 
            if not os.path.isdir(new_dir_path):
                os.makedirs(new_dir_path)
            
            new_file_location = os.path.join(new_dir_path, filename)
            cv2.imwrite(new_file_location, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    print('All images saved in the "categorized" folder!')

def create_tree(colors):
    '''Creates a color tree (cKDTree).'''
    # Creating a cKDTree from C64 colors.
    tree = sp.cKDTree(colors) # pylint: disable=not-callable
    return tree

def query_tree(small_image, tree):
    '''
    Runs through all the pixels in an image and replaces the color
    for the specific pixel with the color that is closest 
    to its resembling 64 color in the color tree.
    '''
    h, w, d = small_image.shape
    small_image_list = small_image.reshape(h * w, d)
    # Get the Euclidean distance and index of each C64 color in the tree.
    _, result = tree.query(small_image_list)

    for idx, c in enumerate(colors64):
        small_image_list[result == idx] = c
    return small_image_list.reshape(h, w, d)

def predict(original_image, filename, save_path, test_image, weights):
    ''' 
    Given a test_image that has been resized, turn it into 64 colors where 
    the array with the rgb values has been reshaped to fit the perceptron. 
    Given the weight corresponding to a certain category, this function will predict 
    whether the image belongs to the category using the perceptron function.
    If the perceptron predicts that the image belongs to the category, the original
    image is saved into its specific category folder. It takes the following arguments:

        - original_image: An array containing the original image.
        - filename: The filename for the image to be stored.
        - save_path: The folder name for the category folder.
        - test_image: An array with the data in a format suitable for the perceptron.
        - weights: An array with the weights for the category.

    If the image is predicted to belong to the given category, it will save
    the image into the category folder and return 1. If not, it will return 0.
    '''
    prediction = perceptron(test_image, weights)
    if (prediction == 1):
        dir_path = os.path.join('categorized', save_path)
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        new_file_location = os.path.join(dir_path, filename)
        cv2.imwrite(new_file_location, cv2.cvtColor(original_image, cv2.COLOR_RGB2BGR))
        return 1
    return 0
