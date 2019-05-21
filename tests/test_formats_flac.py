from pathlib import Path

from audio_metadata.formats.flac import (
	FLAC,
	FLACApplication,
	FLACMetadataBlock,
	FLACPadding,
	FLACSeekPoint,
	FLACSeekTable
)


def test_FLAC():
	for flac in (Path(__file__).parent / 'files' / 'audio').glob('*.flac'):
		FLAC.load(flac.read_bytes())


def test_FLACApplication():
	application_init = FLACApplication(
		id='aiff',
		data=b'FORM\x02\xe0\x9b\x08AIFF'
	)
	application_load = FLACApplication.load(
		b'aiffFORM\x02\xe0\x9b\x08AIFF'
	)

	assert application_init == application_load
	assert application_init.id == application_load.id == 'aiff'
	assert application_init.data == application_load.data == b'FORM\x02\xe0\x9b\x08AIFF'
	assert repr(application_init) == repr(application_load) == '<Application (aiff)>'


def test_FLACMetadataBlock():
	metadata_block = FLACMetadataBlock(
		type=100,
		size=10
	)

	assert repr(metadata_block) == '<MetadataBlock [100] (10 bytes)>'


def test_FLACPadding():
	padding_init = FLACPadding(10)
	padding_load = FLACPadding.load(b'\x00' * 10)

	assert padding_init == padding_load
	assert repr(padding_init) == repr(padding_load) == '<Padding (10 bytes)>'


def test_FLACSeektable():
	seekpoints = [
		FLACSeekPoint(first_sample, offset, num_samples)
		for first_sample, offset, num_samples in [
			(0, 0, 4096),
			(40960, 140, 4096),
			(86016, 294, 4096),
			(131072, 448, 4096),
			(176128, 602, 4096)
		]
	]

	seektable_init = FLACSeekTable(seekpoints)
	seektable_load = FLACSeekTable.load(
		b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00'
		b'\x00\x00\x00\x00\x00\x00\xa0\x00\x00\x00\x00\x00\x00\x00\x00\x8c\x10\x00'
		b'\x00\x00\x00\x00\x00\x01P\x00\x00\x00\x00\x00\x00\x00\x01&\x10\x00'
		b'\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x01\xc0\x10\x00'
		b'\x00\x00\x00\x00\x00\x02\xb0\x00\x00\x00\x00\x00\x00\x00\x02Z\x10\x00'
	)

	assert seektable_init == seektable_load
	assert seektable_init.data == seektable_load.data == seekpoints
