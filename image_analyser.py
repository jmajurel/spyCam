import face_recognition
from pathlib import Path, PurePosixPath 
from PIL import Image, ImageDraw
import numpy as np
import cv2

class ImageAnalyser:

	def __init__(self):
		self.encoded_images = []
		self.names = []
		self.load_images()

	def load_images(self, path= './peoples'):

		self.encoded_images =  []
		self.names = []
		base_path = Path(path)
		files = (entry for entry in base_path.iterdir() if entry.is_file() and (PurePosixPath(entry).suffix in ['.jpg', '.jpeg', '.png']))
		for file in files:
			file_path  = path + '/' + file.name
			image = face_recognition.load_image_file(file_path)
			encoded_image = face_recognition.face_encodings(image)[0]
			self.encoded_images.append(encoded_image)
			self.names.append(PurePosixPath(file.name).stem)

	def identify_people(self, stream):
		image = Image.open(stream)
		image = np.array(image)

		face_locations = face_recognition.face_locations(image)
		face_encodings = face_recognition.face_encodings(image, face_locations)

		pil_image = Image.fromarray(image)
		draw = ImageDraw.Draw(pil_image)

		for(top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
			matches = face_recognition.compare_faces(self.encoded_images, face_encodings)

			name = "Unknow Person"

			if True in matches:
				first_match_index = matches.index(True)
				name = names[first_match_index]

			draw.rectangle(((left, top), (right, bottom)), outline=(128, 0, 128))

			text_width, text_height = draw.textsize(name)

			draw.text((left + 6, bottom - text_height - 5), name, fill=(0, 0, 0))

		del draw
		stream.seek(0)
		stream.truncate()
		pil_image.save(stream, format='JPEG');
		return stream
		

