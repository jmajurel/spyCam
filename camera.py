from io import BytesIO
from time import sleep
from picamera import PiCamera
import cv2

class Camera:
	def __init__(self, width = 1024, height = 768):
		self.__camera = PiCamera()
		self.__camera.resolution = (width, height)
		self.__stream = BytesIO()
		self.__delay = 2

	def warm_up(self):
		self.__camera.start_preview()
		sleep(self.__delay)

	def take_picture(self, name='image.jpeg'):
		self.warm_up()
		self.__camera.capture(name)

	def take_continuous(self):
		for i in self.__camera.capture_continuous(self.__stream, 'jpeg', use_video_port=True):
			self.__stream.seek(0)
			image_as_bytes = self.__stream.read()
			self.__stream.seek(0)
			self.__stream.truncate()
			yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + image_as_bytes + b'\r\n\r\n')


