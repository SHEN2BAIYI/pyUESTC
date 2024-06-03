from utils.data_check import *

# make_det_anno_by_hospital_data_voc(
#     './dataset/private/',
#     './dataset/private/voc',
#     'flaw_removed',
#     'labels',
#     './cls.txt'
# )


# check_voc_mask(
#     './dataset/private/flaw_removed',
#     './dataset/private/voc',
# )


# load_xml('./dataset/private/voc/105(1).xml')

voc2coco(
    './dataset/private/voc',
    './test.json',
    categories={
        'benign': 0,
        'malignant': 1,
    }
)
