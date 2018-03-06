__all__ = [
	'FLACMetadataBlockType', 'ID3PictureType', 'ID3v1Genres', 'LAMEBitrateMode',
	'LAMEChannelMode', 'LAMEPreset', 'LAMEReplayGainOrigin', 'LAMEReplayGainType',
	'LAMESurroundInfo', 'MP3BitrateMode', 'MP3Bitrates', 'MP3ChannelMode',
	'MP3SampleRates', 'MP3SamplesPerFrame'
]

from enum import IntEnum


class FLACMetadataBlockType(IntEnum):
	STREAMINFO = 0
	PADDING = 1
	APPLICATION = 2
	SEEKTABLE = 3
	VORBIS_COMMENT = 4
	CUESHEET = 5
	PICTURE = 6


class ID3PictureType(IntEnum):
	OTHER = 0
	FILE_ICON = 1
	OTHER_FILE_ICON = 2
	COVER_FRONT = 3
	COVER_BACK = 4
	LEAFLET_PAGE = 5
	MEDIA = 6
	LEAD_ARTIST = 7
	ARTIST = 8
	CONDUCTOR = 9
	BAND = 10
	COMPOSER = 11
	LYRICIST = 12
	RECORDING_LOCATION = 13
	DURING_RECORDING = 14
	DURING_PERFORMANCE = 15
	SCREEN_CAPTURE = 16
	FISH = 17
	ILLUSTRATION = 18
	ARTIST_LOGOTYPE = 19
	BAND_LOGOTYPE = 19
	PUBLISHER_LOGOTYPE = 20
	STUDIO_LOGOTYPE = 20


ID3v1Genres = [
	'Blues', 'Classic Rock', 'Country', 'Dance', 'Disco', 'Funk', 'Grunge', 'Hip-Hop', 'Jazz', 'Metal', 'New Age',
	'Oldies', 'Other', 'Pop', 'R&B', 'Rap', 'Reggae', 'Rock', 'Techno', 'Industrial', 'Alternative', 'Ska',
	'Death Metal', 'Pranks', 'Soundtrack', 'Euro-Techno', 'Ambient', 'Trip-Hop', 'Vocal', 'Jazz+Funk', 'Fusion',
	'Trance', 'Classical', 'Instrumental', 'Acid', 'House', 'Game', 'Sound Clip', 'Gospel', 'Noise', 'Alt Rock',
	'Bass', 'Soul', 'Punk', 'Space', 'Meditative', 'Instrumental Pop', 'Instrumental Rock', 'Ethnic', 'Gothic',
	'Darkwave', 'Techno-Industrial', 'Electronic', 'Pop-Folk', 'Eurodance', 'Dream', 'Southern Rock', 'Comedy',
	'Cult', 'Gangsta Rap', 'Top 40', 'Christian Rap', 'Pop/Funk', 'Jungle', 'Native American', 'Cabaret', 'New Wave',
	'Psychedelic', 'Rave', 'Showtunes', 'Trailer', 'Lo-Fi', 'Tribal', 'Acid Punk', 'Acid Jazz', 'Polka', 'Retro',
	'Musical', 'Rock & Roll', 'Hard Rock', 'Folk', 'Folk-Rock', 'National Folk', 'Swing', 'Fast-Fusion', 'Bebop',
	'Latin', 'Revival', 'Celtic', 'Bluegrass', 'Avantgarde', 'Gothic Rock', 'Progressive Rock', 'Symphonic Rock',
	'Slow Rock', 'Big Band', 'Chorus', 'Easy Listening', 'Acoustic', 'Humour', 'Speech', 'Chanson', 'Opera',
	'Chamber Music', 'Sonata', 'Symphony', 'Booty Bass', 'Primus', 'Porn Groove', 'Satire', 'Slow Jam', 'Club',
	'Tango', 'Samba', 'Folklore', 'Ballad', 'Power Ballad', 'Rhythmic Soul', 'Freestyle', 'Duet', 'Punk Rock',
	'Drum Solo', 'A Cappella', 'Euro-House', 'Dance Hall', 'Goa', 'Drum & Bass', 'Club-House', 'Hardcore',
	'Terror', 'Indie', 'BritPop', 'Afro-Punk', 'Polsk Punk', 'Beat', 'Christian Gangsta Rap', 'Heavy Metal',
	'Black Metal', 'Crossover', 'Contemporary Christian', 'Chrstian Rock', 'Merengue', 'Salsa', 'Thrash Metal',
	'Anime', 'JPop', 'Synthpop', 'Abstract', 'Art Rock', 'Baroque', 'Bhangra', 'Big Beat', 'Breakbeat', 'Chillout',
	'Downtempo', 'Dub', 'EBM', 'Eclectic', 'Electro', 'Electroclash', 'Emo', 'Experimental', 'Garage', 'Global',
	'IDM', 'Illibient', 'Industro-Goth', 'Jam Band', 'Krautrock', 'Leftfield', 'Lounge', 'Math Rock', 'New Romantic',
	'Nu-Breakz', 'Post-Punk', 'Post-Rock', 'Psytrance', 'Shoegaze', 'Space Rock', 'Trop Rock', 'World Music',
	'Neoclassical', 'Audiobook', 'Audio Theatre', 'Neue Deutsche Welle', 'Podcast', 'Indie Rock', 'G-Funk',
	'Dubstep', 'Garage Rock', 'Psybient'
]


