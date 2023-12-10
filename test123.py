from ui.image_cropper import ImageCropper
from PyQt5.QtWidgets import *
import sys

from ui.basic import MainWindow, CropperWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageCropper()
    window.show()
    window.set_img('./dataset/Kaggle/archive/69_2.jpg')
    sys.exit(app.exec_())
