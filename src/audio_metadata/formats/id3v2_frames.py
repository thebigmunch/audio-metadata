# http://id3.org/Developer%20Information

__all__ = [
	'ID3v2BaseFrame',
	'ID3v2BinaryDataFrame',
	'ID3v2Comment',
	'ID3v2CommentFrame',
	'ID3v2Frame',
	'ID3v2FrameTypes',
	'ID3v2GEOBFrame',
	'ID3v2GeneralEncapsulatedObject',
	'ID3v2GenreFrame',
	'ID3v2InvolvedPerson',
	'ID3v2Lyrics',
	'ID3v2LyricsFrame',
	'ID3v2MappingListFrame',
	'ID3v2NumberFrame',
	'ID3v2NumericTextFrame',
	'ID3v2Performer',
	'ID3v2Picture',
	'ID3v2PictureFrame',
	'ID3v2PrivateFrame',
	'ID3v2PrivateInfo',
	'ID3v2SynchronizedLyrics',
	'ID3v2SynchronizedLyricsFrame',
	'ID3v2TextFrame',
	'ID3v2TimestampFrame',
	'ID3v2UnsynchronizedLyrics',
	'ID3v2UnsynchronizedLyricsFrame',
	'ID3v2URLLinkFrame',
	'ID3v2UserText',
	'ID3v2UserTextFrame',
	'ID3v2UserURLLink',
	'ID3v2UserURLLinkFrame',
	'ID3v2YearFrame',
]

import re
import string
import struct
from urllib.parse import unquote

import more_itertools
from attr import (
	attrib,
	attrs,
)
from pendulum.parsing import ParserError
from pendulum.parsing.iso8601 import parse_iso8601
from tbm_utils import (
	AttrMapping,
	datareader,
)

from .tables import (
	ID3PictureType,
	ID3v1Genres,
	ID3v2LyricsContentType,
	ID3v2LyricsTimestampFormat,
)
from ..exceptions import InvalidFrame
from ..models import Picture
from ..utils import (
	decode_bytestring,
	decode_synchsafe_int,
	determine_encoding,
	get_image_size,
	split_encoded,
)

_genre_re = re.compile(r"((?:\((?P<id>\d+|RX|CR)\))*)(?P<name>.+)?")


@attrs(
	repr=False,
	kw_only=True,
)
class ID3v2Comment(AttrMapping):
	language = attrib()
	description = attrib()
	text = attrib()


@attrs(
	repr=False,
	kw_only=True,
)
class ID3v2GeneralEncapsulatedObject(AttrMapping):
	mime_type = attrib()
	filename = attrib()
	description = attrib()
	value = attrib()


@attrs(
	repr=False,
	kw_only=True,
)
class ID3v2InvolvedPerson(AttrMapping):
	involvement = attrib()
	name = attrib()


@attrs(
	repr=False,
	kw_only=True,
)
class ID3v2Performer(AttrMapping):
	instrument = attrib()
	name = attrib()


@attrs(
	repr=False,
	kw_only=True,
)
class ID3v2PrivateInfo(AttrMapping):
	owner = attrib()
	data = attrib()


@attrs(
	repr=False,
	kw_only=True,
)
class ID3v2Lyrics(AttrMapping):
	language = attrib()
	description = attrib()
	text = attrib()


@attrs(
	repr=False,
	kw_only=True,
)
class ID3v2SynchronizedLyrics(ID3v2Lyrics):
	timestamp_format = attrib(converter=ID3v2LyricsTimestampFormat)
	content_type = attrib(converter=ID3v2LyricsContentType)


@attrs(
	repr=False,
	kw_only=True,
)
class ID3v2UnsynchronizedLyrics(ID3v2Lyrics):
	pass


@attrs(
	repr=False,
	kw_only=True,
)
class ID3v2UserText(AttrMapping):
	description = attrib()
	text = attrib()


@attrs(
	repr=False,
	kw_only=True,
)
class ID3v2UserURLLink(AttrMapping):
	description = attrib()
	url = attrib()


class ID3v2Picture(Picture):
	@datareader
	@classmethod
	def parse(cls, data):
		data = data.read()

		encoding = determine_encoding(data[0:1])
		mime_start = 1
		mime_end = data.index(b'\x00', 1)
		mime_type = decode_bytestring(data[mime_start:mime_end])

		type_ = ID3PictureType(data[mime_end + 1])

		desc_start = mime_end + 2
		description, image_data = split_encoded(data[desc_start:], encoding)
		description = decode_bytestring(description, encoding)
		width, height = get_image_size(image_data)

		return cls(
			type=type_,
			mime_type=mime_type,
			description=description,
			width=width,
			height=height,
			data=image_data,
		)


