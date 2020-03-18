from ward import (
	raises,
	test,
	using,
)

from audio_metadata import (
	FLAC,
	FLACApplication,
	FLACCueSheet,
	FLACCueSheetIndex,
	FLACCueSheetTrack,
	FLACMetadataBlock,
	FLACPadding,
	FLACPicture,
	FLACSeekPoint,
	FLACSeekTable,
	ID3PictureType,
	InvalidBlock,
	InvalidHeader,
)
from tests.fixtures import (
	flac_0_duration,
	flac_application,
	flac_application_block,
	flac_cuesheet,
	flac_cuesheet_block,
	flac_cuesheet_index_1,
	flac_cuesheet_index_2,
	flac_cuesheet_track_1,
	flac_cuesheet_track_2,
	flac_id3v2,
	flac_invalid_block,
	flac_padding_block,
	flac_picture,
	flac_picture_block,
	flac_reserved_block,
	flac_seektable,
	flac_seektable_block,
	flac_vorbis_comment_block,
	null,
)


@test(
	"Ignore ID3v2",
	tags=['unit', 'flac', 'FLAC'],
)
@using(flac_id3v2=flac_id3v2)
def test_FLAC_load_ID3v2(flac_id3v2):
	FLAC.parse(flac_id3v2)


@test(
	"Load padding block",
	tags=['unit', 'flac', 'FLAC'],
)
@using(flac_padding_block=flac_padding_block)
def test_FLAC_load_padding(flac_padding_block):
	FLAC.parse(flac_padding_block)


@test(
	"Load application block",
	tags=['unit', 'flac', 'FLAC'],
)
@using(flac_application_block=flac_application_block)
def test_FLAC_load_application(flac_application_block):
	FLAC.parse(flac_application_block)


@test(
	"Load seektable block",
	tags=['unit', 'flac', 'FLAC'],
)
@using(flac_seektable_block=flac_seektable_block)
def test_FLAC_load_seektable(flac_seektable_block):
	FLAC.parse(flac_seektable_block)


@test(
	"Load vorbis comment block",
	tags=['unit', 'flac', 'FLAC'],
)
@using(flac_vorbis_comment_block=flac_vorbis_comment_block)
def test_FLAC_load_vorbis_comment(flac_vorbis_comment_block):
	FLAC.parse(flac_vorbis_comment_block)


@test(
	"Load cuesheet block",
	tags=['unit', 'flac', 'FLAC'],
)
@using(flac_cuesheet_block=flac_cuesheet_block)
def test_FLAC_load_cuesheet(flac_cuesheet_block):
	FLAC.parse(flac_cuesheet_block)


@test(
	"Load picture block",
	tags=['unit', 'flac', 'FLAC'],
)
@using(flac_picture_block=flac_picture_block)
def test_FLAC_load_picture(flac_picture_block):
	FLAC.parse(flac_picture_block)


@test(
	"Reserved block type is a FLACMetadataBlock",
	tags=['unit', 'flac', 'FLAC'],
)
@using(flac_reserved_block=flac_reserved_block)
def _(flac_reserved_block):
	flac = FLAC.parse(flac_reserved_block)

	assert flac._blocks[0] == FLACMetadataBlock(
		type=10,
		data=b'',
	)


@test(
	"Load 0 duration",
	tags=['unit', 'flac', 'FLAC'],
)
@using(flac_0_duration=flac_0_duration)
def _(flac_0_duration):
	FLAC.parse(flac_0_duration)


@test(
	"No FLAC header raises InvalidHeader",
	tags=['unit', 'flac', 'FLAC'],
)
@using(null=null)
def _(null):
	with raises(InvalidHeader) as ctx:
		FLAC.parse(null)
	assert str(ctx.raised) == "Valid FLAC header not found."


@test(
	"Invalid block type raises InvalidBlock",
	tags=['unit', 'flac', 'FLAC'],
)
@using(flac_invalid_block=flac_invalid_block)
def _(flac_invalid_block):
	with raises(InvalidBlock) as ctx:
		FLAC.parse(flac_invalid_block)
	assert str(ctx.raised) == "127 is not a valid FLAC metadata block type."


