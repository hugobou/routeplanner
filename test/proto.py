import modelbuilder as mb
import MapReader as mr
import Model as mod
import RoutePlanner as rp
import osmnx as ox

from trainer import BATCH_SIZE

graph = mr.ReadMap("/home/hugo/PycharmProjects/routeplanner/proto/madrid.gml")

model = mod.Model(mb.build_model())

# https://mxnet.apache.org/versions/1.7.0/api/python/docs/api/module/index.html
# https://mxnet-tqchen.readthedocs.io/en/latest/packages/python/module.html

# before loading parameters we have to bind the model
# data size is batch_size, feature width
# lbel size is batch size
mxmodel = model.get_model()

mxmodel.bind(data_shapes=[('data', (BATCH_SIZE, 25))], label_shapes=[('softmax_label', (BATCH_SIZE,))])

mxmodel.load_params("/home/hugo/PycharmProjects/routeplanner/test/model_params")

origin_point = (-3.6121729, 40.4224813)
destination_point = (-3.7090030, 40.4538682)
node_src = ox.distance.nearest_nodes(graph, origin_point[0], origin_point[1])
node_dst = ox.distance.nearest_nodes(graph, destination_point[0], destination_point[1])

route, valid = rp.get_route(model, graph, node_src, node_dst)

print(route)
print(valid)

