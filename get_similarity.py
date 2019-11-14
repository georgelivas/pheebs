import cv2
import numpy as np


def get_similarity(frame1, frame2):
    if frame1.shape == frame2.shape:
        # print("The images have same size and channels")
        difference = cv2.subtract(frame1, frame2)
        b, g, r = cv2.split(difference)

        # if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
        #     print("The images are completely Equal")
        # else:
        #     print("The images are NOT equal")

    sift = cv2.xfeatures2d.SIFT_create()
    kp_1, desc_1 = sift.detectAndCompute(frame1, None)
    kp_2, desc_2 = sift.detectAndCompute(frame2, None)

    index_params = dict(algorithm=0, trees=5)
    search_params = dict()
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(desc_1, desc_2, k=2)

    good_points = []
    for m, n in matches:
        if m.distance < 0.6*n.distance:
            good_points.append(m)

    number_keypoints = 0

    if len(kp_1) <= len(kp_2):
        number_keypoints = len(kp_1)
    else:
        number_keypoints = len(kp_2)

    # print("Keypoints 1ST Image: " + str(len(kp_1)))
    # print("Keypoints 2ND Image: " + str(len(kp_2)))
    # print("GOOD Matches:" + str(len(good_points)))

    print(
        "Frame match: " + str(float(len(good_points)) / float(number_keypoints) * 100),
        end="\r",
        flush=True
    )

    return float(len(good_points)) / float(number_keypoints) * 100
