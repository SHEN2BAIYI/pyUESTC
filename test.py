import cv2
import os
import numpy as np


def label2gray(mask):
    num = len(np.unique(mask)) - 1
    level = 255 // num
    mask = mask * level
    return mask

base_path = 'C:/Users/shens/Desktop/data/v3/1'

ori_img_path = os.path.join(base_path, 'split/images')
bias_img_path = os.path.join(base_path, 'split/images_inhomogeneity/{}')

img1_path = os.path.join(base_path, 'split/images_inhomogeneity/{}/seg/{}')
img2_path = os.path.join(base_path, 'split/images_no_bg_inhomogeneity/{}/seg/{}')

label_path = os.path.join(base_path, 'split/labels')

target = '1_23.bmp'
target1 = target.split('_')[-1]
code = '20240202142553'
models1 = [
    'Unet (origin)_all', 'Unet (MDCA)', 'Deeplabv3+ (origin)', 'Deeplabv3+ (MDCA)'
]

models2 = [
    'fsl', 'maico', 'mico'
]

label = cv2.imread(os.path.join(label_path, target))
label = np.clip(label, 0, 1)
label = label2gray(label)
cv2.imshow('label', label)

ori_img = cv2.imread(os.path.join(ori_img_path, target))
cv2.imshow('ori', ori_img)

bias_img = cv2.imread(os.path.join(bias_img_path.format(code), target))
cv2.imshow('bias', bias_img)

for model in models1:
    img = cv2.imread(os.path.join(img1_path.format(code, model), target))
    img = img * np.clip(label, 0, 1)
    img = label2gray(img)
    cv2.imshow(model, img)

for model in models2:
    if model == 'fsl':
        img = cv2.imread(os.path.join(img2_path.format(code, model), target1))
    else:
        img = cv2.imread(os.path.join(img2_path.format(code, model), target))
    img = img * np.clip(label, 0, 1)
    img = label2gray(img)
    cv2.imshow(model, img)

cv2.waitKey(0)
cv2.destroyAllWindows()





