import csv
import os

import pyexiv2 as pyexiv2


def list_files(directory):
	files = []
	for folder, subfolders, filenames in os.walk(directory):
		for file in filenames:
			if '.DS_Store' not in file:
				files.append(os.path.join(folder, file))
	return files


def split_path(path):
	components = []
	while True:
		path, tail = os.path.split(path)
		if tail:
			components.append(tail)
		else:
			if path:
				components.append(path)
			break
	components.reverse()
	return components


def create_tag(path):
	tag = split_path(path)[-3]
	print('TAG =', tag)
	return tag


def find_related_file(directory, file_name):
	for folder, _, filenames in os.walk(directory):
		for file in filenames:
			# Construct the relative path from the root directory
			relative_path = os.path.relpath(os.path.join(folder, file), directory)
			print('combined name =', relative_path)
			print('file_name =', file_name)
			if relative_path == file_name:
				return os.path.join(folder, file)
	return None


def insert_tag_xmp(file, tag):
	updated = False
	with pyexiv2.Image(file) as image:
		xmp_data = image.read_xmp()
		xmp_keywords = xmp_data.get('Xmp.dc.subject', [])
		print('xmp_keywords =', xmp_keywords)
		if tag not in xmp_keywords:
			xmp_keywords.append(tag)
			updated = True

		image.modify_xmp({'Xmp.dc.subject': xmp_keywords})
	return updated


def generate_csv(data, output_file):
	with open(output_file, 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['OriginPath', 'OriginFile', 'TAG', 'DetinationFile', 'DestinationPath'])
		for entry in data:
			writer.writerow(entry)
	return output_file


def read_csv(file_name):
	with open(file_name, "r") as f:
		return [row for row in csv.reader(f)]
