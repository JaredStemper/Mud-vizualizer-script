import csv
from os import walk, path 

#python 3.6

"""
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

	with open(group_name+'/'+group_name+'.csv', 'w') as csv_output:
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
	path_dict = {}
	for root, dirs, files in walk(dir_name):
		for i in dirs:
			if path_dict.get(i) == None:
				path_dict[i] = []
		for j in files:
			curr_dir = root[root.rfind('/')+1:]
			if (curr_dir+'.csv' == j): 
				path_dict[curr_dir] += [path.join(root, j)]
	return path_dict

def printPathDict(path_dict):
	for i in path_dict:
		print(i)
		for j in path_dict[i]:
			print('\t',j)

def main():
	#iterate through mudviz/plain dirs, collecting the associated usernames and cvs file paths
	mudviz_paths = pathCollection('mudviz')
	plain_paths = pathCollection('plain')
	
	#somewhat arbitrary meta-dictionary is used to simplify passing the groupname (mudviz/plain) to function
	dirDict = {'plain':plain_paths, 'mudviz':mudviz_paths}

	#add the headers/values to rows
	for directory in dirDict:
		path_dict = dirDict[directory]
		for user in path_dict:
			csvPrepend(directory, user, path_dict[user])

	for directory in dirDict:
		path_dict = dirDict[directory]
		csvGroupMerge(directory, path_dict)

if __name__=="__main__":
    main()
