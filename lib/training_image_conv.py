import scipy.spatial as sp
import numpy as np
import os
import cv2
import glob
from PIL import Image

# A function to read an image from file.
def read(path, switch_channels=True):
    image = cv2.imread(path)
    if switch_channels:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

# We use RGB colors to train our perceptrons, but only 64 colors.
# We have chosen to look at RGB colors from the RGB cube 
# made from the values 255x255x255
# This function finds 64 colors by choosing the middle values in 
# each of the 64 small cubes in the RGB color cube.
# The first color will be [32,32,32], the next [96,32,32] and so on..
def _colors64():
    colors = []
    for b in range(4):
        for g in range(4):
            for r in range(4):
                colors.append([32+r*64,32+g*64,32+b*64])
    return colors

_color_list = _colors64()

# This will create a color tree using an scipy.spatial function
def create_tree(colors):
    # Creating kd-tree from C64 colors
    tree = sp.cKDTree(colors)  
    return tree

# This function will go through all the pixel in the picture and replace the color
# for the specific pixel with the color with the nearest color in the color tree.
def query_tree(small_image, tree):
    h, w, d = small_image.shape
    small_image_lst = small_image.reshape(h * w, d)
    # Get Euclidean distance and index of each C64 color in tree
    _, result = tree.query(small_image_lst)      
    for idx, c in enumerate(_color_list):
        small_image_lst[result == idx] = c
    return small_image_lst.reshape(h, w, d)

# A function to resize an image into a fixed size.
def resize(image, new_x_dim, new_y_dim):
    resized_image = cv2.resize(image, (new_x_dim, new_y_dim), interpolation=cv2.INTER_AREA)
    return resized_image
    
# Finds all filenames in a directory and adds them to an array.
def createImageList(cat):
    imageList = os.listdir('../training_images/'+cat)
    return imageList


# Function that takes an imagelist and a category directory name and 
# converts all imagesin the imagelist into a fixed size and with only 
# 64 predefined colors.
# Finally it writes the converted images into the directory specified.
def convert_image(imagelist, cat):

    if not os.path.isdir('../training_images/'+cat+'64'):
        os.makedirs('../training_images/'+cat+'64')

    tree = create_tree(_color_list)

    for filename in imagelist:
        image_location = '../training_images/'+cat+'/'+filename
        image = read(image_location)
        # Resize to a fixed size of 400x300.
        image = resize(image, 400, 300)
        new_image = query_tree(image, tree)
        new_file_location = '../training_images/'+cat+'/'+filename   
        cv2.imwrite(new_file_location, cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR))



category = 'forest'
convert_image(createImageList(category), category)    
