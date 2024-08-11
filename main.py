import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from core.file_manager import FileManager
from ui.main_window import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()  # Ui_MainWindow의 인스턴스를 생성
        self.ui.setupUi(self)  # Ui_MainWindow의 setupUi를 호출

        self.file_manager = FileManager()

        # Signal-slot 연결
        self.ui.browseButton.clicked.connect(self.browse_file)
        self.ui.deleteButton.clicked.connect(self.delete_file)

    def browse_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "파일 선택", "", 
                                                   "Office Files (*.docx *.xlsx *.pptx *.hwp);;All Files (*)", options=options)
        if file_name:
            self.ui.filePathLineEdit.setText(file_name)

    def delete_file(self):
        file_path = self.ui.filePathLineEdit.text()
        if file_path:
            result = self.file_manager.delete_file_and_artifacts(file_path)
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
