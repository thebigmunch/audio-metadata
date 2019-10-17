# API Reference

```{eval-rst}
.. currentmodule:: audio_metadata
```

The main methods of interacting with audio metadata are :func:`load` and :func:`loads`.


## Core

```{eval-rst}
.. autofunction:: determine_format
.. autofunction:: load
.. autofunction:: loads
```


## Exceptions

```{eval-rst}
.. autoexception:: AudioMetadataException
.. autoexception:: FormatError
.. autoexception:: TagError
.. autoexception:: UnsupportedFormat
```

## Base Classes

```{eval-rst}
.. autoclass:: Format

.. autoclass:: Picture
.. autoclass:: StreamInfo
.. autoclass:: Tags
```


## FLAC

```{eval-rst}
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
```


## ID3v1

```{eval-rst}
.. autoclass:: ID3v1

.. autoclass:: ID3v1Fields
```


## ID3v2

```{eval-rst}
.. autoclass:: ID3v2

.. autoclass:: ID3v2Flags
.. autoclass:: ID3v2Frames
.. autoclass:: ID3v2Header
```


## MP3

```{eval-rst}
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
```


MP4
---

.. autoclass:: MP4

.. autoclass:: MP4Atom
.. autoclass:: MP4Atoms
.. autoclass:: MP4StreamInfo
.. autoclass:: MP4Tags



## Ogg

Ogg
---

```{eval-rst}
.. autoclass:: Ogg

.. autoclass:: OggPage
.. autoclass:: OggPageHeader
.. autoclass:: OggPageSegments
```


## Ogg Opus

```{eval-rst}
.. autoclass:: OggOpus

.. autoclass:: OggOpusStreamInfo
.. autoclass:: OggOpusVorbisComments
```


## Ogg Vorbis

```{eval-rst}
.. autoclass:: OggVorbis

.. autoclass:: OggVorbisStreamInfo
.. autoclass:: OggVorbisComments
```


## Vorbis

```{eval-rst}
.. autoclass:: VorbisComment
.. autoclass:: VorbisComments
```


## WAV

```{eval-rst}
.. autoclass:: WAVE

.. autoclass:: RIFFTag
.. autoclass:: RIFFTags
.. autoclass:: WAVEStreamInfo
.. autoclass:: WAVESubchunk
```
