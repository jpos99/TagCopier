import csv
import datetime
import os
import service as service


def csv_assembler(source, destination):
	csv_file = 'output.csv'
	source_files = service.list_files(source)
	csv_data = []
	source_destination_file_map = {}
	destination_file_map = service.build_file_map(destination)
	for file in source_files:
		origin_path_file = service.split_path(file)
		origin_file_name = os.path.join(origin_path_file[-2], origin_path_file[-1])
		tag = origin_path_file[-3]
		destination_path_file = service.find_related_file(destination_file_map, origin_file_name)
		destination_file_name = destination_path_file
		if destination_path_file is not None:
			destination_file_name = os.path.basename(destination_path_file)
		source_destination_file_map[file] = {'tag': tag, 'destination': destination_path_file}
		csv_data.append([file, origin_file_name, tag, destination_file_name, destination_path_file])

	return service.generate_csv(csv_data, csv_file), source_destination_file_map


def insert_tags_in_destinations(source_destination_file_map):
	updated_rows = []
	for source_file in source_destination_file_map.items():

		if service.insert_tag_xmp(source_file[1][ 'destination'], source_file[1]['tag']):
			updated_rows.append(source_file)
	return updated_rows
