import csv
import datetime
import imghdr
import os

import pyexiv2 as pyexiv2


def list_files(directory):
	files = []
	for folder, _, filenames in os.walk(directory):
		for file in filenames:
			#if is_image(os.path.join(folder, file)):
			if file.split('.')[-1] in ['JPG', 'jpg', 'Jpg']:
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


def build_file_map(directory):
	file_map = {}
	for folder, _, filenames in os.walk(directory):
		for file in filenames:
			relative_path = os.path.relpath(os.path.join(folder, file), directory)
			file_map[relative_path] = os.path.join(folder, file)
	return file_map


def find_related_file(file_map, file_name):
	return file_map.get(file_name.replace('_olhos', ''), None)


'''def find_related_file(directory, file_name):
	for folder, subfolder, filenames in os.walk(directory):
		#print('walk', folder, subfolder, filenames)
		#print('file', file_name)
		if file_name.split('/')[-1] in filenames:
			for file in filenames:
				relative_path = os.path.relpath(os.path.join(folder, file), directory)
				if relative_path == file_name:
					print('combined name =', relative_path)
					print('file_related =', file_name)
					return os.path.join(folder, file)
		#print('relative path =', relative_path)
		#print('directory =', directory)
		#print('file_related =', file_name)
	return None'''


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
	print('fim', datetime.datetime.now())
	return output_file


def read_csv(file_name):
	with open(file_name, "r") as f:
		return [row for row in csv.reader(f)]


def is_image(file_path):
	return imghdr.what(file_path) is not None