@test(
	"FLACApplication",
	tags=['unit', 'flac', 'FLACApplication'],
)
@using(flac_application=flac_application)
def _(flac_application):
	application_init = FLACApplication(
		id='aiff',
		data=b'FORM\x02\xe0\x9b\x08AIFF'
	)
	application_load = FLACApplication.parse(flac_application)

	assert application_init == application_load
	assert application_init.id == application_load.id == 'aiff'
	assert application_init.data == application_load.data == b'FORM\x02\xe0\x9b\x08AIFF'
	assert repr(application_init) == repr(application_load) == '<FLACApplication (aiff)>'


@test(
	"FLACCueSheetIndex",
	tags=['unit', 'flac', 'FLACCueSheetIndex'],
)
@using(
	flac_cuesheet_index_1=flac_cuesheet_index_1,
	flac_cuesheet_index_2=flac_cuesheet_index_2,
)
def _(flac_cuesheet_index_1, flac_cuesheet_index_2):
	cuesheet_index_init = FLACCueSheetIndex(
		number=1,
		offset=0,
	)
	cuesheet_index_load = FLACCueSheetIndex.parse(flac_cuesheet_index_1)

	assert cuesheet_index_init == cuesheet_index_load
	assert cuesheet_index_init.number == cuesheet_index_load.number == 1
	assert cuesheet_index_init.offset == cuesheet_index_load.offset == 0
	assert repr(cuesheet_index_init) == repr(cuesheet_index_load) == "<FLACCueSheetIndex({'number': 1, 'offset': 0})>"

	cuesheet_index_init = FLACCueSheetIndex(
		number=2,
		offset=588,
	)
	cuesheet_index_load = FLACCueSheetIndex.parse(flac_cuesheet_index_2)

	assert cuesheet_index_init == cuesheet_index_load
	assert cuesheet_index_init.number == cuesheet_index_load.number == 2
	assert cuesheet_index_init.offset == cuesheet_index_load.offset == 588
	assert repr(cuesheet_index_init) == repr(cuesheet_index_load) == "<FLACCueSheetIndex({'number': 2, 'offset': 588})>"


@test(
	"FLACCueSheetTrack",
	tags=['unit', 'flac', 'FLACCueSheetTrack'],
)
@using(
	flac_cuesheet_track_1=flac_cuesheet_track_1,
	flac_cuesheet_track_2=flac_cuesheet_track_2,
)
def _(flac_cuesheet_track_1, flac_cuesheet_track_2):
	cuesheet_track_init = FLACCueSheetTrack(
		track_number=1,
		offset=0,
		isrc='123456789012',
		type=0,
		pre_emphasis=False,
		indexes=[
			FLACCueSheetIndex(
				number=1,
				offset=0,
			)
		]
	)
	cuesheet_track_load = FLACCueSheetTrack.parse(flac_cuesheet_track_1)

	assert cuesheet_track_init == cuesheet_track_load
	assert cuesheet_track_init.track_number == cuesheet_track_load.track_number == 1
	assert cuesheet_track_init.offset == cuesheet_track_load.offset == 0
	assert cuesheet_track_init.isrc == cuesheet_track_load.isrc == '123456789012'
	assert cuesheet_track_init.type == cuesheet_track_load.type == 0
	assert cuesheet_track_init.pre_emphasis is False
	assert cuesheet_track_load.pre_emphasis is False

	cuesheet_track_init = FLACCueSheetTrack(
		track_number=2,
		offset=44100,
		isrc='',
		type=1,
		pre_emphasis=True,
		indexes=[
			FLACCueSheetIndex(
				number=1,
				offset=0,
			),
			FLACCueSheetIndex(
				number=2,
				offset=588,
			),
		],
	)
	cuesheet_track_load = FLACCueSheetTrack.parse(flac_cuesheet_track_2)

	assert cuesheet_track_init == cuesheet_track_load
	assert cuesheet_track_init.track_number == cuesheet_track_load.track_number == 2
	assert cuesheet_track_init.offset == cuesheet_track_load.offset == 44100
	assert cuesheet_track_init.isrc == cuesheet_track_load.isrc == ''
	assert cuesheet_track_init.type == cuesheet_track_load.type == 1
	assert cuesheet_track_init.pre_emphasis is True
	assert cuesheet_track_load.pre_emphasis is True


