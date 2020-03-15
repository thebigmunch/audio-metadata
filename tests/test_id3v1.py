from ward import (
	raises,
	test,
)

from audio_metadata import (
	ID3v1,
	ID3v1Fields,
	InvalidHeader
)

ID3v1_DATA = (
	b'TAG'
	b'test-title\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
	b'test-artist\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
	b'test-album\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
	b'2000'
	b'test-comment\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
	b'\x01'
	b'\x08'
)


@test(
	"Valid",
	tags=['unit', 'id3', 'id3v1', 'ID3v1'],
)
def _():
	id3v1 = ID3v1.parse(ID3v1_DATA)
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
def _():
	with raises(InvalidHeader):
		ID3v1.parse(ID3v1_DATA[3:])


@test(
	"No title",
	tags=['unit', 'id3', 'id3v1', 'ID3v1'],
)
def _():
	id3v1 = ID3v1.parse(ID3v1_DATA.replace(b'test-title', b'\x00' * 10))
	assert 'title' not in id3v1.tags


@test(
	"No artist",
	tags=['unit', 'id3', 'id3v1', 'ID3v1'],
)
def _():
	id3v1 = ID3v1.parse(ID3v1_DATA.replace(b'test-artist', b'\x00' * 11))
	assert 'artist' not in id3v1.tags


@test(
	"No album",
	tags=['unit', 'id3', 'id3v1', 'ID3v1'],
)
def _():
	id3v1 = ID3v1.parse(ID3v1_DATA.replace(b'test-album', b'\x00' * 10))
	assert 'album' not in id3v1.tags


@test(
	"No year",
	tags=['unit', 'id3', 'id3v1', 'ID3v1'],
)
def _():
	id3v1 = ID3v1.parse(ID3v1_DATA.replace(b'2000', b'\x00' * 4))
	assert 'year' not in id3v1.tags


@test(
	"No comment",
	tags=['unit', 'id3', 'id3v1', 'ID3v1'],
)
def _():
	id3v1 = ID3v1.parse(ID3v1_DATA.replace(b'test-comment', b'\x00' * 12))
	assert 'comment' not in id3v1.tags


@test(
	"No tracknumber",
	tags=['unit', 'id3', 'id3v1', 'ID3v1'],
)
def _():
	id3v1 = ID3v1.parse(ID3v1_DATA.replace(b'\x01', b'\x00'))
	assert 'tracknumber' not in id3v1.tags


@test(
	"Invalid genre",
	tags=['unit', 'id3', 'id3v1', 'ID3v1'],
)
def _():
	id3v1 = ID3v1.parse(ID3v1_DATA.replace(b'\x01\x08', b'\x01\xEF'))
	assert 'genre' not in id3v1.tags
