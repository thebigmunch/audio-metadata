# Change Log

Notable changes to this project based on the [Keep a Changelog](https://keepachangelog.com) format.
This project adheres to [Semantic Versioning](https://semver.org).


## [Unreleased](https://github.com/thebigmunch/audio-metadata/tree/master)

[Commits](https://github.com/thebigmunch/audio-metadata/compare/0.3.3...master)


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
