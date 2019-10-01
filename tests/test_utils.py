import os
from io import DEFAULT_BUFFER_SIZE, BytesIO, FileIO
from pathlib import Path

import pytest

from audio_metadata.utils import (
	DataReader,
	decode_bytestring,
	decode_synchsafe_int,
	determine_encoding,
	get_image_size,
	humanize_bitrate,
	humanize_duration,
	humanize_filesize,
	humanize_sample_rate,
	split_encoded
)

images = (Path(__file__).parent / 'files' / 'image').glob('*.*')
data_file = (Path(__file__).parent / 'files' / 'audio' / 'test-wav-riff.wav')
data_file_size = os.path.getsize(data_file)


def test_DataReader_BytesIO():
	data = DataReader(
		BytesIO(data_file.read_bytes())
	)

	assert len(data.peek(10)) == 10
	assert len(data.peek()) == DEFAULT_BUFFER_SIZE
	assert len(data.peek(100000)) == DEFAULT_BUFFER_SIZE

	assert data.peek(10) == data.read(10)

	data.seek(-10, os.SEEK_CUR)
	assert data.tell() == 0

	assert len(data.read()) == data.tell() == data_file_size

	data.seek(-10, os.SEEK_END)
	assert data.tell() == data_file_size - 10
	assert len(data.peek(20)) == 10

	data.seek(0)
	assert data.tell() == 0

	data.seek(10, os.SEEK_SET)
	assert data.tell() == 10

	data.close()

	with pytest.raises(ValueError):
		data.read()


def test_DataReader_DataReader_FileIO():
	data = DataReader(
		DataReader(
			FileIO(data_file, 'rb')
		)
	)

	assert len(data.peek(10)) == 10
	assert len(data.peek()) == DEFAULT_BUFFER_SIZE
	assert len(data.peek(100000)) == DEFAULT_BUFFER_SIZE

	assert data.peek(10) == data.read(10)

	data.seek(-10, os.SEEK_CUR)
	assert data.tell() == 0

	assert len(data.read()) == data.tell() == data_file_size

	data.seek(-10, os.SEEK_END)
	assert data.tell() == data_file_size - 10
	assert len(data.peek(20)) == 10

	data.seek(0)
	assert data.tell() == 0

	data.seek(10, os.SEEK_SET)
	assert data.tell() == 10

	data.close()

	with pytest.raises(ValueError):
		data.read()


def test_DataReader_DataReader_BytesIO():
	data = DataReader(
		DataReader(
			BytesIO(data_file.read_bytes())
		)
	)

	assert len(data.peek(10)) == 10
	assert len(data.peek()) == DEFAULT_BUFFER_SIZE
	assert len(data.peek(100000)) == DEFAULT_BUFFER_SIZE

	assert data.peek(10) == data.read(10)

	data.seek(-10, os.SEEK_CUR)
	assert data.tell() == 0

	assert len(data.read()) == data.tell() == data_file_size

	data.seek(-10, os.SEEK_END)
	assert data.tell() == data_file_size - 10
	assert len(data.peek(20)) == 10

	data.seek(0)
	assert data.tell() == 0

	data.seek(10, os.SEEK_SET)
	assert data.tell() == 10

	data.close()

	with pytest.raises(ValueError):
		data.read()


def test_DataReader_FileIO():
	data = DataReader(FileIO(data_file, 'rb'))

	assert len(data.peek(10)) == 10
	assert len(data.peek()) == DEFAULT_BUFFER_SIZE
	assert len(data.peek(100000)) == DEFAULT_BUFFER_SIZE

	assert data.peek(10) == data.read(10)

	data.seek(-10, os.SEEK_CUR)
	assert data.tell() == 0

	assert len(data.read()) == data.tell() == data_file_size

	data.seek(-10, os.SEEK_END)
	assert data.tell() == data_file_size - 10
	assert len(data.peek(20)) == 10

	data.seek(0)
	assert data.tell() == 0

	data.seek(10, os.SEEK_SET)
	assert data.tell() == 10

	data.close()

	with pytest.raises(ValueError):
		data.read()


def test_DataReader_bytes():
	data = DataReader(data_file.read_bytes())

	assert len(data.peek(10)) == 10
	assert len(data.peek()) == DEFAULT_BUFFER_SIZE
	assert len(data.peek(100000)) == DEFAULT_BUFFER_SIZE

	assert data.peek(10) == data.read(10)

	data.seek(-10, os.SEEK_CUR)
	assert data.tell() == 0

	assert len(data.read()) == data.tell() == data_file_size

	data.seek(-10, os.SEEK_END)
	assert data.tell() == data_file_size - 10
	assert len(data.peek(20)) == 10

	data.seek(0)
	assert data.tell() == 0

	data.seek(10, os.SEEK_SET)
	assert data.tell() == 10

	data.close()

	with pytest.raises(ValueError):
		data.read()


def test_DataReader_fileobj():
	data = DataReader(data_file.open('rb'))

	assert len(data.peek(10)) == 10
	assert len(data.peek()) == DEFAULT_BUFFER_SIZE
	assert len(data.peek(100000)) == DEFAULT_BUFFER_SIZE

	assert data.peek(10) == data.read(10)

	data.seek(-10, os.SEEK_CUR)
	assert data.tell() == 0

	assert len(data.read()) == data.tell() == data_file_size

	data.seek(-10, os.SEEK_END)
	assert data.tell() == data_file_size - 10
	assert len(data.peek(20)) == 10

	data.seek(0)
	assert data.tell() == 0

	data.seek(10, os.SEEK_SET)
	assert data.tell() == 10

	data.close()

	with pytest.raises(ValueError):
		data.read()


