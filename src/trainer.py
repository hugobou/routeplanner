import logging
import mxnet as mx
from sklearn.model_selection import train_test_split

import modelbuilder as mb
import TrainingData as td
import MapReader as mr


def train(model, X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, train_size=0.8, random_state=42)
    batch_size = 20
    train_iter = mx.io.NDArrayIter(X_train, y_train, batch_size=batch_size, shuffle=True)
    val_iter = mx.io.NDArrayIter(X_test, y_test, batch_size=batch_size)
    logging.getLogger().setLevel(logging.DEBUG)  # logging to stdout
    model.bind(data_shapes=train_iter.provide_data, label_shapes=train_iter.provide_label)
    model.init_params()
    model.fit(train_iter,  # train data
              eval_data=val_iter,  # validation data
              optimizer='adam',  # use SGD to train
              eval_metric='acc',  # report accuracy during training
              # output progress for each 100 data batches
              batch_end_callback=mx.callback.Speedometer(batch_size, 10),
              num_epoch=5)  # train for at most 10 dataset passes


graph = mr.ReadMap("/home/hugo/PycharmProjects/routeplanner/data/map.osm")

X, y = td.generate_training_set(graph, n_samples=1000)

model = mb.build_model()

train(model, X, y)
