import tensorflow as tf
import numpy as np


class Network(object):
    def __init__(self, layers):
        self.input_nodes = layers[0]
        self.model = tf.keras.models.Sequential()
        self.model.add(tf.keras.layers.Dense(
            layers[1], input_dim=layers[0], use_bias=True, kernel_initializer='random_uniform',
            activation='relu'))

        for layer in layers[2:-1]:
            self.model.add(tf.keras.layers.Dense(
                layer, use_bias=True, kernel_initializer='random_uniform',
                activation='relu'))

        self.model.add(tf.keras.layers.Dense(
            layers[-1], use_bias=True, kernel_initializer='random_uniform',
            activation='softmax'))

    def predict(self, inp_arr):
        return(self.model.predict(np.asarray(
            inp_arr, dtype=int).reshape([1, self.input_nodes])).tolist()[0])

    def get_weights(self):
        return self.model.get_weights()

    def set_weights(self, weights):
        self.model.set_weights(weights)
        return
