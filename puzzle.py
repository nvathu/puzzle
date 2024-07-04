import numpy as np
import itertools
import os
import sys

def readMat(path):
	f = open(path, 'rt')
	h, w = [int(x) for x in f.readline().strip().split('\t')]
	assert h > 0 and w > 0
	mat = - np.ones((h, w), dtype=np.int32)
	for ih in range(h):
		iw = 0
		for it in f.readline().strip().split('\t'):
			if it != '.':
				mat[ih][iw] = int(it)
			iw += 1
	f.close()
	return mat

def tim_xung_quanh(toado,mat):
	dx = [-1,0,1]
	dy = [-1,0,1]
	d = []
	for x in dx:
		for y in dy:
			if(toado[0] + x in range(len(mat)) and toado[1] + y in range(len(mat))):
				d.append((toado[0] + x, toado[1] + y))
	return d				
	pass

def tim_theo_toa_do(toado):
	toadofull = tim_xung_quanh(toado,mat)
	result = []
	for toado in toadofull:
		result.append(lvars[toado[0]][toado[1]])
	return result

def chap_tren(toa_do):
	result = []
	x = mat[toa_do[0]][toa_do[1]]
	minus = [-it for it in tim_theo_toa_do(toa_do)]
	for x in itertools.combinations(minus,x+1):
		result.append(x)
	return result
	pass

def chap_duoi(toa_do):
	do_dai_xung_quanh = len(tim_theo_toa_do(toa_do))
	x = mat[toa_do[0]][toa_do[1]]
	temp = []
	result = []
	d = tim_theo_toa_do(toa_do)
	for i in range(do_dai_xung_quanh):
		temp.append(i)
	for count in range(x - 1):
		combinations = []
		for it in itertools.combinations(temp,count+1):
			combinations.append(it)
			for combination in combinations:
				temp1 = [it for it in d]
				for index in combination:
					temp1[index] *= -1
			result.append(temp1)
	return result
	pass

def toCNF():
	
	result = []
	for i,line in enumerate(mat):
		#print(i)
		for j,num in enumerate(line):
			if num != -1:
				d = tim_theo_toa_do((i,j))
				#print(d)
				if num == 0:
					for t in d:
						result.append([t*-1])	
					continue
				result.append(d)
				result += chap_tren((i,j))
				result += chap_duoi((i,j))
	print(result)
	return result	

def fortmatFilledCell(text, cl_code):
	return '\033[1;37;%dm%s\033[1;0;0m'%(cl_code, text)

if __name__ == '__main__':
	infile = sys.argv[1]
	outfile = sys.argv[2]
	mat = readMat(infile)
	print(mat)
	num = mat.shape[0]*mat.shape[1]
	lvars = np.arange(1, num+1, 1).reshape(mat.shape)
	clauses = toCNF()
	
	with open('inSAT.txt', 'wt') as f:
		f.write('p cnf %d %d\n'%(num, len(clauses)))
		for it in clauses:
			for i in it:
				f.write('%d '%(i))
			f.write('0\n')

	open('outSAT.txt', 'wt')

	print('\nPlease follow these steps to continue:')
	print('1. Go to https://jgalenson.github.io/research.js/demos/minisat.html')	
	print('2. Paste the content of "inSAT.txt" to [Input] in the webpage')
	print('3. Copy the content of [Output] in the webpage and paste into "outSAT.txt"')
	print('4. Enter [y]')
	if input('Continue? (y/n)') != 'y':
		exit()

	res = []
	with open('outSAT.txt') as f:
		f.readline()
		tmp = f.readline().strip().split(' ')
		if tmp[0] != 'SAT':
			print ('UNSAT')
			exit()
		for it in tmp[1:]:
			res.append(int(it))

	#print res
	vis_str = ''
	with open(outfile, 'wt') as g:
		for ih in range(mat.shape[0]):
			for iw in range(mat.shape[1]):
				txt = ''
				if mat[ih][iw] >= 0:
					g.write('%d'%(mat[ih][iw]))
					txt += '%-2d'%(mat[ih, iw])
				else:
					g.write(' ')
					txt += '  '

				if lvars[ih][iw] in res:
					g.write('.')
					vis_str += fortmatFilledCell(txt, 42)
				else:
					g.write(' ')
					vis_str += fortmatFilledCell(txt, 41)
			g.write('\n')
			vis_str += '\n'

	print ('\n=======INPUT=======')

	for i in range(mat.shape[0]):
		for j in range(mat.shape[1]):
			if mat[i][j] < 0:
				print ('_', end='')
			else:
				print (mat[i][j], end='')
		print ('')
	print ('===================')
	print ('\n=======ANSWER=======')
	print (vis_str,'=====================')
	#os.system('cat %s'%(outfile))
	print('The answer is saved in ' + outfile)