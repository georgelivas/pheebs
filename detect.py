from imutils.video import VideoStream
from get_similarity import get_similarity
import numpy as np
import cv2
import time
import os

print(' __   ___       ___      \n'
      '/__` |__  |    |__  |\\ |  /\\  \n'
      '.__/ |___ |___ |___ | \\| /~~\\ \n')

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
body_cascade = cv2.CascadeClassifier('/Users/georgelivas/PycharmProjects/humanDetection/haarcascade_fullbody.xml')

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

while True:
	frame = cap.read()
	frame = cv2.resize(frame, (640, 480))

	diff = None
	gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

	bodies = body_cascade.detectMultiScale(gray, 1.1, 4)
	# boxes, weights = hog.detectMultiScale(frame, winStride=(8, 8))
	# boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

	if 1: # old_frame is None or get_similarity(old_frame, frame) < 85:

		if old_frame is None:
			old_frame = frame


		gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
		old_grey = cv2.cvtColor(old_frame, cv2.COLOR_RGB2GRAY)

		diff = cv2.absdiff(frame, old_frame)

		# faces = face_cascade.detectMultiScale(gray, 1.1, 4)
		# boxes, weights = hog.detectMultiScale(diff, winStride=(8, 8), scale=1.1)
		# boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

		for (x, y, w, h) in bodies:
			cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

		# for (xA, yA, xB, yB) in boxes:
		# 	cropped = frame[yA:yB, xA + 10:xB - 10]

			name = 'Unknown Person'

			# for folder in os.listdir('dataset'):
			# 	for photo in os.listdir('dataset/' + folder):
			# 		print(folder + '/' + photo)
			# 		if 0 < get_similarity(cropped, cv2.imread('dataset/' + folder + '/' + photo)):
			# 			name = folder
			# 			print(folder)

			cv2.imwrite('./images/people/Image_' + str(time.time()) + '.jpg', frame)

			cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
			# cv2.putText(frame, name, (xA, yA - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
			# cv2.putText(frame, 'Count: ' + str(boxes.size/4), (450, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.90, (255, 255, 255), 2)

		old_frame = frame
		# old_boxes = boxes
	else:
		for (xA, yA, xB, yB) in old_boxes:
			cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
			# cv2.putText(frame, 'Unknown Person', (xA, yA - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 0, 0), 2)
	# cv2.putText(frame, 'Count: ' + str(old_boxes.size/4), (450, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.90, (255, 0, 0), 2)

	out.write(frame.astype('uint8'))

	cv2.imshow('dif', diff)
	cv2.imshow('Selena', frame)
	if cv2.waitKey(100) & 0xFF == ord('q'):
		break

cap.release()
out.release()

cv2.destroyAllWindows()
cv2.waitKey(1)
