import mapreader as mr
import model as mod
import modelbuilder as mb
import traffic as tf
from application import Application
from features import FEATURE_LENGTH, FeaturesEncoder
from trainer import BATCH_SIZE


def app_create(gml_file_name, pm_dict_file_name, model_params_file_name):
    graph = mr.ReadMap(gml_file_name)
    tf.reset_traffic_info(graph)
    tm_dict = tf.read_tm_dict(pm_dict_file_name)

    model = mod.Model(mb.build_model())

    # https://mxnet.apache.org/versions/1.7.0/api/python/docs/api/module/index.html
    # https://mxnet-tqchen.readthedocs.io/en/latest/packages/python/module.html

    mx_model = model.get_model()

    mx_model.bind(data_shapes=[('data', (BATCH_SIZE, FEATURE_LENGTH))],
                  label_shapes=[('softmax_label', (BATCH_SIZE,))])

    mx_model.load_params("%s" % model_params_file_name)

    feature_encoder = FeaturesEncoder()

    return Application(graph, tm_dict, model, feature_encoder)