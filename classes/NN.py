import tensorflow as tf
import numpy as np


class Network(object):
    def __init__(self):

        self.model = tf.keras.models.Sequential(
            [tf.keras.layers.Dense(
                4, input_dim=6, use_bias=True, kernel_initializer='random_uniform',
                activation='relu'),
             tf.keras.layers.Dense(
                 3, use_bias=True, kernel_initializer='random_uniform',
                 activation='softmax')])

    def predict(self, inp_arr):
        return(self.model.predict(np.asarray(
            inp_arr, dtype=int).reshape([1, 6])).tolist()[0])

    def get_weights(self):
        return self.model.get_weights()

    def set_weights(self, weights):
        self.model.set_weights(weights)
        return
