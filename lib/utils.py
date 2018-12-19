import cv2
import numpy as np

def read(path, switch_channels=True):
    '''Reads an image from file.'''
    image = cv2.imread(path)
    if switch_channels:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def reshape(image):
    '''
    Reshapes the image into one dimensional array to be used for training.
    It will return an array with the RGB values represented on a continuous basis:
    [r,g,b,r,g,b,...,r,g,b]
    '''
    h, w, d = image.shape
    image_list = image.reshape(h * w, d)
    image_arr = np.reshape(image_list, h * w * 3)
    return image_arr

def resize(image, new_x_dim, new_y_dim):
    '''Resizes an image into a fixed size.'''
    resized_image = cv2.resize(image, (new_x_dim, new_y_dim), interpolation=cv2.INTER_AREA)
    return resized_image
