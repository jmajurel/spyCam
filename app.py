from flask import Flask, render_template, send_file, Response
from camera import Camera

app = Flask(__name__)
my_camera = Camera()
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/camera/latest")
def camera_route_handler():
	file_name = "image.jpeg"

	my_camera.take_picture(file_name)
	return send_file(file_name, mimetype='image/jpeg')

@app.route("/camera")
def camera_handler():
	my_camera.warm_up()
	return Response(my_camera.take_continuous(), mimetype='multipart/x-mixed-replace; boundary=frame')

