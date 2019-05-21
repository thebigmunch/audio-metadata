__all__ = [
	'FLAC', 'FLACApplication', 'FLACCueSheet',
	'FLACCueSheetIndex', 'FLACCueSheetTrack', 'FLACMetadataBlock',
	'FLACPadding', 'FLACSeekPoint', 'FLACSeekTable', 'FLACStreamInfo',
]

import binascii
import struct

import bitstruct
from attr import Factory, attrib, attrs

from .id3v2 import ID3v2
from .models import Format, StreamInfo
from .tables import FLACMetadataBlockType
from .vorbis import VorbisComments, VorbisPicture
from ..exceptions import InvalidHeader
from ..structures import DictMixin, ListMixin
from ..utils import DataReader


@attrs(repr=False)
class FLACApplication(DictMixin):
	"""Application metadata block.

	Attributes:
		id (str): The 32-bit application identifier.
		data (bytes): The data defined by the application.
	"""

	id = attrib()  # noqa
	data = attrib()

	def __repr__(self):
		return f"<Application ({self.id})>"

	@classmethod
	def load(cls, data):
		if not isinstance(data, DataReader):  # pragma: nocover
			data = DataReader(data)

		id_ = data.read(4).decode('utf-8', 'replace')
		data = data.read()

		return cls(id_, data)


@attrs(repr=False)
class FLACCueSheetIndex(DictMixin):
	"""A cue sheet track index point.

	Attributes:
		number (int): The index point number.

			The first index in a track must have a number of 0 or 1.

			Index numbers must increase by 1 and be unique within a track.

			For CD-DA, an index number of 0 corresponds to the track pre-gab.

		offset (int): Offset in samples relative to the track offset.
	"""

	number = attrib()
	offset = attrib()


@attrs(repr=False)
class FLACCueSheetTrack(DictMixin):
	"""A FLAC cue sheet track.

	Attributes:
		track_number (int): The track number of the track.

			0 is not allowed to avoid conflicting with the CD-DA spec lead-in track.

			For CD-DA, the track number must be 1-99 or 170 for the lead-out track.

			For non-CD-DA, the track number must be 255 for the lead-out track.

			Track numbers must be unique withint a cue sheet.
		offset (int): Offset in samples relative to the beginning of the FLAC audio stream.
		isrc (str): The ISRC (International Standard Recording Code) of the track.
		type (int): ``0`` for audio, ``1`` for non-audio.
		pre_emphasis (bool): ``True`` if contains pre-emphasis, ``False`` if not.
		indexes (list): The index points for the track as :class:`FLACCueSheetIndex` objects.
	"""

	track_number = attrib()
	offset = attrib()
	isrc = attrib()
	type = attrib()  # noqa
	pre_emphasis = attrib()
	indexes = attrib(default=Factory(list))


class FLACCueSheet(ListMixin):
	"""The cue sheet metadata block.

	A list-like structure of :class:`FLACCueSheetTrack` objects
	along with some information used in the cue sheet.

	Attributes:
		catalog_number (str): The media catalog number.
		lead_in_samples (int): The number of lead-in samples.
			This is only meaningful for CD-DA cuesheets.
			For others, it should be 0.
		compact_disc (bool): ``True`` if the cue sheet corresponds to a compact disc, else ``False``.
	"""

	item_label = 'tracks'

	def __init__(self, tracks, catalog_number, lead_in_samples, compact_disc):
		super().__init__(tracks)
		self.catalog_number = catalog_number
		self.lead_in_samples = lead_in_samples
		self.compact_disc = compact_disc

	@classmethod
	def load(cls, data):
		if not isinstance(data, DataReader):  # pragma: nocover
			data = DataReader(data)

		catalog_number = data.read(128).rstrip(b'\0').decode('ascii', 'replace')
		lead_in_samples = struct.unpack(
			'>Q',
			data.read(8)
		)[0]
		compact_disc = bitstruct.unpack(
			'b1',
			data.read(1)
		)[0]

		data.read(258)
		num_tracks = struct.unpack(
			'B',
			data.read(1)
		)[0]

		tracks = []
		for _ in range(num_tracks):
			offset = struct.unpack(
				'>Q',
				data.read(8)
			)[0]
			track_number = struct.unpack(
				'>B',
				data.read(1)
			)[0]
			isrc = data.read(12).rstrip(b'\x00').decode('ascii', 'replace')

			type_, pre_emphasis = bitstruct.unpack(
				'u1 b1',
				data.read(1)
			)

			data.read(13)
			num_indexes = struct.unpack(
				'>B',
				data.read(1)
			)[0]

			track = FLACCueSheetTrack(track_number, offset, isrc, type_, pre_emphasis)

			for _ in range(num_indexes):
				offset = struct.unpack(
					'>Q',
					data.read(8)
				)[0]

				number = struct.unpack(
					'>B',
					data.read(1)
				)[0]

				data.read(3)

				track.indexes.append(FLACCueSheetIndex(number, offset))

			tracks.append(track)

		return cls(tracks, catalog_number, lead_in_samples, compact_disc)


@attrs(repr=False)
class FLACMetadataBlock(DictMixin):
	type = attrib()  # noqa
	size = attrib()

	def __repr__(self):
		return f"<MetadataBlock [{self.type}] ({self.size} bytes)>"


@attrs(repr=False)
class FLACPadding(DictMixin):
	size = attrib()

	def __repr__(self):
		return f"<Padding ({self.size} bytes)>"

	@classmethod
	def load(cls, data):
		if not isinstance(data, DataReader):  # pragma: nocover
			data = DataReader(data)

		return cls(len(data.peek()))


