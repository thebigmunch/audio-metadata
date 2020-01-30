from pathlib import Path

from ward import (
	each,
	raises,
	test,
)

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


@test(
	"decode_bytestring",
	tags=['unit', 'utils', 'decode_bytestring']
)
def _(
	b=each(
		b'test\x00',
		b'\xff\xfet\x00e\x00s\x00t\x00',
		b'\xff\xfet\x00e\x00s\x00t\x00\x00',
		b'\xfe\xff\x00t\x00e\x00s\x00t',
		b'\xfe\xff\x00t\x00e\x00s\x00t\x00',
		b'test\x00',
		b'test\x00',
		b''
	),
	encoding=each(
		'iso-8859-1',
		'utf-16-le',
		'utf-16-le',
		'utf-16-be',
		'utf-16-be',
		'utf-8',
		None,
		None,
	),
	expected=each(
		'test',
		'test',
		'test',
		'test',
		'test',
		'test',
		'test',
		'',
	)
):
	if encoding is None:
		assert decode_bytestring(b) == expected
	else:
		assert decode_bytestring(b, encoding=encoding) == expected


@test(
	"decode_synchsafe_int",
	tags=['unit', 'utils', 'decode_synchsafe_int']
)
def _():
	assert decode_synchsafe_int(b'\x01\x7f', 7) == 255


@test(
	"determine_encoding",
	tags=['unit', 'utils', 'determine_encoding']
)
def _(
	b=each(
		b'\x00',
		b'\x01\xff\xfe',
		b'\x01\xfe\xff',
		b'\x02',
		b'\x03',
		b'\x04',
		b'',
	),
	encoding=each(
		'iso-8859-1',
		'utf-16-le',
		'utf-16-be',
		'utf-16-be',
		'utf-8',
		'iso-8859-1',
		'iso-8859-1',
	),
):
	assert determine_encoding(b) == encoding


@test(
	"get_image_size",
	tags=['unit', 'utils', 'get_image_size']
)
def test_get_image_size():
	for image in images:
		with image.open('rb') as f:
			assert get_image_size(f) == (16, 16)

	with raises(ValueError):
		get_image_size(b'')


@test(
	"humanize_bitrate",
	tags=['unit', 'utils', 'humanize_bitrate']
)
def _(
	bitrate=each(
		0,
		1,
		100,
		1000,
	),
	humanized=each(
		'0 bps',
		'1 bps',
		'100 bps',
		'1 Kbps',
	),
):
	assert humanize_bitrate(bitrate) == humanized


@test(
	"humanize_sample_rate",
	tags=['unit', 'utils', 'humanize_sample_rate']
)
def _(
	sample_rate=each(
		0,
		1,
		1000,
		44100,
	),
	humanized=each(
		'0.0 Hz',
		'1.0 Hz',
		'1.0 KHz',
		'44.1 KHz',
	),
):
	assert humanize_sample_rate(sample_rate) == humanized


@test(
	"split_encoded",
	tags=['unit', 'utils', 'split_encoded']
)
def _(
	b=each(
		b'test\x00',
		b'\xff\xfe\x00\x00\xff\xfet\x00e\x00s\x00t\x00\x00\x00',
		b'\xff\xfe\x00\x00\xff\xfet\x00e\x00s\x00t\x00\x00',
		b'\xff\xfet\x00e\x00s\x00t\x00\x00\x00',
		b'\xfe\xff\x00t\x00e\x00s\x00t\x00\x00',
		b'\xfe\xff\x00t\x00e\x00s\x00t\x00',
		b'test\x00',
		b'test',
	),
	encoding=each(
		'iso-8859-1',
		'utf-16-le',
		'utf-16-le',
		'utf-16-le',
		'utf-16-be',
		'utf-16-be',
		'utf-8',
		'iso-9959-1',
	),
	expected=each(
		(b'test', b''),
		(b'\xff\xfe', b'\xff\xfet\x00e\x00s\x00t\x00\x00\x00'),
		(b'\xff\xfe', b'\xff\xfet\x00e\x00s\x00t\x00\x00\x00'),
		(b'\xff\xfet\x00e\x00s\x00t\x00', b''),
		(b'\xfe\xff\x00t\x00e\x00s\x00t', b''),
		(b'\xfe\xff\x00t\x00e\x00s\x00t', b''),
		(b'test', b''),
		(b'test',),
	),
):
	assert split_encoded(b, encoding) == expected