class LAMEBitrateMode(IntEnum):
	UNKNOWN = 0
	CBR = 1
	ABR = 2
	VBR_METHOD_1 = 3
	VBR_METHOD_2 = 4
	VBR_METHOD_3 = 5
	VBR_METHOD_4 = 6
	CBR_2_PASS = 8
	ABR_2_PASS = 9
	RESERVED = 15


class LAMEChannelMode(IntEnum):
	MONO = 0
	STEREO = 1
	DUAL_CHANNEL = 2
	JOINT_STEREO = 3
	FORCED = 4
	AUTO = 5
	INTENSITY = 6
	UNDEFINED = 7


# 8 through 320 are reserved for ABR bitrates.
class LAMEPreset(IntEnum):
	Unknown = 0
	V9 = 410
	V8 = 420
	V7 = 430
	V6 = 440
	V5 = 450
	V4 = 460
	V3 = 470
	V2 = 480
	V1 = 490
	V0 = 500
	r3mix = 1000
	standard = 1001
	extreme = 1002
	insane = 1003
	standard_fast = 1004
	extreme_fast = 1005
	medium = 1006
	medium_fast = 1007


class LAMEReplayGainOrigin(IntEnum):
	not_set = 0
	artist = 1
	user = 2
	model = 3
	average = 4


class LAMEReplayGainType(IntEnum):
	not_set = 0
	radio = 1
	audiophile = 2


class LAMESurroundInfo(IntEnum):
	NO_SURROUND = 0
	DPL = 1
	DPL2 = 2
	AMBISONIC = 3


# (version, layer): bitrate in kilobits per second
MP3Bitrates = {
	(1, 1): [0, 32, 64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384, 416, 448],
	(1, 2): [0, 32, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 384],
	(1, 3): [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320],
	(2, 1): [0, 32, 48, 56, 64, 80, 96, 112, 128, 144, 160, 176, 192, 224, 256],
	(2, 2): [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160],
	(2, 3): [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160],
	(2.5, 1): [0, 32, 48, 56, 64, 80, 96, 112, 128, 144, 160, 176, 192, 224, 256],
	(2.5, 2): [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160],
	(2.5, 3): [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160]
}


class MP3BitrateMode(IntEnum):
	UNKNOWN = 0
	CBR = 1
	VBR = 2
	ABR = 3


class MP3ChannelMode(IntEnum):
	STEREO = 0
	JOINT_STEREO = 1
	DUAL_CHANNEL = 2
	MONO = 3


# version
MP3SampleRates = {
	1: [44100, 48000, 32000],
	2: [22050, 24000, 16000],
	2.5: [11025, 12000, 8000]
}


# (version, layer): (samples_per_frame, slot_size)
MP3SamplesPerFrame = {
	(1, 1): (384, 4),
	(1, 2): (1152, 1),
	(1, 3): (1152, 1),
	(2, 1): (384, 4),
	(2, 2): (1152, 1),
	(2, 3): (576, 1),
	(2.5, 1): (384, 4),
	(2.5, 2): (1152, 1),
	(2.5, 3): (576, 1),
}
