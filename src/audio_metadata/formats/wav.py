# http://soundfile.sapp.org/doc/WaveFormat/
# http://www-mmsp.ece.mcgill.ca/Documents/AudioFormats/WAVE/WAVE.html

__all__ = [
	'RIFFTags',
	'WAV',
	'WAVStreamInfo',
]

import os
import struct

from attr import (
	attrib,
	attrs,
)
from bidict import frozenbidict

from .id3v2 import ID3v2
from ..exceptions import (
	InvalidChunk,
	InvalidFrame,
	InvalidHeader,
)
from ..models import (
	Format,
	StreamInfo,
	Tags,
)
from ..utils import datareader


# https://www.recordingblogs.com/wiki/list-chunk-of-a-wave-file
class RIFFTags(Tags):
	FIELD_MAP = frozenbidict(
		{
			'album': 'IPRD',
			'artist': 'IART',
			'comment': 'ICMT',
			'copyright': 'ICOP',
			'date': 'ICRD',
			'encodedby': 'IENC',
			'genre': 'IGNR',
			'language': 'ILNG',
			'rating': 'IRTD',
			'title': 'INAM',
			'tracknumber': 'ITRK',
		},
	)

	@datareader
	@classmethod
	def load(cls, data):
		if data.read(4) != b'INFO':
			raise InvalidChunk('Valid RIFF INFO chunk not found.')

		fields = {}

		field = data.read(4)
		while len(field):
			size = struct.unpack('I', data.read(4))[0]
			value = data.read(size).strip(b'\x00').decode('utf-8')
			fields[field.decode('utf-8')] = [value]

			b = data.read(1)
			while b == b'\x00':
				b = data.read(1)

			if b:
				data.seek(-1, os.SEEK_CUR)

			field = data.read(4)

		return cls(fields)


@attrs(repr=False)
class WAVStreamInfo(StreamInfo):
	_start = attrib()
	_size = attrib()
	bit_depth = attrib()
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
		tags (ID3v2Frames or RIFFTags): The ID3v2 or RIFF tags, if present.
	"""

	tags_type = RIFFTags

	@classmethod
	def load(cls, data):
		self = super()._load(data)

		chunk_id = self._obj.read(4)

		# chunk_size
		self._obj.read(4)

		format_ = self._obj.read(4)

		if chunk_id != b'RIFF' or format_ != b'WAVE':
			raise InvalidHeader("Valid WAVE header not found.")

		subchunk_header = self._obj.read(8)
		while len(subchunk_header) == 8:
			subchunk_id, subchunk_size = struct.unpack(
				'4sI',
				subchunk_header,
			)

			if subchunk_id == b'fmt ':
				audio_format, channels, sample_rate = struct.unpack(
					'HHI',
					self._obj.read(8),
				)

				byte_rate, block_align, bit_depth = struct.unpack(
					'<IHH',
					self._obj.read(8),
				)

				bitrate = byte_rate * 8

				self._obj.read(subchunk_size - 16)  # Read through rest of subchunk if not PCM.
			elif subchunk_id == b'data':
				audio_start = self._obj.tell()
				audio_size = subchunk_size
				self._obj.seek(subchunk_size, os.SEEK_CUR)
			elif (
				subchunk_id == b'LIST'
				and self._obj.peek(4) == b'INFO'
			):
				self._riff = RIFFTags.load(self._obj.read(subchunk_size))
			elif subchunk_id.lower() == b'id3 ':
				try:
					id3 = ID3v2.load(self._obj)
				except (InvalidFrame, InvalidHeader):
					raise
				else:
					self._id3 = id3
			else:
				# TODO
				self._obj.seek(subchunk_size, os.SEEK_CUR)  # pragma: nocover

			subchunk_header = self._obj.read(8)

		if '_id3' in self:
			self.pictures = self._id3.pictures
			self.tags = self._id3.tags
		elif '_riff' in self:
			self.tags = self._riff

		try:
			duration = audio_size / byte_rate

			self.streaminfo = WAVStreamInfo(
				audio_start,
				audio_size,
				bit_depth,
				bitrate,
				channels,
				duration,
				sample_rate,
			)
		except UnboundLocalError:
			raise InvalidHeader("Valid WAVE stream info not found.")

		self._obj.close()

		return self
