# Made by YF
# This script walks down a directory, lists names of all the files in the directory, and optionally calculates their md5 values.
# Two outputs will be created:
# file_list.txt: drive_name, file_path, md5
# error_list.txt: contains the paths of files that can't be read

import os
import hashlib
import re


# change the name of the hard drive
drive_name = 'A'
# the main dir you work on
work_dir = ''
# the dir where output files will be created
out_dir = ''
# decide here if you want to calculate md5 or not
cal_md5 = True


def MD5(file_path, block_size = 2**20):
	m = hashlib.md5()
	
	with open(file_path, 'rb') as f:
		while True:
			chunk = f.read(block_size)
			if not chunk:
				break
			m.update(chunk)
	
	return m.hexdigest()


# WINDOWS WARNING:
# set encoding to utf-8, cuz the windows writer uses gbk as default and it can't encode weird simbols in the file names
# python 2.7 doesn't have the encoding argument
final_df = open(out_dir + drive_name + '_file_list.txt', 'a', encoding = 'utf-8')
err = open(out_dir + drive_name + '_error_list.txt', 'a', encoding = 'utf-8')

# Hard drives have some hidden files that should be filtered out.
# Add more in the garbage bin if you want...partial names are fine!
garbage_bin = ['RECYCLE.BIN', 'Trash-1000', 'System Volume Information']

for root, dirs, files in os.walk(work_dir):
	for file in files:
		file_path = os.path.join(root, file).replace('\\', '/')

		go_on = True
		for garbage in garbage_bin:
			if re.search(garbage, file_path) is not None:
				go_on = False
				break

		if go_on:
			try:
				if cal_md5:
					md5_val = MD5(file_path)
				else:
					md5_val = ''

				each_entry = drive_name + '\t' + file_path + '\t' + md5_val + '\n'
				final_df.write(each_entry)

			except PermissionError:
				each_entry = drive_name + '\t' + file_path + '\n'
				err.write(each_entry)

final_df.close()
err.close()
