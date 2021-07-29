import mxnet as mx
import numpy as np

class Model:
    def __init__(self, model):
        self.__model = model

    def get_model(self):
        return self.__model

    # TODO TEST
    def predict(self, features_vector):
        return np.argmax(self.__model.predict(
            mx.io.NDArrayIter(np.array([features_vector]), np.array([0]))).asnumpy()[0])
