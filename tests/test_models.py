from pathlib import Path

from bidict import frozenbidict
from audio_metadata.tbm_utils import DataReader
from ward import test

from audio_metadata.models import (
	Format,
	Picture,
	StreamInfo,
	Tags
)
from tests.utils import strip_repr


test_image = (Path(__file__).parent / 'image' / 'test.png').resolve()


@test(
	"Format",
	tags=['unit', 'models', 'Format'],
)
def _():
	format_bytes = Format._load(test_image.read_bytes())
	format_bytes_datareader = Format._load(DataReader(test_image.read_bytes()))
	format_fileobj = Format._load(test_image.open('rb'))
	format_fileobj_datareader = Format._load(DataReader(test_image.open('rb')))

	assert isinstance(format_bytes._obj, DataReader)
	assert isinstance(format_bytes_datareader._obj, DataReader)
	assert isinstance(format_fileobj._obj, DataReader)
	assert isinstance(format_fileobj_datareader._obj, DataReader)

	assert format_bytes.filepath is format_bytes_datareader.filepath is None
	assert format_fileobj.filepath == format_fileobj_datareader.filepath == str(test_image)

	assert format_bytes.filesize == format_bytes_datareader.filesize == 96
	assert format_fileobj.filesize == format_fileobj_datareader.filesize == 96

	assert repr(format_bytes) == repr(format_bytes_datareader)
	assert repr(format_fileobj) == repr(format_fileobj_datareader)


@test(
	"Picture",
	tags=['unit', 'models', 'Picture'],
)
def _():
	picture = Picture(
		_test='test',
		height=16,
		width=16,
		data=test_image.read_bytes()
	)

	assert repr(picture) == "<Picture({'data': '96.00 B', 'height': 16, 'width': 16})>"


@test(
	"StreamInfo",
	tags=['unit', 'models', 'StreamInfo'],
)
def _():
	stream_info = StreamInfo(
		_start=0,
		bitrate=320000,
		duration=100,
		sample_rate=44100,
		channels=2
	)

	assert strip_repr(stream_info) == "<StreamInfo({'bitrate': '320 Kbps', 'channels': 2, 'duration': '01:40', 'sample_rate': '44.1 KHz',})>"


@test(
	"Tags",
	tags=['unit', 'models', 'Tags'],
)
def _():
	test_tags = Tags(key1='value1', key2='value2')
	test_tags.FIELD_MAP = frozenbidict({'artist': 'key1', 'title': 'key2'})

	assert test_tags['artist'] == test_tags['key1'] == test_tags.artist == test_tags.key1
	assert test_tags['title'] == test_tags['key2'] == test_tags.title == test_tags.key2

	test_tags['key3'] = 'value3'
	del test_tags['key3']
	assert 'key3' not in test_tags

	test_tags.key3 = 'value3'
	delattr(test_tags, 'key3')
	assert not hasattr(test_tags, 'key3')

	assert list(iter(test_tags)) == ['artist', 'title']

	assert repr(test_tags) == "<Tags({'artist': 'value1', 'title': 'value2'})>"
