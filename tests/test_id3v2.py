from ward import (
	each,
	raises,
	test,
	using,
)

from audio_metadata import (
	FormatError,
	ID3Version,
	ID3v2Flags,
	ID3v2FrameAliases,
	ID3v2Frames,
	ID3v2Header,
)
from tests.fixtures import (
	id3v22,
	id3v23,
	id3v24,
	id3v24_unsync,
	null,
)


@test(
	"ID3v2Frames",
	tags=['unit', 'id3', 'id3v2', 'ID3v2Frames'],
)
@using(
	null=null,
	id3v22=id3v22,
	id3v23=id3v23,
	id3v24=id3v24,
)
def _(null, id3v22, id3v23, id3v24):
	with raises(ValueError) as exc:
		ID3v2Frames(id3_version=(1, 0))
	assert str(exc.raised) == "Unsupported ID3 version: (1, 0)."

	with raises(ValueError) as exc:
		ID3v2Frames(id3_version=None)
	assert str(exc.raised) == "None is not a valid ID3Version"

	with raises(ValueError) as exc:
		ID3v2Frames.parse(null, (1, 0))
	assert str(exc.raised) == "Unsupported ID3 version: ID3Version.v10."

	with raises(ValueError) as exc:
		ID3v2Frames.parse(null, None)
	assert str(exc.raised) == "None is not a valid ID3Version"

	v22_frames_init = ID3v2Frames(id3_version=ID3Version.v22)
	v22_frames_init_tuple = ID3v2Frames(id3_version=(2, 2))
	v22_frames_load = ID3v2Frames.parse(
		id3v22[10:],
		ID3Version.v22,
	)

	v23_frames_init = ID3v2Frames(id3_version=ID3Version.v23)
	v23_frames_init_tuple = ID3v2Frames(id3_version=(2, 3))
	v23_frames_load = ID3v2Frames.parse(
		id3v23[10:],
		ID3Version.v23,
	)

	v24_frames_init = ID3v2Frames(id3_version=ID3Version.v24)
	v24_frames_init_tuple = ID3v2Frames(id3_version=(2, 4))
	v24_frames_load = ID3v2Frames.parse(
		id3v24[10:],
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
			compressed=1,
			extended=1,
			experimental=1,
			footer=1,
			unsync=1,
		),
		ID3v2Flags(
			compressed=True,
			extended=True,
			experimental=True,
			footer=True,
			unsync=True,
		),
		ID3v2Flags(
			compressed=0,
			extended=0,
			experimental=0,
			footer=0,
			unsync=0,
		),
		ID3v2Flags(
			compressed=False,
			extended=False,
			experimental=False,
			footer=False,
			unsync=False,
		),
		ID3v2Flags(),
	),
	expected=each(
		True,
		True,
		False,
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
@using(
	null=null,
	id3v24=id3v24,
	id3v24_unsync=id3v24_unsync
)
def _(null, id3v24, id3v24_unsync):
	with raises(FormatError) as exc:
		ID3v2Header.parse(null)
	assert str(exc.raised) == "Valid ID3v2 header not found."

	v24_header_load = ID3v2Header.parse(id3v24)
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

	v24_header_load = ID3v2Header.parse(id3v24_unsync)
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
