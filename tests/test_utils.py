from pathlib import Path

import pytest

from audio_metadata.utils import (
	decode_bytestring,
	decode_synchsafe_int,
	determine_encoding,
	get_image_size,
	humanize_bitrate,
	humanize_sample_rate,
	split_encoded
)

images = (Path(__file__).parent / 'files' / 'image').glob('*.*')


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
