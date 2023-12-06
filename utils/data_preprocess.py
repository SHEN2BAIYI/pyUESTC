import cv2
import numpy as np


"""  通过二值图像找到最大连通域 """
def find_max_region(img_binary):
    # 最大连通域
    contours, _ = cv2.findContours(img_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 找到最大区域并填充
    area = []
    for i in range(len(contours)):
        area.append(cv2.contourArea(contours[i]))
    if len(area) >= 1:
        max_idx = np.argmax(area)
        max_contour_area = contours[max_idx]

        for k in range(len(contours)):
            if k != max_idx:
                cv2.fillPoly(img_binary, [contours[k]], 0)
    else:
        max_contour_area = 0

    return max_contour_area.squeeze(), img_binary


""" Harris 角点检测 """
def harris_detect(ori):
    # 转换灰度图像
    gray = cv2.cvtColor(ori, cv2.COLOR_BGR2GRAY)

    # 高斯模糊
    gray = cv2.GaussianBlur(gray, (7, 7), 0)

    # 图像转换为 float32
    gray = np.float32(gray)

    # Harris 角点检测
    dst = cv2.cornerHarris(gray, 4, 5, 0.04)

    # 阈值设定
    ori[dst > 0.01 * dst.max()] = [0, 0, 255]
    cv2.imshow('harris', ori)
    cv2.waitKey(0)
    return img


img = cv2.imread('../dataset/Kaggle/archive/4_1.jpg')
img = harris_detect(img)

