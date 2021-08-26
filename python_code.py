#!/usr/bin/env python3

import os

#creating a function to convert raw data files according to the
#conditions mentioned.
def converter(paths):

	#opening the files
	with open(paths) as file:
		line = file.readline()
		words = list(line.split('\t'))
	
		#determing the stations
		if 'Inverter' in paths:
			ind = words.index('i32')
		elif 'WMS' in paths:
			ind = words.index('w23')
		elif 'MFM' in paths:
			ind = words.index('m63')
	
		#editing the first row of raw data files
		#changing the first column data to 'Timestamp'
		line1 = list(line.split('\t'))
		line1.insert(0,'Timestamp')
		line1.pop(ind+1)
		line2 = '\t'.join(line1)

		#creating new directories and assigning filenames
		delimiter = paths.split('/')
		output_path = '<path to Gen1 folder>' + '/'.join(delimiter[5:])
		new_dirs = '<path to Gen1 folder>' + '/'.join(delimiter[5:-1])
		try:
			os.makedirs(new_dirs)
		except OSError as error:
			pass

		#writing the first row to output files
		with open(output_path, 'w') as f:
			f.writelines(line2)

		#reading the remaining data of the raw data files
		line = file.readlines()

		#bringing the requested column to first column
		for item in line:
			li = list(item.split('\t'))
			column = li[ind]
			li.insert(0, column)
			li.pop(ind+1)
			edited = '\t'.join(li)

			#appending the edited data to the output files
			with open(output_path, 'a') as f:
				f.writelines(edited)

#creating main function
if __name__ == "__main__":

	#traversing the raw directory
	path = os.walk('<path to "raw" folder>')
	dirs = []
	for root, directories, files in path:
		for f in files:
			dirs.append(os.path.join(root, f))
	
	#executing 'converter' function for each raw file
	for item in dirs:
		converter(item)