__all__ = ['load', 'loads']

import os

from .exceptions import UnsupportedFormat
from .formats import determine_format


def load(f):
	"""Load audio metadata from filepath or file-like object.

	Parameters:
		f (os.PathLike or file-like object): A filepath or file-like object of an audio file.

	Returns:
		Format: An audio format object.

	Raises:
		UnsupportedFormat: If file is not of a supported format.
		ValueError: If filepath/file-like object is not valid nor readable.
	"""

	if isinstance(f, (os.PathLike, str)):
		fileobj = open(f, 'rb')
	else:
		try:
			f.read(0)
		except AttributeError:
			raise ValueError("Not a valid file-like object.")
		except Exception:
			raise ValueError("Can't read from file-like object.")

		fileobj = f

	parser_cls = determine_format(fileobj.read(4), os.path.splitext(fileobj.name)[1])

	if parser_cls is None:
		raise UnsupportedFormat("Supported format signature not found.")
	else:
		fileobj.seek(0, os.SEEK_SET)

	return parser_cls.load(fileobj)


def loads(b):
	"""Load audio metadata from filepath or file-like object.

	Parameters:
		b (bytes-like object): A bytes-like object of an audio file.

	Returns:
		Format: An audio format object.

	Raises:
		UnsupportedFormat: If file is not of a supported format.
	"""

	parser_cls = determine_format(b[0:4])

	if parser_cls is None:
		raise UnsupportedFormat("Supported format signature not found.")

	return parser_cls.load(b)
