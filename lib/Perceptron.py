import numpy as np
import cv2
import os


def perceptron(input, weights):
  # This is the same as the dot product np.dot(i, w)
  dot_product = np.dot(input, weights)
  # dot_product = sum([i * w for i, w in zip(input, weights)])
  output = activate(dot_product)
  return output

def pla(training_data, no_iterations=1000, eta=0.5):
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
    training_data_list.append((image,1))
  for image in wrong_array:
    training_data_list.append((image,-1))
  return training_data_list



def read(path, switch_channels=True):
    image = cv2.imread(path)
    if switch_channels:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def createFilenameList(path):
    imageList = os.listdir('../training_images/'+path)
    return imageList  

def getImages(imageList, folder):
  images = []
  for filename in imageList:
    path = '../training_images/'+folder+'/'+filename
    image = read(path)
    images.append(image)
  return images


forest_files = createFilenameList('forest64')
forest_images = [reshape(image) for image in getImages(forest_files,'forest64')]
forest_training = get_training_data(forest_images,urban_images)
forest_weights,_ = pla(forest_training)

urban_files = createFilenameList('urban')
urban_images = [reshape(image) for image in getImages(urban_files,'urban64')]
urban_training = get_training_data(urban_images,forest_images)
urban_weights,_ = pla(urban_training)

# water_files = createFilenameList('urban')
# water_images = [reshape(image) for image in getImages(urban_files,'urban64')]
# water_training = get_training_data(urban_images,forest_images)
# water_weights,_ = pla(urban_training)


print(forest_weights)
print(perceptron(forest_images[1], forest_weights))
print(perceptron(urban_images[0], forest_weights))


# np.concatenate(a,b)