import numpy as np
import glob
from PIL import Image

imageFolderPath = '../training_images'
imagePath = glob.glob(imageFolderPath + '/*.JPG') 

im_array = np.array( [np.array(Image.open(img).convert('L'), 'f') for img in imagePath] )

forrest_images = get_image_array(im_array)
forrest_weights = pla(forrest_images)

def perceptron_forrest(input, weights):
  # This is the same as the dot product np.dot(i, w)
  dot_product = sum([i * w for i, w in zip(input, weights)])
  output = activate(dot_product)
  return output


def predict(inp_vec, weights):
  """
  inp_vec:
  An input vector consisting of sepal length and width
  return:
  A class label, either 1 for 'setosa' or -1 for 'other'
  """
  class_label = perceptron_forrest(inp_vec, weights)
  return class_label

def pla(training_data, no_iterations=10000, eta=0.01):
  # eta is the learning rate
  # initial_error
  error = np.random.random()
  dim = len(training_data[0][0])
  weights =  np.random.random(dim)
  weight_history = [np.copy(weights)]

  for i in range(no_iterations):
    inp_vec, expected_label = training_data[i % len(training_data)]
    perceptron_output = perceptron_forrest(inp_vec, weights)
    error = expected_label - perceptron_output
    # print(error)
    weights += eta * error * inp_vec
    weight_history.append(np.copy(weights))
        
    return weights, weight_history 

def activate(num):
  # turn a sum over 0 into 1, and below 0 into -1
  if num > 0:
     return 1
  return -1
    
def get_image_array(img_array):
  training_data_list = []
  for image in img_array:
    h, w, d = image.shape
    small_image_lst = image.reshape(h * w, d)
    training_data_list.append(small_image_lst)
  return training_data_list
