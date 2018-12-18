import cv2
import numpy as np
import os
import scipy.spatial as sp
from tqdm import tqdm

from lib.define_colors64 import color_list as colors64
from modules.weights import forest_weights, urban_weights, water_weights

def categorize_image(image_list):
    '''
    Runs through a list of images and determines which 
    category an image is predicted to belong to.
    '''
    if not os.path.isdir('./categorized/'):
        os.makedirs('./categorized/')

    # Create the color tree to be used when converting images into 64 colors.
    tree = create_tree(colors64)

    print('Determining the category for each image...')
    for filename in tqdm(image_list):
        categories_found = 0

        image_location = './images/' + filename
        image = read(image_location)

        # Resize image to a fixed size of 400x300.
        resized_image = resize(image, 400, 300)

        # Converting image into 64 colors.
        new_image = query_tree(resized_image, tree)
        
        # Reshaping image to be used in the perceptrons.
        test_image = reshape(new_image)

        categories_found += predict(image, filename, 'forest', test_image, forest_weights)
        categories_found += predict(image, filename, 'urban', test_image, urban_weights)
        categories_found += predict(image, filename, 'water', test_image, water_weights)

        # This will check if any matching category has been found for the image.
        # Otherwise, the image will be saved in a folder called 'others'.
        if (categories_found == 0):
            if not os.path.isdir('./categorized/others'):
                os.makedirs('./categorized/others')
            
            new_file_location = './categorized/others/' + filename
            cv2.imwrite(new_file_location, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    print('All images saved in the "categorized" folder!')

def create_tree(colors):
    '''Creates a color tree (cKDTree).'''
    # Creating kd-tree from C64 colors.
    tree = sp.cKDTree(colors) # pylint: disable=not-callable
    return tree

def read(path, switch_channels=True):
    '''Reads an image from file.'''
    image = cv2.imread(path)
    if switch_channels:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def resize(image, new_x_dim, new_y_dim):
    '''Resizes an image into a fixed size.'''
    resized_image = cv2.resize(image, (new_x_dim, new_y_dim), interpolation=cv2.INTER_AREA)
    return resized_image

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

def reshape(image):
    '''
    Reshapes the image into one dimensional array to be used for training.
    It will return an array with the RGB values represented on a continuous basis:
    [r,g,b,r,g,b,...,r,g,b]
    '''
    h, w, d = image.shape
    image_lst = image.reshape(h * w, d)
    image_arr = np.reshape(image_lst, h * w * 3)
    return image_arr

def predict(original_image, filename, save_path, test_image, weights):
    ''' 
    Given a test_image that has been resized, turn into 64 colors and where 
    the array with rgb values has been reshaped to fit the perceptron and given
    the weight corresponding to a certain category, this function will predict 
    if the image belongs to this category using the perceptron function.
    If the perceptron predicts that the image belongs to the category, the original
    image is save into the category folder.
     
        - original_image: An array containing the original image.
        - filename: The filename for the image to be stored.
        - save_path: The folder name for the category folder.
        - test_image: An array with the data in a format suitable
                      for the perceptron.
        - weights: An array with the weights for the category.

    Returns 1 if the image is predicted to belong to the category 
    and saved into the category folder and 0 if not.
    '''
    prediction = perceptron(test_image, weights)
    if (prediction == 1):       
        if not os.path.isdir('./categorized/' + save_path):
            os.makedirs('./categorized/' + save_path)
        new_file_location = './categorized/' + save_path + '/' + filename
        cv2.imwrite(new_file_location, cv2.cvtColor(original_image, cv2.COLOR_RGB2BGR))
        return 1
    return 0

def perceptron(input, weights):
    ''' 
    Sums up all the products of weight values and color values.
    Then uses the activate function to return either 1 or -1 according
    to if the dot product is positive or negative.
    
        - input: An array of RGB color data.
        - weights: An array with the weights that corresponds to 
                   the category that is tested for.
    '''
    dot_product = np.dot(input, weights)
    # The following line does the same as the above line, however it is slower:
    # dot_product = sum([i * w for i, w in zip(input, weights)])
    output = activate(dot_product)
    return output

def activate(num):
    '''Determines the output that the perceptron produces.'''
    # Turn a sum over 0 into 1, and below 0 into -1.
    if num > 0:
        return 1
    return -1
