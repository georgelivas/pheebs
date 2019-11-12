from imutils.video import VideoStream
import numpy as np
import cv2

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
face_cascade = cv2.CascadeClassifier('/Users/georgelivas/PycharmProjects/humanDetection/haarcascade_frontalcatface_extended.xml')

cv2.startWindowThread()

cap = VideoStream("rtsp://admin:admin1@10.10.240.27:554/11").start()

# the output will be written to output.avi
out = cv2.VideoWriter(
	'output.avi',
	cv2.VideoWriter_fourcc(*'MJPG'),
	15.,
	(640, 480))

while (True):
	frame = cap.read()
	frame = cv2.resize(frame, (640, 480))

	gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

	faces = face_cascade.detectMultiScale(gray, 1.1, 4)
	boxes, weights = hog.detectMultiScale(frame, winStride=(8, 8))
	boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

	for (x, y, w, h) in faces:
		cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

	for (xA, yA, xB, yB) in boxes:
		cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
		cv2.putText(frame, 'Unknown Person', (xA, yA-10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 2)

	out.write(frame.astype('uint8'))

	cv2.imshow('frame', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
out.release()

cv2.destroyAllWindows()
cv2.waitKey(1)
