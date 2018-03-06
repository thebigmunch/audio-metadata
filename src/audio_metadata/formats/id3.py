__all__ = [
	'ID3v2', 'ID3v2Frame', 'ID3v2Frames', 'ID3v2Header', 'ID3v2Picture'
]

# TODO: ID3v2.

import re
import struct
from codecs import BOM_UTF16_BE, BOM_UTF16_LE
from collections import defaultdict
from urllib.parse import unquote

from attr import Factory, attrib, attrs
from bidict import frozenbidict

from .models import Picture, Tags
from .tables import ID3PictureType, ID3v1Genres
from ..exceptions import InvalidFrame, InvalidHeader
from ..structures import DictMixin
from ..utils import DataReader, decode_synchsafe_int, get_image_size


_genre_re = re.compile(r"((?:\((?P<id>\d+|RX|CR)\))*)(?P<name>.+)?")


def _determine_encoding(b):
	first = b[0:1]

	if first == b'\x00':
		encoding = 'iso-8859-1'
	elif first == b'\x01':
		encoding = 'utf-16-be' if b[1:3] == b'\xfe\xff' else 'utf-16-le'
	elif first == b'\x02':
		encoding = 'utf-16-be'
	elif first == b'\x03':
		encoding = 'utf-8'
	else:
		encoding = 'iso-8859-1'

	return encoding


def _decode_bytestring(b, encoding='iso-8859-1'):
	if not b:
		return ''

	if encoding.startswith('utf-16'):
		if len(b) % 2 != 0 and b[-1:] == b'\x00':
			b = b[:-1]

		if b.startswith(BOM_UTF16_BE):
			b = b[len(BOM_UTF16_BE):]
		elif b.startswith(BOM_UTF16_LE):
			b = b[len(BOM_UTF16_LE):]

	return b.decode(encoding).rstrip('\x00')


def _split_encoded(data, encoding):
	try:
		if encoding in ['iso-8859-1', 'utf-8']:
			head, tail = data.split(b'\x00', 1)
		else:
			if len(data) % 2 != 0:
				data += b'\x00'

			head, tail = data.split(b'\x00\x00', 1)

			if len(head) % 2 != 0:
				head, tail = data.split(b'\x00\x00\x00', 1)
				head += b'\x00'
	except ValueError:
		return (data,)

	return head, tail


class ID3v2Picture(Picture):
	def __init__(self, **kwargs):
		self.update(**kwargs)

	@classmethod
	def load(cls, data):
		if not isinstance(data, DataReader):
			data = DataReader(data)

		data = data.read()

		encoding = _determine_encoding(data[0:1])
		mime_start = 1
		mime_end = data.index(b'\x00', 1)
		mime_type = _decode_bytestring(data[mime_start:mime_end])

		type = ID3PictureType(data[mime_end + 1])  # noqa

		desc_start = mime_end + 2
		description, image_data = _split_encoded(data[desc_start:], encoding)
		description = _decode_bytestring(description, encoding)
		width, height = get_image_size(image_data)

		return cls(
			type=type, mime_type=mime_type, description=description,
			width=width, height=height, data=image_data
		)


@attrs(repr=False)
class ID3v2BaseFrame(DictMixin):
	id = attrib()  # noqa


@attrs(repr=False)
class ID3v2CommentFrame(ID3v2BaseFrame):
	language = attrib()
	description = attrib()
	value = attrib()


@attrs(repr=False)
class ID3v2GenreFrame(ID3v2BaseFrame):
	value = attrib()


@attrs(repr=False)
class ID3v2GEOBFrame(ID3v2BaseFrame):
	mime_type = attrib()
	filename = attrib()
	description = attrib()
	value = attrib()


@attrs(repr=False)
class ID3v2NumberFrame(ID3v2BaseFrame):
	value = attrib()

	@property
	def number(self):
		return self.value.split('/')[0]

	@property
	def total(self):
		try:
			tot = self.value.split('/')[1]
		except IndexError:
			tot = None

		return tot


@attrs(repr=False)
class ID3v2NumericTextFrame(ID3v2BaseFrame):
	value = attrib()


@attrs(repr=False)
class ID3v2PictureFrame(ID3v2BaseFrame):
	value = attrib(converter=ID3v2Picture.load)


@attrs(repr=False)
class ID3v2PrivateFrame(ID3v2BaseFrame):
	owner = attrib()
	value = attrib()


@attrs(repr=False)
class ID3v2SynchronizedLyricsFrame(ID3v2BaseFrame):
	language = attrib()
	timestamp_format = attrib()
	description = attrib()
	value = attrib()


@attrs(repr=False)
class ID3v2TextFrame(ID3v2BaseFrame):
	value = attrib()


@attrs(repr=False)
class ID3v2UnsynchronizedLyricsFrame(ID3v2BaseFrame):
	language = attrib()
	description = attrib()
	value = attrib()


