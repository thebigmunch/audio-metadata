from ward import (
	raises,
	test,
	using,
)

from audio_metadata import (
	FormatError,
	ID3PictureType,
	ID3Version,
	ID3v2Frame,
	ID3v2FrameFlags,
	ID3v2Picture,
	UnsupportedFormat,
)
from tests.fixtures import (
	id3v22_picture,
	id3v22_picture_data,
	id3v24_picture,
	id3v24_picture_data,
)


@test(
	'ID3v2Picture',
	tags=['unit', 'id3', 'id3v2', 'id3v2frames', 'ID3v2Picture'],
)
@using(
	id3v22_picture=id3v22_picture,
	id3v22_picture_data=id3v22_picture_data,
	id3v24_picture=id3v24_picture,
	id3v24_picture_data=id3v24_picture_data,
)
def _(
	id3v22_picture,
	id3v22_picture_data,
	id3v24_picture,
	id3v24_picture_data,
):
	# v2.4
	id3v24_picture_init = ID3v2Picture(
		data=id3v24_picture_data,
		description='',
		height=16,
		mime_type='image/png',
		type=ID3PictureType.COVER_FRONT,
		width=16,
	)
	id3v24_picture_parse = ID3v2Picture.parse(id3v24_picture)

	assert id3v24_picture_init == id3v24_picture_parse

	# v2.2
	id3v22_picture_init = ID3v2Picture(
		data=id3v22_picture_data,
		description='',
		height=16,
		mime_type='PNG',
		type=ID3PictureType.COVER_FRONT,
		width=16,
	)
	id3v22_picture_parse = ID3v2Picture.parse(id3v22_picture, id3v22=True)

	assert id3v22_picture_init == id3v22_picture_parse


@test(
	'ID3v2FrameFlags',
	tags=['unit', 'id3', 'id3v2', 'id3v2frames', 'ID3v2FrameFlags'],
)
def _():
	id3v24_frame_flags_init = ID3v2FrameFlags(
		alter_tag=False,
		alter_file=False,
		read_only=False,
		grouped=False,
		compressed=False,
		encrypted=False,
		unsync=False,
		data_length_indicator=False,
	)
	id3v24_frame_flags_parse = ID3v2FrameFlags.parse(
		b'\x00\x00',
		ID3Version.v24,
	)

	assert id3v24_frame_flags_init == id3v24_frame_flags_parse == ID3v2FrameFlags()

	id3v24_frame_flags_init = ID3v2FrameFlags(
		alter_tag=True,
		alter_file=True,
		read_only=True,
		grouped=True,
		compressed=True,
		encrypted=True,
		unsync=True,
		data_length_indicator=True,
	)
	id3v24_frame_flags_parse = ID3v2FrameFlags.parse(
		b'pO',
		ID3Version.v24,
	)

	assert id3v24_frame_flags_init == id3v24_frame_flags_parse

	id3v23_frame_flags_init = ID3v2FrameFlags(
		alter_tag=False,
		alter_file=False,
		read_only=False,
		grouped=False,
		compressed=False,
		encrypted=False,
	)
	id3v23_frame_flags_parse = ID3v2FrameFlags.parse(
		b'\x00\x00',
		ID3Version.v23,
	)

	assert id3v23_frame_flags_init == id3v23_frame_flags_parse == ID3v2FrameFlags()

	id3v23_frame_flags_init = ID3v2FrameFlags(
		alter_tag=True,
		alter_file=True,
		read_only=True,
		grouped=True,
		compressed=True,
		encrypted=True,
	)
	id3v23_frame_flags_parse = ID3v2FrameFlags.parse(
		b'\xe0\xe0',
		ID3Version.v23,
	)

	assert id3v23_frame_flags_init == id3v23_frame_flags_parse


@test(
	'Frame size <= 0 in ID3v2Frame raises FormatError',
	tags=['unit', 'id3', 'id3v2', 'id3v2frames', 'ID3v2Frame'],
)
def _():
	with raises(FormatError) as exc:
		ID3v2Frame.parse(
			b'TEST\x00\x00\x00\x00\x00\x00VALUE',
			ID3Version.v24,
			False,
		)
	assert str(exc.raised) == "ID3v2 frame size must be greater than 0."


@test(
	'Unsupported ID3 version in ID3v2Frame raises ValueError',
	tags=['unit', 'id3', 'id3v2', 'id3v2frames', 'ID3v2Frame'],
)
def _():
	with raises(ValueError) as exc:
		ID3v2Frame.parse(
			b'TEST\x00\x00\x00\x05\x00\x00VALUE',
			ID3Version.v11,
			False,
		)
	assert str(exc.raised) == "Unsupported ID3 version: ID3Version.v11."


@test(
	'Encrypted ID3v2Frame raises UnsupportedFormat',
	tags=['unit', 'id3', 'id3v2', 'id3v2frames', 'ID3v2Frame'],
)
def _():
	with raises(UnsupportedFormat) as exc:
		ID3v2Frame.parse(
			b'TEST\x00\x00\x00\x05\x00\x04VALUE',
			ID3Version.v24,
			False,
		)
	assert str(exc.raised) == "ID3v2 frame encryption is not supported."


@test(
	'Compressed ID3v2Frame without data length indicator raises FormatError',
	tags=['unit', 'id3', 'id3v2', 'id3v2frames', 'ID3v2Frame'],
)
def _():
	with raises(FormatError) as exc:
		ID3v2Frame.parse(
			b'TEST\x00\x00\x00\x05\x00\x08VALUE',
			ID3Version.v24,
			False,
		)
	assert str(exc.raised) == "ID3v2 frame compression flag set without data length indicator."


@test(
	'ID3v2Frame with compression',
	tags=['unit', 'id3', 'id3v2', 'id3v2frames', 'ID3v2Frame'],
)
def _():
	assert ID3v2Frame.parse(
		b'TEST\x00\x00\x00\x11\x00\x09\x00\x00\x00\x05x\x9c\x0bs\xf4\tu\x05\x00\x04\x8a\x01~',
		ID3Version.v24,
		False,
	) == ID3v2Frame(
		name='TEST',
		value=b'VALUE',
		encoding=None,
	)


@test(
	'ID3v2Frame with unsynchronization',
	tags=['unit', 'id3', 'id3v2', 'id3v2frames', 'ID3v2Frame'],
)
def _():
	assert ID3v2Frame.parse(
		b'TEST\x00\x00\x00\x07\x00\x02\xFF\x00\xFEVALUE',
		ID3Version.v24,
		False,
	) == ID3v2Frame(
		name='TEST',
		value=b'\xFF\xFEVALUE',
		encoding=None,
	)


@test(
	'ID3v2Frame',
	tags=['unit', 'id3', 'id3v2', 'id3v2frames', 'ID3v2Frame'],
)
def _():
	# v2.4
	assert ID3v2Frame(
		name='TEST',
		value=b'VALUE',
		encoding=None,
	) == ID3v2Frame.parse(
		b'TEST\x00\x00\x00\x05\x00\x00VALUE',
		ID3Version.v24,
		False,
	)

	# v2.3
	assert ID3v2Frame(
		name='TEST',
		value=b'VALUE',
		encoding=None,
	) == ID3v2Frame.parse(
		b'TEST\x00\x00\x00\x05\x00\x00VALUE',
		ID3Version.v23,
		False,
	)

	# v2.2
	assert ID3v2Frame(
		name='TES',
		value=b'VALUE',
		encoding=None,
	) == ID3v2Frame.parse(
		b'TES\x00\x00\x05VALUE',
		ID3Version.v22,
		False,
	)
