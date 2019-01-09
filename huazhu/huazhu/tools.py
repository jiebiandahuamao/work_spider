import numpy as np 
import cv2 as cv
import pytesseract
import os

def show(image):

    cv.imshow('t', image)
    cv.waitKey(0)

def threshold(image):
    ret, th = cv.threshold(image, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    return th

def vertical_cut(image):
    h = image.shape[1]
    tips = 0
    point_x=0
    point_y=0
    points = []
    
    for i in range(h-1, 0, -1):
        col = image[:, i]
        x = np.max(col)
        if (x == 0 or i == 1):
            if (tips == 1):
                point_x = i
                points.append([point_x, point_y])
                tips = 0
        else:
            if (tips == 0):
                point_y = i
                tips = 1
        
    return points

def vertical_projection(thresh):
    (h, w)=thresh.shape
    for j in range(0,w):
        count = np.count_nonzero(thresh[:, j])
        if count == 0:
            continue
        thresh[:, j] = 0
        thresh[h-count:h, j] = 255

    return thresh

def get_vertical(image):
    #th = vertical_projection(image.copy())
    # show(th)
    points = vertical_cut(image)
    return points

def pic_num(pic_path,pic_name):
    image = cv.imread(os.path.join(pic_path,pic_name), 0)
    image1 = cv.imread(os.path.join(pic_path,pic_name))
    th_image = threshold(image)
    # show(th_image)
    points = get_vertical(th_image)

    # i = 1
    # for point in points:
    #     cv.imwrite('t/'+str(i)+'.png',image1[:, point[0]:point[1]+5])
    #     i += 1
    li = []
    for i in range(len(points)):
        li.append(image1[:, points[i][0]:points[i][1]+5])
    z = np.concatenate(li,axis=1)

    text = pytesseract.image_to_string(z)
    print(text,22222222222)
    num = []
    for i in text[::-1]:
        if i==".":
            num.append(i)
        else:
            num.append(int(i))

    print (num)
    return num
