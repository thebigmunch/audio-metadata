from pathlib import Path

from ward import (
	each,
	raises,
	test,
)

from audio_metadata.utils import (
	apply_unsynchronization,
	decode_bytestring,
	decode_synchsafe_int,
	determine_encoding,
	get_image_size,
	humanize_bitrate,
	humanize_duration,
	humanize_sample_rate,
	remove_unsynchronization,
	split_encoded
)

images = (Path(__file__).parent / 'image').glob('*.*')


@test(
	"apply_unsynchronization",
	tags=['unit', 'utils', 'apply_unsynchronization'],
)
def _(
	b=each(
		b'TEST',
		b'\xFF',
		b'\x00',
		b'\xFF\xFE',
		b'\xFF\x00',
		b'\xFF\x00\xFF',
		b'\xFF\x00\x00',
		b'\xFF\x00\xFF\xFE',
	),
	expected=each(
		b'TEST',
		b'\xFF',
		b'\x00',
		b'\xFF\x00\xFE',
		b'\xFF\x00\x00',
		b'\xFF\x00\x00\xFF',
		b'\xFF\x00\x00\x00',
		b'\xFF\x00\x00\xFF\x00\xFE',
	),
):
	assert apply_unsynchronization(b) == expected


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
	tags=['unit', 'utils', 'decode_synchsafe_int'],
)
def _(
	args=each(
		(b'\x00\x00\x01\x7f', 7),
		(b'\x00\x00\x02\x7f', 6),
		(b'\x00\x00\x01\x7f', 6),
	),
	expected=each(
		255,
		255,
		191,
	)
):
	assert decode_synchsafe_int(*args) == expected


@test(
	"Decoding too large synchsafe int raises ValueError",
	tags=['unit', 'utils', 'decode_synchsafe_int'],
)
def _(
	args=each(
		(b'\x80\x00\x00\x00', 7),
		(b'@\x00\x00\x00', 6),
	)
):
	with raises(ValueError):
		decode_synchsafe_int(*args)


@test(
	"encode_synchsafe_int",
	tags=['unit', 'utils', 'encode_synchsafe_int'],
)
def _(
	args=each(
		(255, 7),
		(255, 6),
	),
	expected=each(
		b'\x00\x00\x01\x7f',
		b'\x00\x00\x02\x7f',
	),
):
	assert encode_synchsafe_int(*args) == expected


@test(
	"Encoding too large synchsafe int raises ValueError",
	tags=['unit', 'utils', 'encode_synchsafe_int'],
)
def _(
	args=each(
		(268435456, 7),
		(16777216, 6),
	)
):
	with raises(ValueError):
		encode_synchsafe_int(*args)


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
	"remove_unsynchronization",
	tags=['unit', 'utils', 'remove_unsynchronization'],
)
def _(
	b=each(
		b'TEST',
		b'\xFF',
		b'\x00',
		b'\xFF\x00\xFE',
		b'\xFF\x00\x00',
		b'\xFF\x00\x00\xFF',
		b'\xFF\x00\x00\x00',
		b'\xFF\x00\x00\xFF\x00\xFE',
	),
	expected=each(
		b'TEST',
		b'\xFF',
		b'\x00',
		b'\xFF\xFE',
		b'\xFF\x00',
		b'\xFF\x00\xFF',
		b'\xFF\x00\x00',
		b'\xFF\x00\xFF\xFE',
	),
):
	assert remove_unsynchronization(b) == expected


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
		None,
		0,
		1,
		100,
		1000,
	),
	humanized=each(
		None,
		'0 bps',
		'1 bps',
		'100 bps',
		'1 Kbps',
	),
):
	assert humanize_bitrate(bitrate) == humanized


@test(
	"humanize_duration",
	tags=['unit', 'utils', 'humanize_duration']
)
def _(
	duration=each(
		None,
		0,
		1,
		60,
		3600,
	),
	humanized=each(
		None,
		'00:00',
		'00:01',
		'01:00',
		'01:00:00',
	),
):
	assert humanize_duration(duration) == humanized


@test(
	"humanize_sample_rate",
	tags=['unit', 'utils', 'humanize_sample_rate']
)
def _(
	sample_rate=each(
		None,
		0,
		1,
		1000,
		44100,
	),
	humanized=each(
		None,
		'0.0 Hz',
		'1.0 Hz',
		'1.0 KHz',
		'44.1 KHz',
	),
):
	assert humanize_sample_rate(sample_rate) == humanized


@test(
	"split_encoded ({b}, {encoding})",
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
		[b'test'],
		[b'\xff\xfe', b'\xff\xfet\x00e\x00s\x00t\x00'],
		[b'\xff\xfe', b'\xff\xfet\x00e\x00s\x00t\x00'],
		[b'\xff\xfet\x00e\x00s\x00t\x00'],
		[b'\xfe\xff\x00t\x00e\x00s\x00t'],
		[b'\xfe\xff\x00t\x00e\x00s\x00t'],
		[b'test'],
		[b'test'],
	),
):
	assert split_encoded(b, encoding) == expected
