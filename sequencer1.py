import os, sys, time
from lcsseq import lcs
from itertools import combinations

def get_files():
	path = sys.argv[1]
	files = os.listdir(path)
	encoded_files = []
	for file in files:
		if '.encoded' in file:
			encoded_files.append(path + '/' + file)
	return encoded_files

def compare(f1, f2):
	return lcs(f1, f2)


def main():
	t1 = time.time()
	files = get_files()
	file_pairs = combinations(files, 2)
	for pair in file_pairs:
		result = compare(pair[0], pair[1])
	t2 = time.time()
	with open('timelog.txt', 'a') as timelog:
		timelog.write('\nTotal time: ' + str(t2 - t1) + '\n' + ('-' * 71) + '\n')

if __name__ == '__main__':
	main()
