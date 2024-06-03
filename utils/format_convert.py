"""
    数据格式的转换，主要作用是将自己的数据格式转换为 coco 或者 voc 标准数据格式。
"""
import os
import cv2
import time
import shutil
import openpyxl
import numpy as np
import nibabel as nib

from PIL import Image

from utils.matrix_eval import SegmentationMatrix
from utils.use_xml import *
from utils.mask_tool import *

############################
###     NJ医院数据转换     ###
############################

""" 根据NJ医院数据制作类别标签(.txt) """
def make_cls_txt_by_hospital_data(folder_path, save_path):
    """
        根据NJ医院数据制作类别标签(.txt)，没有通用性。

    :param folder_path: 文件夹路径，如：'./dataset/private/flaw_removed'
    :param save_path: 保存路径，如：'./cls.txt'
    :return:
    """

    # 根据文件名制作类别标签
    cls = {}

    # 遍历医院数据文件夹
    for file in os.listdir(folder_path):
        # 判断是否为文件夹
        if os.path.isdir(os.path.join(folder_path, file)):
            # 进入该文件夹下的 'cls' 文件夹，并判断该文件夹是否存在
            cls_folder = os.path.join(folder_path, file, 'cls')
            if not os.path.exists(cls_folder):
                continue

            # 寻找 'cls' 文件夹下的 txt 文件
            for cls_file in os.listdir(cls_folder):
                # 判断文件后缀是否为.txt
                if os.path.splitext(cls_file)[1] == '.txt':
                    # 读取 txt 文件
                    f = open(os.path.join(cls_folder, cls_file), 'r')
                    lines = f.readlines()
                    f.close()

                    # 将 txt 文件中的内容添加到 cls 中
                    for line in lines:
                        line = line.strip()
                        if line:
                            if line in ['1', '2', '3']:
                                cls[line] = 'benign'
                            else:
                                cls[line] = 'malignant'

    # 将字典写入文件
    if save_path:
        f = open(save_path, 'w')
        for key, value in cls.items():
            f.write('{} {}\n'.format(key, value))
        f.close()


""" 规范NJ医院数据中的文件名 """
def std_name_in_folder(folder_path):
    """
        规范NJ医院数据中的文件名。

    :param folder_path: 文件夹路径，如：'./dataset/private/flaw_removed'
    :return:
    """
    # 遍历文件夹
    for file in os.listdir(folder_path):
        # 将文件名中中文字符替换为英文字符
        new_file = file.replace('（', '(').replace('）', ')').replace('，', ',').replace('：', ':').replace('；', ';')
        # 去除空格
        new_file = new_file.replace(' ', '')

        # 重命名文件
        if file != new_file:
            print('Rename {} to {}'.format(file, new_file))
            os.rename(os.path.join(folder_path, file),
                      os.path.join(folder_path, new_file))


