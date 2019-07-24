import os, sys, time
from lcsseq import lcs
from itertools import combinations
from random import choice

def get_files():
	path = sys.argv[1]
	if os.path.isdir(path):
		files = os.listdir(path)
	elif os.path.isfile(path):
		files = [path]
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

def enseq(flist):
	if len(flist) <= 1:
		return
	else:
		file1 = pick(flist)
		file2 = pick(flist)
		compare(file1, file2)
		enseq(flsit)
		return

def inital(flist):

	with open(db, 'r') as sequences_file:
		sequences = sequences_file.readlines()

	if len(flist) <= 1:
		return
		
	else:
		file1 = pick(flist)
		file2 = pick(flist)
		compare(file1, file2)
		initial(flsit)
		return

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
