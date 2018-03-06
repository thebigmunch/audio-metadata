from .flac import *
from .id3 import *
from .models import *
from .mp3 import *
from .vorbis import *
from .wav import *


def determine_format(data, extension=None):
	if data.startswith((b'ID3', b'\xFF\xFB')):  # TODO: Catch all MP3 possibilities.
		if extension is None or extension.endswith('.mp3'):
			return MP3

	if data.startswith((b'fLaC', b'ID3')):
		if extension is None or extension.endswith('.flac'):
			return FLAC

	if data.startswith(b'RIFF'):
		if extension is None or extension.endswith('.wav'):
			return WAV

	return None


__all__ = [
	*flac.__all__,
	*id3.__all__,
	*models.__all__,
	*mp3.__all__,
	*vorbis.__all__,
	*wav.__all__,
	'determine_format'
]
