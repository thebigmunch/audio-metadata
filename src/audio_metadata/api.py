__all__ = [
	'determine_format',
	'load',
	'loads'
]

import os
from io import BufferedReader, FileIO

from .exceptions import InvalidFormat, UnsupportedFormat
from .formats import FLAC, MP3, WAV, ID3v2, MP3StreamInfo
from .utils import DataReader


def determine_format(data, extension=None):
	"""Determine the format of an audio file.

	Parameters:
		data (bytes-like object, str, os.PathLike, or file-like object):
			A bytes-like object, filepath, path-like object
			or file-like object of an audio file.
		extension (str): The file extension of the file.
			Used as a tie-breaker for formats that can
			be used in multiple containers (e.g. ID3).

	Returns:
		Format: An audio format class if supported, else None.
	"""

	if extension and not extension.endswith(('flac', 'mp3', 'wav')):
		return None

	if not isinstance(data, DataReader):
		try:
			data = DataReader(data)
		except AttributeError:
			return None

	data.seek(0, os.SEEK_SET)
	d = data.read(4)

	if (
		d.startswith(b'\xFF\xFB')
		or (
			extension
			and extension.lower().endswith('mp3')
		)
	):
		return MP3

	if (
		d.startswith(b'fLaC')
		or (
			extension
			and extension.lower().endswith('flac')
		)
	):
		return FLAC

	if (
		d.startswith(b'RIFF')
		or (
			extension
			and extension.lower().endswith('wav')
		)
	):
		return WAV

	if d.startswith(b'ID3'):
		data.seek(0)
		ID3v2.load(data)

		if data.peek(4) == b'fLaC':
			return FLAC
		elif data.peek(2) == b'\xFF\xFB':
			return MP3
		else:
			try:
				frames = MP3StreamInfo.find_mp3_frames(data)
			except InvalidFormat:
				return None
			else:
				return MP3 if frames else None

	return None


def load(f):
	"""Load audio metadata from filepath or file-like object.

	Parameters:
		f (str, os.PathLike, or file-like object):
			A filepath, path-like object or file-like object of an audio file.

	Returns:
		Format: An audio format object.

	Raises:
		UnsupportedFormat: If file is not of a supported format.
		ValueError: If filepath/file-like object is not valid or readable.
	"""

	if (
		not isinstance(f, (os.PathLike, str))
		and not (
			isinstance(f, BufferedReader)
			and isinstance(f.raw, FileIO)
		)
	):
		raise ValueError("Not a valid filepath or file-like object.")

	data = DataReader(f)

	parser_cls = determine_format(data, os.path.splitext(data.name)[1])

	if parser_cls is None:
		raise UnsupportedFormat("Supported format signature not found.")
	else:
		data.seek(0, os.SEEK_SET)

	return parser_cls.load(data)


def loads(b):
	"""Load audio metadata from a bytes-like object.

	Parameters:
		b (bytes-like object): A bytes-like object of an audio file.

	Returns:
		Format: An audio format object.

	Raises:
		UnsupportedFormat: If file is not of a supported format.
	"""

	try:
		memoryview(b)
	except TypeError:
		raise ValueError("Not a valid bytes-like object.")

	data = DataReader(b)

	parser_cls = determine_format(data)

	if parser_cls is None:
		raise UnsupportedFormat("Supported format signature not found.")
	else:
		data.seek(0, os.SEEK_SET)

	return parser_cls.load(data)
