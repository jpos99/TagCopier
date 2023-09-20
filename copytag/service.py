import csv
import datetime
import imghdr
import os

import pyexiv2 as pyexiv2

if os.name == 'nt':
	import win32api
	import win32security


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
			print('file in map =', file)
			relative_path = os.path.relpath(os.path.join(folder, file), directory)
			file_map[relative_path] = os.path.join(folder, file)
	return file_map


def find_related_file(file_map, file_name):
	print('related file =', file_map.get(file_name.replace('_olhos', ''), None))
	return file_map.get(file_name.replace('_olhos', ''), None)


def insert_tag_xmp(file, tag):
	updated = False
	with pyexiv2.Image(file) as image:
		xmp_data = image.read_xmp()
		xmp_keywords = xmp_data.get('Xmp.dc.subject', [])
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


def ask_for_permission(file_path):
	if os.name == 'posix' or os.name == 'mac':
		os.chmod(file_path, 0o600)
	elif os.name == 'nt':
		user_sid = win32api.GetUserNameEx(win32api.NameSamCompatible)
		dacl = win32security.ACL()
		dacl.AddAccessAllowedAce(win32security.ACL_REVISION, win32con.FILE_GENERIC_READ | win32con.FILE_GENERIC_WRITE, user_sid)
		win32security.SetFileSecurity(file_path, win32security.DACL_SECURITY_INFORMATION, dacl)
