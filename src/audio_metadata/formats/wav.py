__all__ = ['WAV', 'WAVStreamInfo']

import struct

from attr import attrib, attrs

from .id3 import ID3v2, ID3v2Frames
from .models import Format, StreamInfo
from ..exceptions import InvalidFrame, InvalidHeader


@attrs(repr=False)
class WAVStreamInfo(StreamInfo):
	_start = attrib()
	_size = attrib()
	bitrate = attrib()
	channels = attrib()
	duration = attrib()
	sample_rate = attrib()


class WAV(Format):
	"""WAV file format object.

	Extends :class:`Format`.

	Attributes:
		pictures (list): A list of :class:`ID3v2Picture` objects.
		streaminfo (WAVStreamInfo): The audio stream information.
		tags (ID3v2Frames): The ID3v2 tag frames, if present.
	"""

	tags_type = ID3v2Frames

	@classmethod
	def load(cls, data):
		self = super()._load(data)

		chunk_id, chunk_size, format_ = struct.unpack('4sI4s', self._obj.read(12))

		if chunk_id != b'RIFF' or format_ != b'WAVE':
			raise InvalidHeader("Valid WAVE header not found.")

		# TODO: Support other subchunks?
		subchunk_header = self._obj.read(8)
		while len(subchunk_header) == 8:
			subchunk_id, subchunk_size = struct.unpack('4sI', subchunk_header)

			if subchunk_id == b'fmt ':
				audio_format, channels, sample_rate = struct.unpack('HHI', self._obj.read(8))
				byte_rate, block_align, bit_depth = struct.unpack('<IHH', self._obj.read(8))

				bitrate = byte_rate * 8

				self._obj.read(subchunk_size - 16)  # Read through rest of subchunk if not PCM.
			elif subchunk_id == b'self._obj':
				audio_start = self._obj.tell()
				audio_size = subchunk_size
			elif subchunk_id.upper() == b'ID3 ':
				try:
					id3 = ID3v2()
					id3._load(self._obj)
					self._id3 = id3._header
					self.pictures = id3.pictures
					self.tags = id3.tags
				except (InvalidFrame, InvalidHeader):
					self._id3 = None
			else:
				self._obj.read(subchunk_size)

			subchunk_header = self._obj.read(8)

		duration = audio_size / byte_rate

		self.streaminfo = WAVStreamInfo(
			audio_start, audio_size, bitrate, channels, duration, sample_rate
		)

		return self
