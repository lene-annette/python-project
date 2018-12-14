import numpy as np
import glob
from PIL import Image

forestFolderPath = '../training_images/forest'
forestImagePath = glob.glob(forestFolderPath + '/*.JPG') 
urbanFolderPath = '../training_images/urban'
urbanImagePath = glob.glob(urbanFolderPath + '/*.JPG') 


forest_array = np.array( [np.array(Image.open(img).convert('L'), 'f') for img in forestImagePath] )
urban_array = np.array( [np.array(Image.open(img).convert('L'), 'f') for img in urbanImagePath] )

forest_training = get_training_data(forest_array,urban_array)
forest_weights,_ = pla(forest_training)
urban_training = get_training_data(urban_array,forest_array)
urban_weights,_ = pla(urban_training)


def perceptron(input, weights):
  # This is the same as the dot product np.dot(i, w)
  dot_product = sum([i * w for i, w in zip(input, weights)])
  output = activate(dot_product)
  return output

def pla(training_data, no_iterations=10000, eta=0.01):
  # eta is the learning rate
  # initial_error
  error = np.random.random()
  dim = len(training_data[0][0])
  weights =  np.random.random(dim)
  weight_history = [np.copy(weights)]

  for i in range(no_iterations):
    inp_vec, expected_label = training_data[i % len(training_data)]
    perceptron_output = perceptron(inp_vec, weights)
    error = expected_label - perceptron_output
    weights += eta * error * inp_vec
    weight_history.append(np.copy(weights))        
    return weights, weight_history 

def activate(num):
  # turn a sum over 0 into 1, and below 0 into -1
  if num > 0:
     return 1
  return -1

def reshape(image):
  h, w, d = image.shape
  image_lst = image.reshape(h * w, d)
  image_arr = np.reshape(image_lst, h*w*3)
  return image_arr

def get_training_data(right_array,wrong_array):
  training_data_list = []
  for image in right_array:
    training_data_list.append((reshape(image),1))
  for image in wrong_array:
    training_data_list.append((reshape(image),-1))
  return training_data_list
