import sys
from pathlib import Path
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QApplication
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from img_detect import ImageScanScreen  # img_detect.py의 ImageScanScreen 클래스
from doc_detect import DocumentScanScreen  # doc_detect.py의 DocumentScanScreen 클래스


class SenDataMainWindow(QMainWindow):
    def __init__(self):
        super(SenDataMainWindow, self).__init__()

        # 윈도우 설정
        self.setFixedSize(900, 706)
        self.setWindowTitle("Sensitive Data Detection")

        # 배경 이미지 설정
        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap("ui/img/mainscreen.png"))
        self.background_label.setGeometry(0, 0, 900, 706)
        self.background_label.setScaledContents(True)

        # 버튼 위치 및 크기 설정
        browse_button_x = 110
        browse_button_y = 530
        delete_button_x = 480
        delete_button_y = 530

        # 첫 번째 버튼 (Browse - doc_data.png)
        browse_button_width = 300
        browse_button_height = 95
        self.browse_button = QPushButton(self)
        self.browse_button.setFixedSize(browse_button_width, browse_button_height)
        self.browse_button.setStyleSheet(f"""
            QPushButton {{
                border: none;
                background: transparent;
                image: url(ui/img/doc_data.png);
            }}
        """)
        self.browse_button.move(browse_button_x, browse_button_y)
        self.browse_button.clicked.connect(self.open_doc_detect)

        # 두 번째 버튼 (Delete - image_data.png)
        delete_button_width = 310
        delete_button_height = 95
        self.delete_button = QPushButton(self)
        self.delete_button.setFixedSize(delete_button_width, delete_button_height)
        self.delete_button.setStyleSheet(f"""
            QPushButton {{
                border: none;
                background: transparent;
                image: url(ui/img/image_data.png);
            }}
        """)
        self.delete_button.move(delete_button_x, delete_button_y)
        self.delete_button.clicked.connect(self.open_img_detect)

    def open_doc_detect(self):
        # doc_detect.py의 DocumentScanScreen 창 열기
        self.doc_window = DocumentScanScreen()
        self.doc_window.show()

    def open_img_detect(self):
        # img_detect.py의 ImageScanScreen 창 열기
        self.img_window = ImageScanScreen()
        self.img_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = SenDataMainWindow()
    main_window.show()
    sys.exit(app.exec_())
