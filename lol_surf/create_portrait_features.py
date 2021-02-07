import cv2
import os

sift = cv2.SIFT_create()

portraits_dict = {}

for portrait in os.listdir(os.path.join("data", "portraits")):
    portrait_image = cv2.imread(os.path.join("data", "portraits", portrait))

    portraits_dict[portrait[:4]] = sift.detectAndCompute(portrait_image, None)
