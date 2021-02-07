import cv2
import numpy as np

champion_portrait = cv2.imread('data/portraits/Zilean.png')
champion_select = cv2.imread('data/champion_select/portraits_only.png')

sift = cv2.SIFT_create()
kp1, des1 = sift.detectAndCompute(champion_portrait, None)
kp2, des2 = sift.detectAndCompute(champion_select, None)

# matcher takes normType, which is set to cv2.NORM_L2 for SIFT and SURF, cv2.NORM_HAMMING for ORB, FAST and BRIEF
bf = cv2.BFMatcher(cv2.NORM_L2SQR, crossCheck=True)
matches = bf.match(des1, des2)
matches = sorted(matches, key=lambda x: x.distance)

# draw first 50 matches
match_img = cv2.drawMatches(champion_portrait, kp1, champion_select, kp2, matches[:20], None)
# cv2.imshow('Matches', match_img)
# cv2.waitKey()

matches_array = np.array([kp2[m.trainIdx].pt for m in matches[:10]])

median = np.median(matches_array, axis=0)

print(np.std(matches_array, axis=0))

norm = 0
for row in matches_array:
    norm += np.linalg.norm(row-median)

print(np.linalg.norm(matches_array-median))
print(norm)

##
