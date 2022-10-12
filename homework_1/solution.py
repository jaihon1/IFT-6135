# -*- coding: utf-8 -*-
"""hw1_solution.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1M7bj67fOJENbPFk8nepM3vYWp9OomJlq

# IFT6135-A2022
# Assignment 1: Practical

You must fill in your answers to various questions in this notebook, following which you must export this notebook to a Python file named `solution.py` and submit it on Gradescope.

Only edit the functions specified in the PDF (and wherever marked – `# WRITE CODE HERE`). Do not change definitions or edit the rest of the template, else the autograder will not work.

**Make sure you request a GPU runtime (especially for Question 3)!**
"""
#%%
# DO NOT MODIFY!
import matplotlib.pyplot as plt
import numpy as np
import random


#%%
# Fix random seed
random.seed(0)
np.random.seed(0)

#%%
"""## Question 1: Implementing MLPs with NumPy (30 points)"""

class NN(object):
  """
    Implements an MLP.
  """

  def __init__(self,
               dims=(784, 128, 64, 10), # h_0, h_1, h_2, h_3
               activation="relu",       # Activation function
               epsilon=1e-6,            # Correction factor
               lr=0.01,                 # Learning rate
               seed=0                   # Random seed
              ):
    """
      Constructor of the NN class.

      dims: list or tuple or np.array, default (784, 128, 64, 10)
        Values of h_0 (no. of features), h_1 (hidden dim. 1), h_2 (hidden dim. 2), h_3 (no. of output classes).
      activation: string, default "relu"
        Activation function to use.
      epsilon: float or double, default 1e-6
        Correction factor to clip probabilities.
      lr: float or double, default 0.01
        Learning rate for weight updates.
      seed: int, default 0
        Random seed.
    """
    super(NN, self).__init__()

    self.dims = dims
    self.n_hidden = len(dims) - 2
    self.activation_str = activation
    self.epsilon = epsilon
    self.lr = lr
    self.seed = seed

  def initialize_weights(self):
    """
      Results: Initializes the weights of the MLP from uniform(-1/sqrt(h_0), 1/sqrt(h_0)) and the biases to zeros.
    """
    if self.seed is not None:
      np.random.seed(self.seed)

    self.weights = {}
    # self.weights is a dictionary with keys W1, b1, W2, b2, ..., Wm, Bm where m - 1 is the number of hidden layers
    # The keys W1, W2, ..., Wm correspond to weights while b1, b2, ..., bm correspond to biases
    for layer_n in range(1, self.n_hidden + 2):
      # Set the biases to zero (one bias per neuron of current layer)
      self.weights[f"b{layer_n}"] = np.zeros((1, self.dims[layer_n]))

      # Set the weights (one weight per neuron of current layer to each neuron of previous layer)
      num_of_features = self.dims[0] # h_0
      previous_layer_size = self.dims[layer_n - 1]
      current_layer_size = self.dims[layer_n]

      self.weights[f"W{layer_n}"] = np.random.uniform(
          low=-1/np.sqrt(num_of_features),
          high=1/np.sqrt(num_of_features),
          size=(previous_layer_size, current_layer_size)
      )


  def relu(self, x, grad=False):
    """
      x: np.array
        Inputs to calculate ReLU(x) for. x may contain a batch of inputs!
      grad: bool, default False
        If True, return the gradient of the activation with respect to the inputs to the function.

      Outputs: Implements the ReLU activation function or its gradient.
    """
    if grad:
      # WRITE CODE HERE
      gradient = np.zeros(x.shape)
      gradient[x > 0] = 1

      return gradient

    # WRITE CODE HERE
    activated_x = np.maximum(0, x)

    return activated_x

  def sigmoid(self, x, grad=False):
    """
      x: np.array
        Inputs to calculate sigmoid(x) for. x may contain a batch of inputs!
      grad: bool, default False
        If True, return the gradient of the activation with respect to the inputs to the function.

      Outputs: Implements the Sigmoid activation function or its gradient.
    """
    if grad:
      # WRITE CODE HERE
      gradient = np.exp(-x) / (1 + np.exp(-x))**2

      return gradient

    # WRITE CODE HERE
    activated_x = 1 / (1 + np.exp(-x))

    return activated_x

  def tanh(self, x, grad=False):
    """
      x: np.array
        Inputs to calculate tanh(x) for. x may contain a batch of inputs!
      grad: bool, default False
        If True, return the gradient of the activation with respect to the inputs to the function.

      Outputs: Implements the tanh activation function or its gradient.
    """
    if grad:
      # WRITE CODE HERE
      gradient = 1 - np.tanh(x)**2

      return gradient

    # WRITE CODE HERE
    activated_x = np.tanh(x)

    return activated_x

  def activation(self, x, grad=False):
    """
      x: np.array
        Inputs to calculate activation(x) for. x may contain a batch of inputs!
      grad: bool, default False
        If True, return the gradient of the activation with respect to the inputs to the function.

      Outputs: Returns the value of the activation or the gradient.
    """
    if self.activation_str == "relu":
      # WRITE CODE HERE
      activated_x = self.relu(x, grad)
    elif self.activation_str == "sigmoid":
      # WRITE CODE HERE
      activated_x = self.sigmoid(x, grad)
    elif self.activation_str == "tanh":
      # WRITE CODE HERE
      activated_x = self.tanh(x, grad)
    else:
      raise Exception("Invalid activation")

    return activated_x

  def softmax(self, x):
    """
      x: np.array
        Inputs to calculate softmax over. x may contain a batch of inputs!

      Outputs: Implements the softmax function, returns the array containing softmax(x).
    """
    # Remember that softmax(x-C) = softmax(x) when C is a constant.
    # WRITE CODE HERE

    # Substract the maximum value of each row to avoid overflow
    x = x - np.max(x, axis=1, keepdims=True)

    # Every row of x is a sample, so must sum over the columns (axis=1)
    softmax_x = np.exp(x) / np.sum(np.exp(x), axis=1, keepdims=True)

    return softmax_x

  def forward(self, x):
    """
      x: np.array
        Inputs to the MLP. Note that x may contain multiple input examples, not just one example.

      Outputs: Implements the forward pass, returns cache as described below.
    """
    cache = {"Z0": x}
    # cache is a dictionary with keys Z0, A1, Z1, ..., Am, Zm where m - 1 is the number of hidden layers
    # Z0 just contains the inputs x to the network
    # Ai corresponds to the preactivation at layer i, Zi corresponds to the activation at layer i
    # WRITE CODE HERE

    for layer_n in range(1, self.n_hidden + 2):
      # Calculate the preactivation
      cache[f"A{layer_n}"] = np.dot(
        cache[f"Z{layer_n - 1}"], self.weights[f"W{layer_n}"]
      )
      # Add the bias to the preactivation vector
      cache[f"A{layer_n}"] += self.weights[f"b{layer_n}"]

      # Calculate the activation
      if layer_n == self.n_hidden + 1:
        # Last layer, use softmax
        cache[f"Z{layer_n}"] = self.softmax(cache[f"A{layer_n}"])

      else:
        # Hidden layer, use the activation function
        cache[f"Z{layer_n}"] = self.activation(cache[f"A{layer_n}"])

    return cache

  def loss(self, prediction, labels):
    """
      prediction: np.array
        Predicted probabilities for each class for inputs. May contain multiple examples (a batch)!
      labels: np.array
        True labels corresponding to the inputs (assume they are one-hot encoded). May contain multiple examples (a batch)!

      Outputs: Returns the crossentropy loss (take the mean over number of inputs).
    """
    prediction[np.where(prediction < self.epsilon)] = self.epsilon
    prediction[np.where(prediction > 1 - self.epsilon)] = 1 - self.epsilon
    # WRITE CODE HERE

    batch_size = labels.shape[0]
    # Calculate the crossentropy loss
    loss = -np.sum(labels * np.log(prediction)) / batch_size

    return loss

  def backward(self, cache, labels):
    """
      cache: np.array
        Results of the backward pass. This may be for multiple examples (a batch).
      labels: np.array
        True labels corresponding to the inputs in cache. May contain multiple examples (a batch)!

      Outputs: Implements the backward pass, returns grads as described below.
    """
    output = cache[f"Z{self.n_hidden + 1}"]
    grads = {}

    # grads is a dictionary with keys dAm, dWm, dbm, dZ(m-1), dA(m-1), ..., dW1, db1
    # Remember to account for the number of input examples!
    # WRITE CODE HERE

    batch_size = labels.shape[0]

    # Calculate the gradient of the loss with respect to the last preactivation (softmax output layer)
    grads[f"dA{self.n_hidden + 1}"] = output - labels

    # Calculate the gradient of the loss with respect to the last weight matrix
    grads[f"dW{self.n_hidden + 1}"] = np.dot(
      cache[f"Z{self.n_hidden}"].T, grads[f"dA{self.n_hidden + 1}"]
    ) / batch_size

    # Calculate the gradient of the loss with respect to the last bias vector
    grads[f"db{self.n_hidden + 1}"] = np.sum(
      grads[f"dA{self.n_hidden + 1}"], axis=0, keepdims=True
    ) / batch_size

    # Calculate the gradient of the loss with respect to the last activation
    grads[f"dZ{self.n_hidden}"] = np.dot(
      grads[f"dA{self.n_hidden + 1}"], self.weights[f"W{self.n_hidden + 1}"].T
    )

    # Calculate the gradient of the loss with respect to the rest of the network
    for layer_n in range(self.n_hidden, 0, -1):
      # Calculate the gradient of the loss with respect to the preactivation
      grads[f"dA{layer_n}"] = grads[f"dZ{layer_n}"] * self.activation(
        cache[f"A{layer_n}"], grad=True
      )

      # Calculate the gradient of the loss with respect to the weight matrix
      grads[f"dW{layer_n}"] = np.dot(
        cache[f"Z{layer_n - 1}"].T, grads[f"dA{layer_n}"]
      ) / batch_size

      # Calculate the gradient of the loss with respect to the bias vector
      grads[f"db{layer_n}"] = np.sum(
        grads[f"dA{layer_n}"], axis=0, keepdims=True
      ) / batch_size

      # Calculate the gradient of the loss with respect to the previous activation
      if layer_n > 1:
        grads[f"dZ{layer_n - 1}"] = np.dot(
          grads[f"dA{layer_n}"], self.weights[f"W{layer_n}"].T
        )

    return grads

  def update(self, grads):
    """
      grads: np.dictionary
        Gradients obtained from the backward pass.

      Results: Updates the network's weights and biases.
    """
    for layer in range(1, self.n_hidden + 2):
      # WRITE CODE HERE

      # Update the weight matrix
      self.weights[f"W{layer}"] -= self.lr * grads[f"dW{layer}"]
      # Update the bias vector
      self.weights[f"b{layer}"] -= self.lr * grads[f"db{layer}"]


