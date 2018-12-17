from tqdm import tqdm
import scipy.spatial as sp
import numpy as np
import os
import cv2
from modules.weights import forest_weights,urban_weights,water_weights

# This is the function that determines which output the perceptron is producing
def activate(num):
  # turn a sum over 0 into 1, and below 0 into -1
  if num > 0:
     return 1
  return -1

def perceptron(input, weights):
  dot_product = np.dot(input, weights)
  # Dot_product = sum([i * w for i, w in zip(input, weights)])
  # This is the same as the dot product np.dot(i, w)
  # But slower..
  output = activate(dot_product)
  return output

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
    _, result = tree.query(small_image_lst)  # get Euclidean distance and index of each C64 color in tree

    for idx, c in enumerate(_color_list):
        small_image_lst[result == idx] = c
    return small_image_lst.reshape(h, w, d)

# This function reshapes the images into one dimensional arrays to be used for training
# It will return an array with the RGB values represented on a continuous basis:
# [r,g,b,r,g,b,...,r,g,b] 
def reshape(image):
  h, w, d = image.shape
  image_lst = image.reshape(h * w, d)
  image_arr = np.reshape(image_lst, h*w*3)
  return image_arr

# A function to resize an image into a fixed size.
def resize(image, new_x_dim, new_y_dim):
    resized_image = cv2.resize(image, (new_x_dim, new_y_dim), interpolation=cv2.INTER_AREA)
    return resized_image

# This function will predict if the image is in a certain category
# It will use an test image that has been resized and turn into 64 colors
# If the prediction is 'true' it will save the original picture in the 
# category folder.
def predict(test_image, weights, image, filename, save_path):
    prediction = perceptron(test_image, weights)
    if (prediction == 1):       
        if not os.path.isdir("./categorized/"+save_path):
            os.makedirs("./categorized/"+save_path)
        new_file_location = './categorized/'+save_path+'/'+filename
        cv2.imwrite(new_file_location, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
        return 1
    return 0

# This function runs though a list of images and determines which categories
# the images is predicted to belong to.
def categorize_image(imagelist):

    if not os.path.isdir("./categorized/"):
        os.makedirs("./categorized/")

    # Creates the color tree to be used when converting images into 64 colors.
    tree = create_tree(_color_list)

    print('Finding matching categories and saving pictures in category folders.. ')

    for filename in tqdm(imagelist):

        categories_found = 0

        image_location = './images/'+filename
        image = read(image_location)

        # Resize to a fixed size of 400x300.
        resized_image = resize(image, 400, 300)

        # Converting image into 64 colors
        new_image = query_tree(resized_image, tree)
        
        # Reshaping image to be used in the perceptrons
        test_image = reshape(new_image)

        categories_found += predict(test_image, forest_weights, image, filename, 'forest')
        categories_found += predict(test_image, urban_weights, image, filename, 'urban')
        categories_found += predict(test_image, water_weights, image, filename, 'water')

        # This will check if any matching categories has been found
        # Elseway the image will be saved in a folder called 'others'
        if (categories_found == 0):       
            if not os.path.isdir("./categorized/others"):
             os.makedirs("./categorized/others")
            new_file_location = './categorized/others/'+filename
            cv2.imwrite(new_file_location, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