@attrs(repr=False)
class ID3v2URLLinkFrame(ID3v2BaseFrame):
	value = attrib()


@attrs(repr=False)
class ID3v2UserURLLinkFrame(ID3v2BaseFrame):
	description = attrib()
	value = attrib()


@attrs(repr=False)
class ID3v2UserTextFrame(ID3v2BaseFrame):
	description = attrib()
	value = attrib()


@attrs(repr=False)
class ID3v2Frame(ID3v2BaseFrame):
	value = attrib()

	# TODO: SYLT/USLT. TMED. PCNT. TDRC.
	# TODO: ID3v2.2.
	_FRAME_TYPES = {
		# Complex Text Frames
		'COMM': ID3v2CommentFrame, 'GEOB': ID3v2GEOBFrame, 'PRIV': ID3v2PrivateFrame, 'TXXX': ID3v2UserTextFrame,
		# Genre Frame
		'TCON': ID3v2GenreFrame,
		# Lyrics Frames
		'SYLT': ID3v2SynchronizedLyricsFrame, 'USLT': ID3v2UnsynchronizedLyricsFrame,
		# Number Frames
		'TPOS': ID3v2NumberFrame, 'TRCK': ID3v2NumberFrame,
		# Numeric Text Frames
		'TBPM': ID3v2NumericTextFrame, 'TDLY': ID3v2NumericTextFrame, 'TLEN': ID3v2NumericTextFrame,
		'TSIZ': ID3v2NumericTextFrame, 'TYER': ID3v2NumericTextFrame,
		# Picture Frames
		'APIC': ID3v2PictureFrame,
		# Text Frames
		'TAL': ID3v2TextFrame, 'TALB': ID3v2TextFrame, 'TCMP': ID3v2TextFrame, 'TCOM': ID3v2TextFrame, 'TCOP': ID3v2TextFrame,
		'TENC': ID3v2TextFrame, 'TEXT': ID3v2TextFrame, 'TIME': ID3v2TextFrame, 'TIT1': ID3v2TextFrame,
		'TIT2': ID3v2TextFrame, 'TIT3': ID3v2TextFrame, 'TKEY': ID3v2TextFrame, 'TLAN': ID3v2TextFrame,
		'TMOO': ID3v2TextFrame, 'TOAL': ID3v2TextFrame, 'TOLY': ID3v2TextFrame, 'TOPE': ID3v2TextFrame,
		'TORY': ID3v2TextFrame, 'TPE1': ID3v2TextFrame, 'TPE2': ID3v2TextFrame, 'TPE3': ID3v2TextFrame,
		'TPE4': ID3v2TextFrame, 'TPUB': ID3v2TextFrame, 'TRDA': ID3v2TextFrame, 'TSO2': ID3v2TextFrame,
		'TSOA': ID3v2TextFrame, 'TSOC': ID3v2TextFrame, 'TSOP': ID3v2TextFrame, 'TSOT': ID3v2TextFrame,
		'TSRC': ID3v2TextFrame, 'TSSE': ID3v2TextFrame, 'TSST': ID3v2TextFrame,
		# URL Link Frames
		'WCOM': ID3v2URLLinkFrame, 'WXXX': ID3v2UserURLLinkFrame
	}

	@classmethod
	def load(cls, data, struct_pattern, size_len, per_byte):
		if not isinstance(data, DataReader):
			data = DataReader(data)

		try:
			frame = struct.unpack(struct_pattern, data.read(struct.calcsize(struct_pattern)))
		except struct.error:
			raise InvalidFrame("Not enough data.")

		frame_size = decode_synchsafe_int(frame[1:1 + size_len], per_byte)
		if frame_size == 0:
			raise InvalidFrame("Not a valid ID3v2 frame")

		frame_id = frame[0].decode('iso-8859-1')
		frame_type = ID3v2Frame._FRAME_TYPES.get(frame_id, cls)
		frame_data = data.read(frame_size)

		# TODO: Move logic into frame classes?
		args = [frame_id]
		if frame_type is ID3v2CommentFrame:
			encoding = _determine_encoding(frame_data[0:1])

			language = _decode_bytestring(frame_data[1:4])
			args.append(language)

			values = [_decode_bytestring(v, encoding) for v in _split_encoded(frame_data[4:], encoding)]

			# Ignore empty comments.
			if len(values) < 2:
				return None

			args.extend(values)
		elif frame_type is ID3v2GenreFrame:
			encoding = _determine_encoding(frame_data[0:1])

			remainder = frame_data[1:]
			values = []
			while True:
				split = _split_encoded(remainder, encoding)
				values.extend([_decode_bytestring(v, encoding) for v in split])

				if len(split) < 2:
					break

				remainder = split[1]

			genres = []
			for value in values:
				match = _genre_re.match(value)

				if match['name']:
					genres.append(match['name'])
				elif match['id']:
					if match['id'].isdigit() and int(match['id']):
						try:
							genres.append(ID3v1Genres[int(match['id'])])
						except IndexError:
							genres.append(value)
					elif match['id'] == 'CR':
						genres.append('Cover')
					elif match['id'] == 'RX':
						genres.append('Remix')

			args.append(genres)
		elif frame_type is ID3v2GEOBFrame:
			encoding = _determine_encoding(frame_data[0:1])

			mime_type, remainder = _split_encoded(frame_data[1:], encoding)
			filename, remainder = _split_encoded(remainder, encoding)
			description, value = _split_encoded(remainder, encoding)

			values = [_decode_bytestring(mime_type)]
			values.extend([_decode_bytestring(v, encoding) for v in [filename, description]])
			values.append(value)

			args.extend(values)
		elif frame_type is ID3v2PictureFrame:
			args.append(frame_data)
		elif frame_type is ID3v2PrivateFrame:
			owner_end = frame_data.index(b'\x00')
			args.append(frame_data[0:owner_end].decode('iso-8859-1'))
			args.append(frame_data[owner_end + 1:])
		elif frame_type is ID3v2UnsynchronizedLyricsFrame:
			encoding = _determine_encoding(frame_data[0:1])

			language = _decode_bytestring(frame_data[1:4])
			args.append(language)

			for v in _split_encoded(frame_data[4:], encoding):
				args.append(_decode_bytestring(v, encoding))
		elif frame_type is ID3v2URLLinkFrame:
			args.append(unquote(_decode_bytestring(frame_data)))
		elif frame_type is ID3v2UserURLLinkFrame:
			encoding = _determine_encoding(frame_data)

			description, url = _split_encoded(frame_data[1:], encoding)
			args.append(_decode_bytestring(description, encoding))
			args.append(unquote(_decode_bytestring(url)))
		elif frame_type in (ID3v2NumberFrame, ID3v2NumericTextFrame, ID3v2TextFrame, ID3v2UserTextFrame):
			encoding = _determine_encoding(frame_data[0:1])
			args.append(_decode_bytestring(frame_data[1:], encoding))
		elif frame_type is ID3v2Frame:
			args.append(frame_data)
		else:
			args.append(_decode_bytestring(frame_data))

		try:
			return frame_type(*args)
		except TypeError:  # Bad frame value.
			return None


