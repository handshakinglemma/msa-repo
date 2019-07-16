import sys, time
from hbdm_encodeV5 import get_chunk_info
from hbdm_decodeV4 import read_encoded, decode
from chunk_fileV3_1 import chunk

# https://rosettacode.org/wiki/Longest_common_subsequence#Python on 19/07/08

def lcs(a, b):
    # generate matrix of length of longest common subsequence for substrings of both words
    lengths = [[0] * (len(b)+1) for _ in range(len(a)+1)]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if x == y:
                lengths[i+1][j+1] = lengths[i][j] + 1
            else:
                lengths[i+1][j+1] = max(lengths[i+1][j], lengths[i][j+1])

    # read a substring from the matrix
    result = []
    j = len(b)
    for i in range(1, len(a)+1):
        if lengths[i][j] != lengths[i-1][j]:
            result.append(a[i-1])

    return result

def read_file(filename):
    file = open(filename, 'rb')
    content = file.read()
    file.close()
    return str(content)

def write_file(filename, content):
    file = open(filename, 'wb')

    for pair in content:
        #bytePair = pair[0] + pair[1].to_bytes(3, 'big')
        file.write(pair)

    file.close()

def read_chunks(filename):
    file = open(filename, 'rb')
    content = file.readlines()
    file.close()
    print(content)
    return content

def make_list(strx):
    new = []
    for item in strx:
        new.append(item[0])
    return new


def main():
    str1 = read_encoded(sys.argv[1])
    str2 = read_encoded(sys.argv[2])
    #trash1, str1 = chunk(sys.argv[1])
    #rash2, str2 = chunk(sys.argv[2])
    #str1 = make_list(str1)
    #str2 = make_list(str2)
    #print(str1)
    #print()
    #print('***')
    #print()
    #print(str2)
    #print()
    #print('***')
    #print()
    t1 = time.time()
    result = lcs(str1, str2)
    write_file('lcs.data.encoded', result)
    #print(result)
    t2 = time.time()
    print('Time:', t2 - t1)

    '''
    print()
    print('***')
    print()

    new = bytearray()
    for i in str1:
        new += i
    print(new)
    '''

main()
