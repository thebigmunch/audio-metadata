from ward import (
	raises,
	test,
	using,
)

from audio_metadata import (
	WAV,
	InvalidChunk,
	InvalidHeader,
	RIFFTags
)
from tests.fixtures import (
	null,
	riff_tags,
)


@test(
	"RIFFTags",
	tags=['unit', 'wav', 'RIFFTags']
)
@using(
	null=null,
	riff_tags=riff_tags,
)
def _(null, riff_tags):
	with raises(InvalidChunk):
		RIFFTags.parse(null)

	riff_tags_init = RIFFTags(
		album=['test-album'],
		artist=['test-artist'],
		comment=['test-comment'],
		date=['2000'],
		genre=['test-genre'],
		title=['test-title'],
		tracknumber=['1'],
	)

	riff_tags_load = RIFFTags.parse(riff_tags)

	assert riff_tags_init == riff_tags_load


@test(
	"Invalid header",
	tags=['unit', 'wav', 'WAV']
)
@using(null=null)
def _(null):
	with raises(InvalidHeader) as ctx:
		WAV.parse(null)
	assert str(ctx.raised) == "Valid WAVE header not found."

	with raises(InvalidHeader):
		WAV.parse(null)


@test(
	"Invalid ID3",
	tags=['unit', 'wav', 'WAV']
)
def _():
	with raises(InvalidHeader):
		WAV.parse(b'RIFF0000WAVEid3 1234')


@test(
	"Invalid stream info",
	tags=['unit', 'wav', 'WAV']
)
def _():
	with raises(InvalidHeader) as ctx:
		WAV.parse(b'RIFF0000WAVE')
	assert str(ctx.raised) == "Valid WAVE stream info not found."
