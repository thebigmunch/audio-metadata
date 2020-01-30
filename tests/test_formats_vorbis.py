from audio_metadata.formats.tables import ID3PictureType
from audio_metadata.formats.vorbis import (
	VorbisComments,
	VorbisPicture
)


def test_VorbisComments():
	vorbis_comments_init = VorbisComments(
		_vendor='reference libFLAC 1.3.2 20170101',
		album=['test-album'],
		artist=['test-artist'],
		comment=['test-comment'],
		date=['2000'],
		discnumber=['1'],
		disctotal=['99'],
		genre=['test-genre'],
		title=['test-title'],
		tracknumber=['1'],
		tracktotal=['99'],
	)
	vorbis_comments_load = VorbisComments.load(
		b' \x00\x00\x00reference libFLAC 1.3.2 20170101\n\x00\x00\x00'
		b'\x10\x00\x00\x00album=test-album'
		b'\x12\x00\x00\x00artist=test-artist'
		b'\x14\x00\x00\x00COMMENT=test-comment'
		b'\t\x00\x00\x00date=2000'
		b'\x0c\x00\x00\x00discnumber=1'
		b'\x10\x00\x00\x00genre=test-genre'
		b'\x10\x00\x00\x00title=test-title'
		b'\x0c\x00\x00\x00DISCTOTAL=99'
		b'\r\x00\x00\x00TRACKTOTAL=99'
		b'\r\x00\x00\x00tracknumber=1'
	)

	assert vorbis_comments_init == vorbis_comments_load


def test_VorbisPicture():
	image_data = (
		b'\x00\x00\x00\x03\x00\x00\x00\timage/png\x00\x00\x00\x00'
		b'\x00\x00\x00\x10\x00\x00\x00\x10\x00\x00\x00 \x00\x00'
		b'\x00\x00\x00\x00\x00`\x89PNG\r\n\x1a\n\x00\x00\x00\r'
		b'IHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00'
		b'\x00\x1f\xf3\xffa\x00\x00\x00\tpHYs\x00\x00\x0b\x12\x00'
		b'\x00\x0b\x12\x01\xd2\xdd~\xfc\x00\x00\x00\x12IDAT8\xcbc`'
		b'\x18\x05\xa3`\x14\x8c\x02\x08\x00\x00\x04\x10\x00\x01\x85'
		b'?\xaar\x00\x00\x00\x00IEND\xaeB`\x82'
	)

	vorbis_picture_init = VorbisPicture(
		type=ID3PictureType.COVER_FRONT,
		mime_type='image/png',
		description='',
		width=16,
		height=16,
		depth=32,
		colors=0,
		data=image_data[41:],
	)
	vorbis_picture_load = VorbisPicture.load(image_data)

	assert vorbis_picture_init == vorbis_picture_load
