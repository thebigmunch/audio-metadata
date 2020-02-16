__all__ = [
	'VorbisComment',
	'VorbisComments',
	'VorbisPicture',
]

import struct
from collections import defaultdict

from attr import attrib, attrs
from tbm_utils import AttrMapping

from .models import (
	Picture,
	Tags,
)
from .tables import ID3PictureType
from ..exceptions import InvalidComment
from ..utils import datareader


@attrs(repr=False)
class VorbisComment(AttrMapping):
	name = attrib(converter=lambda n: n.lower())
	value = attrib()

	@datareader
	@classmethod
	def load(cls, data):
		length = struct.unpack('I', data.read(4))[0]
		comment = data.read(length).decode('utf-8', 'replace')

		if '=' not in comment:
			raise InvalidComment("Vorbis comment must contain an '='.")

		name, value = comment.split('=', 1)

		return cls(name, value)


# TODO: Number frames.
class VorbisComments(Tags):
	@datareader
	@classmethod
	def load(cls, data):
		vendor_length = struct.unpack('I', data.read(4))[0]
		vendor = data.read(vendor_length).decode('utf-8', 'replace')
		num_comments = struct.unpack('I', data.read(4))[0]

		fields = defaultdict(list)

		for _ in range(num_comments):
			comment = VorbisComment.load(data)
			fields[comment.name].append(comment.value)

		return cls(**fields, _vendor=vendor)


class VorbisPicture(Picture):
	@datareader
	@classmethod
	def load(cls, data):
		type_, mime_length = struct.unpack('>2I', data.read(8))
		mime_type = data.read(mime_length).decode('utf-8', 'replace')

		desc_length = struct.unpack('>I', data.read(4))[0]
		description = data.read(desc_length).decode('utf-8', 'replace')

		width, height, depth, colors = struct.unpack('>4I', data.read(16))

		data_length = struct.unpack('>I', data.read(4))[0]
		data = data.read(data_length)

		return cls(
			type=ID3PictureType(type_),
			mime_type=mime_type,
			description=description,
			width=width,
			height=height,
			depth=depth,
			colors=colors,
			data=data,
		)
