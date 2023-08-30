import csv
import datetime
import os
import service as service


def csv_assembler(source, destination):
	csv_file = 'output.csv'
	source_files = service.list_files(source)
	csv_data = []

	destination_file_map = service.build_file_map(destination)
	for file in source_files:
		origin_path_file = service.split_path(file)
		origin_file_name = os.path.join(origin_path_file[-2], origin_path_file[-1])
		tag = origin_path_file[-3]
		destination_path_file = service.find_related_file(destination_file_map, origin_file_name)
		destination_file_name = destination_path_file
		if destination_path_file is not None:
			destination_file_name = os.path.basename(destination_path_file)
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
