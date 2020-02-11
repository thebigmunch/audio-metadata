def strip_repr(obj):
	return repr(obj).replace(
		'\r\n', ''
	).replace(
		'\n', ''
	).replace(
		'\r', ''
	).replace(
		',    ', ', '
	).replace(
		'    ', ''
	)
