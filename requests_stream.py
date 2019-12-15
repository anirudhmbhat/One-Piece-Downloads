import requests, os, zipfile

while True:
	path_to_write = input("Specify the path to download the files to:")
	if not os.path.isdir(path_to_write):
		print('Please enter a valid path!')
	else:
		break

def download_file(data):
	(local_filename,url) = data
	try:
		with requests.get(url, stream=True) as r:
			r.raise_for_status()
			print('Downloading {}'.format(local_filename))
			with open(path_to_write+os.sep+local_filename, 'wb') as f:
				for chunk in r.iter_content(chunk_size = 8192):
					if chunk:
						f.write(chunk)
		return path_to_write+os.sep+local_filename
	except requests.exceptions.RequestException as e:  # This is the correct syntax
		print('Exception while downloading {}:{}'.format(url,e))

def download_file_compress(url):
	output_file_path = download_file(url)
	print('Compressing {}'.format(output_file_path))
	zout = zipfile.ZipFile('{}.zip'.format(output_file_path), "w", zipfile.ZIP_DEFLATED)
	zout.write(os.path.basename(output_file_path))
	zout.close()
	try:
	    os.remove(output_file_path)
	except OSError:
	    pass
