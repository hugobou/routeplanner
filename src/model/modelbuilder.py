import mxnet as mx

from model.features import FEATURE_LENGTH, MAX_OUT_DEGREE

BATCH_SIZE = 20


def build_model(context=mx.cpu()):

    data = mx.sym.var('data')
    label = mx.sym.var('softmax_label')

    fc2 = mx.sym.FullyConnected(data=data, num_hidden=32)
    fc2 = mx.sym.Activation(data=fc2, act_type="relu")

    fc3 = mx.sym.FullyConnected(data=fc2, num_hidden=MAX_OUT_DEGREE)
    mlp = mx.sym.SoftmaxOutput(data=fc3, label=label)

    return mx.mod.Module(symbol=mlp, context=context)


def load_model(model_params_file_name):
    # https://mxnet.apache.org/versions/1.7.0/api/python/docs/api/module/index.html
    # https://mxnet-tqchen.readthedocs.io/en/latest/packages/python/module.html
    mx_model = build_model()
    mx_model.bind(data_shapes=[('data', (BATCH_SIZE, FEATURE_LENGTH))],
                  label_shapes=[('softmax_label', (BATCH_SIZE,))])
    mx_model.load_params("%s" % model_params_file_name)
    return mx_model
