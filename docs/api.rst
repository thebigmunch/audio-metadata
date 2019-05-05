.. _api:

API Reference
=============

.. currentmodule:: audio_metadata

The main methods of interacting with audio metadata are :func:`load` and :func:`loads`.


Core
----

.. autoapifunction:: determine_format
.. autoapifunction:: load
.. autoapifunction:: loads


Exceptions
----------

.. autoapiexception:: AudioMetadataException
.. autoapiexception:: InvalidFrame
.. autoapiexception:: InvalidHeader
.. autoapiexception:: UnsupportedFormat


Base Classes
------------

.. autoapiclass:: Format

.. autoapiclass:: Picture
.. autoapiclass:: Tags


FLAC
----

.. autoapiclass:: FLAC

.. autoapiclass:: FLACMetadataBlock
.. autoapiclass:: FLACApplication
.. autoapiclass:: FLACCueSheet
.. autoapiclass:: FLACCueSheetTrack
.. autoapiclass:: FLACCueSheetIndex
.. autoapiclass:: FLACPadding
.. autoapiclass:: FLACSeekPoint
.. autoapiclass:: FLACSeekTable
.. autoapiclass:: FLACStreamInfo



ID3v2
-----

.. autoapiclass:: ID3v2


MP3
---

.. autoapiclass:: MP3


Vorbis
------

.. autoapiclass:: VorbisComment
.. autoapiclass:: VorbisPicture


WAV
---

.. autoapiclass:: WAV
.. autoapiclass:: WAVStreamInfo
