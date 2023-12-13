from utils.data_check import *


if __name__ == '__main__':
    # check_data_origin('./dataset/public/origin_flawR/96.xml', './dataset/public/origin_flawR/96_{}.jpg', True)
    # origin2det('./dataset/public/origin_flawR/1.xml', './dataset/public/origin_flawR/det_annot/1_{}.xml')

    # for i in range(10, 650):
    #     try:
    #         path = './dataset/public/origin_flawR/{}.{}'
    #         img_path = path.format('image/{}_{}'.format(i, '{}'), 'jpg')
    #         xml_path = path.format('ori_annot/{}'.format(i), 'xml')
    #         out_path = path.format('det_annot/{}_{}'.format(i, '{}'), 'xml')
    #         print(xml_path, out_path)
    #         # origin2det(xml_path, out_path)
    #         check_data_origin(xml_path, img_path, False, out_path)
    #     except FileNotFoundError:
    #         continue

    # make_dataset_by_mask('./dataset/public/origin_flawR/det_annot', './dataset/public/origin_flawR/mask.txt')
    check_dataset_txt('./dataset/public/origin_flawR/image.txt', './dataset/public/origin_flawR/mask.txt')
