from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap

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

        # 첫 번째 버튼 (Browse)
        browse_pixmap = QPixmap("ui/img/doc_data.png")
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
        self.browse_button.clicked.connect(self.do_nothing)  # 기본 동작 설정

        # 두 번째 버튼 (Delete)
        delete_pixmap = QPixmap("ui/img/image_data.png")
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
        self.delete_button.clicked.connect(self.do_nothing)  # 기본 동작 설정

    def do_nothing(self):
        # 이 메서드는 아무 작업도 하지 않음
        pass
