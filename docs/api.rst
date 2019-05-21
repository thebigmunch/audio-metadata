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
.. autoexception:: InvalidFrame
.. autoexception:: InvalidHeader
.. autoexception:: UnsupportedFormat


Base Classes
------------

.. autoclass:: Format

.. autoclass:: Picture
.. autoclass:: Tags


FLAC
----

.. autoclass:: FLAC

.. autoclass:: FLACMetadataBlock
.. autoclass:: FLACApplication
.. autoclass:: FLACCueSheet
.. autoclass:: FLACCueSheetTrack
.. autoclass:: FLACCueSheetIndex
.. autoclass:: FLACPadding
.. autoclass:: FLACSeekPoint
.. autoclass:: FLACSeekTable
.. autoclass:: FLACStreamInfo



ID3v2
-----

.. autoclass:: ID3v2


MP3
---

.. autoclass:: MP3


Vorbis
------

.. autoclass:: VorbisComments
.. autoclass:: VorbisPicture


WAV
---

.. autoclass:: WAV
.. autoclass:: WAVStreamInfo
