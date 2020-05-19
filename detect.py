from imutils.video import VideoStream
from imutils.video import FPS

import numpy as np
import cv2
import dlib
import random

from pyimagesearch.centroidtracker import CentroidTracker
from pyimagesearch.trackableobject import TrackableObject


class colors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'


net = cv2.dnn.readNetFromCaffe(
	'mobilenet_ssd/MobileNetSSD_deploy.prototxt',
	'mobilenet_ssd/MobileNetSSD_deploy.caffemodel')

cv2.startWindowThread()

cap = cv2.VideoCapture(0) #VideoStream('rtsp://admin:admin1@10.10.240.43:554/11').start()
fps = FPS().start()
totalFrames = 0

print(f'[{colors.OKGREEN}info{colors.ENDC}] Camera Ready')

# the output will be written to output.avi
out = cv2.VideoWriter(
	'output.avi',
	cv2.VideoWriter_fourcc(*'MJPG'),
	15.,
	(640, 480))

old_frame = None
old_boxes = None

ct = CentroidTracker(maxDisappeared=40, maxDistance=100)

W = None
H = None

pathPoints = {}
pathColors = {}
trackers = []
trackableObjects = {}

errors = 0

print(f'[{colors.OKGREEN}info{colors.ENDC}] Window Open')
print(f'[{colors.OKGREEN}info{colors.ENDC}] Starting Tracking...\n')

while True:
	_, frame = cap.read()
	frame = cv2.resize(frame, (640, 480))

	diff = None
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

	if W is None or H is None:
		(H, W) = frame.shape[:2]

	blob = cv2.dnn.blobFromImage(frame, 0.007843, (W, H), 127.5)
	net.setInput(blob)
	detections = net.forward()

	boxes = []
	rects = []
	trackers = []

	# loop over the detections
	for i in np.arange(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated
		# with the prediction
		confidence = detections[0, 0, i, 2]

		if confidence > 0.6:
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
				errors += 1
				continue

			boxes.append(box.astype('int'))

			(startX, startY, endX, endY) = box.astype('int')

			tracker = dlib.correlation_tracker()
			rect = dlib.rectangle(startX, startY, endX, endY)
			tracker.start_track(rgb, rect)

			trackers.append(tracker)
	# cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

	for tracker in trackers:
		tracker.update(rgb)
		pos = tracker.get_position()

		# unpack the position object
		startX = int(pos.left())
		startY = int(pos.top())
		endX = int(pos.right())
		endY = int(pos.bottom())

		# add the bounding box coordinates to the rectangles list
		rects.append((startX, startY, endX, endY))

	objects = ct.update(rects)

	for (objectID, centroid) in objects.items():
		# check to see if a trackable object exists for the current
		# object ID
		to = trackableObjects.get(objectID, None)

		# if there is no existing trackable object, create one
		if to is None:
			to = TrackableObject(objectID, centroid)
			pathPoints[objectID] = [[centroid[0], centroid[1]]]
			pathColors[objectID] = (random.randint(20, 255), random.randint(0, 255), random.randint(30, 255))
		#
		# # store the trackable object in the dictionary
		# trackableObjects[objectID] = to

		# (startX, startY, endX, endY) = box.astype('int')
		# # cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
		# cv2.circle(frame, (int((startX + endX) / 2), startY - 10), 8, (0, 255, 0), -1)
		#
		trackableObjects[objectID] = to

		pathPoints[objectID].append([centroid[0], centroid[1]])

		text = "ID {}".format(objectID)
		cv2.putText(frame, text, (centroid[0] - 10, int(centroid[1] / 2) - 10),
		            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
		cv2.circle(frame, (centroid[0], int(centroid[1] / 2)), 4, (0, 255, 0), -1)

	# f'[{colors.OKGREEN}info{colors.ENDC}]

	for (objectID, points) in pathPoints.items():
		cv2.polylines(frame, np.int32([np.array(points)]), False, pathColors[objectID], 2, lineType=cv2.LINE_AA)

		# for coords in points:
		# 	(x, y) = coords
		# 	cv2.circle(frame, (int(x), int(y)), 2, pathColors[objectID], -1)

	totalFrames += 1
	fps.update()
	fps.stop()

	print(
		f'\r[{colors.OKBLUE}stat{colors.ENDC}] People in frame: '
		+ colors.WARNING
		+ str(len(objects.items()))
		+ colors.ENDC
		+ '\t Errors Prevented: '
		+ colors.FAIL
		+ str(errors)
		+ colors.ENDC
		+ '\t FPS: '
		+ colors.OKBLUE
		+ '{:.2f}'.format(int(fps.fps()))
		+ colors.ENDC
		, sep=' ', end='', flush=True
	)
	fps.start()
	# print('\r[stat] Errors Prevented: ' + str(errors), end='\r')

	cv2.imshow('Pheebs', frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

print(f'\n\n[{colors.OKGREEN}info{colors.ENDC}] Terminating...')

fps.stop()
out.release()

cv2.destroyAllWindows()
cv2.waitKey(1)
