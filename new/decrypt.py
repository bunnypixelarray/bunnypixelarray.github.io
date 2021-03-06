#!/usr/bin/python3

from sys import argv
from os import walk
from os.path import splitext, join
from os import remove as rm
from struct import unpack, calcsize
from Crypto.Cipher import AES

LEN_READ = 1024
FILE_EXT = '.enc'


def crypted_file(filename):
    global FILE_EXT
    return (True if filename.endswith(FILE_EXT) else False)


def decrypt(key, filename):
    global LEN_READ, FILE_EXT
    newname = splitext(filename)[0]
    with open(newname, "wb") as f_out:
        with open(filename, "rb") as f_in:
            size = unpack('Q', f_in.read(calcsize('Q')))[0]
            iv = f_in.read(16)
            cryptor = AES.new(key, AES.MODE_CBC, iv)
            while True:
                txt = f_in.read(LEN_READ)
                if not len(txt):
                    break
                f_out.write(cryptor.decrypt(txt))
                del txt
            f_out.truncate(size)


key = bytes("e8bb1e9227109ed5", "utf-8")
if len(key) != 16:
    print("Key failure")
    exit(0)

for dirpath, dirnames, filenames in walk(argv[1]):
    for fn in filenames:
        name = join(dirpath, fn)
        if crypted_file(name):
            try:
                decrypt(key, name)
                rm(name)
            except:
                print("Decrypt failure : {}".format(name))
