__all__ = [
	'FLAC', 'FLACApplication', 'FLACCueSheet',
	'FLACCueSheetIndex', 'FLACCueSheetTrack', 'FLACMetadataBlock',
	'FLACPadding', 'FLACSeekPoint', 'FLACSeekTable', 'FLACStreamInfo',
]

import binascii
import struct

from attr import Factory, attrib, attrs

from .models import Format, StreamInfo
from .tables import FLACMetadataBlockType
from .vorbis import VorbisComment, VorbisPicture
from ..exceptions import InvalidHeader
from ..structures import DictMixin, ListMixin
from ..utils import DataReader, bytes_to_int_be, decode_synchsafe_int


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
		if not isinstance(data, DataReader):
			data = DataReader(data)

		id = data.read(4).decode('utf-8', 'replace')  # noqa.
		data = data.read()

		return cls(id, data)


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
		if not isinstance(data, DataReader):
			data = DataReader(data)

		catalog_number = data.read(128).rstrip(b'\0').decode('ascii', 'replace')
		lead_in_samples = bytes_to_int_be(data.read(8))
		compact_disc = bool(bytes_to_int_be(data.read(1)) & 128)

		data.read(258)
		num_tracks = bytes_to_int_be(data.read(1))

		tracks = []
		for i in range(num_tracks):
			offset = bytes_to_int_be(data.read(8))
			track_number = bytes_to_int_be(data.read(1))
			isrc = data.read(12).rstrip(b'\x00').decode('ascii', 'replace')

			flags = bytes_to_int_be(data.read(1))
			type_ = (flags & 128) >> 7
			pre_emphasis = bool(flags & 64)

			data.read(13)
			num_indexes = bytes_to_int_be(data.read(1))

			track = FLACCueSheetTrack(track_number, offset, isrc, type_, pre_emphasis)

			for i in range(num_indexes):
				offset = bytes_to_int_be(data.read(8))
				number = bytes_to_int_be(data.read(1))
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
		if not isinstance(data, DataReader):
			data = DataReader(data)

		return cls(len(data.peek()))


@attrs(repr=False)
class FLACSeekPoint(DictMixin):
	first_sample = attrib()
	offset = attrib()
	num_samples = attrib()

	@classmethod
	def load(cls, data):
		if not isinstance(data, DataReader):
			data = DataReader(data)

		return cls(*struct.unpack('>QQH', data.read()))


class FLACSeekTable(ListMixin):
	item_label = 'seekpoints'

	def __init__(self, items):
		super().__init__(items)

	@classmethod
	def load(cls, data):
		if not isinstance(data, DataReader):
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
	channels = attrib()
	duration = attrib()
	md5 = attrib()
	sample_rate = attrib()

	@classmethod
	def load(cls, data):
		if not isinstance(data, DataReader):
			data = DataReader(data)

		stream_info_block_data = struct.unpack('2s2s3s3s8B16s', data.read(34))

		min_block_size = bytes_to_int_be(stream_info_block_data[0])
		max_block_size = bytes_to_int_be(stream_info_block_data[1])
		min_frame_size = bytes_to_int_be(stream_info_block_data[2])
		max_frame_size = bytes_to_int_be(stream_info_block_data[3])

		sample_rate = bytes_to_int_be(stream_info_block_data[4:7]) >> 4
		channels = ((stream_info_block_data[6] >> 1) & 7) + 1

		bps_start = (stream_info_block_data[6] & 1) << 4
		bps_end = (stream_info_block_data[7] & 240) >> 4

		bit_depth = int(bps_start + bps_end + 1)

		total_samples = bytes_to_int_be(
			[stream_info_block_data[7] & 15] + list(stream_info_block_data[8:12])
		)
		duration = total_samples / sample_rate

		md5sum = binascii.hexlify(stream_info_block_data[12:][0]).decode('ascii', 'replace')

		return cls(
			None, None, min_block_size, max_block_size, min_frame_size,
			max_frame_size, bit_depth, channels, duration, md5sum, sample_rate
		)


class FLAC(Format):
	"""FLAC file format object.

	Extends :class:`Format`.

	Attributes:
		cuesheet (FLACCueSheet): The cuesheet metadata block.
		pictures (list): A list of :class:`VorbisPicture` objects.
		seektable (FLACSeekTable): The seektable metadata block.
		streaminfo (FLACStreamInfo): The audio stream information.
		tags (VorbisComment): The Vorbis comment metadata block.
	"""

	tags_type = VorbisComment

	def __init__(self):
		super().__init__()
		self._blocks = []

	@classmethod
	def load(cls, data):
		self = super()._load(data)

		# Ignore ID3v2 in FLAC.
		if self._obj.peek(3)[0:3] == b'ID3':
			self._obj.seek(5)
			extended = bool((self._obj.read(1)[0] & 64))
			self._obj.read(decode_synchsafe_int(self._obj.read(4), 7))

			if extended:
				ext_size = decode_synchsafe_int(struct.unpack('4B', self._obj.read(4))[0], 7)
				self._obj.read(ext_size)

		if self._obj.read(4) != b'fLaC':
			raise InvalidHeader("Valid FLAC header not found.")

		header_data = self._obj.read(4)

		while len(header_data):
			metadata_block_header = struct.unpack('B3B', header_data)
			block_type = metadata_block_header[0] & 127
			is_last_block = bool(metadata_block_header[0] & 128)

			# There are examples of tools writing incorrect block sizes.
			# The FLAC reference implementation unintentionally (I hope?) parses them.
			# I've chosen not to add special handling for these invalid files.
			# If needed, mutagen (https://github.com/quodlibet/mutagen) may support them.
			size = bytes_to_int_be(metadata_block_header[1:4])
			metadata_block_data = self._obj.read(size)

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
				comment_block = VorbisComment.load(metadata_block_data)
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
				self._blocks.append(FLACMetadataBlock(block_type, size))

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
