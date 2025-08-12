import os

import exiftool
BASEDIR = '/Users/joao/Documents/PycharmProjects/CopyTag/fotos'

files = os.listdir(BASEDIR)
for file in files:
	if file.endswith('.jpg'):
		with exiftool.ExifToolHelper() as et:
			xmp_data = et.get_metadata(os.path.join(BASEDIR, file))
			for k in xmp_data:
				print(f"Dict: {k} ")
				xmp_weighted_keywords = k.get('Xmp.lr.weightedFlatSubject', [])
				xmp_dc_keywords = k.get('Xmp.dc.subject', [])
				print('XMP keywords =', xmp_dc_keywords)
				print('XMP weighted =', xmp_weighted_keywords)

			'''xmp_weighted_keywords = xmp_data.get('Xmp.lr.weightedFlatSubject', [])
			xmp_dc_keywords = xmp_data.get('Xmp.dc.subject', [])
			xmp_hierarchical = xmp_data.get('Xmp.lr.hierarchicalSubject', [])

			#xmp_keywords.pop(index_to_remove)
			#if not 'JoaodaSilvaSauro' in xmp_keywords:
			#xmp_dc_keywords.append('JoaodaSilvaSauro')
			#xmp_weighted_keywords.append('JoaodaSilvaSauro')
			#image.modify_xmp({'Xmp.dc.subject': xmp_dc_keywords})
			#image.modify_xmp({'Xmp.lr.weightedFlatSubject': xmp_weighted_keywords})
			#index_to_remove = xmp_hierarchical.index('BrunoPinheiroAlvesSalgado')
			#xmp_hierarchical = xmp_hierarchical.append('JoaodaSilvaSauro')
			#image.modify_xmp({'Xmp.lr.hierarchicalSubject': xmp_hierarchical})

			print('XMP data =', xmp_data)
			print('XMP weighted =', xmp_weighted_keywords)
			print('XMP keywords =', xmp_dc_keywords)
			'''