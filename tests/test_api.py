from pathlib import Path

import pytest

import audio_metadata
from audio_metadata import UnsupportedFormat

test_filepaths = list((Path(__file__).parent / 'files' / 'audio').iterdir())


@pytest.mark.integration
def test_determine_format_id3v2_no_mp3_frames():
	assert audio_metadata.determine_format(
		b'ID3\x04\x00\x80\x00\x00\x00\x00\x00\xff\xfb'
	) is None


@pytest.mark.integration
def test_determine_format_invalid_value():
	assert audio_metadata.determine_format([__file__]) is None


@pytest.mark.integration
def test_determine_format_non_audio():
	assert audio_metadata.determine_format(__file__) is None


@pytest.mark.integration
def test_determine_format_bytes():
	for fp in test_filepaths:
		assert issubclass(
			audio_metadata.determine_format(fp.read_bytes()),
			audio_metadata.Format
		)


@pytest.mark.integration
def test_determine_format_filepath():
	for fp in test_filepaths:
		assert issubclass(
			audio_metadata.determine_format(fp),
			audio_metadata.Format
		)


@pytest.mark.integration
def test_determine_format_fileobj():
	for fp in test_filepaths:
		assert issubclass(
			audio_metadata.determine_format(fp.open('rb')),
			audio_metadata.Format
		)


@pytest.mark.integration
def test_determine_format_pathobj():
	for fp in test_filepaths:
		assert issubclass(
			audio_metadata.determine_format(fp),
			audio_metadata.Format
		)


@pytest.mark.integration
def test_load_non_audio():
	with pytest.raises(UnsupportedFormat):
		audio_metadata.load(__file__)


@pytest.mark.integration
def test_load_non_file():
	with pytest.raises(ValueError):
		audio_metadata.load(b'test')


@pytest.mark.integration
def test_load_filepath():
	for fp in test_filepaths:
		audio_metadata.load(fp)


@pytest.mark.integration
def test_load_fileobj():
	for fp in test_filepaths:
		with open(fp, 'rb') as f:
			audio_metadata.load(f)


@pytest.mark.integration
def test_load_pathobj():
	for fp in test_filepaths:
		audio_metadata.load(fp)


@pytest.mark.integration
def test_loads_non_audio():
	with pytest.raises(UnsupportedFormat):
		with open(__file__, 'rb') as f:
			audio_metadata.loads(f.read())


@pytest.mark.integration
def test_loads_non_bytes_like():
	with pytest.raises(ValueError):
		audio_metadata.loads(__file__)


@pytest.mark.integration
def test_loads_bytes():
	for fp in test_filepaths:
		audio_metadata.loads(fp.read_bytes())


@pytest.mark.integration
def test_loads_bytearray():
	for fp in test_filepaths:
		audio_metadata.loads(bytearray(fp.read_bytes()))


@pytest.mark.integration
def test_loads_memoryview():
	for fp in test_filepaths:
		audio_metadata.loads(memoryview(fp.read_bytes()))
