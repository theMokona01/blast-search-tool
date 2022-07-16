#!/usr/local/bin/python3
import cgi, json 
import os 
import jinja2
import re
from biocode import utils
import subprocess
print('Content-Type: application/json\n\n')

def start_processes(DNA, trainingSeq):
	processes = ['echo "{}" > query.fa'.format(DNA), 'blastn -query query.fa -db nt -remote -out blast.txt' ]
	for p in processes:
		subprocess.run(p, shell=True)

def read_file(file_name):
	temp_file = open(str(file_name), 'r')
	temp_file = temp_file.readLines()
	return temp_file

class initialize_program():

	form = cgi.FieldStorage()
	DNA = form.getvalue('DNA') 
	trainingSeq = form.getvalue('trainingSeq')

	start_processes(DNA, trainingSeq)

	blast = open('blast.txt', 'r') 
	blast = blast.readlines()
	
	allLengths = []
	seqLength = ''
	numBlastAlignments = 0 
	blastACC = []
	blastScore = []
	blastEVal = []
	blastStrand = []
	blastPerIdn = []

	results = { 'seqLength':0, 'numBlastAlignments':0, 'blastResults':list()}
	
	for i in blast:
		if i.startswith('Length'):
			x = i.split('=')
			x = filter(str.isdigit, x[1])
			x = ''.join(x)
			allLengths.append(x)
	seqLength = allLengths[0]
	results['seqLength'] = seqLength
	for i in blast:
		if i.startswith('>'):
			results[ 'numBlastAlignments'] += 1
			i = i.strip()
			blastACC.append(i) 
		if i.startswith(' Score ='):
			i = i.strip()
			x = i.split(' ')
			blastScore.append(x[2]) 
			blastEVal.append(x[-1])
		if i.startswith(' Identities ='):
			i = i.strip()
			x = i.split(' ')
			blastPerIdn.append(x[3])
		if i.startswith(' Strand='):
			i = i.strip()
			x = i.split('=')
			blastStrand.append(x[1])
	for i in range(0, results['numBlastAlignments']):
		results['blastResults'].append({'blastID':blastACC[i], 'blastScore':blastScore[i], 'blastEVal':blastEVal[i], 'blastStrand':blastStrand[i], 'blastPerIdn':blastPerIdn[i], 'blastLength':allLengths[i]}) 
	print(json.dumps(results))

if __name__ == '__main__':
        initialize_program()
