import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize
from core.file_manager import FileManager

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # 윈도우 크기 설정
        self.setFixedSize(900, 706)  # 창 크기를 900x706으로 설정

        # 배경 이미지 설정
        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap("ui/img/mainscreen.png"))
        self.background_label.setGeometry(0, 0, 900, 706)  # QLabel의 크기를 창 크기와 동일하게 설정
        self.background_label.setScaledContents(True)  # 이미지가 QLabel 크기에 맞게 조정되도록 설정

        # FileManager 인스턴스 생성
        self.file_manager = FileManager()

        # 버튼 간의 간격 및 위치 조정
        browse_button_x = 100  # 파일 선택 버튼의 X 좌표
        browse_button_y = 530  # 파일 선택 버튼의 Y 좌표
        delete_button_x = 450  # 파일 삭제 버튼의 X 좌표
        delete_button_y = 530  # 파일 삭제 버튼의 Y 좌표

        # 파일 선택 버튼
        browse_pixmap = QPixmap("ui/img/doc_del_button.png")
        browse_button_width = 284
        browse_button_height = 95
        self.browse_button = QPushButton(self)
        self.browse_button.setFixedSize(browse_button_width, browse_button_height)  # 버튼 크기를 이미지 크기로 설정
        self.browse_button.setStyleSheet(f"""
            QPushButton {{
                border: none;
                background: transparent;
                image: url(ui/img/doc_del_button.png);
            }}
        """)
        self.browse_button.move(browse_button_x, browse_button_y)  # 원하는 위치로 이동
        self.browse_button.clicked.connect(self.browse_file)

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
        self.delete_button.move(delete_button_x, delete_button_y)  # 원하는 위치로 이동
        self.delete_button.clicked.connect(self.delete_file)

    def browse_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "파일 선택", "",
                                                   "Office Files (*.docx *.xlsx *.pptx *.hwp);;All Files (*)", options=options)
        if file_name:
            QMessageBox.information(self, "파일 선택", f"선택한 파일: {file_name}")
            self.selected_file = file_name

    def delete_file(self):
        if hasattr(self, 'selected_file') and self.selected_file:
            result = self.file_manager.delete_file_and_artifacts(self.selected_file)
            if result:
                QMessageBox.information(self, "성공", "파일 및 관련 아티팩트가 성공적으로 삭제되었습니다.")
            else:
                QMessageBox.warning(self, "실패", "파일 또는 아티팩트를 삭제하지 못했습니다.")
        else:
            QMessageBox.warning(self, "파일 선택 안됨", "먼저 파일을 선택해주세요.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
