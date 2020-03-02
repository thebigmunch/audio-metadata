import struct
from pathlib import Path

from tbm_utils import DataReader
from ward import (
	each,
	raises,
	test,
)

from audio_metadata import (
	InvalidFormat,
	InvalidFrame,
	InvalidHeader,
	LAMEBitrateMode,
	LAMEChannelMode,
	LAMEEncodingFlags,
	LAMEHeader,
	LAMEPreset,
	LAMEReplayGain,
	LAMEReplayGainOrigin,
	LAMEReplayGainType,
	LAMESurroundInfo,
	MP3ChannelMode,
	MP3StreamInfo,
	MPEGFrameHeader,
	VBRIHeader,
	VBRIToC,
	XingHeader,
	XingToC,
)
from tests.utils import strip_repr


@test(
	"LAMEReplayGain",
	tags=['unit', 'mp3', 'lame', 'LAMEReplayGain']
)
def _():
	replay_gain_load = LAMEReplayGain.load(b'\x00\x1b\xfa\x05,D\x00\x00')
	replay_gain_init = LAMEReplayGain(
		peak=0.21856749057769775,
		track_type=1,
		track_origin=3,
		track_adjustment=6.8,
		album_type=0,
		album_origin=0,
		album_adjustment=0.0
	)

	assert replay_gain_load == replay_gain_init
	assert replay_gain_load.peak == replay_gain_init.peak == 0.21856749057769775
	assert replay_gain_load.track_type == replay_gain_init.track_type == 1
	assert replay_gain_load.track_origin == replay_gain_init.track_origin == 3
	assert replay_gain_load.track_adjustment == replay_gain_init.track_adjustment == 6.8
	assert replay_gain_load.album_type == replay_gain_init.album_type == 0
	assert replay_gain_load.album_origin == replay_gain_init.album_origin == 0
	assert replay_gain_load.album_adjustment == replay_gain_init.album_adjustment == 0.0

	replay_gain_load = LAMEReplayGain.load(b'\x00\x00\x00\x00\x00\x00\x00\x00')
	replay_gain_init = LAMEReplayGain(
		peak=None,
		track_type=0,
		track_origin=0,
		track_adjustment=0.0,
		album_type=0,
		album_origin=0,
		album_adjustment=0.0
	)

	assert replay_gain_load == replay_gain_init
	assert replay_gain_load.peak is replay_gain_init.peak is None
	assert replay_gain_load.track_type == replay_gain_init.track_type == 0
	assert replay_gain_load.track_origin == replay_gain_init.track_origin == 0
	assert replay_gain_load.track_adjustment == replay_gain_init.track_adjustment == 0.0
	assert replay_gain_load.album_type == replay_gain_init.album_type == 0
	assert replay_gain_load.album_origin == replay_gain_init.album_origin == 0
	assert replay_gain_load.album_adjustment == replay_gain_init.album_adjustment == 0.0

	replay_gain_load = LAMEReplayGain.load(b'\x00\x1b\xfa\x05.D\x02\x00')
	replay_gain_init = LAMEReplayGain(
		peak=0.21856749057769775,
		track_type=1,
		track_origin=3,
		track_adjustment=-6.8,
		album_type=0,
		album_origin=0,
		album_adjustment=-0.0
	)

	assert replay_gain_load == replay_gain_init
	assert replay_gain_load.peak == replay_gain_init.peak == 0.21856749057769775
	assert replay_gain_load.track_type == replay_gain_init.track_type == 1
	assert replay_gain_load.track_origin == replay_gain_init.track_origin == 3
	assert replay_gain_load.track_adjustment == replay_gain_init.track_adjustment == -6.8
	assert replay_gain_load.album_type == replay_gain_init.album_type == 0
	assert replay_gain_load.album_origin == replay_gain_init.album_origin == 0
	assert replay_gain_load.album_adjustment == replay_gain_init.album_adjustment == -0.0


