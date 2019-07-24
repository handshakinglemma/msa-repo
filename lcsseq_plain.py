import sys, time
from hbdm_encodeV5 import get_chunk_info
from hbdm_decodeV4 import read_encoded, decode
from chunk_fileV3_1 import chunk

# https://rosettacode.org/wiki/Longest_common_subsequence#Python on 19/07/08

# TODO: Should probably break this up into two functions: the LCS function
# and a wrapper function to call in other programs.
def lcs(file1, file2):

    a = read_encoded(file1)
    b = read_encoded(file2)

    # generate matrix of length of longest common subsequence for substrings of both words
    t1 = time.time()
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

    write_file('lcs.data.encoded', result)

    t2 = time.time()
    log_time(file1, file2, t2 - t1)

    return result

def read_file(filename):
    file = open(filename, 'rb')
    content = file.read()
    file.close()
    return str(content)

def write_file(filename, content):
    file = open(filename, 'ab')

    for pair in content:
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

def log_time(file1, file2, time):
    with open('timelog.txt', 'a') as timelog:
        timelog.write(file1 + ' ' + file2 + ': ' + str(time) + '\n')

def main():
    lcs(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()
