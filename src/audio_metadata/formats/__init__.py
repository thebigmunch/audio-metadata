from .flac import *
from .id3v2 import *
from .id3v2_frames import *
from .models import *
from .mp3 import *
from .tables import *
from .vorbis import *
from .wav import *


__all__ = [
	*flac.__all__,
	*id3v2_frames.__all__,
	*id3v2.__all__,
	*models.__all__,
	*mp3.__all__,
	*tables.__all__,
	*vorbis.__all__,
	*wav.__all__
]
