import xml.etree.ElementTree as ET

def indent(elem, level=0):
    i = "\n" + level*"\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def load_xml(xml_path):
    def walk_in_base(base):
        value = {}
        for index, item in enumerate(base):
            # 将其作为根节点进行遍历
            if item.tag not in value.keys():
                value[item.tag] = walk_in_base(item)

                # 如果输出是 dict 类型，则将其转换为 list
                if isinstance(value[item.tag], dict):
                    value[item.tag] = [value[item.tag]]

            else:
                # 如果已经存在，则将其转换为 list
                value[item.tag].append(walk_in_base(item))

            # 遍历到最后一层，将其值赋给 value
            if value[item.tag] == [{}]:
                value[item.tag] = item.text

        return value

    # 导入 xml 文件
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # 将 xml 文件导入为 dict
    data = walk_in_base(root)
    return data


def save_xml(xml_path, data_dict):
    # 创建 xml 文件
    root = ET.Element('root')
    tree = ET.ElementTree(root)

    for key, value in data_dict.items():
        # 创建子节点
        child = ET.Element(key)
        child.text = str(value)
        root.append(child)

    # 格式化 xml 文件
    indent(root)
    tree.write(xml_path, encoding='utf-8', xml_declaration=True)


def indent_xml(xml_path):
    # 导入 xml 文件
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # 更新 xml 文件
    indent(root)
    tree.write(xml_path, encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
    load_xml('../dataset/public/origin_flawR/96.xml')



