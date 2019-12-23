import os
import time
import datetime

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
		