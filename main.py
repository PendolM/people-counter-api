from flask import Flask, request
from flask_restful import Resource, Api
import cv2
import requests
import numpy as np

app = Flask(__name__)
api = Api(app)

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


class PeopleCounter(Resource):
    def get(self):
        img = cv2.imread('images/dworzec.jpeg')
        boxes, weights = hog.detectMultiScale(img, winStride=(8, 8))

        return {'count': len(boxes)}


class PeopleCounterLink(Resource):
    def get(self):
        resp = requests.get(request.args.get('url'))
        arr = np.asarray(bytearray(resp.content), dtype=np.uint8)
        img = cv2.imdecode(arr, -1)
# img = cv2.imread(request.args.get('url'))
        boxes, weights = hog.detectMultiScale(img, winStride=(8, 8))

        return {'count': len(boxes)}


'''
class PeopleCounterPost(Resource):
    def post(self):
        resp = requests.get(request.args.get('url'))
        arr = np.asarray(bytearray(resp.content), dtype=np.uint8)
        img = cv2.imdecode(arr, -1)
# img = cv2.imread(request.args.get('url'))
        boxes, weights = hog.detectMultiScale(img, winStride=(8, 8))

        return {'count': len(boxes)}
'''


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class HelloWorld2(Resource):
    def get(self):
        return {'hello': 'world2'}


api.add_resource(PeopleCounter, '/')
api.add_resource(PeopleCounterLink, '/link')
api.add_resource(HelloWorld, '/test')
api.add_resource(HelloWorld2, '/test2')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
