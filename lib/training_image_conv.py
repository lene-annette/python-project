import scipy.spatial as sp
import numpy as np
import os
import cv2
import glob
from PIL import Image

def read(path, switch_channels=True):
    image = cv2.imread(path)
    if switch_channels:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image


def _colors64():
    colors = []
    for b in range(4):
        for g in range(4):
            for r in range(4):
                colors.append([32+r*64,32+g*64,32+b*64])
    return colors

_color_list = _colors64()

def create_tree(colors):
    # pylint: disable=not-callable
    tree = sp.cKDTree(colors)  # creating kd-tree from C64 colors
    return tree


def query_tree(small_image, tree):
    h, w, d = small_image.shape
    small_image_lst = small_image.reshape(h * w, d)
    _, result = tree.query(small_image_lst)  # get Euclidean distance and index of each C64 color in tree

    for idx, c in enumerate(_color_list):
        small_image_lst[result == idx] = c
    return small_image_lst.reshape(h, w, d)

def convert_image(imagelist):

    if not os.path.isdir("../training_images/water64"):
        os.makedirs("../training_images/water64")

    tree = create_tree(_color_list)

    for filename in imagelist:

        image_location = '../training_images/water/'+filename
        image = read(image_location)
        # Resize to a fixed size of 400x300.
        image = resize(image, 400, 300)
        # new_image = to_c64_colors(image)
        new_image = query_tree(image, tree)

        new_file_location = '../training_images/water64/'+filename
    
        cv2.imwrite(new_file_location, cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR))

def resize(image, new_x_dim, new_y_dim):
    resized_image = cv2.resize(image, (new_x_dim, new_y_dim), interpolation=cv2.INTER_AREA)
    return resized_image

def createImageList():
    imageList = os.listdir('../training_images/water')
    return imageList

convert_image(createImageList())    
