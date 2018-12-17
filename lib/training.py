import numpy as np
import cv2
import os
from tqdm import tqdm

# This is the function that determines which output the perceptron is producing
def activate(num):
  # Turn a sum over 0 into 1, and below 0 into -1
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

# This is the perceptron training algoritme
# no_iteration is the number of times the training algoritm should
# should pick an image from the training data and learn from it
# A high number of iteration is prefered
# eta is the learning rate and should be low in order to get the most precise weights
def pla(training_data, no_iterations=10000, eta=0.5):  
  # Initial_error
  error = np.random.random()
  dim = len(training_data[0][0])
  # An array of random values between 0 and 1 is made to be used as starting weights
  # before the learning algoritm begins
  weights =  np.random.random(dim)
  for i in tqdm(range(no_iterations)):
    inp_vec, expected_label = training_data[i % len(training_data)]
    perceptron_output = perceptron(inp_vec, weights)
    # Error is 0 if the perceptron predicts correct and either -2 or 2 if it predicts wrongly
    error = expected_label - perceptron_output
    # If an error is different from 0 the weights will be adjusted.
    weights += eta * error * inp_vec          
  return weights 

# This function reshapes the images into one dimensional arrays to be used for training
# It will return an array with the RGB values represented on a continuous basis:
# [r,g,b,r,g,b,...,r,g,b]  
def reshape(image):
  h, w, d = image.shape
  image_lst = image.reshape(h * w, d)
  image_arr = np.reshape(image_lst, h*w*3)
  return image_arr

# This function adds labels to the training data images
# depending on how the trainer should perceive them.
# It uses 1 for images to be considered correct and -1 for the opposite 
def get_training_data(right_array,wrong_array):
  training_data_list = []
  for image in right_array:
    training_data_list.append((image,1))
  for image in wrong_array:
    training_data_list.append((image,-1))
  return training_data_list

# A function to read an image from file.
def read(path, switch_channels=True):
    image = cv2.imread(path)
    if switch_channels:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

# This function makes a list with filenames of all files in a specific directory
def createFilenameList(path):
    imageList = os.listdir('./training_images/'+path)
    return imageList  

# This function reads all images from a filename list and appends it to an array.
def getImages(imageList, folder):
  images = []
  for filename in imageList:
    path = './training_images/'+folder+'/'+filename
    image = read(path)
    images.append(image)
  return images

# This method is used when writing weights into the module file.
# It turns the weights array into a string that can be written into a file
def make_result(weights):
  result = "[ "
  for weight in tqdm(weights):
    result += str(weight)+", "
  result += " ]"
  return result

# This function will use helping functions to read the training images from file
# and reshape them and then finally use the pla function to calculate the weigths
# to be used be the perceptrons.
# It will also write the weights into the python weights module to be imported in 
# another library file. 
def find_weights(no_iterations, eta):
  print('Calculating weights..')
  print('Iterations: '+str(no_iterations))
  print('Learning rate: '+str(eta))
  forest_files = createFilenameList('forest64')
  forest_images = [reshape(image) for image in getImages(forest_files,'forest64')]

  urban_files = createFilenameList('urban64')
  urban_images = [reshape(image) for image in getImages(urban_files,'urban64')]

  water_files = createFilenameList('water64')
  water_images = [reshape(image) for image in getImages(water_files,'water64')]

  forest_training = get_training_data(forest_images, urban_images + water_images)
  urban_training = get_training_data(urban_images, forest_images + water_images)
  water_training = get_training_data(water_images, forest_images + urban_images)

  forest_weights = pla(forest_training, no_iterations, eta)
  urban_weights = pla(urban_training, no_iterations, eta)
  water_weights = pla(water_training, no_iterations, eta)

  try:
    print('Exporting weights to module..')
    forest_str = make_result(forest_weights)
    urban_str = make_result(urban_weights)
    water_str = make_result(water_weights)
    module_txt = 'forest_weights = {} \nurban_weights = {} \nwater_weights = {} \niterations = {} \neta = {}'.format(forest_str, urban_str, water_str, no_iterations, eta)   
    module_dir = './modules'
    if not os.path.isdir(module_dir):
      os.makedirs(module_dir)
    with open(os.path.join(module_dir, 'weights.py'), "w" ) as fp:
      fp.write(module_txt)
    print('Weight module created successfully.')  
  except Exception as _:
    print('Python module save failure!')  
  




