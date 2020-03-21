from ward import (
	each,
	raises,
	test,
	using,
)

from audio_metadata import (
	FormatError,
	TagError,
	VorbisComment,
	VorbisComments,
)
from tests.fixtures import vorbis_comments


@test(
	"VorbisComment",
	tags=['unit', 'vorbis', 'comment', 'comments', 'VorbisComment'],
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
	"Invalid ``=`` in Vorbis comment raises FormatError",
	tags=['unit', 'vorbis', 'comment', 'comments', 'VorbisComment'],
)
def _():
	with raises(FormatError) as exc:
		VorbisComment.parse(b'\x09\x00\x00\x00albumtest-album')
	assert str(exc.raised) == "Vorbis comment must contain an ``=``."


@test(
	"Invalid character in Vorbis comment name raises TagError",
	tags=['unit', 'vorbis', 'comment', 'comments', 'VorbisComment'],
)
def _():
	with raises(TagError) as exc:
		VorbisComment.parse(b'\x10\x00\x00\x00albu~=test-album')
	assert str(exc.raised) == "Invalid character in Vorbis comment name: ``albu~``."


@test(
	"VorbisComments",
	tags=['unit', 'vorbis', 'comment', 'comments', 'VorbisComments'],
)
@using(data=vorbis_comments)
def _(data):
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
	vorbis_comments_load = VorbisComments.parse(data)

	assert vorbis_comments_init == vorbis_comments_load


@test(
	"Invalid character in Vorbis comment name raises TagError in VorbisComments",
	tags=['unit', 'vorbis', 'comment', 'comments', 'VorbisComments'],
)
def _():
	with raises(TagError) as exc:
		VorbisComments({'albu~': 'test-album'})
	assert str(exc.raised) == "Invalid character in Vorbis comment name: ``albu~``."
