#!/usr/bin/env python3
import os, sys
#stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
import face_recognition as fr
#sys.stderr = stderr

class Rekognize:
	def __init__(self):
		self.database = "Database/"
		self.known = []
		for img in os.listdir(self.database):
			self.known.append(fr.face_encodings(fr.load_image_file(self.database + img))[0])
		self.images = "Images/"
		print("Successfully started the imageClassifier")

	def classify(self, filename):
		print("Classifying filename")
		img = fr.load_image_file(filename)
		try:
			results = fr.compare_faces(self.known, fr.face_encodings(img)[0], tolerance=0.5)
			sys.stdout.flush()
			return os.listdir(self.database)[results.index(True)].split(".")[0]
		except IndexError:
			return None
		# nothing was returned. Default: return NoneType
		return None
