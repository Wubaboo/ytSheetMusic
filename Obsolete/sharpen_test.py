import cv2 as cv
import numpy as np
import os

folder = 'AliceInWonderland-BillEvans'
files = [f for f in os.listdir(folder) \
         if '.jpg' in f]

image = cv.imread(os.path.join(folder, files[0]))
image = cv.resize(image, (image.shape[1]*2, image.shape[0]*2))
sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])

sharpen_kernel_2 = np.array([[0, -1, 0],
                            [-1, 5, -1],
                            [0, -1, 0]])

gaussian_kernel = np.array([[1,4,6,4,1],
                            [4,16,24,16,4],
                            [6,24,36,24,6],
                            [4,16,24,16,4],
                            [1,4,6,4,1]]) / 256
unsharp_masking = np.array([[1,4,6,4,1],
                            [4,16,24,16,4],
                            [6,24,-476,24,6],
                            [4,16,24,16,4],
                            [1,4,6,4,1]]) / -256

#blur = cv.GaussianBlur(image, (5,5), 1)
sharpen = cv.filter2D(blur, -1, unsharp_masking)
gray = cv.cvtColor(sharpen, cv.COLOR_BGR2GRAY)
inv = 255-gray
threshold, thresh = cv.threshold(inv, 30, 255, cv.THRESH_BINARY)
#sharpen = cv.filter2D(sharpen, -1, unsharp_masking)
inv = 255 - thresh


cv.imshow('sharpen', inv)
cv.waitKey()