#%%
nn = NN()
nn.initialize_weights()

x = np.random.uniform(low=-1/np.sqrt(784),
          high=1/np.sqrt(784),
          size=(2, 784))

cache = nn.forward(x)
predictions = cache[f"Z{nn.n_hidden + 1}"]
labels = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0]])

grads = nn.backward(cache, labels)

#%%
"""## Question 2: Implementing CNN layers with NumPy (20 points)
Note: You may assume that there are no biases, no input padding (valid convolution) and also that convolution here refers to cross-correlation, i.e., no kernel flipping when convolving the inputs.
"""

class Convolution2dLayer(object):
  """
    Implements a 2D convolution layer.
  """

  def __init__(self, filter_size=3, stride=1, n_units=64, seed=0):
    """
      Constructor of the Convolution2dLayer class.

      Note: We assume that the input images have only a single channel.

      filter_size: int, default 3
        Filter size to use for convolution. We assume equal height and width.
      stride: int, default 1
        Stride for convolution.
      n_units: int, default 64
        Number of output channels, i.e., number of filters in the layer.
      seed: int, default 0
        Random seed.
    """
    super(Convolution2dLayer, self).__init__()

    self.filter_size = filter_size
    self.stride = stride
    self.n_units = n_units
    self.seed = seed

  def initialize_weights(self):
    """
      Results: Initializes the weights of the CNN from uniform(0, 1).
    """
    if self.seed is not None:
      np.random.seed(self.seed)

    # self.weights is an np.array of shape (n_units, filter_size, filter_size)
    # We do not consider biases in this convolution layer implementation
    # WRITE CODE HERE
    self.weights = np.random.uniform(
      low=0, high=1, size=(self.n_units, self.filter_size, self.filter_size)
    )

  def forward(self, x):
    """
      x: np.array
        Inputs to convolve. This may contain multiple input examples, not just one.
        Note: We assume that the input images have only a single channel, e.g. (5, 1, 32, 32) where 5 is the number of
        images, 1 channel, 32x32 image size.

      Outputs: Inputs and the result of the convolution operation on the inputs stored in cache.

      Note: You need not flip the kernel! You may just implement cross-correlation.
    """
    cache = {}

    # cache is a dictionary where cache["x"] stores the inputs and cache["out"] stores the outputs of the layer
    # WRITE CODE HERE
    cache["x"] = x
    cache["out"] = None

    output_dimensions = (
      (x.shape[2] - self.filter_size) // self.stride + 1,
      (x.shape[3] - self.filter_size) // self.stride + 1
    )

    # Initialize the output array
    # (batch size, output channels, output height, output width)
    cache["out"] = np.zeros(
      (x.shape[0], self.n_units, output_dimensions[0], output_dimensions[1])
    )

    # Perform convolution
    for image_n in range(x.shape[0]): # For each image in the batch
      for filter_n in range(self.n_units): # For each filter
        for row in range(output_dimensions[0]): # For each row in the output filter
          for col in range(output_dimensions[1]): # For each column in the output filter
            cache["out"][image_n, filter_n, row, col] = np.sum(
              x[
                image_n,
                :,
                row * self.stride:row * self.stride + self.filter_size,
                col * self.stride:col * self.stride + self.filter_size
              ] * self.weights[filter_n]
            )

    return cache

  def backward(self, cache, grad_output):
    """
      cache: dictionary
        Contains the inputs and the result of the convolution operation applied on them.
      grad_output: np.array
        Gradient of the loss with respect to the outputs of the convolution layer.

      Outputs: Gradient of the loss with respect to the parameters of the convolution layer.
    """
    # grads is an np.array containing the gradient of the loss with respect to the parameters in the convolution layer
    # Remember to account for the number of input examples!
    # WRITE CODE HERE

    # Initialize the gradient array with the same shape as the weights
    grads = np.zeros(self.weights.shape)

    batch_size = cache["x"].shape[0]

    # Go through each example in the batch
    for image_n in range(batch_size):
      # Go through each filter
      for filter_n in range(self.n_units):
        # Go through each row in the output filter
        for row in range(grad_output.shape[2]):
          # Go through each column in the output filter
          for col in range(grad_output.shape[3]):
            # Remove first dimension of the input (1, 3, 3) -> (3, 3)
            input_image = np.squeeze(cache["x"][
              image_n, :, row * self.stride:row * self.stride + self.filter_size, col * self.stride:col * self.stride + self.filter_size
            ], axis=0)

            # Add gradient to the specific filter
            grads[filter_n] += input_image * grad_output[image_n, filter_n, row, col]

    return grads

