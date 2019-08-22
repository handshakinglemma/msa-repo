import sys, time
from hbdm_encodeV5 import get_chunk_info
from hbdm_decodeV4 import read_encoded, decode
from chunk_fileV3_1 import chunk

# https://rosettacode.org/wiki/Longest_Common_Substring#Python on 19/08/15

def lcs_str(f1, f2):
	s1 = read_encoded(f1)
	s2 = read_encoded(f2)
	len1, len2 = len(s1), len(s2)
	ir, jr = 0, 0
	for i1 in range(len1):
	    i2 = s2.find(s1[i1])
	    while i2 >= 0:
	        j1, j2 = i1+1, i2+1
	        while j1 < len1 and j2 < len2 and s2[j2] == s1[j1]:
	            if j1-i1 > jr-ir:
	                ir, jr = i1, j1
	            j1 += 1; j2 += 1
	        i2 = s2.find(s1[i1], i2+1)
	print (s1[ir:jr+1])

def lcs(f1, f2):
	s1 = read_encoded(f1)
	s2 = read_encoded(f2)
	len1, len2 = len(s1), len(s2)
	ir, jr = 0, 0
	for i1 in range(len1):
		if s1[i1] in s2:
			i2 = s2.index(s1[i1])
			#i2 = s2.find(s1[i1])
			while i2 >= 0:
				j1, j2 = i1+1, i2+1
				while j1 < len1 and j2 < len2 and s2[j2] == s1[j1]:
					if j1-i1 > jr-ir:
						ir, jr = i1, j1
					j1 += 1; j2 += 1
				try:
					i2 = s2.index(s1[i1], i2+1)
				finally:
					break
	result = s1[ir:jr+1]
	write_file('lcsstr.data.encoded', result)

def write_file(filename, content):
    file = open(filename, 'wb')

    for pair in content:
        file.write(pair)

    file.close()


def main():
	lcs(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()