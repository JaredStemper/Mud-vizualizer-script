#!/usr/bin/python3
#this project uses a minumum of python 3.6

import argparse
import csv
from os import walk, path, getcwd 


"""
Notes:
	2 groups
		20 users
			4 csvs 

	=======
	need to transform this into
		also track the username and groupname from directory structure in csv columns

	2 groups
		20 users
			1 csv per user; with a headers row and a values row
		1 cvs per group; with header/value row and all users from group in the following rows
"""

def csvPrepend(group_name, user_name, csv_paths):
	"""inserts new columns to the user_csv
		\n\ta new question/values header
		\n\ta column to track the group and username
	"""

	for csv_path in csv_paths:
		with open(csv_path,'r') as csv_file:
			with open(csv_path[0:-4]+'_updated.csv', 'w') as csv_output:
				reader = csv.reader(csv_file)
				writer = csv.writer(csv_output)

				count = 1
				for row in reader:
					if count==1:
							writer.writerow(["Header"]+['Group_name']+['User_name']+row)
					elif count==2:
							writer.writerow(["Values"]+[group_name]+[user_name]+row)
					else:
						writer.writerow(row+[row[0]])
					count+=1

def csvGroupMerge(group_name, path_dict):
	"""inserts new columns to the user_csv
		\n\ta new question/values header
		\n\ta column to track the group and username
	"""

	group_lowest_dir = group_name[group_name.rfind('/')+1:]	#grab the lowest directory name to be stored as the value

	with open(group_name+'/'+group_lowest_dir+'.csv', 'w') as csv_output:
		firstFile = True
		for user in path_dict:
			for csv_path in path_dict[user]:
				with open(csv_path[0:-4]+'_updated.csv','r') as csv_file:
					writer = csv.writer(csv_output)
					reader = csv.reader(csv_file)

					count = 1
					# avoid header row except for the first file
					for row in reader:
						if firstFile:
							writer.writerow(row)
						elif count == 2:
							writer.writerow(row)
						count += 1
			firstFile = False
				

def pathCollection(dir_name):
	"""walks the given directory name and stores all csv files found underneath it with the sub-directory name stored as a value\n
	note: walks the FULL directory, so make sure to only use on a directory with the user files inside of it"""

	path_dict = {}
	for root, dirs, files in walk(dir_name):
		for i in dirs:
			if path_dict.get(i) == None:
				path_dict[i] = []
		for j in files:
			curr_dir = root[root.rfind('/')+1:]	#grab the lowest directory name to be stored as the value
			if (curr_dir+'.csv' == j): 
				path_dict[curr_dir] += [path.join(root, j)]
	return path_dict

def printPathDict(path_dict):
	for i in path_dict:
		print(i)
		for j in path_dict[i]:
			print('\t',j)

def main(args):
	#iterate through mudviz/plain dirs, collecting the associated usernames and cvs file paths
	groupName1 = args['dir']+'/mudviz'
	groupName2 = args['dir']+'/plain'
	
	#avoid potential user-input trouble with extra forward slashes
	if args['dir'][-1] == '/':
		groupName1 = args['dir'][:-1]+'/mudviz'
		groupName2 = args['dir'][:-1]+'/plain'
	
	mudviz_paths = pathCollection(groupName1)
	plain_paths = pathCollection(groupName2)

	#printPathDict(plain_paths)

	#somewhat arbitrary meta-dictionary is used to simplify passing the groupname (mudviz/plain) to function
	dirDict = {groupName1:mudviz_paths, groupName2:plain_paths}

	#add the headers/values to rows
	for directory in dirDict:
		path_dict = dirDict[directory]
		for user in path_dict:
			csvPrepend(directory, user, path_dict[user])

	for directory in dirDict:
		path_dict = dirDict[directory]
		csvGroupMerge(directory, path_dict)

if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('dir', nargs='?', default=getcwd(), help='set root directory of user files (default is current dir) (example: .. or ./user-files)')
	args = parser.parse_args()
	args = vars(parser.parse_args())

	main(args)
