import numpy as np
from flojoy import flojoy, DataContainer


@flojoy
def CONSTANT(dc_inputs, params):
    """Generates a single x-y vector of numeric (floating point) constants"""

    if dc_inputs.__len__() > 0:
        x = dc_inputs[0].y
        y = np.full(len(x), float(params["constant"]))
        return DataContainer(x=x, y=y)

    x = list()
    for i in range(1000):
        x.append(i)
    y = np.full(1000, float(params["constant"]))

    return DataContainer(x=x, y=y)