@attrs(repr=False)
class FLACSeekPoint(DictMixin):
	first_sample = attrib()
	offset = attrib()
	num_samples = attrib()

	@classmethod
	def load(cls, data):
		if not isinstance(data, DataReader):  # pragma: nocover
			data = DataReader(data)

		return cls(*struct.unpack('>QQH', data.read()))


class FLACSeekTable(ListMixin):
	item_label = 'seekpoints'

	def __init__(self, items):
		super().__init__(items)

	@classmethod
	def load(cls, data):
		if not isinstance(data, DataReader):  # pragma: nocover
			data = DataReader(data)

		seekpoints = []
		seekpoint = data.read(18)
		while len(seekpoint) == 18:
			seekpoints.append(FLACSeekPoint.load(seekpoint))
			seekpoint = data.read(18)

		return cls(seekpoints)


@attrs(repr=False)
class FLACStreamInfo(StreamInfo):
	_start = attrib()
	_size = attrib()
	_min_block_size = attrib()
	_max_block_size = attrib()
	_min_frame_size = attrib()
	_max_frame_size = attrib()
	bit_depth = attrib()
	bitrate = attrib()
	channels = attrib()
	duration = attrib()
	md5 = attrib()
	sample_rate = attrib()

	@classmethod
	def load(cls, data):
		if not isinstance(data, DataReader):  # pragma: nocover
			data = DataReader(data)

		stream_info_block_data = bitstruct.unpack(
			'u16 u16 u24 u24 u20 u3 u5 u36 r128',
			data.read(34)
		)

		min_block_size = stream_info_block_data[0]
		max_block_size = stream_info_block_data[1]
		min_frame_size = stream_info_block_data[2]
		max_frame_size = stream_info_block_data[3]
		sample_rate = stream_info_block_data[4]
		channels = stream_info_block_data[5] + 1
		bit_depth = stream_info_block_data[6] + 1
		total_samples = stream_info_block_data[7]
		md5sum = binascii.hexlify(stream_info_block_data[8]).decode('ascii', 'replace')
		duration = total_samples / sample_rate

		return cls(
			None, None, min_block_size, max_block_size,
			min_frame_size, max_frame_size, bit_depth,
			None, channels, duration, md5sum, sample_rate
		)


class FLAC(Format):
	"""FLAC file format object.

	Extends :class:`Format`.

	Attributes:
		cuesheet (FLACCueSheet): The cuesheet metadata block.
		pictures (list): A list of :class:`VorbisPicture` objects.
		seektable (FLACSeekTable): The seektable metadata block.
		streaminfo (FLACStreamInfo): The audio stream information.
		tags (VorbisComments): The Vorbis comment metadata block.
	"""

	tags_type = VorbisComments

	def __init__(self):
		super().__init__()
		self._blocks = []

	@classmethod
	def load(cls, data):
		self = super()._load(data)

		# Ignore ID3v2 in FLAC.
		if self._obj.peek(3) == b'ID3':
			ID3v2.load(self._obj)

		if self._obj.read(4) != b'fLaC':
			raise InvalidHeader("Valid FLAC header not found.")

		header_data = self._obj.read(4)

		while True:
			is_last_block, block_type, block_size = bitstruct.unpack(
				'b1 u7 u24',
				header_data
			)

			# There are examples of tools writing incorrect block sizes.
			# The FLAC reference implementation unintentionally (I hope?) parses them.
			# I've chosen not to add special handling for these invalid files.
			# If needed, mutagen (https://github.com/quodlibet/mutagen) may support them.
			metadata_block_data = self._obj.read(block_size)

			if block_type == FLACMetadataBlockType.STREAMINFO:
				streaminfo_block = FLACStreamInfo.load(metadata_block_data)
				self.streaminfo = streaminfo_block
				self._blocks.append(streaminfo_block)
			elif block_type == FLACMetadataBlockType.PADDING:
				self._blocks.append(FLACPadding.load(metadata_block_data))
			elif block_type == FLACMetadataBlockType.APPLICATION:
				application_block = FLACApplication.load(metadata_block_data)
				self._blocks.append(application_block)
			elif block_type == FLACMetadataBlockType.SEEKTABLE:
				seektable = FLACSeekTable.load(metadata_block_data)
				self.seektable = seektable
				self._blocks.append(seektable)
			elif block_type == FLACMetadataBlockType.VORBIS_COMMENT:
				comment_block = VorbisComments.load(metadata_block_data)
				self.tags = comment_block
				self._blocks.append(comment_block)
			elif block_type == FLACMetadataBlockType.CUESHEET:
				cuesheet_block = FLACCueSheet.load(metadata_block_data)
				self.cuesheet = cuesheet_block
				self._blocks.append(cuesheet_block)
			elif block_type == FLACMetadataBlockType.PICTURE:
				picture = VorbisPicture.load(metadata_block_data)
				self.pictures.append(picture)
				self._blocks.append(picture)
			elif block_type >= 127:
				raise InvalidHeader("FLAC header contains invalid block type.")
			else:
				self._blocks.append(FLACMetadataBlock(block_type, block_size))

			if is_last_block:
				pos = self._obj.tell()
				self.streaminfo._start = pos
				self.streaminfo._size = self.filesize - self.streaminfo._start

				if self.streaminfo.duration > 0:
					self.streaminfo.bitrate = self.streaminfo._size * 8 / self.streaminfo.duration

				break
			else:
				header_data = self._obj.read(4)

		return self
