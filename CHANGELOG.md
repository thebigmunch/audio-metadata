# Change Log

Notable changes to this project based on the [Keep a Changelog](https://keepachangelog.com) format.
This project adheres to [Semantic Versioning](https://semver.org).


## [Unreleased](https://github.com/thebigmunch/audio-metadata/tree/main)

[Commits](https://github.com/thebigmunch/audio-metadata/compare/0.11.1...main)


## [0.11.1](https://github.com/thebigmunch/audio-metadata/releases/tag/0.11.1) (2020-05-14)

[Commits](https://github.com/thebigmunch/audio-metadata/compare/0.11.0...0.11.1)

### Fixed

* Attribute-style access for some ``Tags`` subclasses using field map aliases.


## [0.11.0](https://github.com/thebigmunch/audio-metadata/releases/tag/0.11.0) (2020-05-01)

[Commits](https://github.com/thebigmunch/audio-metadata/compare/0.10.0...0.11.0)

### Added

* ``ID3v2Disc``.
* ``ID3v2DiscFrame``.
* ``ID3v2Track``.
* ``ID3v2TrackFrame``.
* ``ID3v2TPROFrame``.
* Support for ID3v2 Popularimeter frames.
	* ``ID3v2Popularimeter``.
	* ``ID3v2PopularimeterFrame``.
* ``ID3v2PodcastFrame``.
* Support for Apple ``GRP1`` and ``TCAT`` ID3v2 frames.
* ``ID3v2AudioEncryptionFrame``.
* Support for ID3v2 play counter frames.
	* ``ID3v2PlayCounterFrame``.
* Support for ID3v2 recommended buffer frames.
	* ``ID3v2RecommendedBuffer``.
	* ``ID3v2RecommendedBufferFrame``.
* Support for ID3v2 event timing codes frames.
	* ``ID3v2Event``.
	* ``ID3v2Events``.
	* ``ID3v2EventTypes``.
	* ``ID3v2EventTimingCodesFrame``.

### Changed

* ``ID3v2NumberFrame`` value is not the appropriate class
	(``ID3v2Disc`` or ``ID3v2Track``) rather than having
	the number/total abstraction on the frame class itself.
* Use a single enum for ID3v2 timestamp format.
	* Remove ``ID3v2LyricsTimestampFormat``.
	* Remove ``ID3v2TempoTimestampFormat``.

### Removed

* ``ID3v2LyricsTimestampFormat``.
* ``ID3v2TempoTimestampFormat``.

### Fixed

* Missing maxsplit argument in ``ID3v2UniqueFileIdentiferFrame`` parsing.


## [0.10.0](https://github.com/thebigmunch/audio-metadata/releases/tag/0.10.0) (2020-04-08)

[Commits](https://github.com/thebigmunch/audio-metadata/compare/0.9.0...0.10.0)

### Added

* ``WAVSubchunk``.
* ``audio_format`` attribute to ``WAVEStreamInfo``.
* ``WAVEAudioFormat`` enum.
* Audio format extension data to ``WAVEStreamInfo``.
* Support for bitmap images.
* Properly support ID3v2 header flag differences between versions.
* Support for ID3v2 unsynchronization and frame flags.
* ``encode_synchsafe_int``.

### Changed

* 'WAV' -> 'WAVE' to match the name rather than extension.
* Refactor ``WAVE.parse``.
	* Move subchunk parsing into separate method.
	* Add ``WAVESubchunk``.
* Keep unhandled WAVE subchunks.
* Store ``ID3v2`` in ``FLAC`` in ``_id3`` attribute.
* Emit warning when ignoring ID3v2 frames with bad values.
* Ignore ID3v2 frames with no value.
* Catch and raise more exceptions when parsing ID3v2 frames.
* Raise exception when decoding too large synchsafe integer.

### Fixed

* Invalid duration calculation for ``WAV``.
* Properly handle invalid comment, involved people list, and TMCL frames
* Properly support ID3v2.2 ``PIC`` frames.
* Make ``apply_unsynchronization``/``remove_unsynchronization``
	functions fully comply with the ID3v2 unsynchronization scheme.


## [0.9.0](https://github.com/thebigmunch/audio-metadata/releases/tag/0.9.0) (2020-03-25)

[Commits](https://github.com/thebigmunch/audio-metadata/compare/0.8.0...0.9.0)

### Added

* ``Tag``.
* ``RIFFTag``.
* ``ID3v1Field``.
* ``ID3v1AlbumField``.
* ``ID3v1ArtistField``.
* ``ID3v1CommentField``.
* ``ID3v1GenreField``.
* ``ID3v1TitleField``.
* ``ID3v1TrackNumberField``.
* ``ID3v1YearField``.
* `ID3v2InvolvedPeopleListFrame`` as subclass of ``ID3v2PeopleListFrame``.
* ``ID3v2TMCLFrame`` as subclass of ``ID3v2PeopleListFrame``.
* ``FormatError``.
* ``TagError``.
* ``FLACVorbisComments``.
* Support for ID3v2 unique file identifier frames.
	* ``ID3v2UniqueFileIdentifier``.
	* ``ID3v2UniqueFileIdentifierFrame``.
* Support for ID3v2 synchronized tempo codes frames.
	* ``ID3v2TempoTimestampFormat``,
	* ``ID3v2SynchronizedTempoCodes``.
	* ``ID3v2SynchronizedTempoCodesFrame``.
* Support for multiple text strings in ID3v2 user text frames.
* Support for ID3v2 ``USER`` frames.
	* ``ID3v2TermsOfUse``.
	* ``ID3v2USERFrame``.
* Support for ID3v2 ``GRID`` frames.
	* ``ID3v2GroupID``.
	* ``ID3v2GRIDFrame``.
* Support for ID3v2 ``OWNE`` frames.
	* ``ID3v2OwnershipTransaction``.
	* ``ID3v2OWNEFrame``.

### Changed

* Rename ``value`` attribute of ``ID3v2GeneralEncapsulatedObject`` to ``object``.
* Make ``VorbisComment`` subclass ``Tag``.
* Refactor ID3v1 to use tag classes.
	* ``ID3v1Field``.
	* ``ID3v1AlbumField``.
	* ``ID3v1ArtistField``.
	* ``ID3v1CommentField``.
	* ``ID3v1GenreField``.
	* ``ID3v1TitleField``.
	* ``ID3v1TrackNumberField``.
	* ``ID3v1YearField``.
* Rename ``ID3v2MappingListFrame`` to ``ID3v2PeopleListFrame``.
* Use ``ID3v2Frame`` as base class for all ID3v2 frame classes.
* Make ``ID3v2Frame`` subclass ``Tag``.
* Refactor ID3v2 frame parsing.
	* Add ``_parse_frame_header`` helper method on ``ID3v2Frame``.
	* Add ``_parse_frame_data`` helper method to all ID3v2 frame classes.
	* ``ID3v2Frame.parse`` calls into helper methods for appropriate subclass.
* Revise exceptions.
* Check for framing bit in Ogg Vorbis comments.
* Check for invalid characters in Vorbis comment field names.
* Rename some ID3v2 frame classes:
	* ``ID3v2GEOBFrame`` -> ``ID3v2GeneralEncapsulatedObjectFrame``.
	* ``ID3v2TDATFrame`` -> ``ID3v2DateFrame``.
	* ``ID3v2TIMEFrame`` -> ``ID3v2TimeFrame``.
* Refactor ``FLAC.parse``.
	* Move metadata block parsing into separate method.
	* Add ``FormatError`` exceptions where needed.

### Removed

* ``ID3v2BaseFrame``.
* ``InvalidBlock``.
* ``InvalidChunk``.
* ``InvalidComment``.
* ``InvalidFormat``.
* ``InvalidFrame``.
* ``InvalidHeader``.

### Fixed

* ``ID3v2BinaryDataFrame`` not inheriting from ``ID3v2BaseFrame``.
* Support for ID3v2 frames with more than 2 values.
* ID3v2 genre frame parsing.


## [0.8.0](https://github.com/thebigmunch/audio-metadata/releases/tag/0.8.0) (2020-03-05)

[Commits](https://github.com/thebigmunch/audio-metadata/compare/0.7.0...0.8.0)

### Added

* Support for ID3v2 involved people list frames.
	* ``ID3v2InvolvedPerson``.
	* ``ID3v2MappingListFrame``.
* ``ID3v2Comment``.
* Ogg machinery.
	* ``Ogg``.
	* ``OggPage``.
	* ``OggPageHeader``.
	* ``OggPageSegments``.
* Ogg Opus load(s) support.
	* ``OggOpus``.
	* ``OggOpusStreaminfo``.
	* ``OggOpusVorbisComments``.
* ``AudioMetadataWarning``.
* ``ID3v2BinaryDataFrame``.
* Support for MCDI ID3v2 frame.
* Finish support for ID3v2.4 timestamp frames.
	* ``TDEN``.
	* ``TDOR``.
	* ``TDRC``.
	* ``TDRL``.
	* ``TDTG``.
* Support for TMCL ID3v2.4 frame.
	* ``ID3v2Performer``.
* Ogg Vorbis load(s) support.
	* ``OggVorbis``.
	* ``OggVorbisStreamInfo``.
	* ``OggOpusVorbisComments``.
* ``ID3v2GeneralEncapsulatedObject``.
* ``ID3v2PrivateInfo``.
* ``ID3v2UserURLLink``.
* ``ID3v2UserText``.
* ``ID3v2Lyrics``.
* ``ID3v2SynchronizedLyrics``.
* ``ID3v2UnsynchronizedLyrics``.
* ``ID3v2LyricsFrame``.
* ``ID3v2LyricsContentType``.
* ``ID3v2LyricsTimestampFormat``.
* ``ID3v2FrameAliases``.
* ``ID3v2FrameTypes``.


### Changed

* Make all attrs classes require keyword arguments.
* Rework ID3v2 comments abstractions.
	* Add ``ID3v2Comment`` class to encapsulate each comment.
	* Change ``ID3v2CommentFrame`` to have only value attribute
		that contains a single comment.
	* Change ``ID3v2Frames`` to present a list of comments for ``comment`` key.
* Rename ``formats.vorbis`` module to ``formats.vorbis_comments``.
* Load most commonly used unoffical ID3v2 frames.
* Rename class builder methods to ``parse``.
* Rework ID3v2 general encapsulated object abstractions.
	* Add ``ID3v2GeneralEncapsulatedObject`` class.
	* Change ``ID3v2GEOBFrame`` to have only value attribute
		that contains a single general encapsulated object.
	* Change ``ID3v2Frames`` to present a list of general
		encapsulated objects for ``GEOB`` key.
* Rework ID3v2 private information frame abstractions.
	* Add ``ID3v2PrivateInfo`` class.
	* Change ``ID3v2PrivateFrame`` to have only value attribute
		that contains a single private information object.
	* Change ``ID3v2Frames`` to present a list of private info
		objects for ``PRIV`` key.
* Rework ID3v2 user URL link frame abstractions.
	* Add ``ID3v2UserURLLink`` class.
	* Change ``ID3v2UserURLLinkFrame`` to have only value attribute
		that contains a single user URL link object.
	* Change ``ID3v2Frames`` to present a list of user URL link
		objects for ``WXXX`` key.
* Rework ID3v2 user text frame abstractions.
	* Add ``ID3v2UserText`` class.
	* Change ``ID3v2UserTextFrame`` to have only value attribute
		that contains a single user text object.
	* Change ``ID3v2Frames`` to present a list of user text
		objects for ``TXXX`` key.
* Rework ID3v2 lyrics frames abstractions.
	* Add ``ID3v2Lyrics``, ``ID3v2SynchronizedLyrics``,
		and ``ID3v2UnsynchronizedLyrics`` classes.
	* Change ``ID3v2SynchronizedLyricsFrame``
		and``ID3v2UnsynchronizedLyricsFrame``
		to have only value attribute
		that contains a single lyrics object.
	* Change ``ID3v2Frames`` to present a list of lyrics
		objects for ``SYLT``/``USLT`` keys.
* Move ID3v2 frame alias map out of ``ID3v2Frames``.
* Move ID3v2 frame type map out of ``ID3v2Frame``.

### Removed

* Move ``DataReader`` class and ``datareader`` decorator to ``tbm-utils``.

### Fixed

* Apply CBR bitrate mode check to MP3s with non-LAME Xing headers.
* Properly determine UTF-16 encodings in ID3v2 frames.


## [0.7.0](https://github.com/thebigmunch/audio-metadata/releases/tag/0.7.0) (2020-02-17)

[Commits](https://github.com/thebigmunch/audio-metadata/compare/0.6.0...0.7.0)

### Added

* ID3 version as attribute on ``ID3v2Frames``.
* ``VorbisComment``.
* ``InvalidComment`` exception.

### Changed

* Set ``FIELD_MAP`` on instance rather than class in ``ID3v2Frames.load``.
* Convert ``LAMEHeader.unwise_settings_used`` to boolean.
* Handle ID3 frames not valid for ID3 header version.
	Ignore them and emit a warning to the user.
* Move models module to top level.
* ``vorbis.VorbisPicture`` -> ``flac.FLACPicture``.

### Fixed

* ``RIFFTags`` field values are now lists.
* Regression with ``MP3StreamInfo.find_mpeg_frames`` caching.


## [0.6.0](https://github.com/thebigmunch/audio-metadata/releases/tag/0.6.0) (2019-10-18)

[Commits](https://github.com/thebigmunch/audio-metadata/compare/0.5.0...0.6.0)

### Added

* ``InvalidChunk`` exception.
* Support for VBRI headers in MP3.
* ``LAMEEncodingFlags``.
* ``ID3v2Flags``.
* ABR presets to ``LAMEPreset`` enum.
* ``InvalidBlock`` exception.

### Changed

* Refactor high-level API functions and ``DataReader`` to handle
	various inputs better, especially file-like objects.
* Support 0-duration FLAC files.
* Raise proper exception if WAV stream info not found.
* Make LAMEReplayGain contain both track and album gains.
	* Attributes are now:
		``peak, track_type, track_origin, track_adjustment,
		album_type, album_origin, album_adjustment``
	* LAMEHeader attributes from ``album_gain, track_gain`` to
		``replay_gain``.
* Use MusicBrainz Picard tag mappings.
* RIFFTags loading.
	It now expects ``INFO`` at start and raises an exception if not.
* Use find_mp3_frames for all possible MP3 inputs in determine_format.
	This prevents some misidentification, specifically
	in the case of little-endian BOM of UTF-16-encoded text.
* Rename ``XingTOC`` to ``XingToC``.
* Improve load(s) performance:
		* Use ``functools.lru_cache`` to remove penalty
			of calling ``MP3Streaminfo.find_mpeg_frames``
			once when determining format of MP3s and
			again when loading the MP3.
		* Use ``bitstruct`` C extension when available.

### Removed

* ``extension`` parameter from ``determine_format``.
	The purpose it served is no longer necessary.

### Fixed

* APEv2/ID3v1 searching for MP3 causing load failures in some cases.


## [0.5.0](https://github.com/thebigmunch/audio-metadata/releases/tag/0.5.0) (2019-07-22)

[Commits](https://github.com/thebigmunch/audio-metadata/compare/0.4.0...0.5.0)

### Added

* ``bit_depth`` to ``WAVStreamInfo``.
* Support for RIFF tags to WAV.

### Changed

* Expose full ID2v2 object in MP3 instead of just the header.
* Use ID3v1.1 format instead of ID3v1.0.
* ``determine_format`` extension check:
	* Force lowercase comparison.
	* Don't require period.
* Rename ``VorbisComment`` to ``VorbisComments``.
* Improve MP3 frame detection.

### Fixed

* Actually check if a bytes-like object was given to ``loads``.


## [0.4.0](https://github.com/thebigmunch/audio-metadata/releases/tag/0.4.0) (2019-01-31)

[Commits](https://github.com/thebigmunch/audio-metadata/compare/0.3.4...0.4.0)

## Added

* Validation for ``ID3v2NumberFrame`` and ``ID3v2NumericTextFrame``.
* ``ID3Version`` enum.

### Changed

* Use different field maps for different ID3v2 versions.


## [0.3.4](https://github.com/thebigmunch/audio-metadata/releases/tag/0.3.4) (2019-01-27)

[Commits](https://github.com/thebigmunch/audio-metadata/compare/0.3.3...0.3.4)

### Fixed

* ``TDAT`` and ``TIME`` frame validation to support multiple values.


## [0.3.3](https://github.com/thebigmunch/audio-metadata/releases/tag/0.3.3) (2019-01-26)

[Commits](https://github.com/thebigmunch/audio-metadata/compare/0.3.2...0.3.3)

### Fixed

* Missing ``encoding`` argument to ``decode_bytestring`` call.


## [0.3.2](https://github.com/thebigmunch/audio-metadata/releases/tag/0.3.2) (2019-01-26)

[Commits](https://github.com/thebigmunch/audio-metadata/compare/0.3.1...0.3.2)

### Added

* Support for multiple values in ID3v2.4 text information frames.
* Support for ``TDRC`` and ``TDRL`` frames.


## [0.3.1](https://github.com/thebigmunch/audio-metadata/releases/tag/0.3.1) (2019-01-16)

[Commits](https://github.com/thebigmunch/audio-metadata/compare/0.3.0...0.3.1)

### Changed

* Move ``Tags`` subclass ``__init__`` methods to ``Tags`` class.
	This should have been the case from the beginning; I just didn't notice.
	This should have no effect to users except that ``Tags`` can now be
	initialized like a dict itself.


## [0.3.0](https://github.com/thebigmunch/audio-metadata/releases/tag/0.3.0) (2019-01-15)

[Commits](https://github.com/thebigmunch/audio-metadata/compare/0.2.0...0.3.0)

### Added

* ID3v1 support. ID3v1 is loaded from MP3s if, and only if, no ID3v2 header is found.
* ``items`` property to ``ListMixin``.

### Fixed

* High memory usage spikes when loading some ID3 tags.


## [0.2.0](https://github.com/thebigmunch/audio-metadata/releases/tag/0.2.0) (2018-11-13)

[Commits](https://github.com/thebigmunch/audio-metadata/compare/0.1.0...0.2.0)

### Added

* Add support for loading ID3v2.2 tags.

### Changed

* Refactor ``determine_format``.

### Fixed

* Loading MP3 files with less than 4 MPEG frames
	now works so long as there is a XING header.
* Various bugs with loading WAV files.


## [0.1.0](https://github.com/thebigmunch/audio-metadata/releases/tag/0.1.0) (2018-10-19)

[Commits](https://github.com/thebigmunch/audio-metadata/commit/63d7eebe98d4d99cc27cfa2385cc2965cca22676)

* Initial release.
