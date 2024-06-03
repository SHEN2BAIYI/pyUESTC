import os
import cv2
import time

import numpy as np
import nibabel as nib
import SimpleITK as sitk
import random
import matplotlib.pyplot as plt


file_range = {
    '1': {
        'min': 13,
        'max': 32,
    },
    '2': {
        'min': 17,
        'max': 36,
    },
    '3': {
        'min': 14,
        'max': 36,
    },
    '4': {
        'min': 14,
        'max': 34,
    },
    '5': {
        'min': 10,
        'max': 35,
    },
    '6': {
        'min': 14,
        'max': 34,
    },
    '7': {
        'min': 16,
        'max': 32,
    },
    '8': {
        'min': 15,
        'max': 37,
    },
    '9': {
        'min': 14,
        'max': 38,
    },
}


def create_inhomogeneity(width, height, gray_range=0.5, order=1, params=None):
    """
        Creates an inhomogeneous numpy matrix.
    """
    # 根据 x 方向从 0 递增的矩阵
    x = np.zeros([height, width])
    for i in range(width):
        x[:, i] = i + 1

    # 根据 y 方向从 0 递增的矩阵
    y = np.zeros([height, width])
    for i in range(height):
        y[i, :] = i + 1

    if order == 1:
        z = order1(x, y)
    else:
        z = order2(x, y, params)

    z = np.ones_like(z) - (z - np.min(z)) / (np.max(z) - np.min(z)) * gray_range

    return z


# 一阶函数
def order1(x, y):
    """
        Z = AX + BY + C
    """
    a = random.choice([i for i in range(0, 10)])
    b = random.choice([i for i in range(0, 10)])
    c = random.choice([i for i in range(0, 20)])

    a_signal = random.choice([1, -1])
    b_signal = random.choice([1, -1])
    c_signal = random.choice([1, -1])

    z = a_signal * a * x + b_signal * b * y + c_signal * c

    return z


# 二阶函数
def order2(x, y, params=None):
    """
        Z = AX^2 + BY^2 + CXY + DX + EY + F
    """
    width, height = x.shape

    if not params:
        # 将该函数的最低点限制在图像内部
        a = random.choice([i for i in range(0, 10)])
        b = random.choice([i for i in range(0, 10)])
        c = random.choice([i for i in range(0, 10)])
        d = random.choice([i for i in range(0, 10 * width)])
        e = random.choice([i for i in range(0, 10 * height)])
        f = random.choice([i for i in range(0, 20)])

        a_signal = random.choice([1, -1])
        b_signal = random.choice([1, -1])
        c_signal = random.choice([1, -1])
    else:
        a = params['a']
        b = params['b']
        c = params['c']
        d = params['d']
        e = params['e']
        f = params['f']
        a_signal = params['a_signal']
        b_signal = params['b_signal']
        c_signal = params['c_signal']

    print(a, b, c, d, e, f)
    print(a_signal, b_signal, c_signal)

    z = a_signal * a * x ** 2 + b_signal * b * y ** 2 + c_signal * c * x * y + \
        -1 * a_signal * d * x + -1 * b_signal * e * y + f

    return z


def add_inhomogeneity_by_file(img_data, gray_range=0.9,
                              params=None, img_inhomogeneity=None, need_format=True):
    if img_inhomogeneity is not None:
        return np.round(img_data * img_inhomogeneity).astype(np.uint8), img_inhomogeneity
    ROI = img_data > 30
    # 获取 ROI 的四角坐标
    coords = np.where(ROI)
    y_min, y_max = np.min(coords[0]), np.max(coords[0])
    x_min, x_max = np.min(coords[1]), np.max(coords[1])

    roi_inhomogeneity = create_inhomogeneity(x_max-x_min+2, y_max-y_min+2,
                                             gray_range=gray_range, order=2, params=params)

    img_inhomogeneity = np.ones_like(img_data).astype(np.float64)
    img_inhomogeneity[y_min-1:y_max+1, x_min-1:x_max+1] = roi_inhomogeneity
    if not need_format:
        return np.round(img_data * img_inhomogeneity), img_inhomogeneity

    img_tmp = np.round(img_data * img_inhomogeneity).astype(np.uint8)
    return img_tmp, img_inhomogeneity


def add_inhomogeneity_by_folder(img_folder_path, store_folder_path, mask_folder_path=None, store_folder_path_extra=None,
                                gray_range=0.9, params=None, show=True, store=False):
    # mask_folder_path 和 store_folder_path_extra 同时为 None 或者同时不为 None
    assert (mask_folder_path is None and store_folder_path_extra is None) or \
            (mask_folder_path is not None and store_folder_path_extra is not None)

    img_list = os.listdir(img_folder_path)
    for img_name in img_list:
        img_path = os.path.join(img_folder_path, img_name)
        img = cv2.imread(img_path, 0)
        img_tmp, img_inhomogeneity = add_inhomogeneity_by_file(img, gray_range=gray_range, params=params)

        if mask_folder_path:
            mask_path = os.path.join(mask_folder_path, img_name)
            mask = np.clip(cv2.imread(mask_path, 0), 0, 1)

            img_no_bg_tmp = img_tmp * mask

        if show:
            cv2.imshow('img', img)
            cv2.imshow('img_tmp', img_tmp)
            if mask_folder_path:
                cv2.imshow('img_no_bg_tmp', img_no_bg_tmp)

            cv2.waitKey(0)
            cv2.destroyAllWindows()

        if store:
            if not os.path.exists(store_folder_path):
                os.makedirs(store_folder_path)
            cv2.imwrite(os.path.join(store_folder_path, img_name), img_tmp)

            if mask_folder_path:
                if not os.path.exists(store_folder_path_extra):
                    os.makedirs(store_folder_path_extra)
                cv2.imwrite(os.path.join(store_folder_path_extra, img_name), img_no_bg_tmp)


