# https://xiph.org/vorbis/doc/v-comment.html

__all__ = [
	'VorbisComment',
	'VorbisComments',
]

import struct
from collections import defaultdict

from attr import attrib, attrs
from tbm_utils import (
	AttrMapping,
	datareader,
)

from ..exceptions import InvalidComment
from ..models import Tags


@attrs(
	repr=False,
	kw_only=True,
)
class VorbisComment(AttrMapping):
	name = attrib(converter=lambda n: n.lower())
	value = attrib()

	@datareader
	@classmethod
	def parse(cls, data):
		length = struct.unpack('I', data.read(4))[0]
		comment = data.read(length).decode('utf-8', 'replace')

		if '=' not in comment:
			raise InvalidComment("Vorbis comment must contain an '='.")

		name, value = comment.split('=', 1)

		return cls(
			name=name,
			value=value,
		)


# TODO: Number frames.
class VorbisComments(Tags):
	@datareader
	@classmethod
	def parse(cls, data):
		vendor_length = struct.unpack('I', data.read(4))[0]
		vendor = data.read(vendor_length).decode('utf-8', 'replace')
		num_comments = struct.unpack('I', data.read(4))[0]

		fields = defaultdict(list)

		for _ in range(num_comments):
			comment = VorbisComment.parse(data)
			fields[comment.name].append(comment.value)

		return cls(
			_vendor=vendor,
			**fields,
		)
