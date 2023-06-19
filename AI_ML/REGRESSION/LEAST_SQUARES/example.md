In this example, two`LINSPACE` each generates an array of 1000 samples.

One of the array is passed down to 'RAND' node which randomizes the data points.

Two ordered_pairs are passed down to 'LEAST SQUARES' which calculates the coefficients that minimize the errors
from all the data points. Then for the simplicity of plotting, the initial X matrix from first linspace is multiplied
to the coefficients so that the line is drawn and it can be passed as ordered_pair with X.