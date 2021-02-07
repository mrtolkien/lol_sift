from lol_surf.lol_window_utils import *
import cv2

select_lol_window()
img = get_champion_select_image()

cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()


##

