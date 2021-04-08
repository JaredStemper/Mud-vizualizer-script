#!/usr/bin/python3
#this project uses a minumum of python 3.6

import argparse
from os import walk, path, getcwd
import pandas as pd
import matplotlib.pyplot as plt

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

#list of all column names. cutting out portions can be used to help simply sorting relevant data in pandas.read_csv()
totalCols = [
	"Can_the_smart_fridge_communicate_with_any_other_local_devices_beside_itself",
	"How_many_computer_programming_languages_do_you_know_Not_including_HTML",
	"How_many_local_devices_and_remote_servers_can_the_Vase_device_communicate_with",
	"How_many_remote_servers_websites_on_the_Internet_can_the_smart_coffee_maker_communicate_with",
	"How_many_years_of_working_experience_do_you_have_in_network_operation_and_security_area",
	"I_felt_very_confident_performing_the_analysis",
	"I_found_the_analysis_unnecessarily_complex",
	"I_found_the_various_components_in_this_analysis_were_well_integrated",
	"I_found_this_analysis_very_cumbersome_to_perform",
	"I_needed_to_learn_a_lot_of_things_before_I_could_get_going_with_the_analysis",
	"I_think_that_I_would_like_to_perform_this_analysis_frequently",
	"I_think_that_I_would_need_the_support_of_a_technical_person_to_be_able_to_perform_the_analysis",
	"I_thought_the_analysis_was_easy",
	"I_thought_there_was_too_much_inconsistency_in_this_analysis",
	"I_would_imagine_that_most_people_would_learn_to_use_this_analysis_very_quickly",
	"On_average_how_many_times_do_you_have_to_deal_with_computer_security_related_problems",
	"SQL_injection_is_a_technique_to",
	"The_difference_between_a_passive_and_reactive_Intrusion_Detection_System_is",
	"What_is_Access_Control_List",
	"What_is_the_highest_degree_or_level_of_school_you_have_completed_If_you_are_currently_enrolled_in_school_please_indicate_the_highest_degree_you_have_received_",
	"What_is_the_main_definition_of_IoT",
	"What_is_your_age",
	"What_is_your_annual_income",
	"What_is_your_current_employment_status",
	"When_the_motion_sensor_communicates_with_the_coffee_maker_locally_over_UDP_which_internet_layer_protocol_source_port_number_and_destination_port_number_would_it_use",
	"When_the_smart_coffee_maker_communicates_with_the_motion_sensor_locally_which_destination_port_numbers_should_it_use",
	"When_the_smart_coffee_maker_communicates_with_the_motion_sensor_locally_which_source_port_numbers_should_it_use",
	"Which_gender_do_you_most_identify_with",
	"Which_local_device_can_the_coffee_maker_communicate_with",
	"Without_any_other_changes_in_the_default_settings_of_a_web_server_what_can_be_the_motivation_to_close_port_80",
	"assignmentId",
	"mud_ResponseTime",
	"mud_participant",
	"mud_valid_participant",
	"sis_ResponseTime",
	"sis_participant",
	"sis_valid_participant",
	"skill_ResponseTime",
	"skill_participant",
	"skill_valid_participant",
	"survey_ResponseTime",
	"survey_valid_participant",
	"undefined_Access_control_AC",
	"undefined_Antivirus",
	"undefined_Configured_a_firewall",
	"undefined_Created_a_database",
	"undefined_Designed_a_website",
	"undefined_Firewall",
	"undefined_Hacking_someones_computer",
	"undefined_IP4_800_80",
	"undefined_IPv4_777_888",
	"undefined_IPv4_Any_source_port_Any_destination_port",
	"undefined_IPv6_777_888",
	"undefined_IPv6_800_80",
	"undefined_IPv6_Any_source_port_Any_destination_port",
	"undefined_I_Do_not_Know",
	"undefined_Installed_a_computer_program",
	"undefined_Intrusion_Detection_System_IDS",
	"undefined_Making_a_fake_website_that_looks_legitimate_to_steal_user_information",
	"undefined_Other",
	"undefined_Other_methods_for_stealing_information",
	"undefined_Pretending_to_be_someone_or_a_company_to_steal_users_information",
	"undefined_Pretty_Good_Privacy_PGP",
	"undefined_Registered_a_domain_name",
	"undefined_Secure_Shell_SSH",
	"undefined_Sending_spam_emails_Defrauding_someone_online",
	"undefined_TCP_IPv4_Any_Source_Port_443",
	"undefined_TCP_IPv6_Any_Source_Port_443",
	"undefined_The_certificate_actively_is_secure_and_safe_against_malicious_stuff_including_hackers",
	"undefined_The_certificate_protects_information",
	"undefined_The_certificate_provides_encryption",
	"undefined_The_certificate_shows_the_website_is_registered_and_valid",
	"undefined_The_website_is_trustworthy_and_has_proper_privacy_protection_and_is_accountable_for_information_use",
	"undefined_Tracking_your_internet_habits_to_send_advertisements_",
	"undefined_UDP_IPv4_Any_Source_Port_Any_Destination_Port",
	"undefined_UDP_IPv6_Any_Source_Port_Any_Destination_Port",
	"undefined_Used_SSH",
	"undefined_Written_a_computer_program",
	"undefined_certificate",
	"undefined_https",
	"undefined_lock_icon_on_the_page",
	"undefined_professionallooking_website",
	"undefined_type_of_website",
	"undefined_website_privacy_statements",
	"undefined_www_vasedatabase_com",
	"undefined_www_vasedb_com",
	"undefined_www_vasefileserver_com",
	"undefined_www_vasefirmware_com",
	"undefined_www_vaselinks_com",
	"undefined_www_vaseupdater_com",
	"workerId",
]



def csvParsing(groupPath):
	"""function to parse/manipulate csv data"""

	df = pd.read_csv(groupPath)

	df.info()
	df.plot()
	plt.show()

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
	"""analyze the created group.csv files"""

	groupPath1 = args['dir']+'/mudviz/mudviz.csv'
	groupPath2 = args['dir']+'/plain/plain.csv'

	#avoid potential user-input trouble with extra forward slashes
	if args['dir'][-1] == '/':
		groupPath1 = args['dir'][:-1]+'/mudviz/mudviz.csv'
		groupPath2 = args['dir'][:-1]+'/plain/plain.csv'

	
	csvParsing(groupPath1)
	csvParsing(groupPath2)



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
