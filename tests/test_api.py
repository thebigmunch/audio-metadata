from pathlib import Path

from ward import (
	each,
	raises,
	test,
	using,
)

import audio_metadata
from audio_metadata import UnsupportedFormat
from tests.fixtures import id3v2_header

AUDIO_FILEPATHS = list((Path(__file__).parent / 'audio').iterdir())


@test(
	"ID3v2-only is None",
	tags=['unit', 'api', 'determine_format'],
)
@using(id3v2_header=id3v2_header)
def _(id3v2_header):
	assert audio_metadata.determine_format(id3v2_header) is None


@test(
	"Invalid file is None",
	tags=['unit', 'api', 'determine_format']
)
def _():
	assert audio_metadata.determine_format([__file__]) is None


@test(
	"Non-audio file is None",
	tags=['unit', 'api', 'determine_format']
)
def _():
	assert audio_metadata.determine_format(__file__) is None


@test(
	"Bytes ({fp.name})",
	tags=['integration', 'api', 'determine_format']
)
def _(fp=each(*AUDIO_FILEPATHS)):
	assert issubclass(
		audio_metadata.determine_format(fp.read_bytes()),
		audio_metadata.Format
	)


@test(
	"Filepath ({fp.name})",
	tags=['integration', 'api', 'determine_format']

)
def _(fp=each(*AUDIO_FILEPATHS)):
	assert issubclass(
		audio_metadata.determine_format(str(fp)),
		audio_metadata.Format
	)


@test(
	"File-like object ({fp.name})",
	tags=['integration', 'api', 'determine_format']
)
def _(fp=each(*AUDIO_FILEPATHS)):
	assert issubclass(
		audio_metadata.determine_format(fp.open('rb')),
		audio_metadata.Format
	)


@test(
	"Path object ({fp.name})",
	tags=['integration', 'api', 'determine_format']
)
def _(fp=each(*AUDIO_FILEPATHS)):
	assert issubclass(
		audio_metadata.determine_format(fp),
		audio_metadata.Format
	)


@test(
	"Non-audio file raises UnsupportedFormat",
	tags=['unit', 'api', 'load'],
)
def _():
	with raises(UnsupportedFormat) as exc:
		audio_metadata.load(__file__)
	assert str(exc.raised) == "Supported format signature not found."


@test(
	"Non-file raises ValueError",
	tags=['unit', 'api', 'load'],
)
def _():
	with raises(ValueError) as exc:
		audio_metadata.load(b'test')
	assert str(exc.raised) == "Not a valid filepath or file-like object."


@test(
	"Filepath ({fp.name})",
	tags=['integration', 'api', 'load'],
)
def _(fp=each(*AUDIO_FILEPATHS)):
	audio_metadata.load(str(fp))


@test(
	"File-like object ({fp.name})",
	tags=['integration', 'api', 'load'],
)
def _(fp=each(*AUDIO_FILEPATHS)):
	with open(fp, 'rb') as f:
		audio_metadata.load(f)


@test(
	"Path object ({fp.name})",
	tags=['integration', 'api', 'load'],
)
def _(fp=each(*AUDIO_FILEPATHS)):
	audio_metadata.load(fp)


@test(
	"Non-audio raises UnsupportedFormat",
	tags=['unit', 'api', 'loads'],
)
def _():
	with raises(UnsupportedFormat) as exc:
		with open(__file__, 'rb') as f:
			audio_metadata.loads(f.read())
	assert str(exc.raised) == "Supported format signature not found."


@test(
	"Non-bytes-like object raises ValueError",
	tags=['unit', 'api', 'loads'],
)
def _():
	with raises(ValueError) as exc:
		audio_metadata.loads(__file__)
	assert str(exc.raised) == "Not a valid bytes-like object."


@test(
	"Bytes ({fp.name})",
	tags=['integration', 'api', 'loads'],
)
def _(fp=each(*AUDIO_FILEPATHS)):
	audio_metadata.loads(fp.read_bytes())


@test(
	"Bytearray ({fp.name})",
	tags=['integration', 'api', 'loads'],
)
def _(fp=each(*AUDIO_FILEPATHS)):
	audio_metadata.loads(bytearray(fp.read_bytes()))


@test(
	"Memory view ({fp.name})",
	tags=['integration', 'api', 'loads'],
)
def _(fp=each(*AUDIO_FILEPATHS)):
	audio_metadata.loads(memoryview(fp.read_bytes()))
