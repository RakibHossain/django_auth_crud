import os
import time
import datetime
from io import BytesIO

from PIL import Image
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage


class FileUpload():

	def upload(path, file):
		file_path = path+'/'+datetime.date.today().isoformat()
		fs = FileSystemStorage(location='media/'+file_path)
		tempname = str(time.time_ns())+'.png'

		filename = fs.save(tempname, file)

		file_original_path = file_path+'/'+str(filename)
		uploaded_file_url = fs.url(file_original_path)

		return uploaded_file_url

	def resizeUpload(path, image_file):

		try:
			file_path = path+'/'+datetime.date.today().isoformat()
			fs = FileSystemStorage(location='media/'+file_path)
			tempname = str(time.time_ns())+'.png'

			# ------------ image resize ------------
			size = 420, 420
			image_file = BytesIO(image_file.file.read())
			image = Image.open(image_file)
			image.thumbnail(size, Image.ANTIALIAS)
			image_file = BytesIO()
			image.save(image_file, 'PNG')
			# --------- end of image resize ---------

			filename = fs.save(tempname, image_file)

			file_original_path = file_path+'/'+str(filename)
			uploaded_file_url = fs.url(file_original_path)

			return uploaded_file_url
		except IOError:
			logger.exception("Error during resize image")
