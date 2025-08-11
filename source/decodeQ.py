#(c) 2024  David Shadoff
import os
import sys

# Notes:
#
# This program will write the PC-FX's external Backup memory card (FX-BMP) from a 128KB file
#
#   Usage: putbmp <input_file> [COM port]
#
#   Example:
#     python putbmp.py pcfxbmp.bin COM3
#

if (len(sys.argv) != 2):
    print("Usage: decodeQ <subcode_file>")
    exit()

file_stat = os.stat(sys.argv[1])
#file_stat = os.stat('IMAGE.sub')
filesize = file_stat.st_size
num_sectors = filesize / 96

f = open(sys.argv[1], 'rb') 
#f = open('IMAGE.sub', 'rb') 

print("number of sectors =", int(num_sectors))
print(" ")

sector = 0
track = 0
index = 0
rejects = 0
adr2 = 0
adr3 = 0
adr_other = 0

while (sector < num_sectors):
    memory = f.read(96) 
    subq = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for i in range(12):
        subq[i] = memory [i+12]

    lsb=0               #-initial value (zero for both CD-TEXT and Sub-Q)
    msb=0
    for i in range(10):      #-len (10h for CD-TEXT, 0Ah for Sub-Q)
        x = subq[i] ^ (msb & 0xff)
        x = x ^ ((x >> 4) & 0xff)
        msb = lsb ^ ((x >> 3) & 0xff) ^ ((x << 4) & 0xff)
        lsb = x ^ ((x << 5) & 0xff)
    msb = msb ^ 0xff
    lsb = lsb ^ 0xff

    if ((msb != subq[10]) or (lsb != subq[11])):
#        print("sector {0:d} CRC failure msb = {1:02X} lsb = {2:02X}, subq[10] = {3:02X}, subq[11] = {4:02X}".format(sector, msb, lsb, subq[10], subq[11]))
        sector = sector + 1
        rejects = rejects + 1
        continue

    adr = subq[0] & 0x0f
    if (subq[0] & 0x40 == 0):
        trk_type = "AUDIO"
    else:
        trk_type = "DATA "

    ctrl_other = subq[0] & 0xb0

    if adr == 1:
        track_temp = ((subq[1] & 0xF0)>>4) * 10 + (subq[1] & 0x0F)
        index_temp = ((subq[2] & 0xF0)>>4) * 10 + (subq[2] & 0x0F)
        if ((track != track_temp) | (index != index_temp)):
            track = track_temp
            track_str = "{0:2d}".format(track)
            index = index_temp
            message = "       "
            if ((track == 1) and (index == 0)):
                message = "Leadin "
            if (subq[1] == 0xAA):
                message = "Leadout"
                track_str = "**"

            print("{0:5s} Track {1:2s} Index {2:2d}  Start = {3:02X}:{4:02X}:{5:02X}   {6:02X}:{7:02X}:{8:02X}   {9:7s}   Sector {10:d}".format(trk_type, track_str, index, subq[3], subq[4], subq[5], subq[7], subq[8], subq[9], message, sector))

    if adr == 2:
        adr2 = adr2 + 1

    if adr == 3:
        adr3 = adr3 + 1

    if ((adr != 1) and (adr != 2) and (adr !=3)):
        adr_other = adr_other + 1

    sector = sector + 1

f.close()

print(" ")
if (rejects > 0):
    print("Rejected SUBQ records due to bad CRC = {0:7d}".format(rejects))

if (adr2 > 0):
    print("ADR type 2  (catalog number)         = {0:7d}".format(adr2))

if (adr3 > 0):
    print("ADR type 3  (track ISRC number)      = {0:7d}".format(adr3))

if (adr_other > 0):
    print("Other ADR records                    = {0:7d}".format(adr_other))
