from chunk_fileV3_1 import chunk
import sys
import os
import time

def get_chunk_info(commonFile): #function to read the chunks out of the file
    byteIndex = 0
    fileBytes = open(commonFile, 'rb').read()
    chunk_dict = {}
    counter = 0
    while byteIndex < len(fileBytes):
        hash = fileBytes[byteIndex : byteIndex + 20]
        byteIndex += 20
        length = fileBytes[byteIndex : byteIndex + 3] 
        byteIndex += 3
        chunk = bytearray(b'')
        while len(chunk) < int.from_bytes(length, 'big'):
            chunk.append(fileBytes[byteIndex])
            byteIndex += 1
        pair = hash + length
        chunk_dict[pair] = chunk
        counter += 1
    if counter > 2 ** 24:
        raise("TOO MANY CHUNKS CANNOT REPRESENT IN 3 BYTES")
    return chunk_dict

def encode(inputFile, outputFile, commonFile, windowSize=3, polynomial=283): #commonFile is the file where the chunks are store
    # common_chunk_dict, common_chunk_nums = get_chunk_info(commonFile)
    common_chunk_dict = get_chunk_info(commonFile) #runs get_chunk_info to get a dictionary of chunks and hashes, common_chunk_dict[hash] = chunk
    org_chunk_dict, org_chunk_lst = chunk(inputFile, windowSize, polynomial) #converts input file into chunks. org_chunk_dict contains unique chunks, addressed as their hashes
    #org_chunk_lst contains the order of the chunks
    encodedFile = open(outputFile, 'wb')
    all_chunks_file = open(commonFile, 'ab')
    counter = len(common_chunk_dict)

    for pair in org_chunk_lst:
        bytePair = pair[0] + pair[1].to_bytes(3, 'big')
        encodedFile.write(bytePair) #write to the output file. what is written is exactly the same as org_chunk_lst
        if bytePair not in common_chunk_dict: #if there is a new chunk, save it
            all_chunks_file.write(bytePair + org_chunk_dict[pair])
            common_chunk_dict[bytePair] = org_chunk_dict[pair]
            counter += 1
    if counter > 2 ** 24:
        raise("TOO MANY CHUNKS CANNOT REPRESENT IN 3 BYTES")

if __name__ == "__main__":
    if len(sys.argv) > 4:
        maskSize = int(sys.argv[4])
    else:
        maskSize = 6
    input = sys.argv[1]
    if os.path.isdir(input):
        for fileName in os.listdir(input):
            print(fileName)
            if "encoded" not in fileName and "decoded" not in fileName and "desktop.ini" not in fileName:
                encode(os.getcwd() + "/" + input + "/" + fileName, os.getcwd() + "/" + input + "/" + fileName +  ".encoded", sys.argv[2], maskSize)
    else:
        encode(input, input + ".encoded", sys.argv[2])