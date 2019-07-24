import os, sys, time
from lcsseq import lcs
from itertools import combinations
from random import choice

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

def pick(flist):
	file = choice(flist)
	flist.remove(file)
	return file

def inital(flist):

	with open(db, 'r') as sequences_file:
		sequences = sequences_file.readlines()

	if len(flist) <= 1:
		
	elif len(flist) == 2:
		result = compare(flist[0], flist[1])
		with open('SequenceDB', 'a') as seqfile:
			seqfile.write(result + '\n')
		return
	elif len(flist) % 3 == 0:
		file_groups = []
		group = []
		for index, file in enumerate(flist, 1):
			group.append(file)
			if index % 3 == 0:
				file_groups.append(group)
				group = []
		print(file_groups)
	elif len(flist) % 2 == 0:
		file_groups = []
		group = []
		for index, file in enumerate(flist, 1):
			group.append(file)
			if index % 2 == 0:
				file_groups.append(group)
				group = []
		print(file_groups)

		#result = compare(compare(flist[0], flist[1]), flist[2])


	pass

def add():
	pass


def main():
	t1 = time.time()

	# If there is one new file, seq and add it.
	# If there is a directory of unsequenced files, seq them all.

	files = get_files()
	done_files = []

	file1 = pick(files)
	file2 = pick(files)
	print(file1, file2, files)
	
	t2 = time.time()
	#with open('timelog.txt', 'a') as timelog:
	#	timelog.write('\nTotal time: ' + str(t2 - t1) + '\n' + ('-' * 71) + '\n')

if __name__ == '__main__':
	main()