#%%
conv_layer = Convolution2dLayer()
conv_layer.initialize_weights()

x = np.random.uniform(low=0, high=1, size=(5, 1, 32, 32))
cache = conv_layer.forward(x)

grad_output = np.random.uniform(low=0, high=1, size=cache["out"].shape)
grads = conv_layer.backward(cache, grad_output)

#%%
class MaxPooling2dLayer(object):
  """
    Implements a 2D max-pooling layer.
  """

  def __init__(self, filter_size=2):
    """
      Constructor of the MaxPooling2dLayer class.

      filter_size: int, default 2
        Filter size to use for max-pooling. We assume equal height and width, and stride = height = width.
    """
    super(MaxPooling2dLayer, self).__init__()

    self.filter_size = filter_size
    self.stride = filter_size

  def forward(self, x):
    """
      x: np.array
        Inputs to compute max-pooling for. This may contain multiple input examples, not just one.
        Note: The input dimensions to max-pooling are the output dimensions of the convolution!

      Outputs: Inputs and the result of the max-pooling operation on the inputs stored in cache.
    """
    cache = {}

    # cache is a dictionary where cache["x"] stores the inputs and cache["out"] stores the outputs of the layer
    # WRITE CODE HERE
    cache["x"] = x
    cache["out"] = None

    # Calculate the output dimensions
    output_dimensions = (
      (x.shape[2] - self.filter_size) // self.stride + 1,
      (x.shape[3] - self.filter_size) // self.stride + 1
    )

    # Initialize the output array
    # (batch size, output channels, output height, output width)
    cache["out"] = np.zeros(
      (x.shape[0], x.shape[1], output_dimensions[0], output_dimensions[1])
    )

    # Perform max-pooling
    for image_n in range(x.shape[0]): # For each image in the batch
      for channel_n in range(x.shape[1]): # For each channel
        for row in range(output_dimensions[0]): # For each row in the output filter
          for col in range(output_dimensions[1]): # For each column in the output filter
            cache["out"][image_n, channel_n, row, col] = np.max(
              x[
                image_n,
                channel_n,
                row * self.stride:row * self.stride + self.filter_size,
                col * self.stride:col * self.stride + self.filter_size
              ]
            )

    return cache

  def backward(self, cache, grad_output):
    """
      cache: dictionary
        Contains the inputs and the result of the max-pooling operation applied on them.
      grad_output: np.array
        Gradient of the loss with respect to the outputs of the max-pooling layer.

      Outputs: Gradient of the loss with respect to the inputs to the max-pooling layer.
    """
    grads = None # WRITE CODE HERE (initialize grads correctly)

    # Initialize the gradient array with the same shape as the input
    grads = np.zeros(cache["x"].shape)

    # grads is an np.array containing the gradient of the loss with respect to the inputs to the max-pooling layer
    # Remember to account for the number of input examples!
    # WRITE CODE HERE

    batch_size = cache["x"].shape[0]

    # Go through each example in the batch
    for image_n in range(batch_size):
      # Go through each channel
      for channel_n in range(cache["x"].shape[1]):
        # Go through each row in the output filter
        for row in range(grad_output.shape[2]):
          # Go through each column in the output filter
          for col in range(grad_output.shape[3]):
            input_image = cache["x"][
              image_n,
              channel_n,
              row * self.stride:row * self.stride + self.filter_size,
              col * self.stride:col * self.stride + self.filter_size
            ]

            # Find the maximum value in the input image
            max_value = np.max(input_image)

            # Find the indices of the maximum value
            max_indices = np.argwhere(input_image == max_value)
            max_indice_i = max_indices[0][0]
            max_indice_j = max_indices[0][1]

            # Add gradient to the specific filter, rest is all zeros
            grads[
              image_n,
              channel_n,
              row * self.stride + max_indice_i,
              col * self.stride + max_indice_j
            ] += grad_output[image_n, channel_n, row, col]

    return grads
