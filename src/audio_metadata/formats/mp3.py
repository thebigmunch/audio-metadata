__all__ = [
	'LAMEHeader', 'MP3', 'MP3StreamInfo', 'MPEGFrameHeader', 'XingHeader', 'XingTOC'
]

import os
import re
import struct
from enum import Enum

import more_itertools
from attr import attrib, attrs

from .id3 import ID3v2, ID3v2Frames
from .models import Format, StreamInfo
from .tables import (
	LAMEBitrateMode, LAMEChannelMode, LAMEPreset, LAMEReplayGainOrigin, LAMEReplayGainType, LAMESurroundInfo,
	MP3BitrateMode, MP3Bitrates, MP3ChannelMode, MP3SampleRates, MP3SamplesPerFrame
)
from ..exceptions import InvalidFrame, InvalidHeader
from ..structures import DictMixin, ListMixin
from ..utils import DataReader, humanize_bitrate, humanize_filesize, humanize_sample_rate


@attrs(repr=False)
class LAMEReplayGain(DictMixin):
	type = attrib()  # noqa
	origin = attrib()
	adjustment = attrib()
	peak = attrib()

	def __repr__(self):
		repr_dict = {}

		for k, v in sorted(self.items()):
			if isinstance(v, Enum):
				repr_dict[k] = v.name
			elif not k.startswith('_'):
				repr_dict[k] = v

		return super().__repr__(repr_dict=repr_dict)

	@classmethod
	def load(cls, data):
		if not isinstance(data, DataReader):
			data = DataReader(data)

		replay_gain_data = struct.unpack('>I2B', data.read(6))

		peak_data = replay_gain_data[0]

		if peak_data == b'\x00\x00\x00\x00':
			gain_peak = None
		else:
			gain_peak = (peak_data - 0.5) / 2 ** 23

		gain_type = LAMEReplayGainType(replay_gain_data[1] >> 5)
		gain_origin = LAMEReplayGainOrigin((replay_gain_data[1] >> 2) & 7)
		gain_sign = (replay_gain_data[1] >> 1) & 1

		adjustment_start = (replay_gain_data[1] & 1) << 4
		adjustment_end = replay_gain_data[2]
		gain_adjustment = (adjustment_start + adjustment_end) / 10

		if gain_sign:
			gain_adjustment *= -1

		if not gain_type:
			return None

		return cls(gain_type, gain_origin, gain_adjustment, gain_peak)


