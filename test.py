import time
import requests
import random,string
import cv2
import numpy as np
from utils.flaw_removal import *

img = cv2.imread('./dataset/Kaggle/archive/mask.jfif')

img_url = upload_img('./dataset/Kaggle/archive/69_2.jpg')
print(img_url)
time.sleep(1)
mask_url = upload_img('./dataset/Kaggle/archive/mask.jfif')
print(mask_url)
time.sleep(1)

response = flaw_removal(img_url, mask_url)
res = json.loads(response.text)['data']['response_file'][0]
print(1)
