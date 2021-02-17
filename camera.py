from io import BytesIO
from time import sleep
from picamera import PiCamera
from image_analyser import ImageAnalyser
import cv2

class Camera:
	def __init__(self, width = 1024, height = 768):
		self.__camera = PiCamera()
		self.__camera.resolution = (width, height)
		self.stream = BytesIO()
		self.__delay = 2
		self.__image_analyser = ImageAnalyser()
		

	def warm_up(self):
		self.__camera.start_preview()
		sleep(self.__delay)

	def take_picture(self, name='image.jpeg'):
		self.warm_up()
		self.__camera.capture(name)

	def take_continuous(self):
		for i in self.__camera.capture_continuous(self.stream, 'jpeg', use_video_port=True):
			self.stream = self.__image_analyser.identify_people(self.stream)
			self.stream.seek(0)
			image_as_bytes = self.stream.read()
			self.stream.seek(0)
			self.stream.truncate()
			yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + image_as_bytes + b'\r\n\r\n')


