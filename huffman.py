from heapq import heappush, heappop, heapify
from collections import defaultdict
import sys, time
from hbdm_encodeV5 import get_chunk_info
from hbdm_decodeV4 import read_encoded, decode
from chunk_fileV3_1 import chunk

# https://rosettacode.org/wiki/Huffman_coding#Python on 19/08/14

def encode(symb2freq):
    """Huffman encode the given dict mapping symbols to weights"""
    heap = [[wt, [sym, ""]] for sym, wt in symb2freq.items()]
    heapify(heap)
    while len(heap) > 1:
        lo = heappop(heap)
        hi = heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p))
 
txt = read_encoded(sys.argv[1])
symb2freq = defaultdict(int)
for ch in txt:
    symb2freq[ch] += 1
# in Python 3.1+:
# symb2freq = collections.Counter(txt)
huff = encode(symb2freq)
print("Symbol\tWeight\tHuffman Code")
for p in huff:
    print("%s\t%s\t%s" % (p[0], symb2freq[p[0]], p[1]))