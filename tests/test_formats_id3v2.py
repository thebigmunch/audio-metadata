from pathlib import Path

import pytest

from audio_metadata import (
	ID3Version,
	ID3v2Flags,
	ID3v2Frames,
	ID3v2Header,
	InvalidHeader,
)


def test_ID3v2Frames():
	with pytest.raises(ValueError):
		ID3v2Frames(id3_version=(1, 0))

	with pytest.raises(ValueError):
		ID3v2Frames(id3_version=None)

	with pytest.raises(ValueError):
		ID3v2Frames.load(b'data', (1, 0))

	with pytest.raises(ValueError):
		ID3v2Frames.load(b'data', None)

	v22_frames_init = ID3v2Frames(id3_version=ID3Version.v22)
	v22_frames_init_tuple = ID3v2Frames(id3_version=(2, 2))
	v22_frames_load = ID3v2Frames.load(
		(Path(__file__).parent / 'files' / 'audio' / 'test-mp3-id3v22.mp3').read_bytes()[10:],
		ID3Version.v22,
	)

	v23_frames_init = ID3v2Frames(id3_version=ID3Version.v23)
	v23_frames_init_tuple = ID3v2Frames(id3_version=(2, 3))
	v23_frames_load = ID3v2Frames.load(
		(Path(__file__).parent / 'files' / 'audio' / 'test-mp3-id3v23.mp3').read_bytes()[10:],
		ID3Version.v23,
	)

	v24_frames_init = ID3v2Frames(id3_version=ID3Version.v24)
	v24_frames_init_tuple = ID3v2Frames(id3_version=(2, 4))
	v24_frames_load = ID3v2Frames.load(
		(Path(__file__).parent / 'files' / 'audio' / 'test-mp3-id3v24.mp3').read_bytes()[10:],
		ID3Version.v24,
	)

	default_frames = ID3v2Frames()

	assert v22_frames_init._version == v22_frames_init_tuple._version == v22_frames_load._version == ID3Version.v22
	assert v22_frames_init.FIELD_MAP == v22_frames_init_tuple.FIELD_MAP == v22_frames_load.FIELD_MAP == ID3v2Frames._v22_FIELD_MAP

	assert v23_frames_init._version == v23_frames_init_tuple._version == v23_frames_load._version == ID3Version.v23
	assert v23_frames_init.FIELD_MAP == v23_frames_init_tuple.FIELD_MAP == v23_frames_load.FIELD_MAP == ID3v2Frames._v23_FIELD_MAP

	assert v24_frames_init._version == v24_frames_init_tuple._version == v24_frames_load._version == default_frames._version == ID3Version.v24
	assert v24_frames_init.FIELD_MAP == v24_frames_init_tuple.FIELD_MAP == ID3v2Frames._v24_FIELD_MAP
	assert v24_frames_load.FIELD_MAP == default_frames.FIELD_MAP == ID3v2Frames._v24_FIELD_MAP


def test_ID3v2Flags():
	assert all(
		flag is True
		for flag in ID3v2Flags(1, 1, 1, 1).values()
	)

	assert all(
		flag is True
		for flag in ID3v2Flags(True, True, True, True).values()
	)

	assert all(
		flag is False
		for flag in ID3v2Flags(0, 0, 0, 0).values()
	)

	assert all(
		flag is False
		for flag in ID3v2Flags(False, False, False, False).values()
	)


def test_ID3v2Header():
	v24_header_load = ID3v2Header.load(Path(__file__).parent / 'files' / 'audio' / 'test-mp3-id3v24.mp3')
	v24_header_init = ID3v2Header(
		2254,
		flags=ID3v2Flags(
			experimental=False,
			extended=False,
			footer=False,
			unsync=True,
		),
		version=ID3Version.v24,
	)

	with pytest.raises(InvalidHeader):
		ID3v2Header.load(
			(Path(__file__).parent / 'files' / 'audio' / 'test-mp3-id3v24.mp3').read_bytes()[3:]
		)

	assert v24_header_load == v24_header_init