#%%

max_pool_layer = MaxPooling2dLayer()
x = np.random.uniform(low=0, high=1, size=(5, 1, 32, 32))
cache = max_pool_layer.forward(x)

grad_output = np.random.uniform(low=0, high=1, size=cache["out"].shape)
grads = max_pool_layer.backward(cache, grad_output)


#%%
"""## Question 3: Implementing a CNN and comparison with MLPs using PyTorch (50 points)"""

# DO NOT MODIFY!
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.nn.init as init
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
device = "cuda" if torch.cuda.is_available() else "cpu"

#%%

# Fix random seed
torch.manual_seed(0)
torch.cuda.manual_seed_all(0)
torch.cuda.manual_seed(0)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

#%%
class ResidualBlock(nn.Module):
  """This class implements the Residual Block used in ResNet-18."""

  def __init__(self, in_channels, channels, conv_stride=1, activation_str="relu", initialization="xavier_normal"):
    """
      Constructor for the ResidualBlock class.

      in_channels: int
        Number of channels in the input to the block.
      channels: int
        Number of output channels for the block, i.e., number of filters.
      conv_stride: int, default 1
        Stride of the first convolution layer and downsampling convolution (if required).
      activation_str: string, default "relu"
        Activation function to use.
      initialization: string, default "xavier_normal"
        Initialization for convolution layer weights.
    """
    super(ResidualBlock, self).__init__()

    self.in_channels = in_channels
    self.channels = channels
    self.conv_stride = conv_stride
    self.activation_str = activation_str
    self.initialization = initialization

    # Define these members by replacing `None` with the correct definitions
    # self.conv1 = None # WRITE CODE HERE
    # self.bn1 = None   # WRITE CODE HERE
    # self.conv2 = None # WRITE CODE HERE
    # self.bn2 = None   # WRITE CODE HERE

    self.conv1 = nn.Conv2d(
      in_channels=self.in_channels,
      out_channels=self.channels,
      kernel_size=3,
      stride=self.conv_stride,
      padding=1,
      bias=False
    )

    self.bn1 = nn.BatchNorm2d(self.channels)

    self.conv2 = nn.Conv2d(
      in_channels=self.channels,
      out_channels=self.channels,
      kernel_size=3,
      stride=1,
      padding=1,
      bias=False
    )

    self.bn2 = nn.BatchNorm2d(self.channels)

    self.residual_connection = self.residual(in_channels, channels, conv_stride)

    # Initialize weights for convolution layers
    if initialization == "xavier_normal":
      init.xavier_normal_(self.conv1.weight)
      init.xavier_normal_(self.conv2.weight)
    elif initialization == "xavier_uniform":
      init.xavier_uniform_(self.conv1.weight)
      init.xavier_uniform_(self.conv2.weight)
    elif initialization == "kaiming_normal":
      init.kaiming_normal_(self.conv1.weight)
      init.kaiming_normal_(self.conv2.weight)
    else:
      raise Exception("Invalid initialization")

  def activation(self, input):
    """
      input: Tensor
        Input on which the activation is applied.

      Output: Result of activation function applied on input.
        E.g. if self.activation_str is "relu", return relu(input).
    """
    if self.activation_str == "relu":
      # WRITE CODE HERE
      return F.relu(input)
    elif self.activation_str == "tanh":
      # WRITE CODE HERE
      return torch.tanh(input)
    else:
      raise Exception("Invalid activation")


  def residual(self, in_channels, channels, conv_stride=1):
    """
      in_channels: int
        Number of input channels in the input to the block.
      channels: int
        Number of output channels for the block, i.e., number of filters.
      conv_stride: int, default 1
        Stride to use for downsampling 1x1 convolution.

      Output: Returns an nn.Sequential object which computes the identity function of the input if stride is 1
              and the number of input channels equals the number of output channels. Otherwise, it returns an
              nn.Sequential object that downsamples its input using a 1x1-conv of the stride specified and
              followed by a BatchNorm2d.
    """
    layers = []
    if conv_stride != 1 or in_channels != channels:
      # WRITE CODE HERE

      # Adding a 1x1 convolution layer
      layers.append(nn.Conv2d(
        in_channels,
        channels,
        kernel_size=1,
        stride=conv_stride,
        bias=False
      ))

      # Adding BatchNorm2d layer
      layers.append(nn.BatchNorm2d(channels))

    return nn.Sequential(*layers)

  def forward(self, x):
    """
      x: Tensor
        Input to the block.

      Outputs: Returns the output of the forward pass of the block.
    """
    # WRITE CODE HERE

    # First convolution layer
    out = self.conv1(x)

    # BatchNorm2d layer
    out = self.bn1(out)

    # Activation layer
    out = self.activation(out)

    # Second convolution layer
    out = self.conv2(out)

    # BatchNorm2d layer
    out = self.bn2(out)

    # Adding the residual connection
    out += self.residual_connection(x)

    # Activation layer
    out = self.activation(out)

    return out

