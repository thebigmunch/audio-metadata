from ward import (
	each,
	raises,
	test,
)

from audio_metadata import (
	InvalidComment,
	VorbisComment,
	VorbisComments,
)


@test(
	"VorbisComment",
	tags=['unit', 'vorbis', 'comments', 'VorbisComment'],
)
def _(
	data=each(
		b'\x10\x00\x00\x00album=test-album',
		b'\x14\x00\x00\x00COMMENT=test-comment',
		b'\t\x00\x00\x00date=2000',
		b'\x0c\x00\x00\x00discnumber=1',
		b'\x10\x00\x00\x00genre=test-genre',
		b'\x0c\x00\x00\x00DISCTOTAL=99',
		b'\r\x00\x00\x00TRACKTOTAL=99',
		b'\r\x00\x00\x00tracknumber=1',
	),
	expected=each(
		VorbisComment(
			name='album',
			value='test-album',
		),
		VorbisComment(
			name='comment',
			value='test-comment',
		),
		VorbisComment(
			name='date',
			value='2000',
		),
		VorbisComment(
			name='discnumber',
			value='1',
		),
		VorbisComment(
			name='genre',
			value='test-genre',
		),
		VorbisComment(
			name='disctotal',
			value='99',
		),
		VorbisComment(
			name='tracktotal',
			value='99',
		),
		VorbisComment(
			name='tracknumber',
			value='1',
		),
	)
):
	assert VorbisComment.parse(data) == expected


@test(
	"Invalid '=' in Vorbis comment raises InvalidComment",
	tags=['unit', 'vorbis', 'comments', 'VorbisComment'],
)
def _():
	with raises(InvalidComment):
		VorbisComment.parse(b'\x09\x00\x00\x00albumtest-album')


@test(
	"VorbisComments",
	tags=['unit', 'vorbis', 'comments', 'VorbisComments'],
)
def _():
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
	vorbis_comments_load = VorbisComments.parse(
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
