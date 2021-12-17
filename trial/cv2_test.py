import cv2

img1 = cv2.imread('test.jpg')
img2 = cv2.imread('duck.jpg')

rows, cols,channels =img2.shape
roi = img1[0:612, 0:612]

# Now create a mask of logo and create its inverse mask also
img2gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
mask_inv = cv2.bitwise_not(mask)

img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
cv2.imshow('res', img1_bg)

'''
cv2.imshow('res', img2gray)
cv2.imshow('ret', ret)
cv2.imshow('mask', mask)
cv2.imshow('mask_inv', mask_inv)
'''
cv2.waitKey()