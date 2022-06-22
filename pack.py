#!/usr/bin/env python3

from datetime import datetime
date = datetime.now()


def rc4(data):
    K = [0x7C,0x4E,0x03,0x04,0x55,0x05,0x09,0x07,0x2D,0x2C,0x7B,0x38,0x17,0x0D,0x17,0x11]
    C = []

    S = [i for i in range(256)]
    l = len(K)
    j = 0
    for i in range(256):
        j = (j + S[i] + K[i % l]) % 256
        S[i], S[j] = S[j], S[i]

    i = 0
    j = 0
    for b in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        C.append(b ^ S[(S[i] + S[j]) % 256])
    return bytearray(C)


def crc32(data):
    crc = 0
    for b in data:
        crc = crc ^ (b << 24)
        for i in range(8):
            if crc & 0x80000000:
                crc = (crc << 1) ^ 0x04c10db7
            else:
                crc = crc << 1
            crc = crc & 0xffffffff
    return crc


data = bytearray()
with open('app.bin', 'rb') as f:
    data.extend(rc4(f.read(65536)))
    data.extend(f.read())

BYTE = 1
HWORD = 2
WORD = 4

hdr = {
    'signature': (WORD, 0x544f4f42),    # 'BOOT'
    'size': (HWORD, 32),
    'version': (HWORD, 0x0100),         # 1.0
    'reserved': (WORD, 0),
    'magic': (HWORD, 0x0103),
    'year': (HWORD, date.year),
    'month': (BYTE, date.month),
    'day': (BYTE, date.day),
    'hour': (BYTE, date.hour),
    'minute': (BYTE, date.minute),
    'second': (BYTE, date.second),
    'model': (WORD, 0x33333038),
    'file_descriptor_type': (BYTE, 1),
    'file_descriptor_offset': (WORD, 32),
    'file_descriptor_length': (BYTE, 57),
    'padding': (1, 0),

    # file descriptor
    'descriptor_length': (BYTE, 57),
    'file_type': (WORD, 1),
    'file_name': (40, 0x007000700061),  # 'app' (UCS2 string)
    'file_offset': (WORD, 89),
    'file_size': (WORD, len(data)),
    'unknown': (WORD, 0)
}

out = bytearray()
for key in hdr.keys():
    out.extend(hdr[key][1].to_bytes(hdr[key][0], 'little'))
out.extend(data)
out.extend(crc32(out).to_bytes(WORD, 'little'))

with open('loader.bin', 'wb') as f:
    f.write(out)
