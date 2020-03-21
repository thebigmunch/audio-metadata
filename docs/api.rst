.. _api:

API Reference
=============

.. currentmodule:: audio_metadata

The main methods of interacting with audio metadata are :func:`load` and :func:`loads`.


Core
----

.. autofunction:: determine_format
.. autofunction:: load
.. autofunction:: loads


Exceptions
----------

.. autoexception:: AudioMetadataException
.. autoexception:: FormatError
.. autoexception:: TagError
.. autoexception:: UnsupportedFormat


Base Classes
------------

.. autoclass:: Format

.. autoclass:: Picture
.. autoclass:: StreamInfo
.. autoclass:: Tags


FLAC
----

.. autoclass:: FLAC

.. autoclass:: FLACApplication
.. autoclass:: FLACCueSheet
.. autoclass:: FLACCueSheetIndex
.. autoclass:: FLACCueSheetTrack
.. autoclass:: FLACMetadataBlock
.. autoclass:: FLACPadding
.. autoclass:: FLACPicture
.. autoclass:: FLACSeekPoint
.. autoclass:: FLACSeekTable
.. autoclass:: FLACStreamInfo
.. autoclass:: FLACVorbisComments


ID3v1
-----

.. autoclass:: ID3v1

.. autoclass:: ID3v1Fields


ID3v2
-----

.. autoclass:: ID3v2

.. autoclass:: ID3v2Flags
.. autoclass:: ID3v2Frames
.. autoclass:: ID3v2Header


MP3
---

.. autoclass:: MP3

.. autoclass:: LAMEEncodingFlags
.. autoclass:: LAMEHeader
.. autoclass:: LAMEReplayGain
.. autoclass:: MP3StreamInfo
.. autoclass:: MPEGFrameHeader
.. autoclass:: VBRIHeader
.. autoclass:: VBRIToC
.. autoclass:: XingHeader
.. autoclass:: XingToC


Ogg
---

.. autoclass:: Ogg

.. autoclass:: OggPage
.. autoclass:: OggPageHeader
.. autoclass:: OggPageSegments


Ogg Opus
--------

.. autoclass:: OggOpus

.. autoclass:: OggOpusStreamInfo
.. autoclass:: OggOpusVorbisComments


Ogg Opus
--------

.. autoclass:: OggVorbis

.. autoclass:: OggVorbisStreamInfo
.. autoclass:: OggVorbisComments


Vorbis
------

.. autoclass:: VorbisComment
.. autoclass:: VorbisComments


WAV
---

.. autoclass:: WAV

.. autoclass:: RIFFTags
.. autoclass:: WAVStreamInfo
