import tensorflow as tf
import numpy as np


class Network(object):
    def __init__(self):
        self.model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(
                4, input_dim=6, use_bias=True, activation='relu'),
            tf.keras.layers.Dense(3, use_bias=True, activation='softmax')
        ])

    def predict(self, inp_arr):
        return(self.model.predict(np.asarray(
            inp_arr, dtype=int).reshape([1, 6])).tolist()[0])
