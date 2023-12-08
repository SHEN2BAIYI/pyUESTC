import time
import requests
import random,string
from requests_toolbelt import MultipartEncoder
import cv2
import numpy as np
from utils.flaw_removal import *


img_url = upload_img('./dataset/Kaggle/archive/1_1.jpg')
print(img_url)
time.sleep(1)
mask_url = upload_img('./mask.jpg')
print(mask_url)
time.sleep(1)

# boundary = '----WebKitFormBoundary' \
#            + ''.join(random.sample(string.ascii_letters + string.digits, 16))

# m = MultipartEncoder(fields=data, boundary=boundary)

headers = {
    'authority': 'appsrv.passfab.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'authorization': '',
    'cache-control': 'no-cache',
    'origin': 'https://online.niuxuezhang.cn',
    'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryaeyrPOTEd1clFLDi',
    'pragma': 'no-cache',
    'referer': 'https://online.niuxuezhang.cn/',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

# data = {
#     'image_url': img_url,
#     'mask_url': mask_url,
#     'width': str(560),
#     'height': str(360),
#     'from_site': 'pc',
# }

data = '------WebKitFormBoundaryaeyrPOTEd1clFLDi\r\nContent-Disposition: form-data; name="image_url"\r\n\r\n{}\r\n------WebKitFormBoundaryaeyrPOTEd1clFLDi\r\nContent-Disposition: form-data; name="mask_url"\r\n\r\n{}\r\n------WebKitFormBoundaryaeyrPOTEd1clFLDi\r\nContent-Disposition: form-data; name="width"\r\n\r\n560\r\n------WebKitFormBoundaryaeyrPOTEd1clFLDi\r\nContent-Disposition: form-data; name="height"\r\n\r\n360\r\n------WebKitFormBoundaryaeyrPOTEd1clFLDi\r\nContent-Disposition: form-data; name="from_site"\r\n\r\npc\r\n------WebKitFormBoundaryaeyrPOTEd1clFLDi--\r\n'.format(
    img_url, mask_url
)

response = requests.post('https://appsrv.passfab.com/app/v2/photo/remove-watermark', headers=headers, data=data)

print(1)
