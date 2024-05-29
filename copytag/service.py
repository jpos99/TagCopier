import csv
import datetime
import imghdr
import os
from pathlib import Path
import pyexiv2 as pyexiv2
import logging

if os.name == 'nt':
	import win32api
	import win32security

logging.basicConfig(
	level=logging.DEBUG,
	format='%(asctime)s - %(levelname)s - %(message)s',
	handlers=[
		logging.FileHandler("app.log"),
	]
)


def list_files(directory):
	logging.info(f"Listing files in directory: {directory}")
	files = []
	for folder, _, filenames in os.walk(directory):
		for file in filenames:
			if file.split('.')[-1] in ['JPG', 'jpg', 'Jpg']:
				files.append(os.path.join(folder, file))
	logging.debug(f"Files found: {files}")
	return files


def split_path(path):
	logging.info(f"Splitting path: {path}")
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
	logging.debug(f"Path components: {components}")
	return components


def create_tag(path):
	logging.info(f"Creating tag for path: {path}")
	tag = split_path(path)[-3]
	logging.debug(f"TAG = {tag}")
	return tag


def build_file_map(directory):
	logging.info(f"Building file map for directory: {directory}")
	file_map = {}
	directory_path = Path(directory)
	for file_path in directory_path.rglob('*'):
		if file_path.is_file():
			logging.debug(f"File in map: {file_path.name}")
			relative_path = file_path.relative_to(directory_path)
			file_map[str(relative_path)] = str(file_path)
	logging.debug(f"File map: {file_map}")
	return file_map


def find_related_file(file_map, file_name):
	logging.info(f"Finding related file for: {file_name}")
	related_file = file_map.get(file_name.replace('_olhos', ''), None)
	logging.debug(f"Related file: {related_file}")
	return related_file


def read_tags_xmp(file):
	logging.info(f"Reading XMP tags from file: {file}")
	with pyexiv2.Image(file) as image:
		xmp_data = image.read_xmp()
		xmp_dc_keywords = xmp_data.get('Xmp.dc.subject', [])
		xmp_lr_keywords = xmp_data.get('Xmp.lr.weightedFlatSubject', [])
		if not isinstance(xmp_lr_keywords, list):
			xmp_lr_keywords = [xmp_data.get('Xmp.lr.weightedFlatSubject', [])]
	logging.debug(f"XMP DC Keywords: {xmp_dc_keywords}")
	logging.debug(f"XMP LR Keywords: {xmp_lr_keywords}")
	return xmp_dc_keywords, xmp_lr_keywords


def include_new_tag(file, tag):
	logging.info(f"Including new tag '{tag}' in file: {file}")
	xmp_dc_keywords, xmp_lr_keywords = read_tags_xmp(file)

	if tag not in xmp_dc_keywords:
		logging.debug(f"Appending tag to XMP DC Keywords: {xmp_dc_keywords}")
		xmp_dc_keywords.append(tag)
	if tag not in xmp_lr_keywords:
		logging.debug(f"Appending tag to XMP LR Keywords: {xmp_lr_keywords}")
		xmp_lr_keywords.append(tag)
	return xmp_dc_keywords, xmp_lr_keywords


def clear_tags_xmp(file):
	logging.info(f"Clearing XMP tags from file: {file}")
	with pyexiv2.Image(file) as image:
		image.modify_xmp({'Xmp.dc.subject': []})
		image.modify_xmp({'Xmp.lr.weightedFlatSubject': []})


def insert_tag_xmp(file, tag):
	logging.info(f"Inserting tag '{tag}' into file: {file}")
	updated = False
	xmp_dc_keywords, xmp_lr_keywords = include_new_tag(file, tag)
	clear_tags_xmp(file)
	with pyexiv2.Image(file) as image:
		image.modify_xmp({'Xmp.dc.subject': xmp_dc_keywords})
		image.modify_xmp({'Xmp.lr.weightedFlatSubject': xmp_lr_keywords})
		updated = True
	logging.debug(f"Tags inserted. Updated: {updated}")
	return updated


def generate_csv(data, output_file):
	logging.info(f"Generating CSV file: {output_file}")
	with open(output_file, 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['OriginPath', 'OriginFile', 'TAG', 'DetinationFile', 'DestinationPath'])
		for entry in data:
			writer.writerow(entry)
	logging.debug(f"CSV file generated: {output_file}")
	return output_file


def read_csv(file_name):
	logging.info(f"Reading CSV file: {file_name}")
	with open(file_name, "r") as f:
		rows = [row for row in csv.reader(f)]
	logging.debug(f"Rows read from CSV: {rows}")
	return rows


def is_image(file_path):
	logging.info(f"Checking if file is an image: {file_path}")
	result = imghdr.what(file_path) is not None
	logging.debug(f"Is image: {result}")
	return result


def ask_for_permission(file_path):
	logging.info(f"Asking for permission to access file: {file_path}")
	if os.name == 'posix' or os.name == 'mac':
		os.chmod(file_path, 0o600)
	elif os.name == 'nt':
		# Obtém o SID do usuário atual
		user_name = win32api.GetUserNameEx(win32api.NameSamCompatible)
		user_sid, domain, type = win32security.LookupAccountName(None, user_name)

		# Cria um novo DACL (Discretionary Access Control List)
		dacl = win32security.ACL()

		# Adiciona uma ACE (Access Control Entry) que permite leitura e escrita ao usuário
		dacl.AddAccessAllowedAce(win32security.ACL_REVISION, win32con.FILE_GENERIC_READ | win32con.FILE_GENERIC_WRITE,
								 user_sid)

		# Obtém o SD (Security Descriptor) atual do arquivo
		sd = win32security.GetFileSecurity(file_path, win32security.DACL_SECURITY_INFORMATION)

		# Define o novo DACL no SD
		sd.SetSecurityDescriptorDacl(1, dacl, 0)

		# Aplica o novo SD ao arquivo
		win32security.SetFileSecurity(file_path, win32security.DACL_SECURITY_INFORMATION, sd)

	logging.debug(f"Permission set for file: {file_path}")
