# -*- coding: utf-8 -*-
import json, re, os, datetime
# from tqdm import tqdm_notebook as tqdm
# from tqdm import tqdm
from os.path import isfile
from os import listdir

class ipc_regularize(object):

	def ipc45_process(self, ipc_p):
	    string2 = ipc_p.split('/')
	    level4 = string2[0]
	    level5 = string2[1]
	        
	    # process Level 4
	    level4 = level4.lstrip('0')
	    
	    # process Level 5    
	    level5 = level5.lstrip('0')
	    
	    if(len(level5) == 1 or len(level5) == 3):
	        level5 = '0' + level5
	    if(level5 == ''):
	        level5 = '00'
	        
	    return level4 + ' ' + level5

	def ipc_format(self, ipc):
	    if ' ' in ipc:
	        string1 = ipc.split(' ')
	        result = self.ipc45_process(string1[1])           
	        return string1[0] + ' ' + result
	    
	    else:
	        string1 = ipc[0:4]
	        result = self.ipc45_process(ipc[4:])
	        return string1 + ' ' + result
	        
	def ipc_check(self, ipc):
	    if '.' not in ipc:
	        ipc_regex = r'^[A-H][0-9]{2}[A-Z][\s]{0,1}[0-9]{1,3}/[0-9]{1,4}$'    
	        return bool(re.match(ipc_regex, ipc))
	    else:
	        return False

if __name__ == '__main__':
	input_path = "test4.json"
	output_path = "ipc_description2.json"
	regularize = ipc_regularize()


	with open(input_path) as inputfile:
		ipc_json = json.load(inputfile)

	with open(output_path, 'w') as outputfile:
		result = dict((regularize.ipc_format(key), value) for (key, value) in ipc_json.items())
		
		count = 0
		for k,v in ipc_json.items():
			new_key = regularize.ipc_format(k)
			if new_key != k:
				print(new_key, k)
				count += 1
		print(count)

		json.dump(result, outputfile, ensure_ascii=False)

