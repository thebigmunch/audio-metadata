__all__ = [
	'ID3v1',
	'ID3v1Fields'
]

from .models import Tags
from .tables import ID3v1Genres
from ..exceptions import InvalidHeader
from ..utils import DataReader


class ID3v1Fields(Tags):
	@classmethod
	def load(cls, data):
		if not isinstance(data, DataReader):
			data = DataReader(data)

		self = cls()

		title = data.read(30).strip(b'\x00').decode('iso-8859-1')
		artist = data.read(30).strip(b'\x00').decode('iso-8859-1')
		album = data.read(30).strip(b'\x00').decode('iso-8859-1')
		year = data.read(4).strip(b'\x00').decode('iso-8859-1')
		comment = data.read(30).strip(b'\x00').decode('iso-8859-1')
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

		if genre_index < len(ID3v1Genres):
			self.genre = [ID3v1Genres[genre_index]]

		return self


class ID3v1:
	@classmethod
	def load(cls, data):
		if not isinstance(data, DataReader):
			data = DataReader(data)

		if data.read(3) != b"TAG":
			raise InvalidHeader("Valid ID3v1 header not found.")

		self = cls()
		self.tags = ID3v1Fields.load(data)

		return self
