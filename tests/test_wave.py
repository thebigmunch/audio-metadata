from ward import (
	raises,
	test,
	using,
)

from audio_metadata import (
	WAVE,
	FormatError,
	RIFFTags,
	WAVEAudioFormat,
	WAVEStreamInfo,
)
from tests.fixtures import (
	null,
	wave_riff_tags_data,
	wave_riff_tags_subchunk,
	wave_streaminfo_data,
	wave_streaminfo_subchunk,
)


@test(
	"RIFFTags",
	tags=['unit', 'wave', 'RIFFTags']
)
@using(
	null=null,
	wave_riff_tags_data=wave_riff_tags_data,
)
def _(
	null,
	wave_riff_tags_data,
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
	riff_tags_parse = RIFFTags.parse(wave_riff_tags_data)

	assert riff_tags_init == riff_tags_parse


@test(
	"WAVEStreamInfo",
	tags=['unit', 'wave', 'RIFFTags']
)
@using(wave_streaminfo_data=wave_streaminfo_data)
def _(wave_streaminfo_data):

	wave_stream_info_init = WAVEStreamInfo(
		size=None,
		start=None,
		extension_data=None,
		audio_format=WAVEAudioFormat.PCM,
		bit_depth=16,
		bitrate=1411200,
		channels=2,
		duration=None,
		sample_rate=44100,
	)
	wave_stream_info_parse = WAVEStreamInfo.parse(wave_streaminfo_data)

	assert wave_stream_info_init == wave_stream_info_parse


@test(
	"Parse RIFF tags subchunk",
	tags=['unit', 'wave', 'WAVE'],
)
@using(wave_riff_tags_subchunk=wave_riff_tags_subchunk)
def _(wave_riff_tags_subchunk):
	riff_tags = WAVE._parse_subchunk(wave_riff_tags_subchunk)

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
	"Parse WAVE streaminfo subchunk",
	tags=['unit', 'wave', 'WAVE'],
)
@using(wave_streaminfo_subchunk=wave_streaminfo_subchunk)
def _(wave_streaminfo_subchunk):
	wave_streaminfo = WAVE._parse_subchunk(wave_streaminfo_subchunk)

	assert wave_streaminfo == WAVEStreamInfo(
		size=None,
		start=None,
		extension_data=None,
		audio_format=WAVEAudioFormat.PCM,
		bit_depth=16,
		bitrate=1411200,
		channels=2,
		duration=None,
		sample_rate=44100,
	)


@test(
	"Invalid header",
	tags=['unit', 'wave', 'WAVE']
)
@using(null=null)
def _(null):
	with raises(FormatError) as exc:
		WAVE.parse(null)
	assert str(exc.raised) == "Valid WAVE header not found."


@test(
	"Invalid ID3",
	tags=['unit', 'wave', 'WAVE']
)
def _():
	with raises(FormatError) as exc:
		WAVE.parse(b'RIFF0000WAVEid3 1234')
	assert str(exc.raised) == "Valid ID3v2 header not found."


@test(
	"Invalid stream info",
	tags=['unit', 'wave', 'WAVE']
)
def _():
	with raises(FormatError) as exc:
		WAVE.parse(b'RIFF0000WAVE')
	assert str(exc.raised) == "Valid WAVE stream info not found."
