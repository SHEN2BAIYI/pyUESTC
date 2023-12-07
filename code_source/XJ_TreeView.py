# 【XJ_TreeView.py】
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QModelIndex, QItemSelectionModel, pyqtSignal
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import *


class XJ_TreeView(QTreeView):
    class XJ_Iter:
        def __init__(self, iter):
            self.__iter = iter

        def AppendRow(self, data):  # 添加数据(一个列表
            lst = []
            for i in data:
                lst.append(QStandardItem(str(i)))
                lst[-1].setEditable(False)
            self.__iter.appendRow(lst)
            return XJ_TreeView.XJ_Iter(lst[0])

        def Copy(self):
            return XJ_TreeView.XJ_Iter(self.__iter)

        def Back(self):  # 返回上一级(返回失败则返回false
            if (type(self.__iter) == QStandardItemModel):
                return False
            if (self.__iter.parent() == None):
                self.__iter = self.__iter.model()
            else:
                self.__iter = self.__iter.parent()
            return True

        def Next(self, i):  # 进入下一级(进入失败则返回false
            if (0 <= i < self.__iter.rowCount()):
                if (type(self.__iter) != QStandardItemModel):
                    self.__iter = self.__iter.child(i, 0)
                else:
                    self.__iter = self.__iter.itemFromIndex(self.__iter.index(i, 0))
                return True
            else:
                return False

        def GetData(self):  # 获取数据(一个列表
            if (type(self.__iter) != QStandardItem):
                return None
            result = []
            model = self.__iter.model()
            index = self.__iter.index().siblingAtColumn(0)
            i = 1
            while (index.isValid()):
                result.append(model.itemFromIndex(index).text())
                index = index.siblingAtColumn(i)
                i += 1
            return result

        def SetData(self, i, data):  # 设置第i个单元格的内容(设置失败则返回false
            if (type(self.__iter) == QStandardItemModel):
                return False
            model = self.__iter.model()
            index = self.__iter.index().siblingAtColumn(i)
            if (index.isValid() == False):
                return False
            item = model.itemFromIndex(index)
            item.setText(str(data))
            return True

        def SetFont(self, i, font):  # 设置第i个单元格的字体样式(设置失败则返回false
            if (type(self.__iter) == QStandardItemModel):
                return False
            model = self.__iter.model()
            index = self.__iter.index().siblingAtColumn(i)
            item = model.itemFromIndex(index)
            item.setFont(font)
            return True

        def SetCheckable(self, flag):  # 设置是否显示复选框(设置失败则返回false)，复选框为双态
            if (type(self.__iter) == QStandardItemModel):
                return False
            self.__iter.setCheckable(flag)
            if (flag == False):
                self.__iter.setCheckState(-1)
            return True

        def GetCheckable(
                self):  # 获取复选框状态(如果获取失败则返回false)，返回结果为：【全选：Qt.Checked(2)、部分选：Qt.PartiallyChecked(1)、不选：Qt.Unchecked(0)】
            if (type(self.__iter) == QStandardItemModel):
                return None
            return self.__iter.checkState()

        def SetEditable(self, i, flag):  # 设置第i个单元格可以双击修改(设置失败则返回false
            if (type(self.__iter) == QStandardItemModel):
                return False
            model = self.__iter.model()
            index = self.__iter.index().siblingAtColumn(i)
            item = model.itemFromIndex(index)
            item.setEditable(flag)
            return True

    doubleClicked = pyqtSignal(XJ_Iter)  # 槽信号，当前行双击时发送信号（如果行未发生变化则不发送

    def __init__(self, parent=None):
        super(XJ_TreeView, self).__init__(parent)
        model = QStandardItemModel(self)
        self.setModel(model)
        self.headerLables = []
        self.__currIndex = None  # 用于判定选中行是否发生变化

    def GetHead(self):  # 返回根部迭代器
        return XJ_TreeView.XJ_Iter(self.model())

    def Clear(self):
        width = []
        for i in range(self.model().columnCount()):
            width.append(self.columnWidth(i))
        self.model().clear()
        self.model().setHorizontalHeaderLabels(self.headerLables)
        for i in range(len(width)):
            self.setColumnWidth(i, width[i])

    def SetHeaderLabels(self, labels):  # 设置列头
        self.headerLables = labels
        self.model().setHorizontalHeaderLabels(labels)

    def GetCurrIter(self):  # 获取当前行的迭代器
        return XJ_TreeView.XJ_Iter(self.model().itemFromIndex(self.currentIndex()))

    def mouseDoubleClickEvent(self, event):
        currIndex = self.currentIndex()
        self.setCurrentIndex(currIndex)

        if (self.__currIndex != currIndex):
            self.__currIndex = currIndex
            self.doubleClicked.emit(self.GetCurrIter())
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    tv = XJ_TreeView()
    tv.show()

    print(tv.GetCurrIter().GetData())

    iter = tv.GetHead()
    iter.AppendRow(['AAA', '333']).AppendRow(['AAAAA', ''])
    iter.AppendRow(['BBB', '222'])
    iter.AppendRow(['CCC', '111'])

    print(tv.GetCurrIter().GetData())

    tv.doubleClicked.connect(lambda line: print(line.GetData()))
    sys.exit(app.exec())