#%%

residual_block = ResidualBlock(3, 64, conv_stride=2, activation_str="relu", initialization="xavier_normal")

x = torch.randn(1, 3, 32, 32)

y = residual_block(x)


#%%
class ResNet18(nn.Module):
  """This class implements the ResNet-18 architecture from its components."""

  def __init__(self, activation_str="relu", initialization="xavier_normal"):
    """
      Constructor for the ResNet18 class.

      activation_str: string, default "relu"
        Activation function to use.
      initialization: string, default "xavier_normal"
        Weight initialization to use.
    """
    super(ResNet18, self).__init__()

    self.n_classes = 10
    self.activation_str = activation_str
    self.initialization = initialization

    # Define these members by replacing `None` with the correct definitions
    # self.conv1 = None   # WRITE CODE HERE
    # self.bn1 = None     # WRITE CODE HERE
    # self.layer1 = None  # WRITE CODE HERE (use _create_layer)
    # self.layer2 = None  # WRITE CODE HERE (use _create_layer)
    # self.layer3 = None  # WRITE CODE HERE (use _create_layer)
    # self.layer4 = None  # WRITE CODE HERE (use _create_layer)
    # self.avgpool = None # WRITE CODE HERE
    # self.linear = None  # WRITE CODE HERE

    self.conv1 = nn.Conv2d(
      in_channels=3,
      out_channels=64,
      kernel_size=3,
      stride=1,
      padding=1,
      bias=False
    )

    self.bn1 = nn.BatchNorm2d(64)

    self.layer1 = self._create_layer(64, 64, 1)

    self.layer2 = self._create_layer(64, 128, 2)

    self.layer3 = self._create_layer(128, 256, 2)

    self.layer4 = self._create_layer(256, 512, 2)

    self.avgpool = nn.AvgPool2d((4, 4))

    self.linear = nn.Linear(512, self.n_classes)

    # # Initialize weights for convolution layers
    # if initialization == "xavier_normal":
    #   init.xavier_normal_(self.conv1.weight)
    # elif initialization == "xavier_uniform":
    #   init.xavier_uniform_(self.conv1.weight)
    # elif initialization == "kaiming_normal":
    #   init.kaiming_normal_(self.conv1.weight)
    # else:
    #   raise Exception("Invalid initialization")


  def activation(self, input):
    """
      input: Tensor
        Input on which the activation is applied.

      Output: Result of activation function applied on input.
        E.g. if self.activation_str is "relu", return relu(input).
    """
    if self.activation_str == "relu":
      # WRITE CODE HERE
      return F.relu(input)
    elif self.activation_str == "tanh":
      # WRITE CODE HERE
      return torch.tanh(input)
    else:
      raise Exception("Invalid activation")

  def _create_layer(self, in_channels, channels, conv_stride=1):
    """
      in_channels: int
        Number of input channels present in the input to the layer.
      out_channels: int
        Number of output channels for the layer, i.e., the number of filters.
      conv_stride: int, default 1
        Stride of the first convolution layer in the block and the downsampling convolution (if required).

      Outputs: Returns an nn.Sequential object giving a "layer" of the ResNet, consisting of 2 blocks each.
    """
    # Modify the following statement to return an nn.Sequential object containing 2 ResidualBlocks.
    # You must make sure that the appropriate channels and conv_stride are provided.

    # WRITE CODE HERE
    return nn.Sequential(
      ResidualBlock(
        in_channels,
        channels,
        conv_stride=conv_stride,
        activation_str=self.activation_str,
        initialization=self.initialization
      ),
      ResidualBlock(
        channels,
        channels,
        conv_stride=1,
        activation_str=self.activation_str,
        initialization=self.initialization
      )
    )

  def get_first_conv_layer_filters(self):
    """
      Outputs: Returns the filters in the first convolution layer.
    """
    return self.conv1.weight.clone().cpu().detach().numpy()

  def get_last_conv_layer_filters(self):
    """
      Outputs: Returns the filters in the last convolution layer.
    """
    return list(self.layer4.modules())[1].conv2.weight.clone().cpu().detach().numpy()

  def forward(self, x):
    """
      x: Tensor
        Input to the network.

      Outputs: Returns the output of the forward pass of the network.
    """
    # WRITE CODE HERE

    # First convolution layer
    out = self.conv1(x)

    # BatchNorm2d layer
    out = self.bn1(out)

    # Activation layer
    out = self.activation(out)

    # First layer
    out = self.layer1(out)

    # Second layer
    out = self.layer2(out)

    # Third layer
    out = self.layer3(out)

    # Fourth layer
    out = self.layer4(out)

    # Average pooling layer
    out = self.avgpool(out)

    # Flatten the output
    out = out.view(out.size(0), -1)

    # Linear layer
    out = self.linear(out)

    return out

