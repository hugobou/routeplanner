import traffic
import mapreader as mr
from model.trainer import train
from model.model import Model
from model.modelbuilder import build_model
from model.trainingdata import generate_training_set
from model.features import FeaturesEncoder
import traffic as tf


# Weights only used for offline analysis so not added in graph reading
def add_weights(G):
    for s, d, meta in G.edges.data():
        for i in range(len(G[s][d])):
            G[s][d][i]['weight'] = G[s][d][i]['length'] / (G[s][d][i]['speed_kph'] / 3.6 ) * (1 + G[s][d][i]['traffic'])


if __name__ == "__main__":
    graph = mr.ReadMap("../data/madrid.gml")

    print('update_traffic_info')
    tm_dict = tf.read_tm_dict('../data/traffic_measurement_points.csv')
    with open('pm.xml') as xmlfile:
        tm_list = traffic.parse_traffic_data(xmlfile.read(), debug=False)
    tf.update_traffic_info(graph, tm_list, tm_dict)

    print('add_weights')
    add_weights(graph)

    print('generate_training_set')
    X, y = generate_training_set(FeaturesEncoder(), graph, n_samples=15000)

    model = Model(build_model())

    train(model.get_model(), X, y)

    model.get_model().save_params("../data/model_params")
