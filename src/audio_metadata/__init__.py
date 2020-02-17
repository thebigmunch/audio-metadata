import sys
import warnings

from .__about__ import *
from .api import *
from .exceptions import *
from .formats import *
from .models import *

__all__ = [
	*__about__.__all__,
	*api.__all__,
	*exceptions.__all__,
	*formats.__all__,
	*models.__all__,
]


# Override warning output format.
def showwarning(message, category, filename, lineno, file=None, line=None):
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