#%%
resnet18 = ResNet18(activation_str="relu", initialization="xavier_normal")

x = torch.randn(1, 3, 32, 32)

y = resnet18(x)



#%%

def get_cifar10():
  transform = transforms.Compose([
      transforms.ToTensor()
  ])

  train_dataset = torchvision.datasets.CIFAR10(
      root='./data', train=True, download=True, transform=transform)
  train_loader = torch.utils.data.DataLoader(
      train_dataset, batch_size=128, shuffle=True, num_workers=2)

  val_dataset = torchvision.datasets.CIFAR10(
      root='./data', train=False, download=True, transform=transform)
  val_loader = torch.utils.data.DataLoader(
      val_dataset, batch_size=128, shuffle=False, num_workers=2)

  return train_loader, val_loader

#%%

def train_loop(epoch, model, train_loader, criterion, optimizer):
  """
    epoch: int
      Number of the current training epoch (starting from 0).
    model: ResNet18
      The model to train, which is an instance of the ResNet18 class.
    train_loader: DataLoader
      The training dataloader.
    criterion: Module
      A Module object that evaluates the crossentropy loss.
    optimizer: Optimizer
      An Optimizer object for the Adam optimizer.

    Outputs: Returns average train_acc and train_loss for the current epoch.
  """
  train_acc = 0.
  train_loss = 0.

  # WRITE CODE HERE

  # Set the model to training mode
  model.train()

  # Loop over the training data
  for i, (images, labels) in enumerate(train_loader):
    # Move the images and labels to the device
    images = images.to(device)
    labels = labels.to(device)

    # Forward pass
    outputs = model(images)

    # Calculate the loss
    loss = criterion(outputs, labels)

    # Backward pass
    loss.backward()

    # Update the weights
    optimizer.step()

    # Reset the gradients
    optimizer.zero_grad()

    # Calculate the accuracy
    _, predicted = torch.max(outputs.data, 1)
    train_acc += (predicted == labels).sum().item()

    # Calculate the loss
    train_loss += loss.item()

  print(f"Epoch: {epoch} | Train Acc: {train_acc:.6f} | Train Loss: {train_loss:.6f}")
  return train_acc, train_loss

