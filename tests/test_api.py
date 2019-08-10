from pathlib import Path

import audio_metadata
import pytest
from audio_metadata import UnsupportedFormat

test_filepaths = list((Path(__file__).parent / 'files' / 'audio').iterdir())


def test_determine_format_invalid_value():
	assert audio_metadata.determine_format([__file__]) is None


def test_determine_format_non_audio():
	assert audio_metadata.determine_format(__file__) is None


def test_determine_format_bytes():
	for fp in test_filepaths:
		assert issubclass(
			audio_metadata.determine_format(fp.read_bytes()),
			audio_metadata.Format
		)


def test_determine_format_filepath():
	for fp in test_filepaths:
		assert issubclass(
			audio_metadata.determine_format(fp),
			audio_metadata.Format
		)


def test_determine_format_fileobj():
	for fp in test_filepaths:
		assert issubclass(
			audio_metadata.determine_format(fp.open('rb')),
			audio_metadata.Format
		)


def test_determine_format_pathobj():
	for fp in test_filepaths:
		assert issubclass(
			audio_metadata.determine_format(fp),
			audio_metadata.Format
		)


def test_load_non_audio():
	with pytest.raises(UnsupportedFormat):
		audio_metadata.load(__file__)


def test_load_non_file():
	with pytest.raises(ValueError):
		audio_metadata.load(b'test')


def test_load_filepath():
	for fp in test_filepaths:
		audio_metadata.load(fp)


def test_load_fileobj():
	for fp in test_filepaths:
		with open(fp, 'rb') as f:
			audio_metadata.load(f)


def test_load_pathobj():
	for fp in test_filepaths:
		audio_metadata.load(fp)


def test_loads_non_audio():
	with pytest.raises(UnsupportedFormat):
		with open(__file__, 'rb') as f:
			audio_metadata.loads(f.read())


def test_loads_non_bytes_like():
	with pytest.raises(ValueError):
		audio_metadata.loads(__file__)


def test_loads_bytes():
	for fp in test_filepaths:
		audio_metadata.loads(fp.read_bytes())


def test_loads_bytearray():
	for fp in test_filepaths:
		audio_metadata.loads(bytearray(fp.read_bytes()))


def test_loads_memoryview():
	for fp in test_filepaths:
		audio_metadata.loads(memoryview(fp.read_bytes()))
