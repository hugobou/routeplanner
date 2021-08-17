import modelbuilder as mb
import traffic
import trainingdata as td
import mapreader as mr
import trainer as tr
import traffic as tf
import model as mod

graph = mr.ReadMap("../data/madrid.gml")

tm_dict = tf.read_tm_dict('../data/traffic_measurement_points.csv')
with open('pm.xml') as xmlfile:
    tm_list = traffic.parse_traffic_data(xmlfile.read(), debug=False)
tf.update_traffic_info(graph, tm_list, tm_dict)

X, y = td.generate_training_set(graph, n_samples=15000)

model = mod.Model(mb.build_model())

tr.train(model.get_model(), X, y)

model.get_model().save_params("model_params")
