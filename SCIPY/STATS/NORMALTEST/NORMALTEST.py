from flojoy import OrderedPair, flojoy
import scipy.stats


@flojoy(node_type='default')
def NORMALTEST(
	default: OrderedPair,
	axis: int = 0,
	nan_policy: str = 'propagate',
	) -> OrderedPair:
	'''
		Test whether a sample differs from a normal distribution.
		
		This function tests the null hypothesis that a sample comes
		from a normal distribution.  It is based on D'Agostino and
		Pearson's [1]_, [2]_ test that combines skew and kurtosis to
		produce an omnibus test of normality.
		
	-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
	The parameters of the function in this Flojoy wrapper are given below.
	-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.

	Parameters
	----------
	a : array_like
		The array containing the sample to be tested.
	axis : int or None, optional
		Axis along which to compute test. Default is 0. If None,
		compute over the whole array `a`.
	nan_policy : {'propagate', 'raise', 'omit'}, optional
		Defines how to handle when input contains nan.
	The following options are available (default is 'propagate'):
		
	* 'propagate': returns nan
	* 'raise': throws an error
	* 'omit': performs the calculations ignoring nan values
			'''
	result = OrderedPair(
		x=default.x,
		y=scipy.stats.normaltest(
			a=default.y,
			axis=axis,
			nan_policy=nan_policy,
		)
	)
	return result
