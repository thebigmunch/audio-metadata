__all__ = [
	'AudioMetadataWarning'
]

import sys
import warnings


# Override warning output format.
def showwarning(message, category, filename, lineno, file=None, line=None):  # pragma: nocover
	if file is None:
		file = sys.stderr
		if file is None:
			return

	delim = '\n    '
	nl = '\n'
	s = f"{category.__name__}:{delim}{delim.join(line for line in str(message).split(nl))}\n"

	try:
		file.write(s)
	except (IOError, UnicodeError):
		pass


warnings.showwarning = showwarning
del showwarning


class AudioMetadataWarning(UserWarning):
	pass
