from pathlib import Path

from ward import (
	each,
	raises,
	test,
)

from audio_metadata import (
	ID3Version,
	ID3v2FrameAliases,
	ID3v2Flags,
	ID3v2Frames,
	ID3v2Header,
	InvalidHeader,
)


@test(
	"ID3v2Frames",
	tags=['unit', 'id3', 'id3v2', 'ID3v2Frames'],
)
def _():
	with raises(ValueError):
		ID3v2Frames(id3_version=(1, 0))

	with raises(ValueError):
		ID3v2Frames(id3_version=None)

	with raises(ValueError):
		ID3v2Frames.parse(b'data', (1, 0))

	with raises(ValueError):
		ID3v2Frames.parse(b'data', None)

	v22_frames_init = ID3v2Frames(id3_version=ID3Version.v22)
	v22_frames_init_tuple = ID3v2Frames(id3_version=(2, 2))
	v22_frames_load = ID3v2Frames.parse(
		(Path(__file__).parent / 'files' / 'audio' / 'test-mp3-id3v22.mp3').read_bytes()[10:],
		ID3Version.v22,
	)

	v23_frames_init = ID3v2Frames(id3_version=ID3Version.v23)
	v23_frames_init_tuple = ID3v2Frames(id3_version=(2, 3))
	v23_frames_load = ID3v2Frames.parse(
		(Path(__file__).parent / 'files' / 'audio' / 'test-mp3-id3v23.mp3').read_bytes()[10:],
		ID3Version.v23,
	)

	v24_frames_init = ID3v2Frames(id3_version=ID3Version.v24)
	v24_frames_init_tuple = ID3v2Frames(id3_version=(2, 4))
	v24_frames_load = ID3v2Frames.parse(
		(Path(__file__).parent / 'files' / 'audio' / 'test-mp3-id3v24.mp3').read_bytes()[10:],
		ID3Version.v24,
	)

	default_frames = ID3v2Frames()

	assert v22_frames_init == v22_frames_init_tuple
	assert v22_frames_load._version == ID3Version.v22
	assert v22_frames_load.FIELD_MAP == ID3v2FrameAliases[ID3Version.v22]

	assert v23_frames_init == v23_frames_init_tuple
	assert v23_frames_load._version == ID3Version.v23
	assert v23_frames_load.FIELD_MAP == ID3v2FrameAliases[ID3Version.v23]

	assert v24_frames_init == v24_frames_init_tuple == default_frames
	assert v24_frames_load._version == ID3Version.v24
	assert v24_frames_load.FIELD_MAP == ID3v2FrameAliases[ID3Version.v24]


@test(
	"ID3v2Flags",
	tags=['unit', 'id3', 'id3v2', 'ID3v2Flags'],
)
def _(
	flags=each(
		ID3v2Flags(
			extended=1,
			experimental=1,
			footer=1,
			unsync=1,
		),
		ID3v2Flags(
			extended=True,
			experimental=True,
			footer=True,
			unsync=True,
		),
		ID3v2Flags(
			extended=0,
			experimental=0,
			footer=0,
			unsync=0,
		),
		ID3v2Flags(
			extended=False,
			experimental=False,
			footer=False,
			unsync=False,
		),
	),
	expected=each(
		True,
		True,
		False,
		False,
	)
):
	assert all(
		flag is expected
		for flag in flags.values()
	)


@test(
	"ID3v2Header",
	tags=['unit', 'id3', 'id3v2', 'ID3v2Header'],
)
def test_ID3v2Header():
	v24_header_load = ID3v2Header.parse(Path(__file__).parent / 'files' / 'audio' / 'test-mp3-id3v24.mp3')
	v24_header_init = ID3v2Header(
		size=2254,
		flags=ID3v2Flags(
			experimental=False,
			extended=False,
			footer=False,
			unsync=False,
		),
		version=ID3Version.v24,
	)

	assert v24_header_load == v24_header_init

	v24_header_load = ID3v2Header.parse(Path(__file__).parent / 'files' / 'audio' / 'test-mp3-id3v24-unsync.mp3')
	v24_header_init = ID3v2Header(
		size=2254,
		flags=ID3v2Flags(
			experimental=False,
			extended=False,
			footer=False,
			unsync=True,
		),
		version=ID3Version.v24,
	)

	assert v24_header_load == v24_header_init

	with raises(InvalidHeader):
		ID3v2Header.parse(
			(Path(__file__).parent / 'files' / 'audio' / 'test-mp3-id3v24.mp3').read_bytes()[3:]
		)
