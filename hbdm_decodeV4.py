import sys
import time

def read_encoded(inputFile):
    data = open(inputFile, 'rb').read()
    chunk_lst = []
    byteIndex = 0
    while byteIndex < len(data):
        chunk_lst.append(data[byteIndex : byteIndex + 23])
        byteIndex += 23
    return chunk_lst

def decode(inputFile, commonFile):
    chunk_lst = read_encoded(inputFile)
    byteIndex = 0
    fileBytes = open(commonFile, 'rb').read()
    chunk_dict = {}
    while byteIndex < len(fileBytes):
        hash = fileBytes[byteIndex : byteIndex + 20]
        byteIndex += 20
        length = fileBytes[byteIndex : byteIndex + 3]
        byteIndex += 3
        chunk = bytearray(b'')
        while len(chunk) < int.from_bytes(length, 'big'):
            chunk.append(fileBytes[byteIndex])
            byteIndex += 1
        chunk_dict[hash + length] = chunk

    return chunk_lst, chunk_dict

def decode_to_file(inputFile, outputFile, commonFile):
    chunk_lst, chunk_dict = decode(inputFile, commonFile)
    file = open(outputFile, 'wb')
    for pair in chunk_lst:
        file.write(chunk_dict[pair])

if __name__ == "__main__":
    start = time.clock()
    decode_to_file(sys.argv[1] + ".encoded", sys.argv[1] + ".decoded", sys.argv[2])
    print("Time to decode:", time.clock() - start)
