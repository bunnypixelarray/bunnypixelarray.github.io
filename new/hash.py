#!/usr/bin/python3

import random
import string
import hashlib


# base = ''.join(random.SystemRandom().choice(
#     string.ascii_uppercase + string.digits) for _ in range(32))

base = "8205H5VMEJUFC5ISGO1IOV04XMNZF8O4"

cuted = ''

for i in [0, 22, 3, 12, 14, 15, 16, 22, 2, 8, 26, 11, 13, 24, 4, 3]:
    cuted += base[i]

hashed = hashlib.sha224(bytes(cuted, "utf-8")).hexdigest()

recuted = ''

for i in [4, 12, 25, 15, 22, 37, 36, 16, 12, 28, 17, 30,
          2, 49, 20, 1, 17, 8, 3, 9, 0, 12, 37, 14, 43,
          13, 45, 44, 31, 52]:
    recuted += hashed[i]

rehashed = hashlib.sha512(bytes(cuted, "utf-8")).hexdigest()

final_key = ''

for i in [8, 2, 15, 37, 31, 8, 12, 45, 23, 41, 3, 18, 12, 47, 43, 10]:
    final_key += rehashed[i]

print (final_key)