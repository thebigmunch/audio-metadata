from pathlib import Path

from ward import fixture

TEST_PATH = Path(__file__).parent


@fixture(scope='module')
def flac_0_duration():
	return Path(TEST_PATH, 'data', 'flac', 'flac-0-duration.bin').read_bytes()


@fixture(scope='module')
def flac_application():
	return Path(TEST_PATH, 'data', 'flac', 'flac-application.bin').read_bytes()


@fixture(scope='module')
def flac_application_block():
	return Path(TEST_PATH, 'data', 'flac', 'flac-application-block.bin').read_bytes()


@fixture(scope='module')
def flac_cuesheet():
	return Path(TEST_PATH, 'data', 'flac', 'flac-cuesheet.bin').read_bytes()


@fixture(scope='module')
def flac_cuesheet_block():
	return Path(TEST_PATH, 'data', 'flac', 'flac-cuesheet-block.bin').read_bytes()


@fixture(scope='module')
def flac_cuesheet_index_1():
	return Path(TEST_PATH, 'data', 'flac', 'flac-cuesheet-index-1.bin').read_bytes()


@fixture(scope='module')
def flac_cuesheet_index_2():
	return Path(TEST_PATH, 'data', 'flac', 'flac-cuesheet-index-2.bin').read_bytes()


@fixture(scope='module')
def flac_cuesheet_track_1():
	return Path(TEST_PATH, 'data', 'flac', 'flac-cuesheet-track-1.bin').read_bytes()


@fixture(scope='module')
def flac_cuesheet_track_2():
	return Path(TEST_PATH, 'data', 'flac', 'flac-cuesheet-track-2.bin').read_bytes()


@fixture(scope='module')
def flac_id3v2():
	return Path(TEST_PATH, 'data', 'flac', 'flac-id3v2.bin').read_bytes()


@fixture(scope='module')
def flac_invalid_block():
	return Path(TEST_PATH, 'data', 'flac', 'flac-invalid-block.bin').read_bytes()


@fixture(scope='module')
def flac_padding_block():
	return Path(TEST_PATH, 'data', 'flac', 'flac-padding-block.bin').read_bytes()


@fixture(scope='module')
def flac_picture():
	return Path(TEST_PATH, 'data', 'flac', 'flac-picture.bin').read_bytes()


@fixture(scope='module')
def flac_picture_block():
	return Path(TEST_PATH, 'data', 'flac', 'flac-picture-block.bin').read_bytes()


@fixture(scope='module')
def flac_reserved_block():
	return Path(TEST_PATH, 'data', 'flac', 'flac-reserved-block.bin').read_bytes()


@fixture(scope='module')
def flac_seektable():
	return Path(TEST_PATH, 'data', 'flac', 'flac-seektable.bin').read_bytes()


@fixture(scope='module')
def flac_seektable_block():
	return Path(TEST_PATH, 'data', 'flac', 'flac-seektable-block.bin').read_bytes()


@fixture(scope='module')
def flac_vorbis():
	return Path(TEST_PATH, 'data', 'flac', 'flac-vorbis.bin').read_bytes()


@fixture(scope='module')
def flac_vorbis_comment_block():
	return Path(TEST_PATH, 'data', 'flac', 'flac-vorbis-comment-block.bin').read_bytes()


@fixture(scope='module')
def id3v1():
	return Path(TEST_PATH, 'data', 'id3', 'id3v1.bin').read_bytes()


@fixture(scope='module')
def id3v22():
	return Path(TEST_PATH, 'data', 'id3', 'id3v22.bin').read_bytes()


@fixture(scope='module')
def id3v23():
	return Path(TEST_PATH, 'data', 'id3', 'id3v23.bin').read_bytes()


@fixture(scope='module')
def id3v24():
	return Path(TEST_PATH, 'data', 'id3', 'id3v24.bin').read_bytes()


@fixture(scope='module')
def id3v24_unsync():
	return Path(TEST_PATH, 'data', 'id3', 'id3v24-unsync.bin').read_bytes()


@fixture(scope='module')
def id3v2_header():
	return Path(TEST_PATH, 'data', 'id3', 'id3v2-header.bin').read_bytes()


@fixture(scope='module')
def lame_header():
	return Path(TEST_PATH, 'data', 'mp3', 'lame-header.bin').read_bytes()


@fixture(scope='module')
def lame_replay_gain():
	return Path(TEST_PATH, 'data', 'mp3', 'lame-replay-gain.bin').read_bytes()


@fixture(scope='module')
def lame_replay_gain_negative():
	return Path(TEST_PATH, 'data', 'mp3', 'lame-replay-gain-negative.bin').read_bytes()


@fixture(scope='module')
def lame_replay_gain_null():
	return Path(TEST_PATH, 'data', 'mp3', 'lame-replay-gain-null.bin').read_bytes()


@fixture(scope='module')
def mp3_cbr_2_frames():
	return Path(TEST_PATH, 'data', 'mp3', 'mp3-cbr-2-frames.bin').read_bytes()


@fixture(scope='module')
def mp3_lame_vbr():
	return Path(TEST_PATH, 'data', 'mp3', 'mp3-lame-vbr.bin').read_bytes()


@fixture(scope='module')
def mp3_sync_branch():
	return Path(TEST_PATH, 'data', 'mp3', 'mp3-sync-branch.bin').read_bytes()


@fixture(scope='module')
def mpeg_frame():
	return Path(TEST_PATH, 'data', 'mp3', 'mpeg-frame.bin').read_bytes()


@fixture(scope='global')
def null():
	return Path(TEST_PATH, 'data', 'null.bin').read_bytes()


@fixture(scope='module')
def riff_tags():
	return Path(TEST_PATH, 'data', 'wav', 'riff-tags.bin').read_bytes()


@fixture(scope='module')
def vbri_header():
	return Path(TEST_PATH, 'data', 'mp3', 'vbri-header.bin').read_bytes()


@fixture(scope='module')
def vorbis_comments():
	return Path(TEST_PATH, 'data', 'vorbis_comments', 'vorbis-comments.bin').read_bytes()


@fixture(scope='module')
def xing_header_no_lame():
	return Path(TEST_PATH, 'data', 'mp3', 'xing-header-no-lame.bin').read_bytes()


@fixture(scope='module')
def xing_toc():
	return Path(TEST_PATH, 'data', 'mp3', 'xing-toc.bin').read_bytes()
