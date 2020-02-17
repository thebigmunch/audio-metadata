# Change Log

Notable changes to this project based on the [Keep a Changelog](https://keepachangelog.com) format.
This project adheres to [Semantic Versioning](https://semver.org).


## [Unreleased](https://github.com/thebigmunch/audio-metadata/tree/master)

[Commits](https://github.com/thebigmunch/audio-metadata/compare/0.6.0...master)

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
