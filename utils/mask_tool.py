import cv2
import numpy as np

def generate_colors(n_colors, seed=47):
    """
    随机生成颜色
    """
    np.random.seed(seed)
    color_list = [
        (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))
        for _ in range(n_colors)
    ]
    return color_list

def draw_mask_layers(image, mask_layers, mask_tk=1):
    """
        绘制多层的mask，包含mask的边界，mask中不同值表示不同的instance
    :param image: 3 通道图像
    :param mask_layers: 多instance的mask
    :param mask_tk: 边界的厚度
    :return: 绘制边界框
    """
    img_copy = np.copy(image)

    # 拆分Mask
    h, w = mask_layers.shape[:2]
    mask_id = np.unique(mask_layers)[1:]  # 获取Mask的ID, 0是背景
    masks = []
    for i in mask_id:
        m = np.zeros((h, w), dtype=bool)
        m[mask_layers == i] = True
        masks.append(m)

    # 绘制颜色区域
    color_list = generate_colors(len(masks))
    for idx, mask in enumerate(masks):
        img_copy[mask] = color_list[idx]  # 绘制颜色

    image = cv2.addWeighted(image, 0.5, img_copy, 0.5, 0)  # 合并mask

    # 绘制边界，边界不需要透视效果
    for idx, mask in enumerate(masks):
        cnt_mask = np.zeros((h, w))
        cnt_mask[mask] = 255
        cnt_mask = cnt_mask.astype(np.uint8)
        contours, _ = cv2.findContours(cnt_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(image, contours, -1, (255, 255, 255), mask_tk)  # 绘制白色边界

    return image

def seg2color(mask):
    """
        绘制mask，包含mask的边界，mask中不同值表示不同的instance
    :param mask: 单instance的mask
    :return: 绘制边界框
    """

    seg_color = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)
    seg_id = np.unique(mask)[1:]  # 获取Mask的ID, 0是背景
    color_list = generate_colors(len(seg_id))

    for idx, key in enumerate(seg_id):
        seg_color[mask == key] = color_list[idx]

    return seg_color


if __name__ == '__main__':
    # 导入灰度图
    image1 = cv2.imread('C:\\Users\\shens\\Desktop\\MRBrainS13DataNii\\TrainingData\\1\\images\\1_27.jpg')
    # 导入mask
    mask1 = cv2.imread('C:\\Users\\shens\\Desktop\\MRBrainS13DataNii\\TrainingData\\1\\labels\\1_27.jpg', 0)



