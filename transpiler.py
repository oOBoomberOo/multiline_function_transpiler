import sys
import os
import json
from pathlib import Path

def check_path(path):
	dir = Path(*[x for x in path.replace('\\', '/').split('/') if len(x.split('.')) == 1])
	if not os.path.exists(dir):
		os.makedirs(dir)
	return path

def create_file(path):
	return open(check_path(path), 'w')

def transpiler(inf, outf):
	f = open(inf).read()
	f = f.replace('\t', ' ').replace('\n', ' ')
	lines = []
	buffer = ''
	pre_c = ''
	quote = False
	for c in f:
		break_point = False
		buffer = buffer + c
		if c == '\\':
			break_point = True
		if not break_point and not quote:
			if c == '"' or c == '\'':
				quote = True
			if pre_c == c and c == ' ':
				buffer = buffer[:-1]
			if c is ';':
				lines.append(buffer[:-1])
				buffer = ''
			if pre_c == ';' and c == ' ':
				buffer = ''
		if not break_point and quote:
			if c == '"' or c == '\'':
				quote = False
		pre_c = c
	lines.append(buffer)
	with create_file(outf) as f:
		f.write('\n'.join(lines))

def main(directory, output):
	convert_files = [
		Path(x) / i for (x, y, z) in os.walk(directory)
			for i in z
			if i.endswith(('.mlfunction', '.mlfn', '.mcfunction'))
	]
	for p in convert_files:
		path = str(p).replace(directory, output).replace('.mlfunction', '.mcfunction').replace('.mlfn', '.mcfunction')
		transpiler(str(p), path)
if len(sys.argv) == 3:
	main(sys.argv[1], sys.argv[2])
else:
	print('Incorrect argument, python transpiler.py <input directory> <output directory>')