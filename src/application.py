import modelbuilder as mb
import mapreader as mr
import model as mod
import routeplanner as rp
import traffic as tf
from trainer import BATCH_SIZE
from features import FEATURE_LENGTH
from features import FeaturesEncoder

# TODO move to new file
def application_creator(gml_file_name, pm_dict_file_name, model_params_file_name):
    graph = mr.ReadMap(gml_file_name)
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


class Application:
    def __init__(self, graph, pm_dict, model, feature_encoder):
        self.graph = graph
        self.pm_dict = pm_dict
        self.route_planner = rp.RoutePlanner(model, feature_encoder)

    def get_route(self, origin, destination):
        return self.route_planner.get_route_gps(self.graph, origin, destination)

    def update_traffic_info(self, tm_list):
        tf.update_traffic_info(self.graph, tm_list, self.pm_dict)
