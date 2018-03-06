__all__ = [
	'AudioMetadataException', 'InvalidHeader', 'InvalidFrame', 'UnsupportedFormat'
]


class AudioMetadataException(Exception):
	"""Base exception class."""

	pass


class InvalidFrame(AudioMetadataException):
	"""Exception raised when a metadata frame is invalid."""

	pass


class InvalidHeader(AudioMetadataException):
	"""Exception raised when a metadata header is invalid."""

	pass


class UnsupportedFormat(AudioMetadataException):
	"""Exception raised when loading a file that isn't supported."""

	pass
