import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QSlider, QFileDialog, QGraphicsView, QGraphicsScene, QWidget, QFrame, QPushButton
from PyQt5.QtGui import QPixmap, QPainter, QImage
from PyQt5.QtCore import Qt, QMimeData
from StyleTransferModel import StyleTransferModel as TModel
import cv2 as cv
import numpy as np

def convert_cv_to_Qt(cvImg):
    cvImg = (cvImg * 255).astype(np.uint8)
    height, width, channel = cvImg.shape
    bytesPerLine = 3 * width
    cv.cvtColor(cvImg, cv.COLOR_BGR2RGB, cvImg)
    qImg = QImage(cvImg.data, width, height, bytesPerLine, QImage.Format_RGB888)
    return QPixmap.fromImage(qImg)

class DropLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.Box)
        self.setAcceptDrops(True)
        self.has_image = False
        self.maxHeight = 400
        self.maxWidth = 400

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
            for url in e.mimeData().urls():
                self.openFile(url.toLocalFile())

            self.has_image = True
        else:
            e.ignore()

    def openFile(self, url):
        self.setMinimumSize(0, 0)
        pic = QPixmap(url)
        if pic.width() > self.maxWidth or pic.height() > self.maxHeight:
            self.setPixmap(pic.scaled(self.maxWidth, self.maxHeight, Qt.KeepAspectRatio))
        else: 
            self.setPixmap()
        
        self.imagePath = url

    def getImagePath(self):
        return self.imagePath

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.model = TModel()
   
    def initUI(self):
        # Utworzenie etykiet do wyświetlania obrazów
        self.left_label = DropLabel()
        self.left_label.setMinimumSize(300, 300)
        self.right_label = DropLabel()
        self.right_label.setMinimumSize(300, 300)
        self.center_label = QLabel()

        # Ustawienie etykiet jako miejsc do przeciągania i upuszczania
        self.left_label.setAcceptDrops(True)
        self.right_label.setAcceptDrops(True)

        # Utworzenie poziomego suwaka i podłączenie slotu do jego sygnału wartości zmienionej
        self.slider = QSlider(Qt.Horizontal)
        self.slider.valueChanged.connect(self.slider_value_changed)

        # Utworzenie obiektów do wyświetlania obrazów w środkowej etykiecie
        self.central_label = QLabel()
        self.central_label.setFrameShape(QFrame.Box)
        self.central_label.setMinimumSize(300, 300)

        self.start_process_btn = QPushButton()
        self.start_process_btn.setMinimumWidth(90)
        self.start_process_btn.setText('Transfer')
        self.start_process_btn.clicked.connect(self.transfer_btn_pushed)

        # Utworzenie layoutów i umieszczenie w nich elementów interfejsu
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.left_label)
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.right_label)
        center_layout = QVBoxLayout()
        center_layout.addWidget(self.central_label)
        slider_layout = QHBoxLayout()
        slider_layout.addWidget(self.slider)
        slider_layout.addWidget(self.start_process_btn)
        center_layout.addItem(slider_layout)
        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout)
        main_layout.addLayout(center_layout)
        main_layout.addLayout(right_layout)
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Ustawienie wymiarów okna i jego tytułu
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle("StyleTransfer")

    def slider_value_changed(self):
        # TO DO zmiana obrazka w środku

        return None

    def transfer_btn_pushed(self):
        if (self.left_label.has_image and self.right_label.has_image):
            pathL = self.left_label.getImagePath()
            pathR = self.right_label.getImagePath()
            imgL = cv.imread(pathL)
            imgR = cv.imread(pathR)
            self.model.set_content_image(imgL)
            self.model.set_style_image(imgR)
            res = self.model.transfer_image(self.slider.value())

            self.central_label.setPixmap(convert_cv_to_Qt(res))

        return None


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    
    window.show()
    
    sys.exit(app.exec_())
