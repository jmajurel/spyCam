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
                stream.seek(0)
                stream.truncate()
		self.__camera.capture_continuous(self.__stream,format='jpeg')
		self.__stream.seek(0)
		frame = self.__stream.read()
		print('value: ' + str(frame))
		return frame
