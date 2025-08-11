# PCFX_SubcodeQ_Study
A Study of Subcode Q sub-indexes used on PC-FX games

## What is this about ?

This is a review of the various PC-FX games to determine whether they used subcode
"indexes" in any way, and whether that might be required for a potential Optical Disc
Emulation system in the future.

## Methodology

Each disc was re-extracted, using "CD Manipulator"
[https://github.com/Elrinth/CD-Manipulator](https://github.com/Elrinth/CD-Manipulator),
to extract its subcode information, which then underwent review. CD Manipulator
extracts the subcode in the same format as "CloneCD", where each sector takes up
96 (0x60) bytes, with subcode-P occupying the first 12 bytes, subcode-Q occupying
the next 12 bytes, and so on.

Subcode Q information primarily contains information about the disc position (both
absolute and track-relative) at any given time, but also may contain information
such as UPC/media code, and ISRC track information.

There is more comprehensive data at this website, including descriptions of different
control and data (ADR) types, data structures, and how to calculate checksum/CRC fields:
[https://problemkaputt.de/psxspx-cdrom-subchannels.htm](https://problemkaputt.de/psxspx-cdrom-subchannels.htm)

I wrote a python program, [decodeQ.py](source/decodeQ.py), to review the extracted
subcode data, and watch for track and index changes, in order to create short reports
for each disc.

I have also compiled and placed all of the reports in the [extracts](extracts)
folder for review.


## Conclusions

1. There were many individual timing marks which appeared absurd, such as consecutive
sectors moving from track 01 to track 11 and back to track 01. So it seems that the
subcode data can easily be mis-read, and the CRC information is important in order
to determine which information is good or bad.

2. The media (or track) information which may appear from time to time takes up one
sector of subcode-Q informaiton, in the same way that a time marker might; this means
that there may not be a time marker for every single sector, so for continuity, a
replacement system should at least remember the last-known time signature in order to
repeat it (or build a pseudo-marker calculated from it).

3. Only one PC-FX game contained an "INDEX 02" (or any index number greater than 01)
*on an audio track*.  This was Pachio-kun, and the index was only a few seconds prior
to the end of the track, so it may have been an alternate way to set a pregap.

4. Many PC-FX games conatined multiple indexes *on data tracks*. They don't appear
to have the same impact, meaning, or usage when encountered on data tracks as compared
to audio tracks, so it is not clear why they are there. It is possible that they are
an artifact of the mastering process - when compiling a single data track which
contains multiple sections of code (overlays, data, etc.), the mastering program may
have assigned each unit an index number for some reason, possibly debugging.
