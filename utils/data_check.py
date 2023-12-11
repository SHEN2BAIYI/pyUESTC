import xml.etree.ElementTree as ET
import cv2
import os
import json
import numpy as np

from utils.use_xml import *


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

    # 更新 xml 文件
    indent(root)
    tree.write(xml_path, encoding='utf-8', xml_declaration=True)

    for key, value in anno.items():
        if not value:
            continue
        # 读取图片
        img = cv2.imread(img_path.format(key))
        img_anno = img.copy()
        img_anno1 = img.copy()

        # 写入 xml 文件
        root = ET.Element('Root')
        tree = ET.ElementTree(root)

        # 画出点
        for i, points in enumerate(value):
            for index in range(len(points)):
                img_anno = cv2.circle(img_anno, (int(points[index]['x']), int(points[index]['y'])), 3, (0, 0, 255), -1)

            # 找出所有点的最大最小坐标
            points = np.array([(point['x'], point['y']) for point in points])
            min_x = np.min(points[:, 0])
            min_y = np.min(points[:, 1])
            max_x = np.max(points[:, 0])
            max_y = np.max(points[:, 1])

            lt_coords = (min_x, min_y)
            rb_coords = (max_x, max_y)
            img_anno1 = cv2.rectangle(img_anno1, (int(min_x), int(min_y)), (int(max_x), int(max_y)), (0, 255, 0), 2)

            # 写入 xml 文件
            mark = ET.Element('mark', id=str(i))
            root.append(mark)
            coords1 = ET.Element('lt_coords')
            coords1.text = str(lt_coords)
            mark.append(coords1)
            coords2 = ET.Element('rb_coords')
            coords2.text = str(rb_coords)
            mark.append(coords2)

        # 获取点的最大最小坐标
        cv2.imshow('img_{}'.format(key), img)
        cv2.imshow('img_anno_{}'.format(key), img_anno)
        cv2.imshow('img_anno1_{}'.format(key), img_anno1)

        # 保存 xml 文件
        indent(root)
        tree.write(img_path.replace('jpg', 'xml').format(key).replace('origin', 'origin/det_anno'),
                   encoding='utf-8', xml_declaration=True)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def check_data_v2(img_folder, crop_xml_folder, annot_xml_folder):
    # 遍历图像文件夹
    for img_name in os.listdir(img_folder):
        img_path = os.path.join(img_folder, img_name)
        img = cv2.imread(img_path)

        # 读取 crop xml 文件
        crop_xml_path = os.path.join(crop_xml_folder, img_name.replace('jpg', 'xml'))
        tree = ET.parse(crop_xml_path)
        root = tree.getroot()
        for item_index, item in enumerate(root):
            print(item_index, item.tag, item.text)

            if item.tag == 'crop':
                for child_index, child in enumerate(item):
                    print(child_index, child.tag, child.text)

                    if child.tag == 'lt_coords':
                        crop_lt_coords = np.array(eval(child.text))
                    if child.tag == 'rb_coords':
                        crop_rb_coords = np.array(eval(child.text))

        # 读取 anno xml 文件
        anno_xml_path = os.path.join(annot_xml_folder, img_name.replace('jpg', 'xml'))

        # 导入 xml 文件
        tree = ET.parse(anno_xml_path)
        root = tree.getroot()

        for item_index, item in enumerate(root):
            print(item_index, item.tag, item.text)

            if item.tag == 'mark':
                for child_index, child in enumerate(item):
                    print(child_index, child.tag, child.text)

                    if child.tag == 'lt_coords':
                        lt_coords = np.array(eval(child.text))
                    if child.tag == 'rb_coords':
                        rb_coords = np.array(eval(child.text))

                cv2.rectangle(img, lt_coords - crop_lt_coords,
                              rb_coords - crop_lt_coords, (0, 255, 0), 2)

        cv2.imshow('img', img)
        cv2.waitKey(0)


if __name__ == '__main__':
    for i in range(100, 401):
        try:
            xml_path = '../dataset/public/origin/{}.xml'.format(i)
            img_path = '../dataset/public/origin/{}_{}.jpg'.format(i, '{}')
            print(xml_path, img_path)
            check_data(xml_path, img_path)
        except FileNotFoundError:
            continue

    # check_data_v2('../dataset/public/flawRemoved',
    #               '../dataset/public/cropped',
    #               '../dataset/public/origin/det_anno')