@test(
	"FLACCueSheet",
	tags=['unit', 'flac', 'FLACCueSheet'],
)
@using(flac_cuesheet=flac_cuesheet)
def _(flac_cuesheet):
	cuesheet_init = FLACCueSheet(
		[
			FLACCueSheetTrack(
				track_number=1,
				offset=0,
				isrc='123456789012',
				type=0,
				pre_emphasis=False,
				indexes=[
					FLACCueSheetIndex(
						number=1,
						offset=0,
					)
				]
			),
			FLACCueSheetTrack(
				track_number=2,
				offset=44100,
				isrc='',
				type=1,
				pre_emphasis=True,
				indexes=[
					FLACCueSheetIndex(
						number=1,
						offset=0,
					),
					FLACCueSheetIndex(
						number=2,
						offset=588,
					),
				],
			),
			FLACCueSheetTrack(
				track_number=3,
				offset=88200,
				isrc='',
				type=0,
				pre_emphasis=False,
				indexes=[
					FLACCueSheetIndex(
						number=1,
						offset=0,
					)
				],
			),
			FLACCueSheetTrack(
				track_number=170,
				offset=162496,
				isrc='',
				type=0,
				pre_emphasis=False,
				indexes=[]
			)
		],
		catalog_number='1234567890123',
		lead_in_samples=88200,
		compact_disc=True,
	)
	cuesheet_load = FLACCueSheet.parse(flac_cuesheet)

	assert cuesheet_init == cuesheet_load
	assert repr(cuesheet_init) == repr(cuesheet_load) == '<FLACCueSheet (4 tracks)>'


@test(
	"FLACMetadataBlock",
	tags=['unit', 'flac', 'FLACMetadataBlock'],
)
def _():
	metadata_block = FLACMetadataBlock(
		type=100,
		data=b'\x00' * 10
	)

	assert metadata_block.type == 100
	assert metadata_block.data == b'\x00' * 10
	assert repr(metadata_block) == '<FLACMetadataBlock [100] (10 bytes)>'


@test(
	"FLACPadding",
	tags=['unit', 'flac', 'FLACPadding'],
)
def _():
	padding_init = FLACPadding(size=10)
	padding_load = FLACPadding.parse(b'\x00' * 10)

	assert padding_init == padding_load
	assert repr(padding_init) == repr(padding_load) == '<FLACPadding (10 bytes)>'


@test(
	"FLACPicture",
	tags=['unit', 'flac', 'FLACPicture'],
)
@using(flac_picture=flac_picture)
def _(flac_picture):
	vorbis_picture_init = FLACPicture(
		type=ID3PictureType.COVER_FRONT,
		mime_type='image/png',
		description='',
		width=16,
		height=16,
		bit_depth=32,
		colors=0,
		data=flac_picture[41:],
	)
	vorbis_picture_load = FLACPicture.parse(flac_picture)

	assert vorbis_picture_init == vorbis_picture_load


@test(
	"FLACSeekTable",
	tags=['unit', 'flac', 'FLACSeekTable'],
)
@using(flac_seektable=flac_seektable)
def _(flac_seektable):
	seekpoints = [
		FLACSeekPoint(
			first_sample=first_sample,
			offset=offset,
			num_samples=num_samples)
		for first_sample, offset, num_samples in [
			(0, 0, 4096),
			(40960, 140, 4096),
			(86016, 294, 4096),
			(131072, 448, 4096),
			(176128, 602, 4096)
		]
	]

	seektable_init = FLACSeekTable(seekpoints)
	seektable_load = FLACSeekTable.parse(flac_seektable)

	assert seektable_init == seektable_load
	assert seektable_init.data == seektable_load.data == seekpoints
