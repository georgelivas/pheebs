from imutils.video import VideoStream
from get_similarity import get_similarity
import numpy as np
import cv2
import time
import os

from pyimagesearch.centroidtracker import CentroidTracker
from pyimagesearch.trackableobject import TrackableObject

net = cv2.dnn.readNetFromCaffe('/Users/georgelivas/PycharmProjects/humanDetection/mobilenet_ssd/MobileNetSSD_deploy.prototxt', '/Users/georgelivas/PycharmProjects/humanDetection/mobilenet_ssd/MobileNetSSD_deploy.caffemodel')

cv2.startWindowThread()

cap = VideoStream('rtsp://admin:admin1@10.10.240.27:554/11').start()

# the output will be written to output.avi
out = cv2.VideoWriter(
	'output.avi',
	cv2.VideoWriter_fourcc(*'MJPG'),
	15.,
	(640, 480))

old_frame = None
old_boxes = None

ct = CentroidTracker(maxDisappeared=40, maxDistance=50)

W = None
H = None

while True:
	frame = cap.read()
	frame = cv2.resize(frame, (640, 480))

	diff = None
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

	if W is None or H is None:
		(H, W) = frame.shape[:2]

	blob = cv2.dnn.blobFromImage(frame, 0.007843, (W, H), 127.5)
	net.setInput(blob)
	detections = net.forward()

	boxes = []

	# loop over the detections
	for i in np.arange(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated
		# with the prediction
		confidence = detections[0, 0, i, 2]

		if confidence > 0.5:
			# extract the index of the class label from the
			# detections list
			idx = int(detections[0, 0, i, 1])

			# if the class label is not a person, ignore it
			if 15 != idx:
				continue

			box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])

			box_exists = False

			for existing_box in boxes:
				(startX, startY, endX, endY) = existing_box
				(X, Y, X1, Y1) = box.astype('int')

				if startX < X < endX or startX < X1 < endX:
					box_exists = True

			if box_exists:
				print('Duplicate prevented')
				continue

			boxes.append(box.astype('int'))

			(startX, startY, endX, endY) = box.astype('int')
			# cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
			cv2.circle(frame, (int((startX + endX)/2), startY-10), 4, (0, 255, 0), -1)

	cv2.imshow('Pheebs', frame)
	if cv2.waitKey(100) & 0xFF == ord('q'):
		break

cap.release()
out.release()

cv2.destroyAllWindows()
cv2.waitKey(1)
