import modelbuilder as mb
import trainingdata as td
import mapreader as mr
import trainer as tr
import model as mod

graph = mr.ReadMap("../data/madrid.gml")

X, y = td.generate_training_set(graph, n_samples=1000)

model = mod.Model(mb.build_model())

tr.train(model.get_model(), X, y)

model.get_model().save_params("model_params")
