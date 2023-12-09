import json
import time
import base64

import execjs
import requests

from urllib.parse import urlparse
from io import BytesIO
from PIL import Image

""" JS 文件编译并导入 """
with open('./utils/flaw_removal.js', 'r', encoding='utf-8') as f:
    js_code = f.read()
ctx = execjs.compile(js_code)

""" 编码转换 """
def latin2utf(content):
    # 解码
    content = content.decode('latin-1')
    # 编码
    content = content.encode('utf-8')
    return content


""" 编码转换 """
def utf2latin(content):
    # 解码
    content = content.decode('utf-8')
    # 编码
    content = content.encode('latin-1')
    return content


""" 上传图像并获得图像链接 """
def upload_img(img_path):
    """ 第一步：请求服务器，并获得上传链接 """
    # 获取图片
    with open(img_path, 'rb') as f:
        content = f.read()

    # 随机生成文件名
    filename = ctx.call('aa') + '.png'

    # 构造请求头
    headers = {
        'authority': 'appsrv.passfab.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'authorization': '',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://online.niuxuezhang.cn',
        'pragma': 'no-cache',
        'referer': 'https://online.niuxuezhang.cn/',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }

    # 构造请求体
    json_data = {
        'content-length': len(content),
        'content-type': 'image/jpeg',
        'filename': filename,
    }

    # 发送请求
    response = requests.post('https://appsrv.passfab.com/app/v2/preSignUrl',
                             headers=headers,
                             json=json_data)

    # 解析请求
    res = json.loads(response.text)['data']['response_file'][0]
    res_parse = urlparse(res)
    img_url = 'https://ai-hitpaw.oss-cn-shenzhen.aliyuncs.com' + res_parse.path

    """ 第二步：上传图像 """
    params = {
        'Expires': res_parse.query.split('&')[0].split('=')[1],
        'OSSAccessKeyId': res_parse.query.split('&')[1].split('=')[1],
        'Signature': res_parse.query.split('&')[2].split('=')[1].replace('%3D', '='),
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'image/jpeg',
        'Origin': 'https://online.niuxuezhang.cn',
        'Pragma': 'no-cache',
        'Referer': 'https://online.niuxuezhang.cn/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'x-oss-object-acl': 'public-read',
    }
    response = requests.put(
        img_url,
        params=params,
        headers=headers,
        data=content
    )
    if response.status_code == 200:
        print(response.status_code)
        return img_url
    time.sleep(1)
    return upload_img(img_path)


""" 下载图像 """
def download_img(url, path=None):
    response = requests.get(url)

    if response.status_code == 200:
        print(response.status_code)
        # 从响应中获取图片的二进制数据
        image_data = response.content

        # 转换编码格式
        image_data = utf2latin(image_data)

        # 使用 PIL 库打开图片文件
        image = Image.open(BytesIO(image_data))

        # 可选：显示图片
        image.show()


""" 瑕疵消除 """
def flaw_removal(img_url, mask_url, width=560, height=360):
    # 构建请求头
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

    # 构造数据
    data = '------WebKitFormBoundaryaeyrPOTEd1clFLDi\r\nContent-Disposition: form-data; name="image_url"\r\n\r\n{}\r\n------WebKitFormBoundaryaeyrPOTEd1clFLDi\r\nContent-Disposition: form-data; name="mask_url"\r\n\r\n{}\r\n------WebKitFormBoundaryaeyrPOTEd1clFLDi\r\nContent-Disposition: form-data; name="width"\r\n\r\n{}\r\n------WebKitFormBoundaryaeyrPOTEd1clFLDi\r\nContent-Disposition: form-data; name="height"\r\n\r\n{}\r\n------WebKitFormBoundaryaeyrPOTEd1clFLDi\r\nContent-Disposition: form-data; name="from_site"\r\n\r\npc\r\n------WebKitFormBoundaryaeyrPOTEd1clFLDi--\r\n'.format(
        img_url, mask_url, width, height
    )
    # 发送请求
    response = requests.post('https://appsrv.passfab.com/app/v2/photo/remove-watermark', headers=headers, data=data)
    return response


if __name__ == '__main__':
    img_url = upload_img('../dataset/Kaggle/archive/1_1.jpg')
    time.sleep(2)
    if img_url:
        download_img(img_url)

