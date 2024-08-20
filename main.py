import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap

class BrowseWindow(QWidget):
    def __init__(self):
        super(BrowseWindow, self).__init__()

        self.setWindowTitle("Browse File")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()
        self.label = QLabel("This is the Browse File window", self)
        layout.addWidget(self.label)

        self.setLayout(layout)

class DeleteWindow(QWidget):
    def __init__(self):
        super(DeleteWindow, self).__init__()

        self.setWindowTitle("Delete File")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()
        self.label = QLabel("This is the Delete File window", self)
        layout.addWidget(self.label)

        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # 윈도우 크기 설정
        self.setFixedSize(900, 706)

        # 배경 이미지 설정
        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap("ui/img/mainscreen.png"))
        self.background_label.setGeometry(0, 0, 900, 706)
        self.background_label.setScaledContents(True)

        # 버튼 간의 간격 및 위치 조정
        browse_button_x = 100
        browse_button_y = 530
        delete_button_x = 450
        delete_button_y = 530

        # 파일 선택 버튼
        browse_pixmap = QPixmap("ui/img/doc_del_button.png")
        browse_button_width = 284
        browse_button_height = 95
        self.browse_button = QPushButton(self)
        self.browse_button.setFixedSize(browse_button_width, browse_button_height)
        self.browse_button.setStyleSheet(f"""
            QPushButton {{
                border: none;
                background: transparent;
                image: url(ui/img/doc_del_button.png);
            }}
        """)
        self.browse_button.move(browse_button_x, browse_button_y)
        self.browse_button.clicked.connect(self.open_browse_window)

        # 파일 삭제 버튼
        delete_pixmap = QPixmap("ui/img/sen_data_detec.png")
        delete_button_width = 367
        delete_button_height = 95
        self.delete_button = QPushButton(self)
        self.delete_button.setFixedSize(delete_button_width, delete_button_height)
        self.delete_button.setStyleSheet(f"""
            QPushButton {{
                border: none;
                background: transparent;
                image: url(ui/img/sen_data_detec.png);
            }}
        """)
        self.delete_button.move(delete_button_x, delete_button_y)
        self.delete_button.clicked.connect(self.open_delete_window)

    def open_browse_window(self):
        self.browse_window = BrowseWindow()
        self.browse_window.show()

    def open_delete_window(self):
        self.delete_window = DeleteWindow()
        self.delete_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
