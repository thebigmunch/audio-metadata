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
from bidict import frozenbidict
from tbm_utils import AttrMapping

from .id3v2_frames import *
from .tables import (
	ID3Version,
	ID3v2FrameIDs,
)
from ..exceptions import (
	InvalidFrame,
	InvalidHeader,
)
from ..models import Tags
from ..utils import (
	datareader,
	decode_synchsafe_int,
)

try:  # pragma: nocover
	import bitstruct.c as bitstruct
except ImportError:  # pragma: nocover
	import bitstruct


# Mappings used: https://picard.musicbrainz.org/docs/mappings/
class ID3v2Frames(Tags):
	_v22_FIELD_MAP = frozenbidict(
		{
			'album': 'TAL',
			'albumartist': 'TP2',
			'artist': 'TP1',
			'audiodelay': 'TDY',
			'audiolength': 'TLE',
			'audiosize': 'TSI',
			'bpm': 'TBP',
			'comment': 'COM',
			'composer': 'TCM',
			'conductor': 'TP3',
			'copyright': 'TCR',
			'date': 'TYE',
			'discnumber': 'TPA',
			'encodedby': 'TEN',
			'encodersettings': 'TSS',
			'genre': 'TCO',
			'grouping': 'TT1',
			'isrc': 'TRC',
			'label': 'TPB',
			'language': 'TLA',
			'lyricist': 'TXT',
			'lyrics': 'ULT',
			'media': 'TMT',
			'originalalbum': 'TOT',
			'originalartist': 'TOA',
			'originalauthor': 'TOL',
			'originaldate': 'TOR',
			'pictures': 'PIC',
			'playcount': 'CNT',
			'remixer': 'TP4',
			'subtitle': 'TT3',
			'title': 'TT2',
			'tracknumber': 'TRK',
		},
	)

	_v23_FIELD_MAP = frozenbidict(
		{
			'album': 'TALB',
			'albumsort': 'TSOA',
			'albumartist': 'TPE2',
			'albumartistsort': 'TSO2',
			'artist': 'TPE1',
			'artistsort': 'TSOP',
			'audiodelay': 'TDLY',
			'audiolength': 'TLEN',
			'audiosize': 'TSIZ',
			'bpm': 'TBPM',
			'comment': 'COMM',
			'compilation': 'TCMP',
			'composer': 'TCOM',
			'composersort': 'TSOC',
			'conductor': 'TPE3',
			'copyright': 'TCOP',
			'date': 'TYER',
			'discnumber': 'TPOS',
			'encodedby': 'TENC',
			'encodersettings': 'TSSE',
			'genre': 'TCON',
			'grouping': 'TIT1',
			'isrc': 'TSRC',
			'label': 'TPUB',
			'language': 'TLAN',
			'lyricist': 'TEXT',
			'lyrics': 'USLT',
			'media': 'TMED',
			'originalalbum': 'TOAL',
			'originalartist': 'TOPE',
			'originalauthor': 'TOLY',
			'originaldate': 'TORY',
			'pictures': 'APIC',
			'playcount': 'PCNT',
			'remixer': 'TPE4',
			'subtitle': 'TIT3',
			'title': 'TIT2',
			'titlesort': 'TSOT',
			'tracknumber': 'TRCK',
		},
	)

	_v24_FIELD_MAP = frozenbidict(
		{
			'album': 'TALB',
			'albumsort': 'TSOA',
			'albumartist': 'TPE2',
			'albumartistsort': 'TSO2',
			'artist': 'TPE1',
			'artistsort': 'TSOP',
			'audiodelay': 'TDLY',
			'audiolength': 'TLEN',
			'audiosize': 'TSIZ',
			'bpm': 'TBPM',
			'comment': 'COMM',
			'compilation': 'TCMP',
			'composer': 'TCOM',
			'composersort': 'TSOC',
			'conductor': 'TPE3',
			'copyright': 'TCOP',
			'date': 'TDRC',
			'discnumber': 'TPOS',
			'encodedby': 'TENC',
			'encodersettings': 'TSSE',
			'genre': 'TCON',
			'grouping': 'TIT1',
			'isrc': 'TSRC',
			'label': 'TPUB',
			'language': 'TLAN',
			'lyricist': 'TEXT',
			'lyrics': 'USLT',
			'media': 'TMED',
			'mood': 'TMOO',
			'originalalbum': 'TOAL',
			'originalartist': 'TOPE',
			'originalauthor': 'TOLY',
			'originaldate': 'TDOR',
			'pictures': 'APIC',
			'playcount': 'PCNT',
			'remixer': 'TPE4',
			'subtitle': 'TIT3',
			'title': 'TIT2',
			'titlesort': 'TSOT',
			'tracknumber': 'TRCK',
		},
	)

	def __init__(self, mapping=None, *, id3_version=ID3Version.v24, **kwargs):
		self._version = ID3Version(id3_version)

		if self._version is ID3Version.v22:
			self.FIELD_MAP = ID3v2Frames._v22_FIELD_MAP
		elif self._version is ID3Version.v23:
			self.FIELD_MAP = ID3v2Frames._v23_FIELD_MAP
		elif self._version is ID3Version.v24:
			self.FIELD_MAP = ID3v2Frames._v24_FIELD_MAP
		else:
			raise ValueError(f"Unsupported ID3 version: {id3_version}")

		super().__init__(mapping, **kwargs)

	@datareader
	@classmethod
	def load(cls, data, id3_version):
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
				frame = ID3v2Frame.load(data, struct_pattern, size_len, per_byte)
			except InvalidFrame:
				break

			# Ignore oddities/bad frames.
			if frame is None:
				continue

			# TODO: Handle commonly seen frames like from iTunes.
			# Ignore frames not defined in spec for ID3 version.
			# Warn user and encourage reporting.
			if frame.id not in ID3v2FrameIDs[id3_version]:
				warnings.warn(
					f"Ignoring '{frame.id}' frame with value '{frame.value}'.\n"
					f"'{frame.id}' is not supported in the ID3v2.{id3_version.value[1]} specification.\n"
				)
				continue

			# TODO: Finish any missing frame types.
			# TODO: Move representation into frame classes?
			if isinstance(
				frame,
				(
					ID3v2CommentFrame,
					ID3v2SynchronizedLyricsFrame,
					ID3v2UnsynchronizedLyricsFrame,
				),
			):
				frames[f'{frame.id}:{frame.description}:{frame.language}'].append(frame.value)
			elif isinstance(frame, ID3v2GenreFrame):
				frames['TCON'] = frame.value
			elif isinstance(frame, ID3v2GEOBFrame):
				frames[f'GEOB:{frame.description}'].append(
					{

						'filename': frame.filename,
						'mime_type': frame.mime_type,
						'value': frame.value,
					},
				)
			elif isinstance(frame, ID3v2PrivateFrame):
				frames[f'PRIV:{frame.owner}'].append(frame.value)
			elif isinstance(
				frame,
				(
					ID3v2UserTextFrame,
					ID3v2UserURLLinkFrame,
				),
			):
				frames[f'{frame.id}:{frame.description}'].append(frame.value)
			elif isinstance(
				frame,
				(
					ID3v2NumericTextFrame,
					ID3v2TextFrame,
					ID3v2TimestampFrame,
				),
			):
				frames[frame.id] = frame.value
			else:
				frames[frame.id].append(frame.value)

		return cls(frames, id3_version=id3_version)


@attrs(repr=False)
class ID3v2Flags(AttrMapping):
	unsync = attrib(converter=bool)
	extended = attrib(converter=bool)
	experimental = attrib(converter=bool)
	footer = attrib(converter=bool)


@attrs(repr=False)
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
	def load(cls, data):
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

		return cls(size, version, flags)


class ID3v2(AttrMapping):
	def __repr__(self):
		repr_dict = {}

		for k, v in sorted(self.items()):
			if not k.startswith('_'):
				repr_dict[k] = v

		return super().__repr__(repr_dict=repr_dict)

	@datareader
	@classmethod
	def load(cls, data):
		if data.peek(3) != b"ID3":
			raise InvalidHeader("Valid ID3v2 header not found.")

		self = cls()

		self._header = ID3v2Header.load(data.read(10))
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

		self.tags = ID3v2Frames.load(
			data.read(self._header._size),
			self._header.version,
		)
		self.pictures = self.tags.pop('pictures', [])

		return self
