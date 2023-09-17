import numpy as np
from flojoy import flojoy, Vector


@flojoy
def DECIMATE_VECTOR(
    default: Vector,
    factor: int = 1,
) -> Vector:
    """The DECIMATE_VECTOR node returns the input vector where
    the elements are in the reverse order

    Inputs
    ------
    default : Vector
        The input vector

    Parameters
    ----------
    factor : int
        Decimate factor which determines how many elements will be skipped 
        between each selected element in the output vector

    Returns
    -------
    Vector
        Decimated vector
    """
    
    return Vector(v=default.v[::factor])
