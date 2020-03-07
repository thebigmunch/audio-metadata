__all__ = [
	'AudioMetadataException',
	'InvalidBlock',
	'InvalidChunk',
	'InvalidComment',
	'InvalidFormat',
	'InvalidFrame',
	'InvalidHeader',
	'UnsupportedFormat',
]


class AudioMetadataException(Exception):
	"""Base exception class."""


class InvalidBlock(AudioMetadataException):
	"""Exception raised when a FLAC metadata block is invalid."""


class InvalidComment(AudioMetadataException):
	"""Exception raised when a Vorbis comment is invalid."""


class InvalidChunk(AudioMetadataException):
	"""Exception raised when a WAV chunk is invalid."""


class InvalidFormat(AudioMetadataException):
	"""Exception raised when a file format is invalid."""


class InvalidFrame(AudioMetadataException):
	"""Exception raised when an ID3v2 frame is invalid."""


class InvalidHeader(AudioMetadataException):
	"""Exception raised when a metadata header is invalid."""


class UnsupportedFormat(AudioMetadataException):
	"""Exception raised when loading a file that isn't supported."""
