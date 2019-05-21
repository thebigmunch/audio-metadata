__all__ = [
	'ID3v2',
	'ID3v2Frames',
	'ID3v2Header'
]

import struct
from collections import defaultdict

from attr import Factory, attrib, attrs
from bidict import frozenbidict

from .id3v2_frames import *
from .models import Tags
from .tables import ID3Version
from ..exceptions import InvalidFrame, InvalidHeader
from ..structures import DictMixin
from ..utils import DataReader, decode_synchsafe_int


class ID3v2Frames(Tags):
	_v22_FIELD_MAP = frozenbidict({
		'album': 'TAL',
		'albumartist': 'TP2',
		'arranger': 'TP4',
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
		'encodingsettings': 'TSS',
		'genre': 'TCO',
		'grouping': 'TT1',
		'isrc': 'TRC',
		'language': 'TLA',
		'lyricist': 'TXT',
		'lyrics': 'ULT',
		'media': 'TMT',
		'originalalbum': 'TOT',
		'originalartist': 'TOA',
		'originalauthor': 'TOL',
		'originalyear': 'TOR',
		'pictures': 'PIC',
		'playcount': 'CNT',
		'publisher': 'TPB',
		'subtitle': 'TT3',
		'title': 'TT2',
		'tracknumber': 'TRK'
	})

	_v23_FIELD_MAP = frozenbidict({
		'album': 'TALB',
		'albumsort': 'TSOA',
		'albumartist': 'TPE2',
		'albumartistsort': 'TSO2',
		'arranger': 'TPE4',
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
		'encodingsettings': 'TSSE',
		'genre': 'TCON',
		'grouping': 'TIT1',
		'isrc': 'TSRC',
		'language': 'TLAN',
		'lyricist': 'TEXT',
		'lyrics': 'USLT',
		'media': 'TMED',
		'originalalbum': 'TOAL',
		'originalartist': 'TOPE',
		'originalauthor': 'TOLY',
		'originalyear': 'TORY',
		'pictures': 'APIC',
		'playcount': 'PCNT',
		'publisher': 'TPUB',
		'subtitle': 'TIT3',
		'title': 'TIT2',
		'titlesort': 'TSOT',
		'tracknumber': 'TRCK'
	})

	_v24_FIELD_MAP = frozenbidict({
		'album': 'TALB',
		'albumsort': 'TSOA',
		'albumartist': 'TPE2',
		'albumartistsort': 'TSO2',
		'arranger': 'TPE4',
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
		'encodingsettings': 'TSSE',
		'genre': 'TCON',
		'grouping': 'TIT1',
		'isrc': 'TSRC',
		'language': 'TLAN',
		'lyricist': 'TEXT',
		'lyrics': 'USLT',
		'media': 'TMED',
		'mood': 'TMOO',
		'originalalbum': 'TOAL',
		'originalartist': 'TOPE',
		'originalauthor': 'TOLY',
		'originalyear': 'TORY',
		'pictures': 'APIC',
		'playcount': 'PCNT',
		'publisher': 'TPUB',
		'subtitle': 'TIT3',
		'title': 'TIT2',
		'titlesort': 'TSOT',
		'tracknumber': 'TRCK'
	})

	@classmethod
	def load(cls, data, id3_version):
		if not isinstance(data, DataReader):  # pragma: nocover
			data = DataReader(data)

		if id3_version is ID3Version.v22:
			cls.FIELD_MAP = cls._v22_FIELD_MAP

			struct_pattern = '3s3B'
			size_len = 3
			per_byte = 8
		elif id3_version is ID3Version.v23:
			cls.FIELD_MAP = cls._v23_FIELD_MAP

			struct_pattern = '4s4B2B'
			size_len = 4
			per_byte = 8
		elif id3_version is ID3Version.v24:
			cls.FIELD_MAP = cls._v24_FIELD_MAP

			struct_pattern = '4s4B2B'
			size_len = 4
			per_byte = 7
		else:
			raise ValueError(f"Unsupported ID3 version: {id3_version}")

		frames = defaultdict(list)
		while True:
			try:
				frame = ID3v2Frame.load(data, struct_pattern, size_len, per_byte)
			except InvalidFrame:
				break

			# Ignore oddities/bad frames.
			if not isinstance(frame, ID3v2BaseFrame):
				continue

			# TODO: Finish any missing frame types.
			# TODO: Move representation into frame classes?
			if isinstance(
				frame,
				(ID3v2CommentFrame, ID3v2SynchronizedLyricsFrame, ID3v2UnsynchronizedLyricsFrame)
			):
				frames[f'{frame.id}:{frame.description}:{frame.language}'].append(frame.value)
			elif isinstance(frame, ID3v2GenreFrame):
				frames['TCON'] = frame.value
			elif isinstance(frame, ID3v2GEOBFrame):
				frames[f'GEOB:{frame.description}'].append({
					'filename': frame.filename, 'mime_type': frame.mime_type, 'value': frame.value
				})
			elif isinstance(frame, ID3v2PrivateFrame):
				frames[f'PRIV:{frame.owner}'].append(frame.value)
			elif isinstance(frame, (ID3v2UserTextFrame, ID3v2UserURLLinkFrame)):
				frames[f'{frame.id}:{frame.description}'].append(frame.value)
			elif isinstance(
				frame,
				(ID3v2NumericTextFrame, ID3v2TextFrame, ID3v2TimestampFrame)
			):
				frames[frame.id] = frame.value
			else:
				frames[frame.id].append(frame.value)

		return cls(frames)


@attrs(repr=False)
class ID3v2Header(DictMixin):
	_size = attrib()
	version = attrib()
	flags = attrib(default=Factory(DictMixin))

	@classmethod
	def load(cls, data):
		if not isinstance(data, DataReader):  # pragma: nocover
			data = DataReader(data)

		if data.read(3) != b"ID3":
			raise InvalidHeader("Valid ID3v2 header not found.")

		major, revision, _flags, sync_size = struct.unpack('BBB4s', data.read(7))

		try:
			version = ID3Version((2, major))
		except ValueError:
			raise ValueError(f"Unsupported ID3 version (2.{major}).")

		flags = DictMixin()

		flags.unsync = bool((_flags & 128))
		flags.extended = bool((_flags & 64))
		flags.experimental = bool((_flags & 32))
		flags.footer = bool((_flags & 16))

		size = decode_synchsafe_int(sync_size, 7)

		return cls(size, version, flags)


class ID3v2(DictMixin):
	@classmethod
	def load(cls, data):
		if not isinstance(data, DataReader):  # pragma: nocover
			data = DataReader(data)

		if data.peek(3) != b"ID3":
			raise InvalidHeader("Valid ID3v2 header not found.")

		self = cls()
		self._header = ID3v2Header.load(data.read(10))

		if self._header.flags.extended:
			ext_size = decode_synchsafe_int(struct.unpack('4B', data.read(4))[0:4], 7)
			if self._header is ID3Version.v24:
				data.read(ext_size - 4)
			else:
				data.read(ext_size)

		self.tags = ID3v2Frames.load(data.read(self._header._size), self._header.version)
		self.pictures = self.tags.pop('pictures', [])

		return self
