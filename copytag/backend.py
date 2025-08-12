import csv
import datetime
import os
import service as service
import logging
from logging_config import setup_logging

setup_logging()


def csv_assembler(source, destination):
	logging.info(f"Assembling CSV for source: {source} and destination: {destination}")
	logging.debug("Listing source files and building destination map")
	csv_file = 'output.csv'
	source_files = service.list_files(source)
	csv_data = []
	source_destination_file_map = {}
	destination_file_map = service.build_file_map(destination)
	for file in source_files:
		logging.debug(f"Processing source file: {file}")
		origin_path_file = service.split_path(file)
		origin_file_name = os.path.join(origin_path_file[-2], origin_path_file[-1])
		tag = origin_path_file[-3]
		destination_path_file = service.find_related_file(destination_file_map, origin_file_name)
		destination_file_name = destination_path_file
		if destination_path_file is not None:
			destination_file_name = os.path.basename(destination_path_file)
		source_destination_file_map[file] = {'tag': tag, 'destination': destination_path_file}
		csv_data.append([file, origin_file_name, tag, destination_file_name, destination_path_file])
		logging.debug(f"Processed file: {file}, Tag: {tag}, Destination: {destination_file_name}")

	csv_result = service.generate_csv(csv_data, csv_file)
	logging.info(f"CSV file generated: {csv_result}")
	return csv_result, source_destination_file_map


def insert_tags_in_destinations(source_destination_file_map):
	logging.info("Inserting tags in destination files")
	updated_rows = []
	for source_file in source_destination_file_map.items():
		logging.debug(f"Evaluating mapping: {source_file}")
		if source_file[1]['destination'] is not None and source_file[1]['tag'] is not None:
			logging.debug(f"Requesting permission for: {source_file[1]['destination']}")
			service.ask_for_permission(source_file[1]['destination'])
			logging.debug(f"Inserting tag via service.insert_tag_xmp")
			if service.insert_tag_xmp(source_file[1]['destination'], source_file[1]['tag']):
				updated_rows.append(source_file)
				logging.debug(f"Updated destination file: {source_file[1]['destination']} with tag: {source_file[1]['tag']}")
		else:
			logging.warning(f"Skipping mapping due to missing destination or tag: {source_file}")
	logging.info(f"Total updated files: {len(updated_rows)}")
	return updated_rows