def test_DataReader_filepath():
	data = DataReader(data_file)

	assert len(data.peek(10)) == 10
	assert len(data.peek()) == DEFAULT_BUFFER_SIZE
	assert len(data.peek(100000)) == DEFAULT_BUFFER_SIZE

	assert data.peek(10) == data.read(10)

	data.seek(-10, os.SEEK_CUR)
	assert data.tell() == 0

	assert len(data.read()) == data.tell() == data_file_size

	data.seek(-10, os.SEEK_END)
	assert data.tell() == data_file_size - 10
	assert len(data.peek(20)) == 10

	data.seek(0)
	assert data.tell() == 0

	data.seek(10, os.SEEK_SET)
	assert data.tell() == 10

	data.close()

	with pytest.raises(ValueError):
		data.read()


@pytest.mark.parametrize(
	'b,encoding,expected',
	[
		(b'test\x00', 'iso-8859-1', 'test'),
		(b'\xff\xfet\x00e\x00s\x00t\x00', 'utf-16-le', 'test'),
		(b'\xff\xfet\x00e\x00s\x00t\x00\x00', 'utf-16-le', 'test'),
		(b'\xfe\xff\x00t\x00e\x00s\x00t', 'utf-16-be', 'test'),
		(b'\xfe\xff\x00t\x00e\x00s\x00t\x00', 'utf-16-be', 'test'),
		(b'test\x00', 'utf-8', 'test'),
		(b'test\x00', None, 'test'),
		(b'', None, '')
	]
)
def test_decode_bytestring(b, encoding, expected):
	if encoding is None:
		assert decode_bytestring(b) == expected
	else:
		assert decode_bytestring(b, encoding=encoding) == expected


def test_decode_synchsafe_int():
	assert decode_synchsafe_int(b'\x01\x7f', 7) == 255


@pytest.mark.parametrize(
	'b,encoding',
	[
		(b'\x00', 'iso-8859-1'),
		(b'\x01\xff\xfe', 'utf-16-le'),
		(b'\x01\xfe\xff', 'utf-16-be'),
		(b'\x02', 'utf-16-be'),
		(b'\x03', 'utf-8'),
		(b'\x04', 'iso-8859-1'),
		(b'', 'iso-8859-1')
	]
)
def test_determine_encoding(b, encoding):
	assert determine_encoding(b) == encoding


def test_get_image_size():
	for image in images:
		with image.open('rb') as f:
			assert get_image_size(f) == (16, 16)

	with pytest.raises(ValueError):
		get_image_size(b'')


@pytest.mark.parametrize(
	'bitrate,humanized',
	[
		(0, '0 bps'),
		(1, '1 bps'),
		(100, '100 bps'),
		(1000, '1 Kbps')
	]
)
def test_humanize_bitrate(bitrate, humanized):
	assert humanize_bitrate(bitrate) == humanized


@pytest.mark.parametrize(
	'duration,humanized',
	[
		(0, '00:00'),
		(1, '00:01'),
		(60, '01:00'),
		(3600, '01:00:00')
	]
)
def test_humanize_duration(duration, humanized):
	assert humanize_duration(duration) == humanized


@pytest.mark.parametrize(
	'filesize,precision,humanized',
	[
		(0, 0, '0 B'),
		(1, 0, '1 B'),
		(1024, 0, '1 KiB'),
		(1500, 2, '1.46 KiB'),
		(1_048_576, 0, '1 MiB'),
		(2_048_576, 2, '1.95 MiB'),
		(1_073_741_824, 0, '1 GiB'),
		(2_073_741_824, 2, '1.93 GiB'),
		(1_099_511_627_776, 0, '1024 GiB'),
		(2_099_511_627_776, 2, '1955.32 GiB')
	]
)
def test_humanize_filesize(filesize, precision, humanized):
	assert humanize_filesize(filesize, precision=precision) == humanized


@pytest.mark.parametrize(
	'sample_rate,humanized',
	[
		(0, '0.0 Hz'),
		(1, '1.0 Hz'),
		(1000, '1.0 KHz'),
		(44100, '44.1 KHz')
	]
)
def test_humanize_sample_rate(sample_rate, humanized):
	assert humanize_sample_rate(sample_rate) == humanized


@pytest.mark.parametrize(
	'b,encoding,expected',
	[
		(
			b'test\x00',
			'iso-8859-1',
			(b'test', b'')
		),
		(
			b'\xff\xfe\x00\x00\xff\xfet\x00e\x00s\x00t\x00\x00\x00',
			'utf-16-le',
			(b'\xff\xfe', b'\xff\xfet\x00e\x00s\x00t\x00\x00\x00')
		),
		(
			b'\xff\xfe\x00\x00\xff\xfet\x00e\x00s\x00t\x00\x00',
			'utf-16-le',
			(b'\xff\xfe', b'\xff\xfet\x00e\x00s\x00t\x00\x00\x00')
		),
		(
			b'\xff\xfet\x00e\x00s\x00t\x00\x00\x00',
			'utf-16-le',
			(b'\xff\xfet\x00e\x00s\x00t\x00', b'')
		),
		(
			b'\xfe\xff\x00t\x00e\x00s\x00t\x00\x00',
			'utf-16-be',
			(b'\xfe\xff\x00t\x00e\x00s\x00t', b'')
		),
		(
			b'\xfe\xff\x00t\x00e\x00s\x00t\x00',
			'utf-16-be',
			(b'\xfe\xff\x00t\x00e\x00s\x00t', b'')
		),
		(
			b'test\x00',
			'utf-8',
			(b'test', b'')
		),
		(
			b'test',
			'iso-9959-1',
			(b'test',)
		)
	]
)
def test_split_encoded(b, encoding, expected):
	assert split_encoded(b, encoding) == expected