""" 根据NJ医院数据制作检测标签(voc) """
def seg2voc(img_folder_path, mask_folder_path, out_path, cls_file_path):
    """
        根据分割标签制作检测标签，并且将数据转换为 voc 格式。因为分割标签没有类别信息，
    所以需要提供类别信息(使用文件名匹配)。

    :param img_folder_path: 图像文件夹路径，如：'./dataset/private/flaw_removed'
    :param mask_folder_path: 分割标签文件夹路径，如：'./dataset/private/labels'
    :param out_path: voc 格式数据保存路径，如：'./dataset/private/voc'
    :param cls_file_path: 分类文件路径，如：'./cls.txt'
    :return:
    """

    # 读取类别信息
    cls = {}
    with open(cls_file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line:
                line = line.split(' ')
                if line[-1] in ['1', '2', '3']:
                    cls[int(line[0])] = 'benign'
                else:
                    cls[int(line[0])] = 'malignant'

    # 遍历医院数据文件夹
    for file in os.listdir(img_folder_path):
        # 判断是否为图片
        if file.endswith('.jpg') or file.endswith('.png'):
            # 导入图像
            img_path = os.path.join(img_folder_path, file)
            img = cv2.imread(img_path)
            if img is None:
                print('Error: image {} is not exist.'.format(img_path))
                continue

            # 导入 mask 图像
            try:
                mask = np.array(Image.open(
                    os.path.join(mask_folder_path, file.replace('.jpg', '.png'))
                ).convert('L'))
            except FileNotFoundError:
                mask = None

            # 将分割 mask 转换为 voc 检测 mask
            new_data = {
                'folder': img_folder_path,
                'filename': file,
                'path': img_path,
                'source': {
                    'database': 'NanJiang Hospital'
                },
                'size': {
                    'width': img.shape[1],
                    'height': img.shape[0],
                    'depth': img.shape[2]
                },
                'segmented': 1,
                'object': []
            }

            # 创建标注信息
            if mask is not None:
                unique = np.unique(mask)
                for key in unique:
                    if key:
                        new_mask = np.zeros_like(mask)
                        new_mask[mask == key] = 1

                        # 获取 mask 区域的坐标
                        coords = np.where(new_mask == 1)
                    else:
                        continue

                    # 獲得 name
                    if '(' in file:
                        name_key = file.split('(')[0]
                    else:
                        name_key = file.split('.')[0]

                    # 导入 mask 数据
                    child = {
                        'name': cls[int(name_key)] if cls_file_path else 'mask',
                        'pose': 'Unspecified',
                        'truncated': 0,
                        'difficult': 0,
                        'bndbox': {
                            'xmin': np.min(coords[1]),
                            'ymin': np.min(coords[0]),
                            'xmax': np.max(coords[1]),
                            'ymax': np.max(coords[0]),
                        }
                    }
                    new_data['object'].append(child)

            # 保存 xml 文件
            save_xml(os.path.join(out_path, file.replace('.jpg', '.xml')), new_data, True)


############################
###      MRbrainS18      ###
############################

""" 将 MRI 公共数据集数据从 nii 格式分割成一系列图片 """
def split_nii_to_img(img_nii_path, label_nii_path, out_folder, target_id,
                     img_format='bmp', show=False, load_again=False):
    """
        将 MRI 公共数据集数据从 nii 格式分割成一系列图片。
    """
    # 删除非空文件夹
    if os.path.exists(out_folder):
        shutil.rmtree(out_folder)

    # 创建输出文件夹
    if not os.path.exists(out_folder):
        os.makedirs(os.path.join(out_folder, 'images'))
        os.makedirs(os.path.join(out_folder, 'labels'))
        os.makedirs(os.path.join(out_folder, 'labels_color'))

        # 前景背景分割
        os.makedirs(os.path.join(out_folder, 'labels2'))
        os.makedirs(os.path.join(out_folder, 'labels2_color'))

        # 分割图例无标签区域去除
        os.makedirs(os.path.join(out_folder, 'images_no_bg'))

    # 导入 nii 文件
    img = nib.load(img_nii_path)
    img_fdata = img.get_fdata()

    label = nib.load(label_nii_path)
    label_fdata = label.get_fdata()

    assert img_fdata.shape == label_fdata.shape

    # 遍历 nii 文件中的每一张图片
    for i in range(img_fdata.shape[2]):
        # 标签颜色化
        label_color = seg2color(label_fdata[:, :, i])

        # 前景背景分割
        label2 = np.zeros_like(label_fdata[:, :, i])
        label2[label_fdata[:, :, i] > 0] = 1
        label2_color = seg2color(label2)

        # 保存
        img_store_path = os.path.join(out_folder, 'images/{}_{}.{}'.format(target_id, i, img_format))
        label_store_path = os.path.join(out_folder, 'labels/{}_{}.{}'.format(target_id, i, img_format))
        label_store_path_color = os.path.join(out_folder, 'labels_color/{}_{}.{}'.format(target_id, i, img_format))
        label2_store_path = os.path.join(out_folder, 'labels2/{}_{}.{}'.format(target_id, i, img_format))
        label2_store_path_color = os.path.join(out_folder, 'labels2_color/{}_{}.{}'.format(target_id, i, img_format))
        img_store_path_no_bg = os.path.join(out_folder, 'images_no_bg/{}_{}.{}'.format(target_id, i, img_format))

        cv2.imwrite(img_store_path, img_fdata[:, :, i])
        cv2.imwrite(label_store_path, label_fdata[:, :, i])
        cv2.imwrite(label_store_path_color, label_color)
        cv2.imwrite(label2_store_path, label2)
        cv2.imwrite(label2_store_path_color, label2_color)
        cv2.imwrite(img_store_path_no_bg, img_fdata[:, :, i] * label2)

        if show:
            cv2.imshow('img', img_fdata[:, :, i].astype(np.uint8))
            cv2.imshow('label', label_fdata[:, :, i])
            cv2.imshow('label_color', label_color)
            cv2.imshow('label2', label2)
            cv2.imshow('label2_color', label2_color)
            cv2.imshow('img_no_bg', img_fdata[:, :, i] * label2)

            if load_again:
                img = cv2.imread(img_store_path, 0)
                label = cv2.imread(label_store_path, 0)
                label_color = cv2.imread(label_store_path_color)
                label2 = cv2.imread(label2_store_path, 0)
                label2_color = cv2.imread(label2_store_path_color)
                img_no_bg = cv2.imread(img_store_path_no_bg, 0)

                label = seg2color(label)
                label2 = seg2color(label2)
                cv2.imshow('img_again', img)
                cv2.imshow('label_again', label)
                cv2.imshow('label_color_again', label_color)
                cv2.imshow('label2_again', label2)
                cv2.imshow('label2_color_again', label2_color)
                cv2.imshow('img_no_bg_again', img_no_bg)

            cv2.waitKey(0)
            cv2.destroyAllWindows()


""" 将 MRI 公共数据集标签从 8 类标签转换为 3 类标签 """
def convert_mri_label(label):
    """
        将 MRI 公共数据集标签从 8 类标签转换为 3 类标签。

    :param label: 原始标签
    :return: 转换后的标签
    """
    # 读取 nii
    label = nib.load(label)
    label_affine = label.affine
    label_fdata = label.get_fdata()

    # 将标签转换为 3 类
    label_fdata[label_fdata == 1] = 2
    label_fdata[label_fdata == 2] = 2
    label_fdata[label_fdata == 3] = 3
    label_fdata[label_fdata == 4] = 3
    label_fdata[label_fdata == 5] = 1
    label_fdata[label_fdata == 6] = 1
    label_fdata[label_fdata == 7] = 0
    label_fdata[label_fdata == 8] = 0
    label_fdata[label_fdata == 9] = 0
    label_fdata[label_fdata == 10] = 0

    # 保存 nii
    nib.Nifti1Image(label_fdata, label_affine).to_filename(label.get_filename().replace('.nii', '_new.nii'))


############################
###      SPM 分割结果     ###
############################

""" 将 SPM 分割结果转换为层图片并保存、评价、统计 """
def split_nii_to_img_and_eval(pred_nii_path, label_nii_path, out_folder=None,
                              img_format='bmp', show=False):

    # 创建输出文件夹及 excel 文件
    if out_folder:
        if not os.path.exists(out_folder):
            os.makedirs(out_folder)

        # 创建 excel 文件
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.title = 'result'

    # 导入 nii 文件
    pred = nib.load(pred_nii_path)
    pred_fdata = pred.get_fdata()

    label = nib.load(label_nii_path)
    label_fdata = label.get_fdata()

    assert pred_fdata.shape == label_fdata.shape

    # 遍历 nii 文件中的每一张图片
    for i in range(label_fdata.shape[-1]):
        label_slice = label_fdata[:, :, i]
        pred_slice = np.flip(np.rot90(np.round(pred_fdata[:, :, i])), axis=0) * np.clip(label_slice, 0, 1)

        labels = np.unique(label_slice)
        if len(labels) < 4:
            continue

        # 评价
        matrix = SegmentationMatrix(num_classes=4)
        matrix.add_batch(pred_slice, label_slice, [])
        print(matrix.dice_coefficient())

        # 保存
        if out_folder:
            # 保存评价数据
            dice = list(matrix.dice_coefficient())
            dice.insert(0, i)
            sheet.append(dice)

            # 保存图片
            cv2.imwrite(os.path.join(out_folder, '{}.{}'.format(i, img_format)),
                        pred_slice)

        if show:
            cv2.imshow('pred', seg2color(pred_slice))
            cv2.imshow('label', seg2color(label_slice))

            cv2.waitKey(0)
            cv2.destroyAllWindows()

    if out_folder:
        time_info = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        wb.save(os.path.join(out_folder, 'result_{}.xlsx'.format(time_info)))


def test_split_nii_to_img_and_eval():
    codes = [
        '20240202142250',
        '20240202142553',
        '20240202143027',
        '20240202143454',
        '20240202143630'
    ]
    base_path = 'C:/Users/shens/Desktop/data/v3/3/split/images_inhomogeneity/{}'
    pred_nii = os.path.join(base_path, 'mri/p0T1.nii')
    label_nii = 'C:/Users/shens/Desktop/data/v3/3/Label_new.nii'
    out_folder = os.path.join(base_path, 'seg/spm')

    for code in codes:
        split_nii_to_img_and_eval(pred_nii.format(code), label_nii,
                                  out_folder=out_folder.format(code),
                                  show=False)


############################
###      FSL 分割结果     ###
############################

""" 将 FSL 分割结果转换为层图片并保存、评价、统计 """
def split_nii_to_img_and_eval_by_fsl(pred_nii_path, label_nii_path, out_folder=None,
                                     img_format='bmp', show=False):

    # 创建输出文件夹及 excel 文件
    if out_folder:
        if not os.path.exists(out_folder):
            os.makedirs(out_folder)

        # 创建 excel 文件
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.title = 'result'

    # 导入 nii 文件
    pred = nib.load(pred_nii_path)
    pred_fdata = pred.get_fdata()

    label = nib.load(label_nii_path)
    label_fdata = label.get_fdata()

    assert pred_fdata.shape == label_fdata.shape

    # 遍历 nii 文件中的每一张图片
    for i in range(label_fdata.shape[-1]):
        label_slice = label_fdata[:, :, i]
        pred_slice = np.flip(np.rot90(pred_fdata[:, :, i]), axis=0)

        labels = np.unique(label_slice)
        if len(labels) < 4:
            continue

        # 评价
        matrix = SegmentationMatrix(num_classes=4)
        matrix.add_batch(pred_slice, label_slice, [])
        print(matrix.dice_coefficient())

        # 保存
        if out_folder:
            # 保存评价数据
            dice = list(matrix.dice_coefficient())
            dice.insert(0, i)
            sheet.append(dice)

            # 保存图片
            cv2.imwrite(os.path.join(out_folder, '{}.{}'.format(i, img_format)),
                        pred_slice)

        if show:
            cv2.imshow('pred', seg2color(pred_slice))
            cv2.imshow('label', seg2color(label_slice))

            cv2.waitKey(0)
            cv2.destroyAllWindows()

    if out_folder:
        time_info = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        wb.save(os.path.join(out_folder, 'result_{}.xlsx'.format(time_info)))


def test_split_nii_to_img_and_eval_by_fsl():
    codes = [
        '20240202142250',
        '20240202142553',
        '20240202143027',
        '20240202143454',
        '20240202143630'
    ]
    base_path = 'C:/Users/shens/Desktop/data/v3/9/split/images_no_bg_inhomogeneity/{}'
    pred_nii = os.path.join(base_path, 'fsl/T1_seg.nii.gz')
    label_nii = 'C:/Users/shens/Desktop/data/v3/9/Label_new.nii'
    out_folder = os.path.join(base_path, 'seg/fsl')

    for code in codes:
        split_nii_to_img_and_eval_by_fsl(pred_nii.format(code), label_nii,
                                         out_folder=out_folder.format(code),
                                         show=False)


if __name__ == '__main__':

    # # 将 MRI 公共数据集数据从 nii 格式分割成一系列图片
    # for i in range(1, 2):
    #     print(i)
    #     split_nii_to_img(
    #         'C:/Users/shens/Desktop/data/v1/{}/T1.nii'.format(i),
    #         'C:/Users/shens/Desktop/data/v1/{}/Label_new.nii'.format(i),
    #         'C:/Users/shens/Desktop/data/v1/{}/split'.format(i),
    #         i, 'bmp',
    #         # True, True
    #     )
    #
    # # convert_mri_label(
    # #     'C:/Users/shens/Desktop/data/9/Label.nii',
    # # )
    #
    # print('Done.')

    # test_split_nii_to_img_and_eval()
    test_split_nii_to_img_and_eval_by_fsl()