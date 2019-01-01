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
from ..exceptions import InvalidFrame, InvalidHeader
from ..structures import DictMixin
from ..utils import DataReader, decode_synchsafe_int


class ID3v2Frames(Tags):
	FIELD_MAP = frozenbidict({
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
		'bpm': 'TBPM', 'comment': 'COMM',
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
		'mood': 'TMOO',
		'originalalbum': 'TOAL',
		'originalartist': 'TOPE',
		'originalauthor': 'TOLY',
		'originalyear': 'TORY',
		'pictures': 'APIC',
		'playcount': 'PCNT',
		'publisher': 'TPUB',
		'recordingdates': 'TRDA',
		'subtitle': 'TSST',
		'time': 'TIME',
		'title': 'TIT2',
		'titlesort': 'TSOT',
		'tracknumber': 'TRCK'
	})

	def __init__(self, *args, **kwargs):
		self.update(*args, **kwargs)

	@classmethod
	def load(cls, data, id3_version):
		if not isinstance(data, DataReader):
			data = DataReader(data)

		if id3_version[1] == 2:
			struct_pattern = '3s3B'
			size_len = 3
			per_byte = 8
		elif id3_version[1] == 3:
			struct_pattern = '4s4B2B'
			size_len = 4
			per_byte = 8
		elif id3_version[1] == 4:
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
		if not isinstance(data, DataReader):
			data = DataReader(data)

		if data.read(3) != b"ID3":
			raise InvalidHeader("Valid ID3v2 header not found.")

		major, revision, _flags, sync_size = struct.unpack('BBB4s', data.read(7))

		version = (2, major, revision)

		if version[1] not in [2, 3, 4]:
			raise ValueError("Unsupported ID3 version.")

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
		if not isinstance(data, DataReader):
			data = DataReader(data)

		if data.peek(3) != b"ID3":
			raise InvalidHeader("Valid ID3v2 header not found.")

		self = cls()
		self._header = ID3v2Header.load(data.read(10))

		if self._header.flags.extended:
			ext_size = decode_synchsafe_int(struct.unpack('4B', data.read(4))[0:4], 7)
			if self._header.version[1] == 4:
				data.read(ext_size - 4)
			else:
				data.read(ext_size)

		self.tags = ID3v2Frames.load(data.read(self._header._size), self._header.version)
		self.pictures = self.tags.pop('pictures', [])

		return self
