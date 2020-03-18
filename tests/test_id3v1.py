from ward import (
	raises,
	test,
	using,
)

from audio_metadata import (
	ID3v1,
	ID3v1Fields,
	InvalidHeader
)
from tests.fixtures import (
	id3v1,
	null,
)


@test(
	"Valid",
	tags=['unit', 'id3', 'id3v1', 'ID3v1'],
)
@using(id3v1=id3v1)
def _(id3v1):
	id3v1 = ID3v1.parse(id3v1)
	expected_fields = ID3v1Fields(
		title=['test-title'],
		artist=['test-artist'],
		album=['test-album'],
		year=['2000'],
		comment=['test-comment'],
		tracknumber=['1'],
		genre=['Jazz']
	)

	assert id3v1.tags == expected_fields


@test(
	"Missing 'TAG' raises InvalidHeader",
	tags=['unit', 'id3', 'id3v1', 'ID3v1'],
)
@using(null=null)
def _(null):
	with raises(InvalidHeader):
		ID3v1.parse(null)


@test(
	"No title",
	tags=['unit', 'id3', 'id3v1', 'ID3v1'],
)
@using(id3v1=id3v1)
def _(id3v1):
	no_title = ID3v1.parse(id3v1.replace(b'test-title', b'\x00' * 10))
	assert 'title' not in no_title.tags


@test(
	"No artist",
	tags=['unit', 'id3', 'id3v1', 'ID3v1'],
)
@using(id3v1=id3v1)
def _(id3v1):
	no_artist = ID3v1.parse(id3v1.replace(b'test-artist', b'\x00' * 11))
	assert 'artist' not in no_artist.tags


@test(
	"No album",
	tags=['unit', 'id3', 'id3v1', 'ID3v1'],
)
@using(id3v1=id3v1)
def _(id3v1):
	no_album = ID3v1.parse(id3v1.replace(b'test-album', b'\x00' * 10))
	assert 'album' not in no_album.tags


@test(
	"No year",
	tags=['unit', 'id3', 'id3v1', 'ID3v1'],
)
@using(id3v1=id3v1)
def _(id3v1):
	no_year = ID3v1.parse(id3v1.replace(b'2000', b'\x00' * 4))
	assert 'year' not in no_year.tags


@test(
	"No comment",
	tags=['unit', 'id3', 'id3v1', 'ID3v1'],
)
@using(id3v1=id3v1)
def _(id3v1):
	no_comment = ID3v1.parse(id3v1.replace(b'test-comment', b'\x00' * 12))
	assert 'comment' not in no_comment.tags


@test(
	"No tracknumber",
	tags=['unit', 'id3', 'id3v1', 'ID3v1'],
)
@using(id3v1=id3v1)
def _(id3v1):
	no_tracknumber = ID3v1.parse(id3v1.replace(b'\x01', b'\x00'))
	assert 'tracknumber' not in no_tracknumber.tags


@test(
	"Invalid genre",
	tags=['unit', 'id3', 'id3v1', 'ID3v1'],
)
@using(id3v1=id3v1)
def _(id3v1):
	invalid_genre = ID3v1.parse(id3v1.replace(b'\x01\x08', b'\x01\xEF'))
	assert 'genre' not in invalid_genre.tags
