import mxnet as mx

import features as ft


def build_model(context=mx.cpu()):

    data = mx.sym.var('data')
    label = mx.sym.var('softmax_label')

    fc2 = mx.sym.FullyConnected(data=data, num_hidden=32)
    fc2 = mx.sym.Activation(data=fc2, act_type="relu")

    fc3 = mx.sym.FullyConnected(data=fc2, num_hidden=ft.MAX_OUT_DEGREE)
    mlp = mx.sym.SoftmaxOutput(data=fc3, label=label)

    return mx.mod.Module(symbol=mlp, context=context)

