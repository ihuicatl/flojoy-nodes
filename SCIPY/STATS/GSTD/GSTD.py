from flojoy import OrderedPair, flojoy
import scipy.stats


@flojoy(node_type='default')
def GSTD(
	default: OrderedPair,
	axis: int = 0,
	ddof: int = 1,
	) -> OrderedPair:
	'''
		
		Calculate the geometric standard deviation of an array.
		
		The geometric standard deviation describes the spread of a set of numbers
		where the geometric mean is preferred. It is a multiplicative factor, and
		so a dimensionless quantity.
		
		It is defined as the exponent of the standard deviation of ``log(a)``.
		Mathematically the population geometric standard deviation can be
	evaluated as::
		
		gstd = exp(std(log(a)))
		
	.. versionadded:: 1.3.0
		
	-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
	The parameters of the function in this Flojoy wrapper are given below.
	-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.

	Parameters
	----------
	a : array_like
		An array like object containing the sample data.
	axis : int, tuple or None, optional
		Axis along which to operate. Default is 0. If None, compute over
		the whole array `a`.
	ddof : int, optional
		Degree of freedom correction in the calculation of the
		geometric standard deviation. Default is 1.
			'''
	result = OrderedPair(
		x=default.x,
		y=scipy.stats.gstd(
			a=default.y,
			axis=axis,
			ddof=ddof,
		)
	)
	return result