@test(
	"LAMEEncodingFlags",
	tags=['unit', 'mp3', 'lame', 'LAMEEncodingFlags']
)
def _(
	flags=each(
		LAMEEncodingFlags(
			nogap_continuation=1,
			nogap_continued=1,
			nspsytune=1,
			nssafejoint=1,
		),
		LAMEEncodingFlags(
			nogap_continuation=True,
			nogap_continued=True,
			nspsytune=True,
			nssafejoint=True,
		),
		LAMEEncodingFlags(
			nogap_continuation=0,
			nogap_continued=0,
			nspsytune=0,
			nssafejoint=0,
		),
		LAMEEncodingFlags(
			nogap_continuation=False,
			nogap_continued=False,
			nspsytune=False,
			nssafejoint=False,
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
	"LAMEHeader",
	tags=['unit', 'mp3', 'lame', 'LAMEHeader']
)
def _():
	lame_data = (
		b'LAME3.99r\x04\xdd\x00\x00\x00\x00\x00\x00\x00\x00'
		b'5 $\x04\xecM\x00\x01\xf4\x00\x00P\t:\xe9\x1d|'
	)

	lame_header_load = LAMEHeader.load(lame_data, 100)
	lame_header_init = LAMEHeader(
		crc=b'\x1d|',
		ath_type=5,
		audio_crc=b':\xe9',
		audio_size=20489,
		bitrate=32000,
		bitrate_mode=LAMEBitrateMode.VBR_METHOD_2,
		channel_mode=LAMEChannelMode.JOINT_STEREO,
		delay=576,
		encoding_flags=LAMEEncodingFlags(
			nogap_continuation=False,
			nogap_continued=False,
			nspsytune=True,
			nssafejoint=True,
		),
		lowpass_filter=22100,
		mp3_gain=0,
		noise_shaping=1,
		padding=1260,
		preset=LAMEPreset.V0,
		replay_gain=LAMEReplayGain(
			album_adjustment=0.0,
			album_origin=LAMEReplayGainOrigin.NOT_SET,
			album_type=LAMEReplayGainType.NOT_SET,
			peak=None,
			track_adjustment=0.0,
			track_origin=LAMEReplayGainOrigin.NOT_SET,
			track_type=LAMEReplayGainType.NOT_SET,
		),
		revision=0,
		source_sample_rate=1,
		surround_info=LAMESurroundInfo.NO_SURROUND,
		unwise_settings_used=False,
		version=(3, 99),
	)

	with raises(InvalidHeader):
		LAMEHeader.load(lame_data[9:], 100)

	assert lame_header_load == lame_header_init
	assert lame_header_load._crc == lame_header_init._crc == b'\x1d|'
	assert lame_header_load.ath_type == lame_header_init.ath_type == 5
	assert lame_header_load.audio_crc == lame_header_init.audio_crc == b':\xe9'
	assert lame_header_load.audio_size == lame_header_init.audio_size == 20489
	assert lame_header_load.bitrate == lame_header_init.bitrate == 32000
	assert lame_header_load.bitrate_mode == lame_header_init.bitrate_mode == LAMEBitrateMode.VBR_METHOD_2
	assert lame_header_load.channel_mode == lame_header_init.channel_mode == LAMEChannelMode.JOINT_STEREO
	assert lame_header_load.delay == lame_header_init.delay == 576
	assert lame_header_load.encoding_flags == lame_header_init.encoding_flags == LAMEEncodingFlags(
		nogap_continuation=False,
		nogap_continued=False,
		nspsytune=True,
		nssafejoint=True,
	)
	assert lame_header_load.lowpass_filter == lame_header_init.lowpass_filter == 22100
	assert lame_header_load.mp3_gain == lame_header_init.mp3_gain == 0
	assert lame_header_load.noise_shaping == lame_header_init.noise_shaping == 1
	assert lame_header_load.padding == lame_header_init.padding == 1260
	assert lame_header_load.preset == lame_header_init.preset == LAMEPreset.V0
	assert lame_header_load.replay_gain == lame_header_init.replay_gain == LAMEReplayGain(
		album_adjustment=0.0,
		album_origin=LAMEReplayGainOrigin.NOT_SET,
		album_type=LAMEReplayGainType.NOT_SET,
		peak=None,
		track_adjustment=0.0,
		track_origin=LAMEReplayGainOrigin.NOT_SET,
		track_type=LAMEReplayGainType.NOT_SET,
	)
	assert lame_header_load.revision == lame_header_init.revision == 0
	assert lame_header_load.source_sample_rate == lame_header_init.source_sample_rate == 1
	assert lame_header_load.surround_info == lame_header_init.surround_info == LAMESurroundInfo.NO_SURROUND
	assert lame_header_load.unwise_settings_used is lame_header_init.unwise_settings_used is False
	assert lame_header_load.version == lame_header_init.version == (3, 99)
	assert strip_repr(lame_header_load) == strip_repr(lame_header_init) == (
		"<LAMEHeader({'ath_type': 5, 'audio_crc': b':\\xe9', 'audio_size': '20.01 KiB', 'bitrate': '32 Kbps', "
		"'bitrate_mode': <LAMEBitrateMode.VBR_METHOD_2>, 'channel_mode': <LAMEChannelMode.JOINT_STEREO>, 'delay': 576, "
		"'encoding_flags': <LAMEEncodingFlags({'nogap_continuation': False, 'nogap_continued': False, 'nspsytune': True, "
		"'nssafejoint': True, })>, 'lowpass_filter': 22100, 'mp3_gain': 0, 'noise_shaping': 1, 'padding': 1260, "
		"'preset': <LAMEPreset.V0>, 'replay_gain': <LAMEReplayGain({'album_adjustment': 0.0, "
		"'album_origin': <LAMEReplayGainOrigin.NOT_SET>, 'album_type': <LAMEReplayGainType.NOT_SET>, 'peak': None, "
		"'track_adjustment': 0.0, 'track_origin': <LAMEReplayGainOrigin.NOT_SET>, 'track_type': <LAMEReplayGainType.NOT_SET>, })>, "
		"'revision': 0, 'source_sample_rate': '1.0 Hz', 'surround_info': <LAMESurroundInfo.NO_SURROUND>, "
		"'unwise_settings_used': False, 'version': (3, 99),})>"
	)


@test(
	"XingHeader",
	tags=['unit', 'mp3', 'xing', 'XingHeader']
)
def _():
	xing_data = (
		b'Xing'
		b'\x00\x00\x00\x0f'
		b'\x00\x00\x00\xc1'
		b'\x00\x00P\t'
		b'\x00\x02\x05\x07\n\r\x0f\x12\x15\x17\x1a\x1d\x1f'
		b'"%&)+.1369;>@CFHJLORTWZ\\_bdgjlnpsvx{~\x80\x83\x85'
		b'\x88\x8b\x8d\x90\x93\x94\x97\x99\x9c\x9f\xa1\xa4\xa7'
		b'\xa9\xac\xaf\xb1\xb4\xb7\xb8\xbb\xbd\xc0\xc2\xc5\xc8'
		b'\xca\xcd\xd0\xd2\xd5\xd8\xda\xdc\xde\xe1\xe4\xe6\xe9'
		b'\xec\xee\xf1\xf4\xf6\xf9\xfc\xfe'
		b'\x00\x00\x00d'
	)

	with raises(InvalidHeader):
		XingHeader.load(xing_data[4:])

	xing_header_load = XingHeader.load(xing_data)
	xing_header_init = XingHeader(
		lame=None,
		num_bytes=20489,
		num_frames=193,
		quality=100,
		toc=XingToC(bytearray(xing_data[16:116]))
	)

	assert xing_header_load == xing_header_init
	assert xing_header_load._lame is xing_header_init._lame is None
	assert xing_header_load.num_bytes == xing_header_init.num_bytes == 20489
	assert xing_header_load.num_frames == xing_header_init.num_frames == 193
	assert xing_header_load.quality == xing_header_init.quality == 100
	assert xing_header_load.toc == xing_header_init.toc == XingToC(bytearray(xing_data[16:116]))


@test(
	"VBRIHeader",
	tags=['unit', 'mp3', 'vbri', 'VBRIHeader']
)
def _():
	vbri_data = (
		b'VBRI\x00\x01\t1\x00K\x00\x00Pr\x00\x00\x00\xc2\x00\xc1'
		b'\x00\x01\x00\x02\x00\x01\x02\n\x00h\x00h\x00h\x00h\x00h'
		b'\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h'
		b'\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h'
		b'\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h'
		b'\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h'
		b'\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h'
		b'\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h'
		b'\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h'
		b'\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h'
		b'\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h'
		b'\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h'
		b'\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h'
		b'\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h'
		b'\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h'
		b'\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h'
		b'\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h'
		b'\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h'
		b'\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h\x00h'
	)

	with raises(InvalidHeader):
		VBRIHeader.load(vbri_data[4:])

	with raises(InvalidHeader):
		VBRIHeader.load(vbri_data[:23] + b'\x01' + vbri_data[24:])

	toc_entries = []
	i = 26
	for _ in range(193):
		toc_entries.append(
			struct.unpack(
				'>H',
				vbri_data[i : i + 2]
			)[0]
		)
		i += 2

	vbri_header_load = VBRIHeader.load(vbri_data)
	vbri_header_init = VBRIHeader(
		delay=0.00015842914581298828,
		num_bytes=20594,
		num_frames=194,
		num_toc_entries=193,
		quality=75,
		toc=VBRIToC(toc_entries),
		toc_entry_num_bytes=2,
		toc_entry_num_frames=1,
		toc_scale_factor=1,
		version=1,
	)

	assert vbri_header_load == vbri_header_init
	assert vbri_header_load.delay == vbri_header_init.delay == 0.00015842914581298828
	assert vbri_header_load.num_bytes == vbri_header_init.num_bytes == 20594
	assert vbri_header_load.num_frames == vbri_header_init.num_frames == 194
	assert vbri_header_load.num_toc_entries == vbri_header_init.num_toc_entries == 193
	assert vbri_header_load.quality == vbri_header_init.quality == 75
	assert vbri_header_load.toc == vbri_header_init.toc == VBRIToC(toc_entries)
	assert vbri_header_load.toc_entry_num_bytes == vbri_header_init.toc_entry_num_bytes == 2
	assert vbri_header_load.toc_entry_num_frames == vbri_header_init.toc_entry_num_frames == 1
	assert vbri_header_load.toc_scale_factor == vbri_header_init.toc_scale_factor == 1
	assert vbri_header_load.version == vbri_header_init.version == 1


@test(
	"MPEGFrameHeader",
	tags=['unit', 'mp3', 'MPEGFrameHeader']
)
def _():
	mpeg_frame_data = (
		b'\xff\xfb\x90d\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
		b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00Xing\x00\x00\x00\x0f\x00\x00\x00\xc1\x00\x00P\t\x00\x02'
		b'\x05\x07\n\r\x0f\x12\x15\x17\x1a\x1d\x1f"%&)+.1369;>@CFHJLORTWZ\\_bdgjlnpsvx{~\x80\x83\x85\x88\x8b'
		b'\x8d\x90\x93\x94\x97\x99\x9c\x9f\xa1\xa4\xa7\xa9\xac\xaf\xb1\xb4\xb7\xb8\xbb\xbd\xc0\xc2\xc5\xc8\xca'
		b'\xcd\xd0\xd2\xd5\xd8\xda\xdc\xde\xe1\xe4\xe6\xe9\xec\xee\xf1\xf4\xf6\xf9\xfc\xfe\x00\x00\x00dLAME3.99r'
		b'\x04\xdd\x00\x00\x00\x00\x00\x00\x00\x005 $\x04\xecM\x00\x01\xf4\x00\x00P\t:\xe9\x1d|\x00\x00\x00\x00'
		b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
		b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
		b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
		b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
		b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
		b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
		b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
		b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
		b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
	)

	with raises(InvalidFrame):
		MPEGFrameHeader.load(mpeg_frame_data[2:])

	with raises(InvalidFrame):
		MPEGFrameHeader.load(mpeg_frame_data[0:1] + b'\xee' + mpeg_frame_data[2:])

	mpeg_frame_load = MPEGFrameHeader.load(mpeg_frame_data)
	mpeg_frame_init = MPEGFrameHeader(
		start=0,
		size=417,
		vbri=None,
		xing=XingHeader(
			lame=LAMEHeader(
				crc=b'\x1d|',
				ath_type=5,
				audio_crc=b':\xe9',
				audio_size=20489,
				bitrate=32000,
				bitrate_mode=LAMEBitrateMode.VBR_METHOD_2,
				channel_mode=LAMEChannelMode.JOINT_STEREO,
				delay=576,
				encoding_flags=LAMEEncodingFlags(
					nogap_continuation=False,
					nogap_continued=False,
					nspsytune=True,
					nssafejoint=True,
				),
				lowpass_filter=22100,
				mp3_gain=0,
				noise_shaping=1,
				padding=1260,
				preset=LAMEPreset.V0,
				replay_gain=LAMEReplayGain(
					album_adjustment=0.0,
					album_origin=LAMEReplayGainOrigin.NOT_SET,
					album_type=LAMEReplayGainType.NOT_SET,
					peak=None,
					track_adjustment=0.0,
					track_origin=LAMEReplayGainOrigin.NOT_SET,
					track_type=LAMEReplayGainType.NOT_SET,
				),
				revision=0,
				source_sample_rate=1,
				surround_info=LAMESurroundInfo.NO_SURROUND,
				unwise_settings_used=False,
				version=(3, 99),
			),
			num_bytes=20489,
			num_frames=193,
			quality=100,
			toc=XingToC(
				bytearray(
					b'\x00\x02\x05\x07\n\r\x0f\x12\x15\x17\x1a\x1d\x1f'
					b'"%&)+.1369;>@CFHJLORTWZ\\_bdgjlnpsvx{~\x80\x83\x85'
					b'\x88\x8b\x8d\x90\x93\x94\x97\x99\x9c\x9f\xa1\xa4\xa7'
					b'\xa9\xac\xaf\xb1\xb4\xb7\xb8\xbb\xbd\xc0\xc2\xc5\xc8'
					b'\xca\xcd\xd0\xd2\xd5\xd8\xda\xdc\xde\xe1\xe4\xe6\xe9'
					b'\xec\xee\xf1\xf4\xf6\xf9\xfc\xfe'
				)
			),
		),
		bitrate=128000,
		channel_mode=MP3ChannelMode.JOINT_STEREO,
		channels=2,
		layer=3,
		padded=False,
		protected=False,
		sample_rate=44100,
		version=1,
	)

	assert mpeg_frame_load == mpeg_frame_init
	assert mpeg_frame_load._start == mpeg_frame_init._start == 0
	assert mpeg_frame_load._size == mpeg_frame_init._size == 417
	assert mpeg_frame_load.bitrate == mpeg_frame_init.bitrate == 128000
	assert mpeg_frame_load.channel_mode == mpeg_frame_init.channel_mode == MP3ChannelMode.JOINT_STEREO
	assert mpeg_frame_load.channels == mpeg_frame_init.channels == 2
	assert mpeg_frame_load.layer == mpeg_frame_init.layer == 3
	assert mpeg_frame_load.padded is mpeg_frame_init.padded is False
	assert mpeg_frame_load.protected is mpeg_frame_init.protected is False
	assert mpeg_frame_load.sample_rate == mpeg_frame_init.sample_rate == 44100
	assert mpeg_frame_load.version == mpeg_frame_init.version == 1
	assert strip_repr(mpeg_frame_load) == strip_repr(mpeg_frame_init) == (
		"<MPEGFrameHeader({'bitrate': '128 Kbps', 'channel_mode': <MP3ChannelMode.JOINT_STEREO>, "
		"'channels': 2, 'layer': 3, 'padded': False, 'protected': False, 'sample_rate': '44.1 KHz', 'version': 1,})>"
	)


@test(
	"MP3StreamInfo",
	tags=['unit', 'mp3', 'MP3StreamInfo']
)
def _():
	data = DataReader(Path(__file__).parent / 'files' / 'audio' / 'test-mp3-lame-vbr.mp3')
	assert MP3StreamInfo.count_mpeg_frames(data) == 193

	data.seek(0)
	frames = MP3StreamInfo.find_mpeg_frames(data)
	assert len(frames) == 1
	assert frames[0]._xing

	data = DataReader(Path(__file__).parent / 'files' / 'audio' / 'test-mp3-cbr-2-frames.mp3')
	assert MP3StreamInfo.count_mpeg_frames(data) == 2

	data.seek(0)
	frames = MP3StreamInfo.find_mpeg_frames(data)
	assert len(frames) == 2
	assert frames[0]._xing is None

	data = DataReader(Path(__file__).parent / 'files' / 'audio' / 'test-mp3-sync-branch.mp3')
	assert MP3StreamInfo.count_mpeg_frames(data) == 192

	data.seek(0)
	frames = MP3StreamInfo.find_mpeg_frames(data)
	assert len(frames) == 4
	assert frames[0]._xing is None

	data = DataReader(Path(__file__).parent / 'files' / 'audio' / 'test-flac-vorbis.flac')
	assert MP3StreamInfo.count_mpeg_frames(data) == 0

	data.seek(0)
	with raises(InvalidFormat):
		MP3StreamInfo.find_mpeg_frames(data)