class ID3v2Frames(Tags):
	FIELD_MAP = frozenbidict({
		'album': 'TALB', 'album_sort': 'TSOA', 'albumartist': 'TPE2', 'albumartist_sort': 'TSO2',
		'arranger': 'TPE4', 'artist': 'TPE1', 'artist_sort': 'TSOP', 'audio_delay': 'TDLY',
		'audio_length': 'TLEN', 'audio_size': 'TSIZ', 'bpm': 'TBPM', 'comment': 'COMM',
		'compilation': 'TCMP', 'composer': 'TCOM', 'composer_sort': 'TSOC', 'conductor': 'TPE3',
		'copyright': 'TCOP', 'date': 'TYER', 'discnumber': 'TPOS', 'encoded_by': 'TENC',
		'encoding_settings': 'TSSE', 'genre': 'TCON', 'grouping': 'TIT1', 'isrc': 'TSRC',
		'language': 'TLAN', 'lyricist': 'TEXT', 'lyrics': 'USLT', 'media': 'TMED', 'mood': 'TMOO',
		'original_album': 'TOAL', 'original_artist': 'TOPE', 'original_author': 'TOLY', 'original_year': 'TORY',
		'pictures': 'APIC', 'playcount': 'PCNT', 'publisher': 'TPUB', 'recording_dates': 'TRDA', 'subtitle': 'TSST',
		'time': 'TIME', 'title': 'TIT2', 'titlesort': 'TSOT', 'tracknumber': 'TRCK'
	})

	def __init__(self, *args, **kwargs):
		self.update(*args, **kwargs)

	@classmethod
	def load(cls, data, id3_version, header_size):
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
			if isinstance(frame, (ID3v2CommentFrame, ID3v2SynchronizedLyricsFrame, ID3v2UnsynchronizedLyricsFrame)):
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

		self = cls()

		if data.read(3) != b"ID3":
			raise InvalidHeader("Valid ID3v2 header not found.")

		self._header = ID3v2Header.load(data.read(7))

		if self._header.flags.extended:
			ext_size = decode_synchsafe_int(struct.unpack('4B', data.read(4))[0:4], 7)
			if self._header.version[1] == 4:
				data.read(ext_size - 4)
			else:
				data.read(ext_size)

		self.tags = ID3v2Frames.load(data, self._header.version, self._header._size)
		self.pictures = self.tags.pop('pictures', [])

		return self
