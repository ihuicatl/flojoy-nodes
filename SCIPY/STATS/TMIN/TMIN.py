from flojoy import OrderedPair, flojoy
import scipy.stats


@flojoy(node_type='default')
def TMIN(
	default: OrderedPair,
	lowerlimit: None or float,
	axis: int = 0,
	inclusive: bool = True,
	nan_policy: str = 'propagate',
	) -> OrderedPair:
	'''
		Compute the trimmed minimum.
		
		This function finds the miminum value of an array `a` along the
		specified axis, but only considering values greater than a specified
		lower limit.
		
	-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
	The parameters of the function in this Flojoy wrapper are given below.
	-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.

	Parameters
	----------
	a : array_like
		Array of values.
	lowerlimit : None or float, optional
		Values in the input array less than the given limit will be ignored.
		When lowerlimit is None, then all values are used. The default value
		is None.
	axis : int or None, optional
		Axis along which to operate. Default is 0. If None, compute over the
		whole array `a`.
	inclusive : {True, False}, optional
		This flag determines whether values exactly equal to the lower limit
		are included.  The default value is True.
	nan_policy : {'propagate', 'raise', 'omit'}, optional
		Defines how to handle when input contains nan.
	The following options are available (default is 'propagate'):
		
	* 'propagate': returns nan
	* 'raise': throws an error
	* 'omit': performs the calculations ignoring nan values
			'''
	result = OrderedPair(
		x=default.x,
		y=scipy.stats.tmin(
			a=default.y,
			lowerlimit=lowerlimit,
			axis=axis,
			inclusive=inclusive,
			nan_policy=nan_policy,
		)
	)
	return result
