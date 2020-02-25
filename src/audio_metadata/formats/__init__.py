from .flac import *
from .id3v1 import *
from .id3v2 import *
from .id3v2_frames import *
from .mp3 import *
from .ogg import *
from .oggopus import *
from .oggvorbis import *
from .tables import *
from .vorbis_comments import *
from .wav import *


__all__ = [
	*flac.__all__,
	*id3v1.__all__,
	*id3v2_frames.__all__,
	*id3v2.__all__,
	*mp3.__all__,
	*ogg.__all__,
	*oggopus.__all__,
	*oggvorbis.__all__,
	*tables.__all__,
	*vorbis_comments.__all__,
	*wav.__all__,
]