@attrs(
	repr=False,
	kw_only=True,
)
class ID3v2BaseFrame(AttrMapping):
	id = attrib()  # noqa


@attrs(
	repr=False,
	kw_only=True,
)
class ID3v2BinaryDataFrame(AttrMapping):
	value = attrib()


@attrs(
	repr=False,
	kw_only=True,
)
class ID3v2CommentFrame(ID3v2BaseFrame):
	value = attrib()


@attrs(
	repr=False,
	kw_only=True,
)
class ID3v2GenreFrame(ID3v2BaseFrame):
	value = attrib()


@attrs(
	repr=False,
	kw_only=True,
)
class ID3v2GEOBFrame(ID3v2BaseFrame):
	value = attrib()


@attrs(
	repr=False,
	kw_only=True,
)
class ID3v2LyricsFrame(ID3v2BaseFrame):
	value = attrib()


@attrs(
	repr=False,
	kw_only=True,
)
class ID3v2MappingListFrame(ID3v2BaseFrame):
	value = attrib()


@attrs(
	repr=False,
	kw_only=True,
)
class ID3v2NumberFrame(ID3v2BaseFrame):
	value = attrib()

	@value.validator
	def validate_value(self, attribute, value):
		if not all(char in [*string.digits, '/'] for char in value):
			raise ValueError(
				"Number frame values must consist only of digits and '/'.",
			)

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


@attrs(
	repr=False,
	kw_only=True,
)
class ID3v2NumericTextFrame(ID3v2BaseFrame):
	value = attrib()

	@value.validator
	def validate_value(self, attribute, value):
		if not all(v.isdigit() for v in value):
			raise ValueError("Numeric text frame values must consist only of digits.")


@attrs(
	repr=False,
	kw_only=True,
)
class ID3v2PictureFrame(ID3v2BaseFrame):
	value = attrib(converter=ID3v2Picture.parse)


@attrs(
	repr=False,
	kw_only=True,
)
class ID3v2PrivateFrame(ID3v2BaseFrame):
	value = attrib()


@attrs(
	repr=False,
	kw_only=True,
)
class ID3v2SynchronizedLyricsFrame(ID3v2LyricsFrame):
	pass


@attrs(
	repr=False,
	kw_only=True,
)
class ID3v2TextFrame(ID3v2BaseFrame):
	value = attrib()


@attrs(
	repr=False,
	kw_only=True,
)
class ID3v2TimestampFrame(ID3v2BaseFrame):
	value = attrib()

	@value.validator
	def validate_value(self, attribute, value):
		for v in value:
			try:
				parse_iso8601(v)
			except ParserError:
				raise ValueError("Timestamp frame values must conform to the ID3v2-compliant subset of ISO 8601.")


@attrs(
	repr=False,
	kw_only=True,
)
class ID3v2UnsynchronizedLyricsFrame(ID3v2LyricsFrame):
	pass


@attrs(
	repr=False,
	kw_only=True,
)
class ID3v2URLLinkFrame(ID3v2BaseFrame):
	value = attrib()


@attrs(
	repr=False,
	kw_only=True,
)
class ID3v2UserURLLinkFrame(ID3v2BaseFrame):
	value = attrib()


@attrs(
	repr=False,
	kw_only=True,
)
class ID3v2UserTextFrame(ID3v2BaseFrame):
	value = attrib()


@attrs(
	repr=False,
	kw_only=True,
)
class ID3v2YearFrame(ID3v2NumericTextFrame):
	value = attrib()

	@value.validator
	def validate_value(self, attribute, value):
		if not all(
			(
				v.isdigit()
				and len(v) == 4
			)
			for v in value
		):
			raise ValueError("Year frame values must be 4-character number strings.")


@attrs(
	repr=False,
	kw_only=True,
)
class ID3v2TDATFrame(ID3v2NumericTextFrame):
	value = attrib()

	@value.validator
	def validate_value(self, attribute, value):
		if not all(
			(
				v.isdigit()
				and len(v) == 4
				and int(v[0:2]) in range(1, 32)
				and int(v[2:4]) in range(1, 13)
			)
			for v in value
		):
			raise ValueError(
				"TDAT frame values must be a 4-character number string in the DDMM format.",
			)


@attrs(
	repr=False,
	kw_only=True,
)
class ID3v2TIMEFrame(ID3v2NumericTextFrame):
	value = attrib()

	@value.validator
	def validate_value(self, attribute, value):
		if not all(
			(
				v.isdigit()
				and len(v) == 4
				and int(v[0:2]) in range(0, 24)
				and int(v[2:4]) in range(0, 60)
			)
			for v in value
		):
			raise ValueError(
				"TIME frame values must be a 4-character number string in the HHMM format.",
			)


