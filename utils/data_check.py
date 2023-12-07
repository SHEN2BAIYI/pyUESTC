import xml.etree.ElementTree as ET
import cv2
import json
import numpy as np


def check_data(xml_path, img_path):
    # 导入 xml 文件
    tree = ET.parse(xml_path)
    root = tree.getroot()
    anno = {}

    for item_index, item in enumerate(root):
        print(item_index, item.tag, item.text)

        if item.tag == 'mark':
            img_index = 0
            points = []
            for son_index, son in enumerate(item):
                print(son_index, son.tag, son.text)
                # 获取图像标号
                if son.tag == 'image':
                    img_index = int(son.text)
                # 获取标注点
                if son.tag == 'svg':  
                    try:
                        values = json.loads(son.text)
                        for value in values:
                            print(value['points'])
                            points.append(value['points'])
                    except TypeError:
                        continue
            anno[img_index] = points

            print('Find: image {} has {} annotations.'.format(img_index, len(points)))

    for key, value in anno.items():
        if not value:
            continue
        # 读取图片
        img = cv2.imread(img_path.format(key))
        img_anno = img.copy()

        # 画出点
        for point in value:
            for index in range(len(point)):
                img_anno = cv2.circle(img_anno, (int(point[index]['x']), int(point[index]['y'])), 3, (0, 0, 255), -1)

        # 获取点的最大最小坐标
        cv2.imshow('img_{}'.format(key), img)
        cv2.imshow('img_anno_{}'.format(key), img_anno)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    for i in range(1, 400):
        try:
            xml_path = '../dataset/Kaggle/archive/{}.xml'.format(i)
            img_path = '../dataset/Kaggle/archive/{}_{}.jpg'.format(i, '{}')
            print(xml_path, img_path)
            check_data(xml_path, img_path)
        except FileNotFoundError:
            continue


