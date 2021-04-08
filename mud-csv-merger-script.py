#!/usr/bin/python3
#this project uses a minumum of python 3.6

import argparse
import csv
from os import walk, path, getcwd 
import pandas as pd

"""
break people into three categories of expertise and compare those categories
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
def csvParsing(csv_path):
	userDict = {}


	#results = pd.read_csv(csv_path, sep=',')

	#print(len(results))
	return 0
	with open(csv_path,'r') as csv_file:
		reader = csv.reader(csv_file)

		for row in reader:
			if row[0] == 'Header': #NOTE: row 0 is category titles, so it will be skipped initially 
				continue
			for column in row[1:]: #NOTE: column 0 is "Values", so it is not necessary to include
				print(column)
				return 0
	
def csvPrepend(group_name, user_name, csv_path):
	"""inserts new columns to the user_csv
		\n\ta new question/values header
		\n\ta column to track the group and username
	"""
	df = pd.read_csv(csv_path)
	df.insert(loc=0, column='Header', value="Values")
	df.insert(loc=1, column='Group_name', value=group_name)
	df.insert(loc=2, column='User_name', value=user_name)

def csvMerge(group_name, user_name, csv_paths, groupPath):
	"""merges separate csvs together into a single user_name.csv; returns the full filepath the the new csv
	
	\n\t since multiple users had partial files, and sometimes with duplicated column names, special care had to be taken when combining in order to not lose data
	"""
	newPDs = []
	
	for csv_path in csv_paths:
		currDf = pd.read_csv(csv_path)
		newPDs += [currDf]
		if(csv_path.find('raw_sis') != -1):
			currDf.rename(columns = {'ResponseTime':'sis_ResponseTime','participant':'sis_participant','valid_participant':'sis_valid_participant'}, 
							inplace = True)
		if(csv_path.find('raw_skill') != -1):
			currDf.rename(columns = {'ResponseTime':'skill_ResponseTime','participant':'skill_participant','valid_participant':'skill_valid_participant'}, 
							inplace = True)
		if(csv_path.find('raw_mud') != -1):
			currDf.rename(columns = {'ResponseTime':'mud_ResponseTime','participant':'mud_participant','valid_participant':'mud_valid_participant'}, 
							inplace = True)
		if(csv_path.find('raw_survey') != -1):
			currDf.rename(columns = {'ResponseTime':'survey_ResponseTime','participant':'survey_participant','valid_participant':'survey_valid_participant'}, 
							inplace = True)

	df = pd.concat(newPDs, sort=True, axis=1)
	df = df.reindex(sorted(df.columns), axis=1)

	"""
	#If an error occurs when reindexing due to duplicate column names, use the code below to troubleshoot
	col_list = df.columns.values.tolist()
	dupes = set([x for x in col_list if col_list.count(x) > 1])
	#print(dupes)
	"""

	filename = f"{groupPath}/{user_name}/{user_name}.csv"
	df.to_csv(filename, index=False)
	return filename

def csvMergeGroup(group_name, path_dict, groupPath):
	"""merge a single group's user_csv's into a single group_name.csv"""

	newPDs = []
	for user in path_dict:
		df = pd.read_csv(path_dict[user])
		newPDs += [df]
		
	groupDf = pd.concat(newPDs, sort=True, axis=0)
	
	filename = f"{groupPath}/{group_name}.csv"
	groupDf.to_csv(filename, index=False)
	
	return filename

def pathCollection(dir_name):
	"""walks the given directory name and stores all csv files found underneath it with the sub-directory name stored as a value\n
	note: walks the FULL directory, so make sure to only use on a directory with the user files inside of it"""

	path_dict = {}
	for root, dirs, files in walk(dir_name):
		for i in dirs:
			if (i == "deprecated"): #avoid catching deprecated folder included in user data
				continue
			if path_dict.get(i) == None:
				path_dict[i] = []
		for j in files:
			curr_dir = root[root.rfind('/')+1:]	#grab the lowest directory name to be stored as the value
			if (curr_dir == "mudviz" or curr_dir == "plain" or curr_dir == "deprecated"): #avoid error from runnning the script twice and catching newly created csv files
				continue
			if (curr_dir+".csv" == j): #avoid error from runnning the script twice and catching newly created csv files
				continue
			elif (j.find('.csv') != -1): 
				path_dict[curr_dir] += [path.join(root, j)]
	return path_dict

def printPathDict(path_dict):
	for i in path_dict:
		print(i)
		for j in path_dict[i]:
			print('\t',j)

##############
##Structuring#
#############

def csvProcessing(args):
	"""iterate through mudviz/plain dirs, collecting the associated usernames and cvs file paths"""

	groupPath1 = args['dir']+'/mudviz'
	groupPath2 = args['dir']+'/plain'
	
	#avoid potential user-input trouble with extra forward slashes
	if args['dir'][-1] == '/':
		groupPath1 = args['dir'][:-1]+'/mudviz'
		groupPath2 = args['dir'][:-1]+'/plain'
	
	mudviz_paths = pathCollection(groupPath1)
	plain_paths = pathCollection(groupPath2)

	#printPathDict(plain_paths)

	#somewhat arbitrary dict is used to simplify passing the groupname (mudviz/plain) to function
	dirDict = {"mudviz":[mudviz_paths,groupPath1], "plain":[plain_paths,groupPath2]}

	#printPathDict(mudviz_paths)

	for directory in dirDict:
		path_dict = dirDict[directory][0]
		groupPath = dirDict[directory][1]
		for user in path_dict:
			#merge all user csv files into single user.csv file
			path_dict[user] = csvMerge(directory, user, path_dict[user], groupPath)	#NOTE: dict value is now a string, not a list
			#add the headers/values columns
			csvPrepend(directory, user, path_dict[user])
	for directory in dirDict:
		path_dict = dirDict[directory][0]
		groupPath = dirDict[directory][1]
		#merge user.csv's into a single group.csv for each group
		print(csvMergeGroup(directory, path_dict, groupPath))

def csvAnalyzing(args):
	"""analyze the created csv files"""

	groupPath1 = args['dir']+'/mudviz/mudviz.csv'
	groupPath2 = args['dir']+'/plain/plain.csv'
	
	#avoid potential user-input trouble with extra forward slashes
	if args['dir'][-1] == '/':
		groupPath1 = args['dir'][:-1]+'/mudviz/mudviz.csv'
		groupPath2 = args['dir'][:-1]+'/plain/plain.csv'

	csvParsing(groupPath1)



def main(args):
	if (args['process']):
		csvProcessing(args)
	elif (args['analyze']):
		csvAnalyzing(args)
	else:
		csvProcessing(args)
		# csvAnalyzing(args)



if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('dir', nargs='?', default=getcwd(), help='set root directory of user files (default is current dir) (example: .. or ./user-files)')
	parser.add_argument('-p', "--process", action='store_true', help='explictly process the csv files (i.e. merging/creating csv files)')
	parser.add_argument('-a', "--analyze", action='store_true', help='explictly analyze the created csv files')
	args = parser.parse_args()
	args = vars(parser.parse_args())

	main(args)