# TODO:ID3v2.2
# TODO: BUF, CNT, CRA, CRM, ETC, EQU, LNK, MCI, MLL, PCS,
# TODO: POP, REV, RVA, STC, UFI

# TODO: ID3v2.3
# TODO: AENC, COMR, ENCR, EQUA, ETCO, GRID, LINK, MLLT, OWNE
# TODO: PCNT, PCST, POPM, POSS, RBUF, RGAD, RVAD, RVRB, SYTC,
# TODO: UFID, USER, XRVA

# TODO: ID3v2.4
# TODO: ASPI, EQU2, PCST, RGAD, RVA2, SEEK, SIGN,
# TODO: TPRO, XRVA
ID3v2FrameTypes = {
	# Binary data frames
	'MCDI': ID3v2BinaryDataFrame,
	'NCON': ID3v2BinaryDataFrame,

	# Complex Text Frames
	'COM': ID3v2CommentFrame,
	'GEO': ID3v2GEOBFrame,
	'IPL': ID3v2MappingListFrame,
	'TXX': ID3v2UserTextFrame,

	'COMM': ID3v2CommentFrame,
	'GEOB': ID3v2GEOBFrame,
	'IPLS': ID3v2MappingListFrame,
	'PRIV': ID3v2PrivateFrame,
	'TIPL': ID3v2MappingListFrame,
	'TMCL': ID3v2MappingListFrame,
	'TXXX': ID3v2UserTextFrame,

	# Genre Frame
	'TCO': ID3v2GenreFrame,

	'TCON': ID3v2GenreFrame,

	# Lyrics Frames
	'SLT': ID3v2SynchronizedLyricsFrame,
	'ULT': ID3v2UnsynchronizedLyricsFrame,

	'SYLT': ID3v2SynchronizedLyricsFrame,
	'USLT': ID3v2UnsynchronizedLyricsFrame,

	# Number Frames
	'TPA': ID3v2NumberFrame,
	'TRK': ID3v2NumberFrame,

	'TPOS': ID3v2NumberFrame,
	'TRCK': ID3v2NumberFrame,

	# Numeric Text Frames
	'TBP': ID3v2NumericTextFrame,
	'TDA': ID3v2TDATFrame,
	'TDY': ID3v2NumericTextFrame,
	'TIM': ID3v2TIMEFrame,
	'TLE': ID3v2NumericTextFrame,
	'TOR': ID3v2YearFrame,
	'TSI': ID3v2NumericTextFrame,
	'TYE': ID3v2YearFrame,

	'TBPM': ID3v2NumericTextFrame,
	'TDAT': ID3v2TDATFrame,
	'TDLY': ID3v2NumericTextFrame,
	'TIME': ID3v2TIMEFrame,
	'TLEN': ID3v2NumericTextFrame,
	'TORY': ID3v2YearFrame,
	'TSIZ': ID3v2NumericTextFrame,
	'TYER': ID3v2YearFrame,

	# Picture Frames
	'PIC': ID3v2PictureFrame,

	'APIC': ID3v2PictureFrame,

	# Text Frames
	'TAL': ID3v2TextFrame,
	'TCM': ID3v2TextFrame,
	'TCR': ID3v2TextFrame,
	'TDS': ID3v2TextFrame,
	'TEN': ID3v2TextFrame,
	'TFT': ID3v2TextFrame,
	'TKE': ID3v2TextFrame,
	'TLA': ID3v2TextFrame,
	'TMT': ID3v2TextFrame,
	'TOA': ID3v2TextFrame,
	'TOF': ID3v2TextFrame,
	'TOL': ID3v2TextFrame,
	'TOT': ID3v2TextFrame,
	'TP1': ID3v2TextFrame,
	'TP2': ID3v2TextFrame,
	'TP3': ID3v2TextFrame,
	'TP4': ID3v2TextFrame,
	'TPB': ID3v2TextFrame,
	'TRC': ID3v2TextFrame,
	'TRD': ID3v2TextFrame,
	'TS2': ID3v2TextFrame,
	'TSA': ID3v2TextFrame,
	'TSC': ID3v2TextFrame,
	'TSP': ID3v2TextFrame,
	'TSS': ID3v2TextFrame,
	'TST': ID3v2TextFrame,
	'TT1': ID3v2TextFrame,
	'TT2': ID3v2TextFrame,
	'TT3': ID3v2TextFrame,
	'TXT': ID3v2TextFrame,

	'TALB': ID3v2TextFrame,
	'TCMP': ID3v2TextFrame,
	'TCOM': ID3v2TextFrame,
	'TCOP': ID3v2TextFrame,
	'TDES': ID3v2TextFrame,
	'TENC': ID3v2TextFrame,
	'TEXT': ID3v2TextFrame,
	'TFLT': ID3v2TextFrame,
	'TIT1': ID3v2TextFrame,
	'TIT2': ID3v2TextFrame,
	'TIT3': ID3v2TextFrame,
	'TKEY': ID3v2TextFrame,
	'TKWD': ID3v2TextFrame,
	'TLAN': ID3v2TextFrame,
	'TMED': ID3v2TextFrame,
	'TMOO': ID3v2TextFrame,
	'TOAL': ID3v2TextFrame,
	'TOFN': ID3v2TextFrame,
	'TOLY': ID3v2TextFrame,
	'TOPE': ID3v2TextFrame,
	'TOWN': ID3v2TextFrame,
	'TPE1': ID3v2TextFrame,
	'TPE2': ID3v2TextFrame,
	'TPE3': ID3v2TextFrame,
	'TPE4': ID3v2TextFrame,
	'TPUB': ID3v2TextFrame,
	'TRDA': ID3v2TextFrame,
	'TRSN': ID3v2TextFrame,
	'TRSO': ID3v2TextFrame,
	'TSO2': ID3v2TextFrame,
	'TSOA': ID3v2TextFrame,
	'TSOC': ID3v2TextFrame,
	'TSOP': ID3v2TextFrame,
	'TSOT': ID3v2TextFrame,
	'TSRC': ID3v2TextFrame,
	'TSSE': ID3v2TextFrame,
	'TSST': ID3v2TextFrame,
	'XSOA': ID3v2TextFrame,
	'XSOP': ID3v2TextFrame,
	'XSOT': ID3v2TextFrame,

	# Timestamp Frames
	'TDR': ID3v2TimestampFrame,

	'TDEN': ID3v2TimestampFrame,
	'TDOR': ID3v2TimestampFrame,
	'TDRC': ID3v2TimestampFrame,
	'TDRL': ID3v2TimestampFrame,
	'TDTG': ID3v2TimestampFrame,
	'XDOR': ID3v2TimestampFrame,

	# URL Link Frames
	'TID': ID3v2URLLinkFrame,
	'WAF': ID3v2URLLinkFrame,
	'WAR': ID3v2URLLinkFrame,
	'WAS': ID3v2URLLinkFrame,
	'WCM': ID3v2URLLinkFrame,
	'WCP': ID3v2URLLinkFrame,
	'WFD': ID3v2URLLinkFrame,
	'WPB': ID3v2URLLinkFrame,
	'WXX': ID3v2UserURLLinkFrame,

	'TGID': ID3v2URLLinkFrame,
	'WCOM': ID3v2URLLinkFrame,
	'WCOP': ID3v2URLLinkFrame,
	'WFED': ID3v2URLLinkFrame,
	'WOAF': ID3v2URLLinkFrame,
	'WOAR': ID3v2URLLinkFrame,
	'WOAS': ID3v2URLLinkFrame,
	'WORS': ID3v2URLLinkFrame,
	'WPAY': ID3v2URLLinkFrame,
	'WPUB': ID3v2URLLinkFrame,
	'WXXX': ID3v2UserURLLinkFrame,
}


