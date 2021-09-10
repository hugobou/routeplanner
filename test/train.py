import modelbuilder as mb
import traffic
import trainingdata as td
import mapreader as mr
import trainer as tr
import traffic as tf
import model as mod
import features as feat

def add_weights(G):
    for s, d, meta in G.edges.data():
        for i in range(len(G[s][d])):
            G[s][d][i]['weight'] = G[s][d][i]['length'] / G[s][d][i]['speed_kph'] * (1 + G[s][d][i]['traffic'])

graph = mr.ReadMap("../data/madrid.gml")

print('update_traffic_info')
tm_dict = tf.read_tm_dict('../data/traffic_measurement_points.csv')
with open('pm.xml') as xmlfile:
    tm_list = traffic.parse_traffic_data(xmlfile.read(), debug=False)
tf.update_traffic_info(graph, tm_list, tm_dict)

print('add_weights')
add_weights(graph)

print('generate_training_set')
X, y = td.generate_training_set(feat.FeaturesEncoder(), graph, n_samples=15000)

model = mod.Model(mb.build_model())

tr.train(model.get_model(), X, y)

model.get_model().save_params("../data/model_params")
