__all__ = ['VorbisComments', 'VorbisPicture']

import struct
from collections import defaultdict

from .models import Picture, Tags
from .tables import ID3PictureType
from ..utils import DataReader


# TODO: Number frames.
class VorbisComments(Tags):
	@classmethod
	def load(cls, data):
		if not isinstance(data, DataReader):  # pragma: nocover
			data = DataReader(data)

		vendor_length = struct.unpack('I', data.read(4))[0]
		vendor = data.read(vendor_length).decode('utf-8', 'replace')
		num_comments = struct.unpack('I', data.read(4))[0]

		fields = defaultdict(list)

		for _ in range(num_comments):
			length = struct.unpack('I', data.read(4))[0]
			comment = data.read(length).decode('utf-8', 'replace')

			if '=' in comment:  # pragma: nobranch
				field, value = comment.split('=', 1)

				fields[field.lower()].append(value)

		return cls(**fields, _vendor=vendor)


class VorbisPicture(Picture):
	@classmethod
	def load(cls, data):
		if not isinstance(data, DataReader):  # pragma: nocover
			data = DataReader(data)

		type_, mime_length = struct.unpack('>2I', data.read(8))
		mime_type = data.read(mime_length).decode('utf-8', 'replace')

		desc_length = struct.unpack('>I', data.read(4))[0]
		description = data.read(desc_length).decode('utf-8', 'replace')

		width, height, depth, colors = struct.unpack('>4I', data.read(16))

		data_length = struct.unpack('>I', data.read(4))[0]
		data = data.read(data_length)

		return cls(
			type=ID3PictureType(type_), mime_type=mime_type, description=description,
			width=width, height=height, depth=depth, colors=colors,
			data=data
		)