def run_by_all_folder():
    params = {
        'a': 4,
        'b': 5,
        'c': 2,
        'd': 318,
        'e': 811,
        'f': 11,
        'a_signal': -1,
        'b_signal': -1,
        'c_signal': 1,
    }

    key = True

    params = None

    time_info = time.strftime("%Y%m%d%H%M%S", time.localtime())

    for i in range(2, 10):
        print(i)
        img_folder = 'C:/Users/shens/Desktop/data/{}/split/images'.format(i)
        store_folder = 'C:/Users/shens/Desktop/data/{}/split/images_inhomogeneity/{}'.format(
            i, time_info
        )

        # img_no_bg_folder = 'C:/Users/shens/Desktop/data/{}/split/images_no_bg'.format(i)

        mask_folder = 'C:/Users/shens/Desktop/data/{}/split/labels'.format(i)
        store_folder_no_bg = 'C:/Users/shens/Desktop/data/{}/split/images_no_bg_inhomogeneity/{}'.format(
            i, time_info
        )

        add_inhomogeneity_by_folder(img_folder, store_folder, gray_range=0.9, params=params,
                                    mask_folder_path=mask_folder, store_folder_path_extra=store_folder_no_bg,
                                    show=key, store=not key)


def run_by_nii():
    params = {
        'a': 1,
        'b': 5,
        'c': 4,
        'd': 607,
        'e': 1288,
        'f': 7,
        'a_signal': -1,
        'b_signal': -1,
        'c_signal': -1,
    }

    # params = None

    time_info = time.strftime("%Y%m%d%H%M%S", time.localtime())

    for i in range(1, 10):
        print(i)
        img_nii_path = 'C:/Users/shens/Desktop/data/{}/T1.nii'.format(i)
        mask_nii_path = 'C:/Users/shens/Desktop/data/{}/Label_new.nii'.format(i)
        store_folder = 'C:/Users/shens/Desktop/data/{}/split/images_inhomogeneity/{}'.format(
            i, time_info
        )
        store_folder_no_bg = 'C:/Users/shens/Desktop/data/{}/split/images_no_bg_inhomogeneity/{}'.format(
            i, time_info
        )

        # 保存
        if not os.path.exists(store_folder):
            os.makedirs(store_folder)
        if not os.path.exists(store_folder_no_bg):
            os.makedirs(store_folder_no_bg)

        img = nib.load(img_nii_path)
        img_data = np.array(img.get_fdata()).transpose(2, 1, 0)
        mask = nib.load(mask_nii_path)
        mask_data = np.array(mask.get_fdata()).transpose(2, 1, 0)

        img_leak_data = img_data.copy()
        img_no_bg_data = np.zeros_like(img_data)
        for index, (img_layer, mask_layer) in enumerate(zip(img_data, mask_data)):
            img_tmp, _ = add_inhomogeneity_by_file(img_layer, gray_range=0.9, params=params, need_format=False)

            unique = np.unique(mask_layer)
            if len(unique) < 4 or index < file_range[str(i)]['min'] or index > file_range[str(i)]['max']:
                img_leak_data[index, :, :] = 0
            else:
                img_leak_data[index, :, :] = img_tmp
                img_no_bg_data[index, :, :] = img_tmp * np.clip(mask_layer, 0, 1)

                # 保存每一层的图像
                cv2.imwrite(os.path.join(store_folder, '{}_{}.bmp'.format(i, index)),
                            img_tmp.transpose(1, 0))
                cv2.imwrite(os.path.join(store_folder_no_bg, '{}_{}.bmp'.format(i, index)),
                            (img_tmp * np.clip(mask_layer, 0, 1)).transpose(1, 0))

            img_data[index, :, :] = img_tmp

        nib.Nifti1Image(img_no_bg_data.transpose(1, 2, 0), img.affine).to_filename(
            os.path.join(store_folder_no_bg, 'T1.nii'))
        nib.Nifti1Image(img_data.transpose(1, 2, 0), img.affine).to_filename(os.path.join(store_folder, 'T1.nii'))
        nib.Nifti1Image(img_leak_data.transpose(1, 2, 0), img.affine).to_filename(
            os.path.join(store_folder, 'T1_leak.nii'))


def test():
    nii_path = 'C:/Users/shens/Desktop/data/1/T1.nii'
    img = nib.load(nii_path)
    img_data = np.array(img.get_fdata()).transpose(0, 2, 1)

    # 保存
    nib.Nifti1Image(img_data, img.affine).to_filename('C:/Users/shens/Desktop/data/1/T1_1.nii')


if __name__ == '__main__':
    run_by_nii()
    # run_by_all_folder()



