from ward import (
	raises,
	test,
)

from audio_metadata import (
	WAV,
	InvalidChunk,
	InvalidHeader,
	RIFFTags
)


@test(
	"RIFFTags",
	tags=['unit', 'wav', 'RIFFTags']
)
def _():
	with raises(InvalidChunk):
		RIFFTags.load(b'NOTINFO')

	riff_tags_init = RIFFTags(
		album=['test-album'],
		artist=['test-artist'],
		comment=['test-comment'],
		date=['2000'],
		genre=['test-genre'],
		title=['test-title'],
		tracknumber=['1'],
	)

	riff_tags_load = RIFFTags.load(
		b'INFOIPRD\x0b\x00\x00\x00test-album\x00\x00'
		b'IART\x0c\x00\x00\x00test-artist\x00'
		b'IGNR\x0b\x00\x00\x00test-genre\x00\x00'
		b'ICMT\r\x00\x00\x00test-comment\x00\x00'
		b'INAM\x0b\x00\x00\x00test-title\x00\x00'
		b'ITRK\x02\x00\x00\x001\x00'
		b'ICRD\x05\x00\x00\x002000\x00\x00'
	)

	assert riff_tags_init == riff_tags_load


@test(
	"Invalid header",
	tags=['unit', 'wav', 'WAV']
)
def _():
	with raises(InvalidHeader) as ctx:
		WAV.load(b'TEST0000WAVE')
	assert str(ctx.raised) == "Valid WAVE header not found."

	with raises(InvalidHeader):
		WAV.load(b'RIFF0000TEST')


@test(
	"Invalid ID3",
	tags=['unit', 'wav', 'WAV']
)
def _():
	with raises(InvalidHeader):
		WAV.load(b'RIFF0000WAVEid3 1234')


@test(
	"Invalid stream info",
	tags=['unit', 'wav', 'WAV']
)
def _():
	with raises(InvalidHeader) as ctx:
		WAV.load(b'RIFF0000WAVE')
	assert str(ctx.raised) == "Valid WAVE stream info not found."
