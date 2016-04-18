#!/usr/bin/python3

from Crypto.PublicKey import RSA

key = RSA.generate(2048)

f = open("pubkey", "wb")
f.write(key.publickey().exportKey())
f.close()

f = open("privkey", "wb")
f.write(key.exportKey())
f.close()