@attrs(repr=False)
class LAMEHeader(DictMixin):
	_crc = attrib()
	version = attrib()
	revision = attrib()
	album_gain = attrib()
	ath_type = attrib()
	audio_crc = attrib()
	audio_size = attrib()
	bitrate = attrib()
	bitrate_mode = attrib()
	channel_mode = attrib()
	delay = attrib()
	encoding_flags = attrib()
	lowpass_filter = attrib()
	mp3_gain = attrib()
	noise_shaping = attrib()
	padding = attrib()
	preset = attrib()
	source_sample_rate = attrib()
	surround_info = attrib()
	track_gain = attrib()
	unwise_settings_used = attrib()

	def __repr__(self):
		repr_dict = {}

		for k, v in sorted(self.items()):
			if k == 'bitrate':
				repr_dict[k] = humanize_bitrate(v)
			elif k == 'audio_size':
				repr_dict[k] = humanize_filesize(v, precision=2)
			elif isinstance(v, Enum):
				repr_dict[k] = v.name
			elif not k.startswith('_'):
				repr_dict[k] = v

		return super().__repr__(repr_dict=repr_dict)

	@classmethod
	def load(cls, data, xing_quality):
		if not isinstance(data, DataReader):
			data = DataReader(data)

		lame_header_data = struct.unpack('>9s2B4s2s2s9BIHH', data.read(36))

		encoder = lame_header_data[0]
		if not encoder.startswith(b'LAME'):
			raise InvalidHeader('Valid LAME header not found.')

		version_match = re.search(rb'LAME(\d+)\.(\d+)', encoder)
		if version_match:
			version = tuple(int(part) for part in version_match.groups())
		else:
			version = None

		rev_mode = lame_header_data[1]
		revision = rev_mode >> 4
		bitrate_mode = LAMEBitrateMode(rev_mode & 15)

		# TODO: Decide what, if anything, to do with the different meanings in LAME.
		# quality = (100 - xing_quality) % 10
		# vbr_quality = (100 - xing_quality) // 10

		lowpass_filter = lame_header_data[2] * 100

		track_gain = LAMEReplayGain.load(lame_header_data[3] + lame_header_data[4])
		album_gain = LAMEReplayGain.load(lame_header_data[3] + lame_header_data[5])

		enc_flags = lame_header_data[6] >> 4
		nspsytune = bool(enc_flags & 1)
		nssafejoint = bool(enc_flags & 2)
		nogap_continued = bool(enc_flags & 4)
		nogap_continuation = bool(enc_flags & 8)

		encoding_flags = {
			'nogap_continuation': nogap_continuation, 'nogap_continued': nogap_continued,
			'nspsytune': nspsytune, 'nssafejoint': nssafejoint
		}

		ath_type = lame_header_data[6] & 15

		# TODO: Different representation for VBR minimum bitrate vs CBR/ABR specified bitrate?
		# Can only go up to 255.
		bitrate = lame_header_data[7] * 1000

		delay = (lame_header_data[8] + (lame_header_data[9] >> 4)) << 4
		padding = ((lame_header_data[9] & 15) << 8) + lame_header_data[10]

		source_sample_rate = (lame_header_data[11] >> 6) & 3
		unwise_settings_used = bool((lame_header_data[11] >> 5) & 1)
		channel_mode = LAMEChannelMode((lame_header_data[11] >> 2) & 7)
		noise_shaping = lame_header_data[11] & 3

		mp3_gain = lame_header_data[12] & 127
		if lame_header_data[12] & 1:
			mp3_gain *= -1

		surround_info = LAMESurroundInfo((lame_header_data[13] >> 3) & 7)
		preset_used = ((lame_header_data[13] & 7) << 8) + lame_header_data[14]

		try:
			preset = LAMEPreset(preset_used)
		except ValueError:  # 8-320 are used for bitrates and aren't defined in LAMEPreset.
			preset = f"{preset_used} Kbps"

		audio_size = lame_header_data[15]

		audio_crc = lame_header_data[16]
		lame_crc = lame_header_data[17]

		return cls(
			lame_crc, version, revision, album_gain, ath_type, audio_crc, audio_size, bitrate,
			bitrate_mode, channel_mode, delay, encoding_flags, lowpass_filter, mp3_gain, noise_shaping,
			padding, preset, source_sample_rate, surround_info, track_gain, unwise_settings_used
		)


class XingTOC(ListMixin):
	item_label = 'entries'

	def __init__(self, items):
		super().__init__(items)


@attrs(repr=False)
class XingHeader(DictMixin):
	_lame = attrib()
	num_frames = attrib()
	num_bytes = attrib()
	toc = attrib()
	quality = attrib()

	@classmethod
	def load(cls, data):
		if not isinstance(data, DataReader):
			data = DataReader(data)

		if data.read(4) not in [b'Xing', b'Info']:
			raise InvalidHeader('Valid Xing header not found.')

		flags = struct.unpack('>i', data.read(4))[0]

		num_frames = num_bytes = toc = quality = lame_header = None

		if flags & 1:
			num_frames = struct.unpack('>i', data.read(4))[0]

		if flags & 2:
			num_bytes = struct.unpack('>i', data.read(4))[0]

		if flags & 4:
			toc = XingTOC(list(bytearray(data.read(100))))

		if flags & 8:
			quality = struct.unpack('>i', data.read(4))[0]

		if data.read(4) == b'LAME':
			data.seek(-4, os.SEEK_CUR)
			lame_header = LAMEHeader.load(data, quality)

		return cls(lame_header, num_frames, num_bytes, toc, quality)


