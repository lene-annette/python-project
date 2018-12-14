# from scipy.spatial import distance
# from tqdm import tqdm
import scipy.spatial as sp
import numpy as np
import os
import cv2

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

    if not os.path.isdir("./images_64/"):
        os.makedirs("./images_64/")

    tree = create_tree(_color_list)

    for filename in imagelist:

        image_location = './images/'+filename
        image = read(image_location)

        # Resize to a fixed size of 400x300.
        image = resize(image, 400, 300)

        # new_image = to_c64_colors(image)
        new_image = query_tree(image, tree)
        
        new_file_location = './images_64/'+filename
    
        cv2.imwrite(new_file_location, cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR))

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

   

