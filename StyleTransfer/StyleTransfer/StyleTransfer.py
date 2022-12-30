
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QSlider, QFileDialog, QGraphicsView, QGraphicsScene, QWidget, QFrame
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, QMimeData

class DropLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.Box)
        self.setAcceptDrops(True)

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
        else:
            e.ignore()

    def openFile(self, url):
        self.setMinimumSize(0, 0)
        self.setPixmap(QPixmap(url))
        self.imagePath = url

    def getImagePath(self):
        return self.imagePath

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
   
    def initUI(self):
        # Utworzenie etykiet do wyœwietlania obrazów
        self.left_label = DropLabel()
        self.left_label.setMinimumSize(100, 100)
        self.right_label = DropLabel()
        self.right_label.setMinimumSize(100, 100)
        self.center_label = QLabel()

        # Ustawienie etykiet jako miejsc do przeci¹gania i upuszczania
        self.left_label.setAcceptDrops(True)
        self.right_label.setAcceptDrops(True)

        # Utworzenie poziomego suwaka i pod³¹czenie slotu do jego sygna³u wartoœci zmienionej
        self.slider = QSlider(Qt.Horizontal)
        self.slider.valueChanged.connect(self.slider_value_changed)

        # Utworzenie obiektów do wyœwietlania obrazów w œrodkowej etykiecie
        self.view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setRenderHint(QPainter.SmoothPixmapTransform)
        self.view.setMinimumSize(100, 100)

        # Utworzenie layoutów i umieszczenie w nich elementów interfejsu
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.left_label)
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.right_label)
        center_layout = QVBoxLayout()
        center_layout.addWidget(self.view)
        center_layout.addWidget(self.slider)
        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout)
        main_layout.addLayout(center_layout)
        main_layout.addLayout(right_layout)
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Ustawienie wymiarów okna i jego tytu³u
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle("aaa")

    def slider_value_changed(self):
        # TO DO zmiana obrazka w œrodku

        return None

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()

    window.show()

    sys.exit(app.exec_())
