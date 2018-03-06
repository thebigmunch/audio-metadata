__all__ = [
	'DataReader', 'bytes_to_int_be', 'bytes_to_int_le', 'decode_synchsafe_int',
	'get_image_size', 'humanize_bitrate', 'humanize_duration', 'humanize_filesize',
	'humanize_sample_rate', 'int_to_bytes_be', 'int_to_bytes_le'
]

import os
import struct
from functools import reduce
from io import DEFAULT_BUFFER_SIZE

from attr import attrib, attrs


@attrs(slots=True)
class DataReader:
	data = attrib()
	_position = attrib(default=0, repr=False)

	def __attrs_post_init__(self):
		if hasattr(self.data, 'read'):
			self._position = self.data.tell()

	def peek(self, size=DEFAULT_BUFFER_SIZE):
		if size > DEFAULT_BUFFER_SIZE:
			size = DEFAULT_BUFFER_SIZE

		try:
			return self.data.peek(size)[:size]
		except AttributeError:
			return self.data[self._position:self._position + size]

	def read(self, size=None):
		try:
			read_ = self.data.read(size)
		except AttributeError:
			if size is None:
				size = len(self.data)

			read_ = self.data[self._position:self._position + size]

		self._position += len(read_)

		return read_

	def seek(self, offset, whence=os.SEEK_SET):
		try:
			self.data.seek(offset, whence)
			self._position = self.data.tell()
		except AttributeError:
			if whence == os.SEEK_CUR:
				self._position += offset
			elif whence == os.SEEK_SET:
				self._position = 0 + offset
			elif whence == os.SEEK_END:
				self._position = len(self.data) + offset
			else:
				raise ValueError("Invalid 'whence'.")

	def tell(self):
		return self._position


def bytes_to_int_be(b):
	return int.from_bytes(b, 'big')


def bytes_to_int_le(b):
	return int.from_bytes(b, 'little')


def int_to_bytes_be(i):
	return i.to_bytes((i.bit_length() + 7) // 8, 'big')


def int_to_bytes_le(i):
	return i.to_bytes((i.bit_length() + 7) // 8, 'little')


def decode_synchsafe_int(data, per_byte):
	return reduce(lambda value, element: (value << per_byte) + element, data, 0)


def get_image_size(data):
	if hasattr(data, 'read'):
		data = data.read(56)

	size = len(data)

	width = height = 0
	if size >= 10 and data[:6] in [b'GIF87a', b'GIF89a']:
		try:
			width, height = struct.unpack("<hh", data[6:10])
		except struct.error:
			raise ValueError("Invalid GIF file.")
	elif size >= 24 and data.startswith(b'\x89PNG') and data[12:16] == b'IHDR':
		try:
			width, height = struct.unpack(">LL", data[16:24])
		except struct.error:
			raise ValueError("Invalid PNG file.")
	elif size >= 16 and data.startswith(b'\x89PNG'):
		try:
			width, height = struct.unpack(">LL", data[8:16])
		except struct.error:
			raise ValueError("Invalid PNG file.")
	elif size >= 2 and data.startswith(b'\xff\xd8'):
		data = DataReader(data)
		try:
			size = 2
			ftype = 0
			while not 0xc0 <= ftype <= 0xcf or ftype in [0xc4, 0xc8, 0xcc]:
				data.seek(size, os.SEEK_CUR)
				while True:
					b = ord(data.read(1))

					if b != 0xff:
						break

				ftype = b
				size = struct.unpack('>H', data.read(2))[0] - 2

			data.seek(1, os.SEEK_CUR)
			height, width = struct.unpack('>HH', data.read(4))
		except struct.error:
			raise ValueError("Invalid JPEG file.")
	elif size >= 12 and data.startswith(b'\x00\x00\x00\x0cjP'):
		try:
			height, width = struct.unpack('>LL', data[48:])
		except struct.error:
			raise ValueError("Invalid JPEG2000 file.")

	return width, height


def humanize_bitrate(bitrate):
	for divisor, symbol in [(1000 ** 1, 'Kbps'), (1, 'bps')]:
		if bitrate >= divisor:
			break

	return f'{round(bitrate / divisor)} {symbol}'


def humanize_duration(duration):
	if duration // 3600:
		hours = int(duration // 3600)
		minutes = int(duration % 3600 // 60)
		seconds = round(duration % 3600 % 60)

		return f'{hours:02d}:{minutes:02d}:{seconds:02d}'
	elif duration // 60:
		minutes = int(duration // 60)
		seconds = round(duration % 60)

		return f'{minutes:02d}:{seconds:02d}'
	else:
		return f'00:{round(duration):02d}'


def humanize_filesize(filesize, *, precision=0):
	for divisor, symbol in [(1024 ** 3, 'GiB'), (1024 ** 2, 'MiB'), (1024 ** 1, 'KiB'), (1, 'B')]:
		if filesize >= divisor:
			break

	return f'{filesize / divisor:.{precision}f} {symbol}'


def humanize_sample_rate(sample_rate):
	for divisor, symbol in [(1000 ** 1, 'KHz'), (1, 'Hz')]:
		if sample_rate >= divisor:
			break

	value = sample_rate / divisor

	return f'{value if value.is_integer() else value:.1f} {symbol}'
