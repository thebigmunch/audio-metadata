audio-metadata
==============

audio-metadata is a library for reading and, in the future, writing audio metadata.


Getting Started
===============

Install audio-metadata with `pip <https://pip.pypa.io/en/stable/>`_.

.. code-block:: console

	$ pip install -U audio-metadata


Overview
========

The goals of audio-metadata are to provide a nice API and good UX while keeping the codebase as clean and simple as possible.

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


.. code-block:: python

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

See the full :doc:`api`.

.. toctree::
	:hidden:

	api
