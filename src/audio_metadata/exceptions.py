__all__ = [
	'AudioMetadataException',
	'InvalidBlock',
	'InvalidChunk',
	'InvalidFormat',
	'InvalidFrame',
	'InvalidHeader',
	'UnsupportedFormat'
]


class AudioMetadataException(Exception):
	"""Base exception class."""

	pass


class InvalidBlock(AudioMetadataException):
	"""Exception raised when a FLAC metadata block is invalid."""

	pass


class InvalidChunk(AudioMetadataException):
	"""Exception raised when a WAV chunk is invalid."""

	pass


class InvalidFormat(AudioMetadataException):
	"""Exception raised when a file format is invalid."""

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