def valid_loop(epoch, model, val_loader, criterion):
  """
    epoch: int
      Number of the current epoch (starting from 0).
    model: ResNet18
      The model to train, which is an instance of the ResNet18 class.
    val_loader: DataLoader
      The validation dataloader.
    criterion: Module
      A Module object that evaluates the crossentropy loss.

    Outputs: Returns average val_acc and val_loss for the current epoch.
  """
  val_acc = 0.
  val_loss = 0.

  # WRITE CODE HERE

  # Set the model to evaluation mode
  model.eval()

  # Loop over the validation data
  for i, (images, labels) in enumerate(val_loader):
    # Move the images and labels to the device
    images = images.to(device)
    labels = labels.to(device)

    # Forward pass
    outputs = model(images)

    # Calculate the loss
    loss = criterion(outputs, labels)

    # Calculate the accuracy
    _, predicted = torch.max(outputs.data, 1)
    val_acc += (predicted == labels).sum().item()

    # Calculate the loss
    val_loss += loss.item()

  print(f"Epoch: {epoch} | Val Acc: {val_acc:.6f}   | Val Loss: {val_loss:.6f}")
  return val_acc, val_loss

activation_str = "relu"
initialization = "xavier_normal"

if __name__ == "__main__":
  train_accs, train_losses, val_accs, val_losses = [], [], [], []
  n_epochs = 25

  model = ResNet18(
    activation_str=activation_str,
    initialization=initialization
  ).to(device)
  criterion = nn.CrossEntropyLoss()
  optimizer = optim.Adam(model.parameters())

  train_loader, val_loader = get_cifar10()

  for epoch in range(n_epochs):
    # Training
    train_acc, train_loss = train_loop(epoch, model, train_loader, criterion, optimizer)
    train_accs.append(train_acc)
    train_losses.append(train_loss)

    # Validation
    val_acc, val_loss = valid_loop(epoch, model, val_loader, criterion)
    val_accs.append(val_acc)
    val_losses.append(val_loss)

"""### Questions 3.4, 3.5, 3.6, 3.7, 3.8
You may write your own code for these questions below. These will not be autograded and you need not submit code for these, only the report.
"""

# For Q 3.6
if __name__ == "main":
  vis_image = None
  for data, labels in val_loader:
    vis_image = data[12].unsqueeze(0)
  # import matplotlib.pyplot as plt
  # plt.imshow(vis_image.squeeze().permute(1, 2, 0).cpu().detach().numpy())




# %%
