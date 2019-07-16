from rabin_fingerprint import byteWindowFingerprinter3, irreducible_polynomial, print_bits
import sys
import hashlib
#from testing import hist_bins
#import matplotlib.pyplot as plt
import time

#If you don't case about the different parameters just supply the name of the file you want chunked to fileName
#Returns chunk_dict, chunk_lst
#chunk_dict is a dictionary with the keys being the chunk hash and the values being the chunk's content
#chunk_lst is a list of the chunk hashes of the file in order. This is what is written to the encoded file
#Note that this function considers chunk hashes to be tuples of a byte ojects and integers in the form (hash, length)
#where hash is a byte object and length is an int. Other programs such as hbdm_encode and decode considers hashes to just
#be byte objects where the first 20 bytes is the hash and the last 3 are the length.
def chunk(fileName = None, windowSize = 3, polynomial = 283, data = None):
    cutValue = 0
    fingerprinter = byteWindowFingerprinter3(polynomial, windowSize)
    if fileName != None:
        data = open(fileName, 'rb').read()
    chunk_dict = {} #contains each unqiue chunk, adressed as its hash
    chunk_lst = [] #contains the hashes, which refer the the chunks in chunk_dict
                   #outputted to encoded file
    length = 0
    hasher = hashlib.sha1()
    chunk = bytearray()
    for byte in data:
        length += 1
        fingerprint = fingerprinter.update(byte)
        hasher.update(byte.to_bytes(1, 'big'))
        chunk.append(byte)
        if fingerprint == cutValue:
            hash = hasher.digest()
            pair = (hash, length)
            chunk_lst.append(pair)
            if pair not in chunk_dict: #if the chunk has not been encountered before, it saves it
                chunk_dict[pair] = chunk
            elif chunk_dict[pair] != chunk:
                raise("ERROR NON MATCHING CHUNK")
                print(pair)
                print(chunk_dict[pair])
                print(chunk)
            hasher = hashlib.sha1()
            length = 0
            chunk = bytearray()

    hash = hasher.digest()
    pair = (hash, length)
    chunk_lst.append(pair)
    if pair not in chunk_dict:
        chunk_dict[pair] = chunk
    elif chunk_dict[pair] != chunk:
        raise("ERROR NON MATCHING CHUNK")
        print(pair)
        print(chunk_dict[pair])
        print(chunk)

    return chunk_dict, chunk_lst