@attrs(
	repr=False,
	kw_only=True,
)
class ID3v2Frame(ID3v2BaseFrame):
	value = attrib()

	@datareader
	@classmethod
	def parse(cls, data, struct_pattern, size_len, per_byte):
		try:
			frame = struct.unpack(struct_pattern, data.read(struct.calcsize(struct_pattern)))
		except struct.error:
			raise InvalidFrame("Not enough data.")

		frame_size = decode_synchsafe_int(frame[1:1 + size_len], per_byte)
		if frame_size == 0:
			raise InvalidFrame("Not a valid ID3v2 frame")

		frame_id = frame[0].decode('iso-8859-1')
		frame_type = ID3v2FrameTypes.get(frame_id, cls)
		frame_data = data.read(frame_size)

		# TODO: Move logic into frame classes?
		kwargs = {'id': frame_id}
		if frame_type is ID3v2BinaryDataFrame:
			kwargs['value'] = frame_data
		elif frame_type is ID3v2CommentFrame:
			encoding = determine_encoding(frame_data)

			values = split_encoded(frame_data[4:], encoding)
			# Ignore empty comments.
			if len(values) < 2:
				return None

			comment = ID3v2Comment(
				language=decode_bytestring(frame_data[1:4]),
				description=decode_bytestring(values[0], encoding),
				text=decode_bytestring(values[1], encoding),
			)

			kwargs['value'] = comment
		elif frame_type is ID3v2MappingListFrame:
			encoding = determine_encoding(frame_data)

			values = []
			tail = frame_data[1:]

			while tail:
				head, tail = split_encoded(tail, encoding)
				values.append(head)

			if frame_id == 'TMCL':
				mapping_list = [
					ID3v2Performer(
						instrument=decode_bytestring(instrument, encoding),
						name=decode_bytestring(name, encoding),
					)
					for instrument, name in more_itertools.chunked(values, 2)
				]
			else:
				mapping_list = [
					ID3v2InvolvedPerson(
						involvement=decode_bytestring(involvement, encoding),
						name=decode_bytestring(name, encoding),
					)
					for involvement, name in more_itertools.chunked(values, 2)
				]

			# Ignore empty people list.
			if len(values) < 1:
				return None

			kwargs['value'] = mapping_list
		elif frame_type is ID3v2GEOBFrame:
			encoding = determine_encoding(frame_data)

			mime_type, remainder = split_encoded(frame_data[1:], encoding)
			filename, remainder = split_encoded(remainder, encoding)
			description, value = split_encoded(remainder, encoding)

			kwargs['value'] = ID3v2GeneralEncapsulatedObject(
				mime_type=mime_type,
				filename=filename,
				description=description,
				value=value,
			)
		elif frame_type is ID3v2GenreFrame:
			encoding = determine_encoding(frame_data)

			remainder = frame_data[1:]
			values = []
			while True:
				split = split_encoded(remainder, encoding)
				values.extend(
					decode_bytestring(v, encoding)
					for v in split
				)

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

			kwargs['value'] = genres
		elif frame_type is ID3v2PictureFrame:
			kwargs['value'] = frame_data
		elif frame_type is ID3v2PrivateFrame:
			owner_end = frame_data.index(b'\x00')

			kwargs['value'] = ID3v2PrivateInfo(
				owner=frame_data[0:owner_end].decode('iso-8859-1'),
				data=frame_data[owner_end + 1:],
			)
		elif frame_type is ID3v2SynchronizedLyricsFrame:
			encoding = determine_encoding(frame_data)

			description, text = split_encoded(frame_data[6:], encoding)

			kwargs['value'] = ID3v2SynchronizedLyrics(
				language=decode_bytestring(frame_data[1:4]),
				description=decode_bytestring(description, encoding),
				text=decode_bytestring(text, encoding),
				timestamp_format=frame_data[4],
				content_type=frame_data[5],
			)
		elif frame_type is ID3v2UnsynchronizedLyricsFrame:
			encoding = determine_encoding(frame_data)

			description, text = split_encoded(frame_data[4:], encoding)

			kwargs['value'] = ID3v2UnsynchronizedLyrics(
				language=decode_bytestring(frame_data[1:4]),
				description=decode_bytestring(description, encoding),
				text=decode_bytestring(text, encoding)
			)
		elif frame_type is ID3v2URLLinkFrame:
			kwargs['value'] = unquote(decode_bytestring(frame_data))
		elif frame_type is ID3v2UserTextFrame:
			encoding = determine_encoding(frame_data)

			description, text = split_encoded(frame_data[1:], encoding)
			kwargs['value'] = ID3v2UserText(
				description=decode_bytestring(description, encoding),
				text=decode_bytestring(text, encoding),
			)
		elif frame_type is ID3v2UserURLLinkFrame:
			encoding = determine_encoding(frame_data)

			description, url = split_encoded(frame_data[1:], encoding)
			kwargs['value'] = ID3v2UserURLLink(
				description=decode_bytestring(description, encoding),
				url=unquote(decode_bytestring(url)),
			)
		elif issubclass(frame_type, ID3v2NumberFrame):
			encoding = determine_encoding(frame_data)
			kwargs['value'] = decode_bytestring(frame_data[1:], encoding)
		elif issubclass(
			frame_type,
			(
				ID3v2NumericTextFrame,
				ID3v2TextFrame,
				ID3v2TimestampFrame,
			),
		):
			encoding = determine_encoding(frame_data)
			values = [
				decode_bytestring(value, encoding)
				for value in split_encoded(frame_data[1:], encoding)
				if value
			]
			kwargs['value'] = values
		elif frame_type is ID3v2Frame:
			kwargs['value'] = frame_data
		else:
			kwargs['value'] = decode_bytestring(frame_data)

		try:
			return frame_type(**kwargs)
		except (TypeError, ValueError):  # Bad frame value.
			return None
