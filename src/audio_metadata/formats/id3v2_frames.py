__all__ = [
	'ID3v2BaseFrame',
	'ID3v2CommentFrame',
	'ID3v2Frame',
	'ID3v2GEOBFrame',
	'ID3v2GenreFrame',
	'ID3v2NumberFrame',
	'ID3v2NumericTextFrame',
	'ID3v2Picture',
	'ID3v2PictureFrame',
	'ID3v2PrivateFrame',
	'ID3v2SynchronizedLyricsFrame',
	'ID3v2TextFrame',
	'ID3v2UnsynchronizedLyricsFrame',
	'ID3v2URLLinkFrame',
	'ID3v2UserTextFrame',
	'ID3v2UserURLLinkFrame',
	'ID3v2YearFrame'
]

import re
import struct
from urllib.parse import unquote

from attr import attrib, attrs

from .models import Picture
from .tables import ID3PictureType, ID3v1Genres
from ..exceptions import InvalidFrame
from ..structures import DictMixin
from ..utils import (
	DataReader, decode_bytestring, decode_synchsafe_int,
	determine_encoding, get_image_size, split_encoded
)

_genre_re = re.compile(r"((?:\((?P<id>\d+|RX|CR)\))*)(?P<name>.+)?")


class ID3v2Picture(Picture):
	def __init__(self, **kwargs):
		self.update(**kwargs)

	@classmethod
	def load(cls, data):
		if not isinstance(data, DataReader):
			data = DataReader(data)

		data = data.read()

		encoding = determine_encoding(data[0:1])
		mime_start = 1
		mime_end = data.index(b'\x00', 1)
		mime_type = decode_bytestring(data[mime_start:mime_end])

		type = ID3PictureType(data[mime_end + 1])  # noqa

		desc_start = mime_end + 2
		description, image_data = split_encoded(data[desc_start:], encoding)
		description = decode_bytestring(description, encoding)
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
class ID3v2YearFrame(ID3v2NumericTextFrame):
	value = attrib()

	@value.validator
	def validate_value(self, attribute, value):
		if (
			not value.isdigit()
			or len(value) != 4
		):
			raise ValueError("Year frame values must be 4-character number strings.")


@attrs(repr=False)
class ID3v2TDATFrame(ID3v2NumericTextFrame):
	value = attrib()

	@value.validator
	def validate_value(self, attribute, value):
		if (
			not value.isdigit()
			or len(value) != 4
			or int(value[0:2]) not in range(1, 32)
			or int(value[2:4]) not in range(1, 13)
		):
			raise ValueError(
				"TDAT frame value must be a 4-character number string in the DDMM format."
			)


@attrs(repr=False)
class ID3v2TIMEFrame(ID3v2NumericTextFrame):
	value = attrib()

	@value.validator
	def validate_value(self, attribute, value):
		if (
			not value.isdigit()
			or len(value) != 4
			or int(value[0:2]) not in range(0, 24)
			or int(value[2:4]) not in range(0, 60)
		):
			raise ValueError(
				"TIME frame value must be a 4-character number string in the HHMM format."
			)


