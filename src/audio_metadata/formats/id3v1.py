# http://id3.org/ID3v1

__all__ = [
	'ID3v1',
	'ID3v1Fields',
]

from tbm_utils import AttrMapping

from .tables import ID3v1Genres
from ..exceptions import InvalidHeader
from ..models import Tags
from ..utils import datareader


class ID3v1Fields(Tags):
	@datareader
	@classmethod
	def load(cls, data):
		self = cls()

		title = data.read(30).strip(b'\x00').decode('iso-8859-1')
		artist = data.read(30).strip(b'\x00').decode('iso-8859-1')
		album = data.read(30).strip(b'\x00').decode('iso-8859-1')
		year = data.read(4).strip(b'\x00').decode('iso-8859-1')
		comment = data.read(29).strip(b'\x00').decode('iso-8859-1')
		tracknumber = str(data.read(1)[0])
		genre_index = int.from_bytes(data.read(1), byteorder='big')

		if title:
			self.title = [title]

		if artist:
			self.artist = [artist]

		if album:
			self.album = [album]

		if year:
			self.year = [year]

		if comment:
			self.comment = [comment]

		if tracknumber != '0':
			self.tracknumber = [tracknumber]

		if genre_index < len(ID3v1Genres):
			self.genre = [ID3v1Genres[genre_index]]

		return self


class ID3v1(AttrMapping):
	@datareader
	@classmethod
	def load(cls, data):
		if data.read(3) != b"TAG":
			raise InvalidHeader("Valid ID3v1 header not found.")

		self = cls()
		self.tags = ID3v1Fields.load(data)

		return self
