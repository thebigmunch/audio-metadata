# audio-metadata

[![Read the Docs - Stable](https://img.shields.io/readthedocs/audio-metadata/stable.svg?label=stable%20docs)](https://audio-metadata.readthedocs.io/en/stable/)
[![Read the Docs - Latest](https://img.shields.io/readthedocs/audio-metadata/latest.svg?label=latest%20docs)](https://audio-metadata.readthedocs.io/en/latest/)

[audio-metadata](https://github.com/thebigmunch/audio-metadata) is a library for reading and, in the future, writing metadata from audio files.

### Why another audio metadata library? / Why not just use mutagen et al?

Clean and understandable code, nice API, and good UX (user experience) are the focal points of audio-metadata.
One or more of these things I feel are lacking from already existing alternatives
enough to want to write something from scratch with them in mind.
Also, there are certain features not present in other solutions that would be prohibitively painful to add.


### So, why should I use it?

Features and functionality that set it apart:

* Uses the Python standard load(s)/dump(s) API.
	* Can load filepaths, file-like objects and binary data (bytes-like objects).
* Metadata objects look like a dict **and** act like a dict.
	* Some common libraries shadow the representation of a dict
	  and/or dict methods but do not behave like a dict.
	* Supports attribute-style access that can be mixed with dict key-subscription.
* All metadata objects have user-friendly representations.
	* This includes *humanized* representations of certain values
	  like filesize, bitrate, duration, and sample rate.

```
>>> import audio_metadata

>>> metadata = audio_metadata.load('05 - Heart of Hearts.flac')

>>> metadata
<FLAC ({
	'filepath': '05 - Heart of Hearts.flac',
	'filesize': '44.23 MiB',
	'pictures': [],
	'seektable': <FLACSeekTable (37 seekpoints)>,
	'streaminfo': <FLACStreamInfo ({
		'bit_depth': 16,
		'bitrate': '1022 Kbps',
		'channels': 2,
		'duration': '06:03',
		'md5': '3ae700893d099a5d281a5d8db7847671',
		'sample_rate': '44.1 KHz',
	})>,
	'tags': <VorbisComment ({
		'album': ['Myth Takes'],
		'artist': ['!!!'],
		'bpm': ['119'],
		'date': ['2007'],
		'genre': ['Dance Punk'],
		'title': ['Heart of Hearts'],
		'tracknumber': ['05'],
	})>,
})>

>>> metadata['streaminfo']
<FLACStreamInfo ({
	'bit_depth': 16,
	'bitrate': '1022 Kbps',
	'channels': 2,
	'duration': '06:03',
	'md5': '3ae700893d099a5d281a5d8db7847671',
	'sample_rate': '44.1 KHz',
})>

>>> metadata.streaminfo.bitrate
1022134.0362995076

>>> metadata.streaminfo['duration']
362.9066666666667

>>> metadata['streaminfo'].sample_rate
44100
```


## Installation

``pip install audio-metadata``


## Usage

For the release version, see the [stable docs](https://audio-metadata.readthedocs.io/en/stable/).  
For the development version, see the [latest docs](https://audio-metadata.readthedocs.io/en/latest/).

The high-level API and basic usage are covered, but more advanced features/functionality need documentation.


## TODO

Please don't submit issues regarding the following:

* Docs, docs, and more docs.
* Finish ID3 abstractions.
* Add support for more file formats.
	* MP4 reading is already well underway.
* Add write support.

If you're willing to [contribute](https://github.com/thebigmunch/audio-metadata/blob/master/.github/CONTRIBUTING.md)
your time to work on them, post on the **Development** category on the [Discourse forum](https://forum.thebigmunch.me/).


## Appreciation

Showing appreciation is always welcome.

#### Thank

[![Say Thanks](https://img.shields.io/badge/thank-thebigmunch-blue.svg?style=flat-square)](https://saythanks.io/to/thebigmunch)

Get your own thanks inbox at [SayThanks.io](https://saythanks.io/).

#### Contribute

[Contribute](https://github.com/thebigmunch/audio-metadata/blob/master/.github/CONTRIBUTING.md) by submitting bug reports, feature requests, or code.

#### Help Others/Stay Informed

[Discourse forum](https://forum.thebigmunch.me/)

#### Referrals/Donations

[![Coinbase](https://img.shields.io/badge/Coinbase-referral-orange.svg?style=flat-square)](https://www.coinbase.com/join/52502f01e0fdd4d3ef000253) [![Digital Ocean](https://img.shields.io/badge/Digital_Ocean-referral-orange.svg?style=flat-square)](https://m.do.co/c/3823208a0597) [![Namecheap](https://img.shields.io/badge/Namecheap-referral-orange.svg?style=flat-square)](https://www.namecheap.com/?aff=67208) [![PayPal](https://img.shields.io/badge/PayPal-donate-brightgreen.svg?style=flat-square)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=DHDVLSYW8V8N4&lc=US&item_name=thebigmunch&currency_code=USD)

**BTC:** ``1BMLCFPcX8YHE1He2t3aBrsNDGr1pKhfFa``  
**ETH:** ``0x8E3f8d8eAedeA61Bf34A998A2104954FE508D5d0``  
**LTC:** ``LgsQU1YaY4a4s7m9efjn6m35XhVEpW1xoP``
