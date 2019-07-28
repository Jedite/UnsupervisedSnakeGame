import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
import numpy as np


class NeuralNetwork:
    def __init__(self):
        pass

    def create_dummy_model(self, training_data):
        shape_second_parameter = len(training_data[0][0])
        x = np.array([i[0] for i in training_data])
        X = x.reshape(-1, shape_second_parameter, 1)
        y = [i[1] for i in training_data]
        model = self.create_neural_network_model(input_size=len(X[0]), output_size=len(y[0]))
        return model

    def create_neural_network_model(self, input_size, output_size):
        network = input_data(shape=[None, input_size, 1], name='input')
        network = tflearn.fully_connected(network, 32)
        network = tflearn.fully_connected(network, 32)
        network = fully_connected(network, output_size, activation='softmax')
        network = regression(network, name='targets')
        model = tflearn.DNN(network)

        return model

    def train_model(self, training_data, model=False):
        shape_second_parameter = len(training_data[0][0])
        x = np.array([i[0] for i in training_data])
        X = x.reshape(-1, shape_second_parameter, 1)
        y = [i[1] for i in training_data]

        model.fit({'input': X}, {'targets': y}, n_epoch=10, batch_size=16, show_metric=True)

        return model