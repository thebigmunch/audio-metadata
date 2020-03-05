# http://id3.org/Developer%20Information

__all__ = [
	'ID3v2',
	'ID3v2Flags',
	'ID3v2Frames',
	'ID3v2Header',
]

import struct
import warnings
from collections import defaultdict

from attr import (
	attrib,
	attrs,
)
from tbm_utils import (
	AttrMapping,
	datareader,
)

from .id3v2_frames import *
from .tables import (
	ID3Version,
	ID3v2FrameAliases,
	ID3v2FrameIDs,
	ID3v2UnofficialFrameIDs,
)
from ..exceptions import (
	InvalidFrame,
	InvalidHeader,
)
from ..models import Tags
from ..utils import decode_synchsafe_int
from ..warnings import AudioMetadataWarning

try:
	import bitstruct.c as bitstruct
except ImportError:
	import bitstruct


# Mappings based on https://picard.musicbrainz.org/docs/mappings/
class ID3v2Frames(Tags):
	def __init__(self, mapping=None, *, id3_version=ID3Version.v24, **kwargs):
		self._version = ID3Version(id3_version)

		try:
			self.FIELD_MAP = ID3v2FrameAliases[self._version]
		except KeyError:
			raise ValueError(f"Unsupported ID3 version: {id3_version}")

		super().__init__(mapping, **kwargs)

	@datareader
	@classmethod
	def parse(cls, data, id3_version):
		id3_version = ID3Version(id3_version)
		if id3_version is ID3Version.v22:
			struct_pattern = '3s3B'
			size_len = 3
			per_byte = 8
		elif id3_version is ID3Version.v23:
			struct_pattern = '4s4B2B'
			size_len = 4
			per_byte = 8
		elif id3_version is ID3Version.v24:
			struct_pattern = '4s4B2B'
			size_len = 4
			per_byte = 7
		else:
			raise ValueError(f"Unsupported ID3 version: {id3_version}")  # pragma: nocover

		frames = defaultdict(list)
		while True:
			try:
				frame = ID3v2Frame.parse(data, struct_pattern, size_len, per_byte)
			except InvalidFrame:
				break

			# Ignore oddities/bad frames.
			if frame is None:
				continue

			# Ignore frames not defined in spec for ID3 version.
			# Allow unofficial frames to load (3 character frames only load for ID3v2.2).
			# Warn user and encourage reporting.
			if (
				frame.id not in ID3v2FrameIDs[id3_version]
				and frame.id not in ID3v2UnofficialFrameIDs[id3_version]
			):
				warnings.warn(
					(
						f"Ignoring '{frame.id}' frame with value '{frame.value}'.\n"
						f"'{frame.id}' is not supported in the ID3v2.{id3_version.value[1]} specification.\n"
					),
					AudioMetadataWarning,
				)
				continue

			# TODO: Finish any missing frame types.
			# TODO: Move representation into frame classes?
			if isinstance(
				frame,
				(
					ID3v2GenreFrame,
					ID3v2MappingListFrame,
					ID3v2NumericTextFrame,
					ID3v2TextFrame,
					ID3v2TimestampFrame,
				),
			):
				frames[frame.id] = frame.value
			else:
				frames[frame.id].append(frame.value)

		return cls(frames, id3_version=id3_version)


@attrs(
	repr=False,
	kw_only=True,
)
class ID3v2Flags(AttrMapping):
	unsync = attrib(converter=bool)
	extended = attrib(converter=bool)
	experimental = attrib(converter=bool)
	footer = attrib(converter=bool)


@attrs(
	repr=False,
	kw_only=True,
)
class ID3v2Header(AttrMapping):
	_size = attrib()
	version = attrib()
	flags = attrib(converter=ID3v2Flags.from_mapping)

	def __repr__(self):
		repr_dict = {}

		for k, v in sorted(self.items()):
			if not k.startswith('_'):
				repr_dict[k] = v

		return super().__repr__(repr_dict=repr_dict)

	@datareader
	@classmethod
	def parse(cls, data):
		if data.read(3) != b"ID3":
			raise InvalidHeader("Valid ID3v2 header not found.")

		major, revision, flags_, sync_size = struct.unpack('BBs4s', data.read(7))

		try:
			version = ID3Version((2, major))
		except ValueError:  # pragma: nocover
			raise ValueError(f"Unsupported ID3 version (2.{major}).")

		flags = bitstruct.unpack_dict(
			'b1 b1 b1 b1',
			[
				'unsync',
				'extended',
				'experimental',
				'footer',
			],
			flags_,
		)

		size = decode_synchsafe_int(sync_size, 7)

		return cls(
			size=size,
			version=version,
			flags=flags,
		)


class ID3v2(AttrMapping):
	def __repr__(self):
		repr_dict = {}

		for k, v in sorted(self.items()):
			if not k.startswith('_'):
				repr_dict[k] = v

		return super().__repr__(repr_dict=repr_dict)

	@datareader
	@classmethod
	def parse(cls, data):
		if data.peek(3) != b"ID3":
			raise InvalidHeader("Valid ID3v2 header not found.")

		self = cls()

		self._header = ID3v2Header.parse(data.read(10))
		self._size = 10 + self._header._size

		if self._header.flags.extended:
			ext_size = decode_synchsafe_int(
				struct.unpack('4B', data.read(4))[0:4],
				7,
			)
			self._size += ext_size

			if self._header is ID3Version.v24:
				data.read(ext_size - 4)
			else:
				data.read(ext_size)

		if self._header.flags.footer:
			self._size += 10
			data.read(10)

		self.tags = ID3v2Frames.parse(
			data.read(self._header._size),
			self._header.version,
		)
		self.pictures = self.tags.pop('pictures', [])

		return self
