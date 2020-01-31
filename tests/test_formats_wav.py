import pytest

from audio_metadata import (
	WAV,
	InvalidChunk,
	InvalidHeader,
	RIFFTags
)


def test_RIFFTags():
	with pytest.raises(InvalidChunk):
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


def test_WAV_invalid_header():
	with pytest.raises(InvalidHeader, match="Valid WAVE header not found"):
		WAV.load(b'TEST0000WAVE')

	with pytest.raises(InvalidHeader):
		WAV.load(b'RIFF0000TEST')


def test_WAV_ID3_invalid_header():
	with pytest.raises(InvalidHeader):
		WAV.load(b'RIFF0000WAVEid3 1234')


def test_WAV_invalid_stream_info():
	with pytest.raises(InvalidHeader, match="Valid WAVE stream info not found"):
		WAV.load(b'RIFF0000WAVE')
