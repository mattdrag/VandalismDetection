import re
import codecs
from lxml import etree
from glob import glob
import csv
from unicodecsv import DictWriter

# the file to write to
outputFile = codecs.open("./Intermediates/output.txt", 'w', 'utf8')


def join_csv_files():
	# just go ahead and nest em bc idgaf
	with codecs.open("./Intermediates/output.txt", 'r', 'utf8') as outputfile:
		with codecs.open("./test_data/wdvc16_meta.csv.001", 'r', 'utf8') as metafile:
			with codecs.open("./test_data/wdvc16_truth.csv.001", 'r', 'utf8') as truthfile:
				with codecs.open("./Intermediates/output2.txt", 'w', 'utf8') as output2:
					while True:
						outputfile_line = outputfile.readline().strip()
						metafile_line = metafile.readline().strip()
						truthfile_line = truthfile.readline().strip()

						#check if were still reading
						if outputfile_line:
							output2_line = outputfile_line + ','+ metafile_line + ',' + truthfile_line
							output2.write(output2_line + '\n')

						#EOF
						else:
							break


def write_to_csv(data):
	# Data should be a list of strings
	csv_formatted = ",".join(data)
	csv_formatted_n = csv_formatted + '\n'
	outputFile.write(csv_formatted_n)



def process_page(page):
	# Join into one string
	page_string = (''.join(page))
	# A page is a list of lines
	tree = etree.fromstring(''.join(page))

	# This is where we actually get the data we are looking for and extract it
	# Grab info for every revision
	for revision in tree.xpath('./revision'):
		rev_ID = revision.find('id').text
		rev_time = revision.find('timestamp').text
		full_list = [ rev_ID, rev_time ]
		# Write to csv file
		write_to_csv(full_list)





def parse_pages(xmlfile):
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
					print('calling process_page')
					process_page(page_buffer)
					# Clear buffer
					page_buffer[:] = []

			# Theres no more lines in the file
			else:
				break




def main():
	# TODO: We have two different directories, test will be used for now and removed later
	all_xml_docs = glob('../data/wdvc16_*_*.xml')
	test_xml_docs = glob('./test_data/wdvc16_2012_10_first20krev.xml')

	# TODO: Lets determine what categories were looking for in the xml
	# For that reason I'm just going to leave this here:
	init_line = 'REVISION_ID,REVISION_TIME\n'
	outputFile.write(init_line)

	for xml_doc in test_xml_docs:
		# first lets create the intermediate file TODO: which we are calling output.txt, and lets get all revisions from all files and combine them into one csv
		print ('processing file %s...' % xml_doc)
		parse_pages(xml_doc)

	outputFile.close()
	# good, we processed all the xml into one big csv. now lets join it with the 
	join_csv_files()


if __name__ == "__main__":
	main()