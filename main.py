import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap
from doc_del_ui import DocDelWindow  # DocDelWindow로 변경
from sen_data_main import SenDataMainWindow  # sen_data_main에서 SenDataMainWindow 직접 가져오기


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

        self.setFixedSize(900, 706)

        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap("ui/img/mainscreen.png"))
        self.background_label.setGeometry(0, 0, 900, 706)
        self.background_label.setScaledContents(True)

        # Browse button setup
        browse_button_x = 100
        browse_button_y = 530
        browse_button_width = 290
        browse_button_height = 90
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
        self.browse_button.clicked.connect(self.open_doc_del_ui_window)

        # Delete button setup
        delete_button_x = 440
        delete_button_y = 530
        delete_button_width = 360
        delete_button_height = 90
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
        self.delete_button.clicked.connect(self.open_sen_data_main_window)

    def open_browse_window(self):
        self.browse_window = BrowseWindow()
        self.browse_window.show()

    def open_doc_del_ui_window(self):
        # doc_del_ui.py의 DocDelWindow 클래스를 사용하여 새 창 열기
        self.doc_del_ui_window = DocDelWindow()
        self.doc_del_ui_window.show()

    def open_sen_data_main_window(self):
        # sen_data_main.py의 SenDataMainWindow 클래스를 사용하여 새 창 열기
        self.sen_data_main_window = SenDataMainWindow()
        self.sen_data_main_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
