import re
import codecs
from lxml import etree
from glob import glob
import csv
from tqdm import tqdm

# Make global CSV writers for write_to_csv func
trainfile = codecs.open('./Intermediates/wdvc16_train.csv','w','utf8')
trainwriter = csv.writer(trainfile)
valfile = codecs.open('./Intermediates/wdvc16_validation.csv','w','utf8')
valwriter = csv.writer(valfile)
#testwriter = csv.writer(codecs.open('./Intermediates/wdvc16_test.csv','w','utf8'))

# Directories for writing to files
train_dir = glob('./Train/')
validation_dir = glob('./Validation/')
test_dir = glob('./Test/')



# Open all 3 files and join them
def join_csv_files(whichSet):
	#which set tells us which files we are joining
	#Train
	if whichSet == 0:
		features_file = './Intermediates/wdvc16_train.csv'
		meta_file = './Train/wdvc16_meta.csv'
		truth_file = './Train/wdvc16_truth.csv'
		joined_file = './Train/wdvc16_train.csv'


	#Validation
	elif whichSet == 1:
		features_file = './Intermediates/wdvc16_validation.csv'
		meta_file = './Validation/wdvc16_2016_03_meta.csv'
		truth_file = './Validation/wdvc16_2016_03_truth.csv'
		joined_file = './Validation/wdvc16_validation.csv'

	#Test
	else: #whichSet == 2
		features_file = './Intermediates/wdvc16_test.csv'
		meta_file = './Test/wdvc16_2016_05_meta.csv'
		truth_file = './Test/wdvc16_2016_05_truth.csv'
		joined_file = './Test/wdvc16_test.csv'

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


def ip_splitter(ip):
    if not ip:
        return ''
    if '.' in ip:
        return ip.split('.')
    elif ':' in ip:
        return ip.split(':')
    return ip


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
			is_anon = 'T'
			user_name = ''
			user_id = ''
			user_ip = rev_contributor.find('ip').text
			user_ip_split = ip_splitter(user_ip)
			user_ip_1 = user_ip_split[0]
			user_ip_2 = user_ip_split[0] + '_' + user_ip_split[1]
			user_ip_3 = user_ip_split[0] + '_' + user_ip_split[1] + '_' + user_ip_split[2]
			user_ip_4 = user_ip_split[0] + '_' + user_ip_split[1] + '_' + user_ip_split[2] + '_' + user_ip_split[3]

		# If theres a username, then they have username and id.
		else:
			is_anon = 'F'
			user_name = is_none(rev_contributor.find('username'))
			user_id = rev_contributor.find('id').text
			user_ip = ''
			user_ip_1 = ''
			user_ip_2 = ''
			user_ip_3 = ''
			user_ip_4 = ''
		user_name.replace(",", "\,")

		# [ 'REVISION_ID', 'IS_ANON', 'USER_NAME', 'USER_ID', 'USER_IP_1', 'USER_IP_2', 'USER_IP_3', 'USER_IP_4', ]
		full_row = [ rev_ID, is_anon, user_name, user_id, user_ip_1, user_ip_2, user_ip_3, user_ip_4  ]
		# Write to csv file
		write_to_csv(full_row, whichSet)





def parse_pages(xmlfile, whichSet):
	# Keep an accumulator 
	page_buffer = []
	with codecs.open(xmlfile, 'r', 'utf8') as xml:
		# Run loop until there are no more lines to be read
		for line in tqdm(xml):
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



def main():
	# Wwhat categories were looking for in the xml
	init_line = [ 'REVISION_ID', 'IS_ANON', 'USER_NAME', 'USER_ID', 'USER_IP_1', 'USER_IP_2', 'USER_IP_3', 'USER_IP_4', ]

	# Create a csv for each Train, validation, test
	#Train = 0
	#Validation = 1
	#Test = 2

	#Train:
	train_files = glob('./Train/*.xml')
	trainwriter.writerow(init_line)
	for xml_doc in train_files:
		# first lets create the intermediate file 
		print ('Processing file: %s...' % xml_doc)
		parse_pages(xml_doc, 0)
	trainfile.flush()
	join_csv_files(0)

	#TODO: test
	#Validation:
	val_files = glob('./Validation/*.xml')
	valwriter.writerow(init_line)
	for xml_doc in val_files:
		# first lets create the intermediate file 
		print ('Processing file: %s...' % xml_doc)
		parse_pages(xml_doc, 1)
	valfile.flush()
	join_csv_files(1)


if __name__ == "__main__":
	main()