@attrs(repr=False)
class MPEGFrameHeader(DictMixin):
	_start = attrib()
	_size = attrib()
	_xing = attrib()
	version = attrib()
	layer = attrib()
	protected = attrib()
	padded = attrib()
	bitrate = attrib()
	channel_mode = attrib()
	channels = attrib()
	sample_rate = attrib()

	def __repr__(self):
		repr_dict = {}

		for k, v in sorted(self.items()):
			if k == 'bitrate':
				repr_dict[k] = humanize_bitrate(v)
			elif k == 'sample_rate':
				repr_dict[k] = humanize_sample_rate(v)
			elif isinstance(v, Enum):
				repr_dict[k] = v.name
			elif not k.startswith('_'):
				repr_dict[k] = v

		return super().__repr__(repr_dict=repr_dict)

	@classmethod
	def load(cls, data):
		if not isinstance(data, DataReader):
			data = DataReader(data)

		frame_start = data.tell()

		sync, flags, indexes, remainder = struct.unpack('BBBB', data.read(4))

		if sync != 255 or flags >> 5 != 7:
			raise InvalidFrame('Not a valid MPEG audio frame.')

		version_id = (flags >> 3) & 0x03
		version = [2.5, None, 2, 1][version_id]

		layer_index = (flags >> 1) & 0x03
		layer = 4 - layer_index

		protected = bool(not (flags & 1))

		bitrate_index = (indexes >> 4) & 0x0F
		sample_rate_index = (indexes >> 2) & 0x03

		padded = bool(indexes & 0x02)

		channel_mode = MP3ChannelMode((remainder >> 6) & 0x03)
		channels = 1 if channel_mode == 3 else 2

		if version_id == 1 or layer_index == 0 or bitrate_index == 0 or bitrate_index == 15 or sample_rate_index == 3:
			raise InvalidFrame('Not a valid MPEG audio frame.')

		bitrate = MP3Bitrates[(version, layer)][bitrate_index] * 1000
		sample_rate = MP3SampleRates[version][sample_rate_index]

		samples_per_frame, slot_size = MP3SamplesPerFrame[(version, layer)]

		frame_size = (((samples_per_frame // 8 * bitrate) // sample_rate) + padded) * slot_size

		xing_header = None
		if layer == 3:
			if version == 1:
				if channel_mode != 3:
					xing_header_start = 36
				else:
					xing_header_start = 21
			elif channel_mode != 3:
				xing_header_start = 21
			else:
				xing_header_start = 13

			data.seek(frame_start + xing_header_start, os.SEEK_SET)

			t = data.read(4)
			if t in [b'Xing', b'Info']:
				data.seek(-4, os.SEEK_CUR)
				xing_header = XingHeader.load(data.read(frame_size))

		return cls(
			frame_start, frame_size, xing_header, version, layer, protected,
			padded, bitrate, channel_mode, channels, sample_rate
		)


@attrs(repr=False)
class MP3StreamInfo(StreamInfo):
	_start = attrib()
	_size = attrib()
	_xing = attrib()
	version = attrib()
	layer = attrib()
	protected = attrib()
	bitrate = attrib()
	bitrate_mode = attrib()
	channel_mode = attrib()
	channels = attrib()
	duration = attrib()
	sample_rate = attrib()

	@classmethod
	def load(cls, data):
		if not isinstance(data, DataReader):
			data = DataReader(data)

		frames = []
		while len(frames) < 4:
			buffer = data.peek()
			if len(buffer) < 4:
				break

			start = data.tell()
			if buffer[0] == 255 and buffer[1] >> 5 == 7:
				for _ in range(4):
					try:
						frame = MPEGFrameHeader.load(data)
						frames.append(frame)
						data.seek(frame._start + frame._size, os.SEEK_SET)
					except InvalidFrame:
						del frames[:]
						data.seek(start + 1, os.SEEK_SET)
						break
			else:
				index = buffer.find(b'\xFF', 1)
				if index == -1:
					index = len(buffer)
				data.seek(max(index, 1), os.SEEK_CUR)

		samples_per_frame, _ = MP3SamplesPerFrame[(frames[0].version, frames[0].layer)]

		data.seek(0, os.SEEK_END)
		end_pos = data.tell()

		# This is an arbitrary amount that should hopefully encompass all end tags.
		# Starting low so as not to add unnecessary processing time.
		chunk_size = 64 * 1024
		if end_pos > chunk_size:
			data.seek(-(chunk_size), os.SEEK_END)
		else:
			data.seek(0, os.SEEK_SET)

		end_buffer = data.read()

		end_tag_offset = 0
		for tag_type in [b'APETAGEX', b'LYRICSBEGIN', b'TAG']:
			tag_offset = end_buffer.rfind(tag_type)

			if tag_offset > 0:
				tag_offset = len(end_buffer) - tag_offset

				if tag_offset > end_tag_offset:
					end_tag_offset = tag_offset

		audio_start = frames[0]._start
		audio_size = end_pos - audio_start - end_tag_offset

		bitrate_mode = MP3BitrateMode.UNKNOWN

		xing_header = frames[0]._xing
		if xing_header:
			num_samples = samples_per_frame * xing_header.num_frames

			# I prefer to include the Xing/LAME header as part of the audio.
			# Google Music seems to do so for calculating client ID.
			# Haven't tested in too many other scenarios.
			# But, there should be enough low-level info for people to calculate this if desired.
			# audio_start = frames[1]._start
			if xing_header._lame:
				num_samples -= xing_header._lame.delay
				num_samples -= xing_header._lame.padding

				if xing_header._lame.bitrate_mode in [1, 8]:
					bitrate_mode = MP3BitrateMode.CBR
				elif xing_header._lame.bitrate_mode in [2, 9]:
					bitrate_mode = MP3BitrateMode.ABR
				elif xing_header._lame.bitrate_mode in [3, 4, 5, 6]:
					bitrate_mode = MP3BitrateMode.VBR
		else:
			if more_itertools.all_equal([frame['bitrate'] for frame in frames]):
				bitrate_mode = MP3BitrateMode.CBR

			num_samples = samples_per_frame * (audio_size / frames[0]._size)

		if bitrate_mode == MP3BitrateMode.CBR:
			bitrate = frames[0].bitrate
		else:
			# Subtract Xing/LAME frame size from audio_size for bitrate calculation accuracy.
			if xing_header:
				bitrate = ((audio_size - frames[0]._size) * 8 * frames[0].sample_rate) / num_samples
			else:
				bitrate = (audio_size * 8 * frames[0].sample_rate) / num_samples

		duration = (audio_size * 8) / bitrate

		version = frames[0].version
		layer = frames[0].layer
		protected = frames[0].protected
		sample_rate = frames[0].sample_rate
		channel_mode = frames[0].channel_mode
		channels = frames[0].channels

		return cls(
			audio_start, audio_size, xing_header, version, layer, protected, bitrate,
			bitrate_mode, channel_mode, channels, duration, sample_rate
		)


class MP3(Format):
	"""MP3 file format object.

	Extends :class:`Format`.

	Attributes:
		pictures (list): A list of :class:`ID3v2Picture` objects.
		streaminfo (MP3StreamInfo): The audio stream information.
		tags (ID3v2Frames): The ID3v2 tag frames, if present.
	"""

	tags_type = ID3v2Frames

	@classmethod
	def load(cls, data):
		self = super()._load(data)

		try:
			id3 = ID3v2.load(self._obj)
			self._id3 = id3._header
			self.pictures = id3.pictures
			self.tags = id3.tags
			self._obj.seek(self._id3._size, os.SEEK_SET)
		except (InvalidFrame, InvalidHeader):
			self._obj.seek(0, os.SEEK_SET)

		self.streaminfo = MP3StreamInfo.load(self._obj)

		return self
