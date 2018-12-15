from tqdm import tqdm
import scipy.spatial as sp
import numpy as np
import os
import cv2
from modules.weights import forest_weights,urban_weights,water_weights

def activate(num):
  # turn a sum over 0 into 1, and below 0 into -1
  if num > 0:
     return 1
  return -1

def perceptron(input, weights):
  # This is the same as the dot product np.dot(i, w)
  dot_product = np.dot(input, weights)
  # dot_product = sum([i * w for i, w in zip(input, weights)])
  output = activate(dot_product)
  return output

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

def reshape(image):
  h, w, d = image.shape
  image_lst = image.reshape(h * w, d)
  image_arr = np.reshape(image_lst, h*w*3)
  return image_arr

def predict(test_image, weights, image, filename, save_path):
    prediction = perceptron(test_image, weights)
    if (prediction == 1):       
        if not os.path.isdir("./categorized/"+save_path):
            os.makedirs("./categorized/"+save_path)
        new_file_location = './categorized/'+save_path+'/'+filename
        cv2.imwrite(new_file_location, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
        return 1
    return 0
def categorize_image(imagelist):

    if not os.path.isdir("./categorized/"):
        os.makedirs("./categorized/")

    tree = create_tree(_color_list)

    print('Finding matching categories and saving pictures in category folders.. ')

    for filename in tqdm(imagelist):

        categories_found = 0

        image_location = './images/'+filename
        image = read(image_location)

        # Resize to a fixed size of 400x300.
        resized_image = resize(image, 400, 300)

        # new_image = to_c64_colors(image)
        new_image = query_tree(resized_image, tree)
        
        test_image = reshape(new_image)

        categories_found += predict(test_image, forest_weights, image, filename, 'forest')
        categories_found += predict(test_image, urban_weights, image, filename, 'urban')
        categories_found += predict(test_image, water_weights, image, filename, 'water')

        if (categories_found == 0):       
            if not os.path.isdir("./categorized/others"):
             os.makedirs("./categorized/others")
            new_file_location = './categorized/others/'+filename
            cv2.imwrite(new_file_location, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

    print('Categorization finished.')    

def resize(image, new_x_dim, new_y_dim):
    resized_image = cv2.resize(image, (new_x_dim, new_y_dim), interpolation=cv2.INTER_AREA)
    return resized_image







# DEN LANGSOMME MÅDE AT FINDE NÆRMESTE FARVE
#  
# def _get_closest_64_color(value):
#     dst = 200000
#     for color in _color_list:
#         new_dst = distance.euclidean(color, value)
#         if new_dst < dst:
#             dst = new_dst
#             return_color = color
#     return return_color

# def to_c64_colors(image):

#     c64_img = np.copy(image)
#     h, w, _ = c64_img.shape
    
#     for x in tqdm(range(w)):
#         for y in range(h):
#             c64_img[y, x] = _get_closest_64_color(c64_img[y, x])
#     return c64_img

   

