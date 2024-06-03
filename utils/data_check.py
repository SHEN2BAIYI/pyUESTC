import os, sys, cv2, json
import numpy as np
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

from PIL import Image
from segmentation_mask_overlay import overlay_masks
from mmengine.fileio import dump

from utils.use_xml import *


def check_voc_mask(img_folder, xml_folder):
    # 遍历圖像文件夾
    for file in os.listdir(img_folder):
        # 判斷是否為圖像文件
        if file.endswith('.jpg') or file.endswith('.png'):
            # 導入圖像
            img_path = os.path.join(img_folder, file)
            img = cv2.imread(img_path)
            if img is None:
                print('Error: image {} is not exist.'.format(img_path))
                continue

            # 導入 xml 文件
            xml_path = os.path.join(xml_folder, file.replace('.jpg', '.xml'))
            xml_data = load_xml(xml_path)

            # 繪製 mask
            mask_img = img.copy()
            if xml_data['object']:
                if isinstance(xml_data['object'], dict):
                    xml_data['object'] = [xml_data['object']]
                for mask in xml_data['object']:
                    cv2.rectangle(mask_img,
                                  (int(mask['bndbox']['xmin']), int(mask['bndbox']['ymin'])),
                                  (int(mask['bndbox']['xmax']), int(mask['bndbox']['ymax'])),
                                  (0, 0, 255), 2)

            # 顯示圖像
            cv2.imshow('img', img)
            cv2.imshow('mask', mask_img)
            cv2.waitKey(0)


""" 標簽轉換： voc label -> coco label """
def voc2coco(voc_root, out_file, categories):
    """
    :param voc_root: voc 数据集根目录
    :param out_file: 輸出根目錄
    :param categories: 類別字典 {name: id}
    :return:
    """
    annotations = []
    images = []
    obj_count = 0

    # 遍历文件夹
    for idx, file in enumerate(os.listdir(voc_root)):
        # 導入 xml 文件
        xml_path = os.path.join(voc_root, file)
        xml_data = load_xml(xml_path)

        # 添加圖像數據
        images.append(
            dict(
                id=idx, file_name=xml_data['filename'],
                height=int(xml_data['size']['height']),
                width=int(xml_data['size']['width'])
            )
        )

        # 添加標注數據
        if xml_data['object'] is not None:
            if isinstance(xml_data['object'], dict):
                xml_data['object'] = [xml_data['object']]

            for _, obj in enumerate(xml_data['object']):
                annotations.append(
                    dict(
                        id=obj_count,
                        image_id=idx,
                        category_id=categories[obj['name']],
                        iscrowd=0,
                        bbox=[int(obj['bndbox']['xmin']), int(obj['bndbox']['ymin']),
                              int(obj['bndbox']['xmax']) - int(obj['bndbox']['xmin']),
                              int(obj['bndbox']['ymax']) - int(obj['bndbox']['ymin'])],
                        area=(int(obj['bndbox']['xmax']) - int(obj['bndbox']['xmin'])) * (int(obj['bndbox']['ymax']) - int(obj['bndbox']['ymin'])),
                        segmentation=[int(obj['bndbox']['xmin']), int(obj['bndbox']['ymin']),
                                      int(obj['bndbox']['xmin']), int(obj['bndbox']['ymax']),
                                      int(obj['bndbox']['xmax']), int(obj['bndbox']['ymax']),
                                      int(obj['bndbox']['xmax']), int(obj['bndbox']['ymin'])]

                    )
                )
                obj_count += 1

    categories = [{'id': y, 'name': x} for x, y in categories.items()]
    # coco json
    coco_json = dict(
        images=images,
        annotations=annotations,
        categories=categories
    )

    dump(coco_json, out_file)





