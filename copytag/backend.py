import csv
import os
import service as service


def csv_assembler(source, destination):
	csv_file = 'output.csv'
	source_files = service.list_files(source)
	csv_data = []
	for file in source_files:
		print('File =', file)
		origin_path_file = service.split_path(file)
		origin_file_name = os.path.join(origin_path_file[-2], origin_path_file[-1])
		print('file name =', origin_file_name)
		tag = origin_path_file[-3]
		print('tag', tag)
		print('destination =', destination)
		destination_path_file = service.find_related_file(destination, origin_file_name)
		print('destination path =', destination_path_file)
		destination_file_name = os.path.basename(destination_path_file)
		print('destination file =', destination_file_name)
		csv_data.append([file, origin_file_name, tag, destination_file_name, destination_path_file])

	return service.generate_csv(csv_data, csv_file)


def insert_tags_in_destinations(csvfile):
	updated_rows = []
	with open('output.csv', mode='r', encoding='utf-8') as csv_open:
		print('csv =', csv_open)
		list_of_files = csv.DictReader(csv_open)
		for index, row in enumerate(list_of_files, start=1):
			row = dict(row)
			file_to_tag = row['DestinationPath']
			tag = row['TAG']
			if service.insert_tag_xmp(file_to_tag, tag):
				updated_rows.append(index)
	return updated_rows
