import os, sys, cv2, json
import numpy as np
import xml.etree.ElementTree as ET

from utils.use_xml import *

""" 检查原始数据及其原始标签 """
def check_data_origin(xml_path, img_path,
                      indent_flag=False, det_anno_path=None):
    # 导入 xml 文件
    data = load_xml(xml_path)

    # 格式化 xml 文件
    if indent_flag:
        indent_xml(xml_path)

    # 根据 xml 文件中的 mask 信息，将其绘制到图像上
    for mark in data['mark']:
        # 导入图像
        img = cv2.imread(img_path.format(mark['image']))
        img_anno_point = img.copy()
        img_anno_mask = img.copy()
        if img is None:
            print('Error: image {} is not exist.'.format(mark['image']))
            continue

        # 绘制 mask
        if not mark['svg']:
            continue
        anno_all = json.loads(mark['svg'])
        for anno_once in anno_all:
            points_list = anno_once['points']
            for points in points_list:
                cv2.circle(img_anno_point, (int(points['x']), int(points['y'])), 3, (0, 0, 255), -1)

            # 绘制 mask
            mask = points2mask(points_list)
            cv2.rectangle(img_anno_mask, mask['lt_point'], mask['rb_point'], (0, 0, 255), 2)

        # 绘制 mask
        if det_anno_path:
            mask_data = eval(load_xml(det_anno_path.format(mark['image']))['mask'])
            mask_img = img.copy()
            for mask in mask_data:
                cv2.rectangle(mask_img, mask['lt_point'], mask['rb_point'], (0, 0, 255), 2)
            cv2.imshow('mask_img_{}'.format(mark['image']), mask_img)

        # 显示图像
        cv2.imshow('img_{}'.format(mark['image']), img)
        cv2.imshow('img_anno_point_{}'.format(mark['image']), img_anno_point)
        cv2.imshow('img_anno_mask_{}'.format(mark['image']), img_anno_mask)

    # 等待按键
    cv2.waitKey(0)
    cv2.destroyAllWindows()


""" 检查检测数据及其检测标签 """
def check_data_det(xml_path, img_path):
    # 导入 xml 文件
    data = load_xml(xml_path)

    # 根据 xml 文件中的 mask 信息，将其绘制到图像上


""" 原始标签转换为检测标签 """
def origin2det(xml_path, out_path):
    # 加载 xml 文件
    data = load_xml(xml_path)

    # 创建 xml 文件
    new_data = {
        'number': data['number'],
        'cls': data['tirads']
    }

    # 创建标注信息
    for mark in data['mark']:
        # 一张图片的标注
        if not mark['svg']:
            continue
        anno_all = json.loads(mark['svg'])

        new_data['mask'] = []
        for anno_once in anno_all:
            points_list = anno_once['points']
            new_data['mask'].append(points2mask(points_list))

        # 保存 xml 文件
        if data['tirads'] not in ['none', 'None', 'non', '', None]:
            save_xml(out_path.format(mark['image']), new_data)


def points2mask(points):
    # 找出所有点的最大最小坐标值
    points = np.array([(point['x'], point['y']) for point in points])
    min_x = np.min(points[:, 0])
    min_y = np.min(points[:, 1])
    max_x = np.max(points[:, 0])
    max_y = np.max(points[:, 1])

    # 创建 mask
    mask = {
        'lt_point': (min_x, min_y),
        'rb_point': (max_x, max_y),
    }
    return mask


""" 根据文件制作数据集 """
def make_dataset_by_mask(xml_path, out_path):
    files = os.listdir(xml_path)
    # 新建 txt 文件
    f1 = open(out_path, 'w')
    f2 = open(out_path.replace('mask', 'image'), 'w')

    for file in files:
        # 获取文件类型
        file_type = os.path.splitext(file)[1]
        # 判断文件后缀是否为.xml
        if file_type == '.xml':
            # 记录路径
            f1.write('{}\n'.format(os.path.join(xml_path, file)))
            f2.write('{}\n'.format(os.path.join(xml_path, file).replace('.xml', '.jpg').replace('det_annot', 'image')))

    # 关闭文件
    f1.close()
    f2.close()


""" 检查数据集文本文件 """
def check_dataset_txt(img_path, mask_path):
    # 读取 txt 文件
    f1 = open(img_path, 'r')
    f2 = open(mask_path, 'r')
    img_list = f1.readlines()
    mask_list = f2.readlines()

    # 检查数据集
    for img_path, mask_path in zip(img_list, mask_list):
        img_path = img_path.strip()
        mask_path = mask_path.strip()
        print(img_path, mask_path)

        # 导入 mask 数据
        mask_data = load_xml(mask_path)
        mask_data = eval(mask_data['mask'])

        # 导入图像
        img = cv2.imread(img_path)
        mask_img = img.copy()

        # 绘制 mask
        for mask in mask_data:
            cv2.rectangle(mask_img, mask['lt_point'], mask['rb_point'], (0, 0, 255), 2)

        # 显示图像
        cv2.imshow('img', img)
        cv2.imshow('mask', mask_img)
        cv2.waitKey(0)



