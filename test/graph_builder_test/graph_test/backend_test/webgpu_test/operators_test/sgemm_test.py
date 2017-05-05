from collections import Iterable

from nose.tools import raises

from graph_builder.backend.webgpu.operators.sgemm import Sgemm
from graph_builder.graph.axis import Axis
from graph_builder.graph.variable import Variable
from graph_builder.graph.variables.attributes.order import OrderNHWC, OrderNC


def _convert_to_list(x):
    return x if isinstance(x, Iterable) else (x, x)


def test_sgemm():
    op = Sgemm("sgemm", parameters={
        "M": 10,
        "N": 20,
        "K": 30,
        "out_shape": [1, 10, 4, 5],
        "out_order": OrderNHWC,
        "transpose_A": True,
        "transpose_B": True
    })

    x = Variable((10, 30), OrderNC)
    w = Variable((20, 30), OrderNC)

    y, = op(x, w)

    assert y.axis_order == OrderNHWC
    assert y.shape_dict[Axis.N] == 1
    assert y.shape_dict[Axis.H] == 10
    assert y.shape_dict[Axis.W] == 4
    assert y.shape_dict[Axis.C] == 5


@raises(AssertionError)
def test_sgemm_invalid_A_shape():
    op = Sgemm("sgemm", parameters={
        "M": 10,
        "N": 20,
        "K": 30,
        "out_shape": [1, 10, 4, 5],
        "out_order": OrderNHWC,
        "transpose_A": True,
        "transpose_B": True
    })

    x = Variable((20, 30), OrderNC)
    w = Variable((20, 30), OrderNC)
    y, = op(x, w)


@raises(AssertionError)
def test_sgemm_invalid_B_shape():
    op = Sgemm("sgemm", parameters={
        "M": 10,
        "N": 20,
        "K": 30,
        "out_shape": [1, 10, 4, 5],
        "out_order": OrderNHWC,
        "transpose_A": True,
        "transpose_B": True
    })

    x = Variable((10, 30), OrderNC)
    w = Variable((10, 30), OrderNC)
    y, = op(x, w)


@raises(AssertionError)
def test_sgemm_invalid_C_shape():
    op = Sgemm("sgemm", parameters={
        "M": 10,
        "N": 20,
        "K": 30,
        "out_shape": [1, 2, 3, 4],
        "out_order": OrderNHWC,
        "transpose_A": True,
        "transpose_B": True
    })

    x = Variable((10, 30), OrderNC)
    w = Variable((20, 30), OrderNC)
    y, = op(x, w)
