import cv2
import numpy as np


img = np.array([
	[[0, 1, 2], [3, 4, 5]],
	[[6, 7, 8], [9, 10, 11]]
], dtype=np.uint8)


cv2.imwrite("123.bmp", img)
cv2.imwrite("123.png", img)