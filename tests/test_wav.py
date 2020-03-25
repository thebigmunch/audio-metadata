from ward import (
	raises,
	test,
	using,
)

from audio_metadata import (
	WAV,
	FormatError,
	RIFFTags,
	WAVStreamInfo,
)
from tests.fixtures import (
	null,
	wav_riff_tags_data,
	wav_riff_tags_subchunk,
	wav_streaminfo_data,
	wav_streaminfo_subchunk,
)


@test(
	"RIFFTags",
	tags=['unit', 'wav', 'RIFFTags']
)
@using(
	null=null,
	wav_riff_tags_data=wav_riff_tags_data,
)
def _(
	null,
	wav_riff_tags_data,
):
	with raises(FormatError) as exc:
		RIFFTags.parse(null)
	assert str(exc.raised) == "Valid RIFF INFO chunk not found."

	riff_tags_init = RIFFTags(
		album=['test-album'],
		artist=['test-artist'],
		comment=['test-comment'],
		date=['2000'],
		genre=['test-genre'],
		title=['test-title'],
		tracknumber=['1'],
	)
	riff_tags_load = RIFFTags.parse(wav_riff_tags_data)

	assert riff_tags_init == riff_tags_load


@test(
	"WAVStreamInfo",
	tags=['unit', 'wav', 'RIFFTags']
)
@using(wav_streaminfo_data=wav_streaminfo_data)
def _(wav_streaminfo_data):

	wav_stream_info_init = WAVStreamInfo(
		size=None,
		start=None,
		bit_depth=16,
		bitrate=1411200,
		channels=2,
		duration=None,
		sample_rate=44100,
	)
	wav_stream_info_load = WAVStreamInfo.parse(wav_streaminfo_data)

	assert wav_stream_info_init == wav_stream_info_load


@test(
	"Parse RIFF tags subchunk",
	tags=['unit', 'wav', 'WAV'],
)
@using(wav_riff_tags_subchunk=wav_riff_tags_subchunk)
def _(wav_riff_tags_subchunk):
	riff_tags = WAV._parse_subchunk(wav_riff_tags_subchunk)

	assert riff_tags == RIFFTags(
		album=['test-album'],
		artist=['test-artist'],
		comment=['test-comment'],
		date=['2000'],
		genre=['test-genre'],
		title=['test-title'],
		tracknumber=['1'],
	)


@test(
	"Parse WAV streaminfo subchunk",
	tags=['unit', 'wav', 'WAV'],
)
@using(wav_streaminfo_subchunk=wav_streaminfo_subchunk)
def _(wav_streaminfo_subchunk):
	wav_streaminfo = WAV._parse_subchunk(wav_streaminfo_subchunk)

	assert wav_streaminfo == WAVStreamInfo(
		size=None,
		start=None,
		bit_depth=16,
		bitrate=1411200,
		channels=2,
		duration=None,
		sample_rate=44100,
	)


@test(
	"Invalid header",
	tags=['unit', 'wav', 'WAV']
)
@using(null=null)
def _(null):
	with raises(FormatError) as exc:
		WAV.parse(null)
	assert str(exc.raised) == "Valid WAVE header not found."


@test(
	"Invalid ID3",
	tags=['unit', 'wav', 'WAV']
)
def _():
	with raises(FormatError) as exc:
		WAV.parse(b'RIFF0000WAVEid3 1234')
	assert str(exc.raised) == "Valid ID3v2 header not found."


@test(
	"Invalid stream info",
	tags=['unit', 'wav', 'WAV']
)
def _():
	with raises(FormatError) as exc:
		WAV.parse(b'RIFF0000WAVE')
	assert str(exc.raised) == "Valid WAVE stream info not found."