@attrs(repr=False)
class ID3v2Frame(ID3v2BaseFrame):
	value = attrib()

	# TODO:ID3v2.2
	# TODO: BUF, CNT, CRA, CRM, ETC, EQU, IPL, LNK, MCI, MLL, POP, REV,
	# TODO: RVA, STC, UFI

	# TODO: ID3v2.3
	# TODO: AENC, COMR, ENCR, EQUA, ETCO, GRID, IPLS, LINK, MCDI, MLLT, OWNE
	# TODO: PCNT, POPM, POSS, RBUF, RVAD, RVRB, SYTC, UFID, USER

	# TODO: ID3v2.4
	# TODO: ASPI, EQU2, RVA2, SEEK, SIGN, TDEN, TDOR, TDRC, TDRL, TDTG, TIPL
	# TODO: TMCL, TPRO,

	_FRAME_TYPES = {
		# Complex Text Frames
		'COM': ID3v2CommentFrame, 'GEO': ID3v2GEOBFrame,
		'TXX': ID3v2UserTextFrame,

		'COMM': ID3v2CommentFrame, 'GEOB': ID3v2GEOBFrame,
		'PRIV': ID3v2PrivateFrame, 'TXXX': ID3v2UserTextFrame,

		# Genre Frame
		'TCO': ID3v2GenreFrame,

		'TCON': ID3v2GenreFrame,

		# Lyrics Frames
		'SLT': ID3v2SynchronizedLyricsFrame, 'ULT': ID3v2UnsynchronizedLyricsFrame,

		'SYLT': ID3v2SynchronizedLyricsFrame, 'USLT': ID3v2UnsynchronizedLyricsFrame,

		# Number Frames
		'TPA': ID3v2NumberFrame, 'TRK': ID3v2NumberFrame,

		'TPOS': ID3v2NumberFrame, 'TRCK': ID3v2NumberFrame,

		# Numeric Text Frames
		'TBP': ID3v2NumericTextFrame, 'TDA': ID3v2TDATFrame,
		'TDY': ID3v2NumericTextFrame, 'TIM': ID3v2TIMEFrame,
		'TLE': ID3v2NumericTextFrame, 'TOR': ID3v2YearFrame,
		'TSI': ID3v2NumericTextFrame, 'TYE': ID3v2YearFrame,

		'TBPM': ID3v2NumericTextFrame, 'TDAT': ID3v2TDATFrame,
		'TDLY': ID3v2NumericTextFrame, 'TIME': ID3v2TIMEFrame,
		'TLEN': ID3v2NumericTextFrame, 'TORY': ID3v2YearFrame,
		'TSIZ': ID3v2NumericTextFrame, 'TYER': ID3v2YearFrame,

		# Picture Frames
		'PIC': ID3v2PictureFrame,

		'APIC': ID3v2PictureFrame,

		# Text Frames
		'TAL': ID3v2TextFrame, 'TCM': ID3v2TextFrame, 'TCR': ID3v2TextFrame,
		'TEN': ID3v2TextFrame, 'TFT': ID3v2TextFrame, 'TKE': ID3v2TextFrame,
		'TLA': ID3v2TextFrame, 'TMT': ID3v2TextFrame, 'TOA': ID3v2TextFrame,
		'TOF': ID3v2TextFrame, 'TOL': ID3v2TextFrame, 'TOT': ID3v2TextFrame,
		'TP1': ID3v2TextFrame, 'TP2': ID3v2TextFrame, 'TP3': ID3v2TextFrame,
		'TP4': ID3v2TextFrame, 'TPB': ID3v2TextFrame, 'TRC': ID3v2TextFrame,
		'TRD': ID3v2TextFrame, 'TSS': ID3v2TextFrame, 'TT1': ID3v2TextFrame,
		'TT2': ID3v2TextFrame, 'TT3': ID3v2TextFrame, 'TXT': ID3v2TextFrame,

		'TALB': ID3v2TextFrame, 'TCMP': ID3v2TextFrame, 'TCOM': ID3v2TextFrame,
		'TCOP': ID3v2TextFrame, 'TENC': ID3v2TextFrame, 'TEXT': ID3v2TextFrame,
		'TFLT': ID3v2TextFrame, 'TIT1': ID3v2TextFrame, 'TIT2': ID3v2TextFrame,
		'TIT3': ID3v2TextFrame, 'TKEY': ID3v2TextFrame, 'TLAN': ID3v2TextFrame,
		'TMED': ID3v2TextFrame, 'TMOO': ID3v2TextFrame, 'TOAL': ID3v2TextFrame,
		'TOFN': ID3v2TextFrame, 'TOLY': ID3v2TextFrame, 'TOPE': ID3v2TextFrame,
		'TOWN': ID3v2TextFrame, 'TPE1': ID3v2TextFrame, 'TPE2': ID3v2TextFrame,
		'TPE3': ID3v2TextFrame, 'TPE4': ID3v2TextFrame, 'TPUB': ID3v2TextFrame,
		'TRDA': ID3v2TextFrame, 'TRSN': ID3v2TextFrame, 'TRSO': ID3v2TextFrame,
		'TSO2': ID3v2TextFrame, 'TSOA': ID3v2TextFrame, 'TSOC': ID3v2TextFrame,
		'TSOP': ID3v2TextFrame, 'TSOT': ID3v2TextFrame, 'TSRC': ID3v2TextFrame,
		'TSSE': ID3v2TextFrame, 'TSST': ID3v2TextFrame,

		# URL Link Frames
		'WAF': ID3v2URLLinkFrame, 'WAR': ID3v2URLLinkFrame,
		'WAS': ID3v2URLLinkFrame, 'WCM': ID3v2URLLinkFrame,
		'WCP': ID3v2URLLinkFrame, 'WPB': ID3v2URLLinkFrame,
		'WXX': ID3v2UserURLLinkFrame,

		'WCOM': ID3v2URLLinkFrame, 'WCOP': ID3v2URLLinkFrame,
		'WOAF': ID3v2URLLinkFrame, 'WOAR': ID3v2URLLinkFrame,
		'WOAS': ID3v2URLLinkFrame, 'WORS': ID3v2URLLinkFrame,
		'WPAY': ID3v2URLLinkFrame, 'WPUB': ID3v2URLLinkFrame,
		'WXXX': ID3v2UserURLLinkFrame
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
			encoding = determine_encoding(frame_data[0:1])

			language = decode_bytestring(frame_data[1:4])
			args.append(language)

			values = [decode_bytestring(v, encoding) for v in split_encoded(frame_data[4:], encoding)]

			# Ignore empty comments.
			if len(values) < 2:
				return None

			args.extend(values)
		elif frame_type is ID3v2GenreFrame:
			encoding = determine_encoding(frame_data[0:1])

			remainder = frame_data[1:]
			values = []
			while True:
				split = split_encoded(remainder, encoding)
				values.extend([decode_bytestring(v, encoding) for v in split])

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
			encoding = determine_encoding(frame_data[0:1])

			mime_type, remainder = split_encoded(frame_data[1:], encoding)
			filename, remainder = split_encoded(remainder, encoding)
			description, value = split_encoded(remainder, encoding)

			values = [decode_bytestring(mime_type)]
			values.extend([decode_bytestring(v, encoding) for v in [filename, description]])
			values.append(value)

			args.extend(values)
		elif frame_type is ID3v2PictureFrame:
			args.append(frame_data)
		elif frame_type is ID3v2PrivateFrame:
			owner_end = frame_data.index(b'\x00')
			args.append(frame_data[0:owner_end].decode('iso-8859-1'))
			args.append(frame_data[owner_end + 1:])
		elif frame_type is ID3v2UnsynchronizedLyricsFrame:
			encoding = determine_encoding(frame_data[0:1])

			language = decode_bytestring(frame_data[1:4])
			args.append(language)

			for v in split_encoded(frame_data[4:], encoding):
				args.append(decode_bytestring(v, encoding))
		elif frame_type is ID3v2URLLinkFrame:
			args.append(unquote(decode_bytestring(frame_data)))
		elif frame_type is ID3v2UserURLLinkFrame:
			encoding = determine_encoding(frame_data)

			description, url = split_encoded(frame_data[1:], encoding)
			args.append(decode_bytestring(description, encoding))
			args.append(unquote(decode_bytestring(url)))
		elif issubclass(
			frame_type,
			(ID3v2NumberFrame, ID3v2NumericTextFrame, ID3v2TextFrame, ID3v2UserTextFrame,)
		):
			encoding = determine_encoding(frame_data[0:1])
			args.append(decode_bytestring(frame_data[1:], encoding))
		elif frame_type is ID3v2Frame:
			args.append(frame_data)
		else:
			args.append(decode_bytestring(frame_data))

		try:
			return frame_type(*args)
		except (TypeError, ValueError):  # Bad frame value.
			return None
