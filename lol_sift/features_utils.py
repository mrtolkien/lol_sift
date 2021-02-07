from typing import Optional
import cv2
import os
import numpy as np
from datetime import datetime
import threading

os.makedirs("visualisation", exist_ok=True)

sift = cv2.SIFT_create()
bf = cv2.BFMatcher(cv2.NORM_L2SQR, crossCheck=True)

portraits_features_dict = {}
portraits_images_dict = {}

for portrait in os.listdir(os.path.join("data", "portraits")):
    portrait_image = cv2.imread(os.path.join("data", "portraits", portrait))

    portraits_images_dict[portrait[:-4]] = portrait_image
    portraits_features_dict[portrait[:-4]] = sift.detectAndCompute(portrait_image, None)


def find_champion_in_picture(
    champion_name: str, picture, save_matches=True
) -> Optional[tuple]:
    """
    Expects a BGR numpy array for the picture and the *exact* champion name

    Returns None if no portrait was found, else returns the portrait x, y coordinates in the picture
    """
    portrait_keypoints, portrait_descriptors = portraits_features_dict[champion_name]
    picture_keypoints, picture_descriptors = sift.detectAndCompute(picture, None)

    matches = bf.match(portrait_descriptors, picture_descriptors)
    matches = sorted(matches, key=lambda x: x.distance)

    if save_matches:
        match_img = cv2.drawMatches(
            portraits_images_dict[champion_name],
            portrait_keypoints,
            picture,
            picture_keypoints,
            matches[:20],
            None,
        )

        cv2.imwrite(
            os.path.join(
                "visualisation",
                f"{datetime.now().isoformat().replace('-', '').replace(':', '')}.png",
            ),
            match_img,
        )

    # We simply check if the 10 matches are in roughly the same region, and if so, we return the mean

    # First, we make a simple 2D numpy array of the keypoints found
    matches_array = np.array([picture_keypoints[m.trainIdx].pt for m in matches[:10]])

    # We compute the median, which is our hypothesis for portrait "center"
    median = np.median(matches_array, axis=0)

    # TODO I’m 100% sure there’s a better 2D math tool to use for that but I’m too stupid to find what it is
    # Finally we calculate the total distance of the keypoints from that median
    total_distance_from_median = 0
    for row in matches_array:
        total_distance_from_median += np.linalg.norm(row - median)

    # Ezreal, a "hard match", is still bellow 200 on a partial image
    if total_distance_from_median > 500:
        return None
    else:
        return median


##
