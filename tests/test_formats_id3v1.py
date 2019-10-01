import pytest

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


def test_ID3v1():
	id3v1 = ID3v1.load(ID3v1_DATA)
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


def test_ID3v1_no_TAG():
	with pytest.raises(InvalidHeader):
		ID3v1.load(ID3v1_DATA[3:])


def test_ID3v1_no_title():
	id3v1 = ID3v1.load(ID3v1_DATA.replace(b'test-title', b'\x00' * 10))
	assert 'title' not in id3v1.tags


def test_ID3v1_no_artist():
	id3v1 = ID3v1.load(ID3v1_DATA.replace(b'test-artist', b'\x00' * 11))
	assert 'artist' not in id3v1.tags


def test_ID3v1_no_album():
	id3v1 = ID3v1.load(ID3v1_DATA.replace(b'test-album', b'\x00' * 10))
	assert 'album' not in id3v1.tags


def test_ID3v1_no_year():
	id3v1 = ID3v1.load(ID3v1_DATA.replace(b'2000', b'\x00' * 4))
	assert 'year' not in id3v1.tags


def test_ID3v1_no_comment():
	id3v1 = ID3v1.load(ID3v1_DATA.replace(b'test-comment', b'\x00' * 12))
	assert 'comment' not in id3v1.tags


def test_ID3v1_no_tracknumber():
	id3v1 = ID3v1.load(ID3v1_DATA.replace(b'\x01', b'\x00'))
	assert 'tracknumber' not in id3v1.tags


def test_ID3v1_invalid_genre():
	id3v1 = ID3v1.load(ID3v1_DATA.replace(b'\x01\x08', b'\x01\xEF'))
	assert 'genre' not in id3v1.tags
