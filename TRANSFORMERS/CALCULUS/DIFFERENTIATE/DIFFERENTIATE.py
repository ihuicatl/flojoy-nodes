from flojoy import flojoy, OrderedPair, Vector
import numpy as np


@flojoy
def DIFFERENTIATE(default: OrderedPair | Vector) -> OrderedPair:
    """
    The DIFFERENTIATE node takes two lists, x and y, as input.

    It then computes the derivative of the array, y, with respect to x.

    Inputs
    ------
    default : OrderedPair|Vector
        Input we use to get the x and y lists to be differentiate.

    Returns
    -------
    OrderedPair
        x : the x-axis of the input.
        y : the result of the derivative.
    """

    match default:
        case OrderedPair():
            input_x = default.x
            input_y = default.y

            if len(input_x) != len(input_y):
                raise ValueError(
                    f" X and Y keys must have the same length, got x of length {len(input_x)} and y {len(input_y)}"
                )

            differentiate = np.diff(input_y) / np.diff(input_x)

            return OrderedPair(x=input_x, y=differentiate)
        case Vector():
            input_x = np.arange((len(default.v) - 1))
            differentiate = np.zeros_like(input_x)

            for i in range(0, len(input_x)):
                differentiate[i] = default.v[i + 1] - default.v[i]

            return OrderedPair(x=input_x, y=differentiate)
