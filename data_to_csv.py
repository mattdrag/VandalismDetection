import re
import codecs
from lxml import etree
from glob import glob
import pandas 
#import feather
import csv


trainwriter = csv.writer(codecs.open('./Intermediates/wdvc16_train.csv','w','utf8'))

# Directories for writing to files
train_dir = glob('./Train/')
validation_dir = glob('./Validation/')
test_dir = glob('./Test/')

# Make global CSV writers for write_to_csv func
#trainwriter = csv.writer('./Intermediates/wdvc16_train.csv')
#valwriter = csv.writer('./Intermediates/wdvc16_validation.csv')
#testwriter = csv.writer('./Intermediates/wdvc16_test.csv')



# Open all 3 files and join them
def join_csv_files(whichSet):
	#which set tells us which files we are joining
	#Train
	if whichSet == 0:
		features_file = './Intermediates/wdvc16_train.csv'
		meta_file = './Train/wdvc16_meta.csv'
		truth_file = './Train/wdvc16_truth.csv'
		joined_file = './Intermediates/wdvc16_train_joined.csv'


	#Validation
	elif whichSet == 1:
		features_file = './Intermediates/wdvc16_validation.csv'
		meta_file = './Validation/wdvc16_2016_03_meta.csv'
		truth_file = './Validation/wdvc16_2016_03_truth.csv'
		joined_file = './Intermediates/wdvc16_validation_joined.csv'

	#Test
	else: #whichSet == 2
		features_file = './Intermediates/wdvc16_test.csv'
		meta_file = './Validation/wdvc16_2016_05_meta.csv'
		truth_file = './Validation/wdvc16_2016_05_truth.csv'
		joined_file = './Intermediates/wdvc16_test_joined.csv'

	#open the three files and write to an output
	with codecs.open(features_file, 'r', 'utf8') as featuresfile:
		with codecs.open(meta_file, 'r', 'utf8') as metafile:
			with codecs.open(truth_file, 'r', 'utf8') as truthfile:
				with codecs.open(joined_file, 'w', 'utf8') as joinedfile:
					while True:
						featuresfile_line = featuresfile.readline().strip()
						metafile_line = metafile.readline().strip()
						# We dont need Revision ID
						meta_pos = metafile_line.find(',')
						metafile_line_id_removed = metafile_line[meta_pos:]

						truthfile_line = truthfile.readline().strip()
						# We dont need Revision ID
						truth_pos = truthfile_line.find(',')
						truthfile_line_id_removed = truthfile_line[truth_pos:]

						#check if were still reading
						if featuresfile_line:
							joinedfile_line = featuresfile_line + metafile_line_id_removed + truthfile_line_id_removed + '\n'
							joinedfile.write(joinedfile_line)

						#EOF
						else:
							break


def write_to_csv(row, whichSet):
	#which set tells us which file to write to
	#Train
	if whichSet == 0:
		trainwriter.writerow(row)

	#Validation
	elif whichSet == 1:
		valwriter.writerow(row)

	#Test
	else: #whichSet == 2
		testwriter.writerow(row)




def is_none(s):
    if s is None:
        return ''
    else:
        return s.text


def process_page(page, whichSet):
	# Join into one string
	page_string = (''.join(page))
	# A page is a list of lines
	tree = etree.fromstring(''.join(page))

	# Get the page of the revision
	page_title = is_none(tree.find('title'))

	# This is where we actually get the data we are looking for and extract it
	# Grab info for every revision
	for revision in tree.xpath('./revision'):
		# Get revision id and title
		rev_ID = is_none(revision.find('id'))

		# Get user info
		rev_contributor = revision.find('contributor')
		username = is_none(rev_contributor.find('username'))
		# If theres no username, then they only have an ip address.
		if username is '':
			user_name = ''
			user_id = ''
			user_ip = rev_contributor.find('ip').text

		# If theres a username, then they have username and id.
		else:
			user_name = is_none(rev_contributor.find('username'))
			user_id = rev_contributor.find('id').text
			user_ip = ''
		user_name.replace(",", "\,")

		#'REVISION_ID,PAGE_TITLE,USER_NAME,USER_ID,USER_IP,\n'
		full_row = [ rev_ID, page_title, user_name, user_id, user_ip  ]
		# Write to csv file
		write_to_csv(full_row, whichSet)





def parse_pages(xmlfile, whichSet):
	# Keep an accumulator 
	page_buffer = []
	with codecs.open(xmlfile, 'r', 'utf8') as xml:
		# Run loop until there are no more lines to be read
		while True:
			# Read a line and check that it was successfully read
			line = xml.readline()

			if line:
				# Add line to page buffer
				stripped_line = line.strip()

				# We want to skip the beginning of the file
				if stripped_line == "</siteinfo>":
					# Clear everything up to the siteinfo end tag
					page_buffer[:] = []
					continue

				page_buffer.append(line.strip())

				# Check if we've reached the end of the page
				if stripped_line == "</page>":
					# Process current page
					process_page(page_buffer, whichSet)
					# Clear buffer
					page_buffer[:] = []

			# Theres no more lines in the file
			else:
				break



def main():
	# TODO: Lets determine what categories were looking for in the xml
	# For that reason I'm just going to leave this here:
	init_line = [ 'REVISION_ID', 'PAGE_TITLE', 'USER_NAME', 'USER_ID', 'USER_IP' ]

	# Create a csv for each Train, validation, test
	#Train = 0
	#Validation = 1
	#Test = 2

	#Train:
	train_files = glob('./Train/*.xml')
	trainwriter.writerow(init_line)
	for xml_doc in train_files:
		# first lets create the intermediate file TODO: which we are calling output.txt, and lets get all revisions from all files and combine them into one csv
		print ('Processing file: %s...' % xml_doc)
		parse_pages(xml_doc, 0)
	join_csv_files(0)

	#TODO: Validation and test

	# We have one big csv file called output2.txt "./Intermediates/output2.txt"
	# We want a data frame
	# REVISION_ID	PAGE_TITLE	USER_NAME	USER_ID	USER_IP	REVISION_SESSION_ID	USER_COUNTRY_CODE	
	# USER_CONTINENT_CODE	USER_TIME_ZONE	USER_REGION_CODE	USER_CITY_NAME	USER_COUNTY_NAME	REVISION_TAGS	ROLLBACK_REVERTED	UNDO_RESTORE_REVERTED

	df = pandas.read_csv("./Intermediates/wdvc16_train_joined.csv", dtype={"REVISION_ID": int, "PAGE_TITLE": object, "USER_NAME": object, \
		"USER_ID": float, "USER_IP": object, "REVISION_SESSION_ID": int, \
		"USER_COUNTRY_CODE": object, "USER_CONTINENT_CODE": object, "USER_TIME_ZONE": object, \
		"USER_REGION_CODE": object, "USER_CITY_NAME": object, "USER_COUNTY_NAME": object,  \
		"REVISION_TAGS": object, "ROLLBACK_REVERTED": object, "UNDO_RESTORE_REVERTED": object})


	df.USER_ID.fillna(-1, inplace=True)
	df.to_csv("./Train/wdvc16_train.csv")
	#write_dir = "./DataFrames/data.feather"
	#feather.write_dataframe(df, write_dir)


if __name__ == "__main__":
	main()