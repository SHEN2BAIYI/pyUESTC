import os


# 遍历文件夹
for file in os.listdir('./dataset/public/origin_flawR'):
    # 获取文件名
    file_name = os.path.splitext(file)[0]
    # 获取文件后缀
    file_type = os.path.splitext(file)[1]
    # 判断文件后缀是否为.xml
    if file_type == '.xml':
        # 将文件移动到指定文件夹
        os.rename('./dataset/public/origin_flawR/{}'.format(file),
                  './dataset/public/origin_flawR/ori_annot/{}'.format(file))

    if file_type == '.jpg':
        os.rename('./dataset/public/origin_flawR/{}'.format(file),
                  './dataset/public/origin_flawR/image/{}'.format(file))


