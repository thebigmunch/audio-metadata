import pytest
from audio_metadata import (
	InvalidHeader,
	LAMEReplayGain,
	XingHeader,
	XingToC
)


def test_LAMEReplayGain():
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


def test_XingHeader_no_lame():
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

	with pytest.raises(InvalidHeader):
		XingHeader.load(xing_data[4:])

	xing_header_load = XingHeader.load(xing_data)
	xing_header_init = XingHeader(
		None,
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
