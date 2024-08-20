import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
    QFileDialog, QTextEdit, QFrame, QProgressBar
)
from PyQt5.QtGui import QPixmap, QMovie, QPalette, QColor, QFont, QIcon
from PyQt5.QtCore import Qt, QTimer


class ImageScanScreen(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the image scan screen
        self.setWindowTitle('Image Scan Screen')
        self.setFixedSize(1050, 700)  # 고정된 창 크기

        # Set white background
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(Qt.white))
        self.setPalette(palette)

        # Create main layout with fixed ratio 2:1
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)  # 여백 제거

        # 왼쪽 레이아웃: 스캔 버튼, 이미지 프레임, 로그 영역
        left_layout = QVBoxLayout()
        left_layout.setSpacing(0)  # 위젯 사이의 간격 제거

        # 왼쪽 컨테이너 설정
        left_widget = QWidget()
        left_widget.setStyleSheet("background-color: #FFFFE0;")
        left_widget.setLayout(left_layout)
        main_layout.addWidget(left_widget, stretch=2)

        # 이미지 스캔 버튼
        self.scan_button = QPushButton()
        self.scan_button.setFixedSize(200, 75)
        self.scan_button.setStyleSheet("background: transparent;")
        self.scan_button.setIcon(QIcon(r"ui/img/scan.png"))
        self.scan_button.setIconSize(self.scan_button.size())
        self.scan_button.setFont(QFont("Arial", 16, QFont.Bold))
        self.scan_button.clicked.connect(self.scan_images)
        left_layout.addWidget(self.scan_button, alignment=Qt.AlignLeft)

        # 이미지 표시를 위한 큰 프레임
        self.image_frame = QLabel()
        self.image_frame.setFrameStyle(QFrame.Box | QFrame.Sunken)
        self.image_frame.setAlignment(Qt.AlignCenter)
        self.image_frame.setFixedSize(700, 400)
        self.image_frame.setStyleSheet("background-color: white;")
        left_layout.addWidget(self.image_frame, alignment=Qt.AlignCenter)

        # 로그 영역
        self.log_area = QTextEdit()
        self.log_area.setFixedSize(700, 120)
        self.log_area.setReadOnly(True)
        self.log_area.setStyleSheet("background-color: white; color: black; font-weight: normal;")
        left_layout.addWidget(self.log_area)

        # "Yes/No" 버튼
        self.yes_button = QPushButton('예')
        self.no_button = QPushButton('아니오')
        self.yes_button.setVisible(False)
        self.no_button.setVisible(False)

        # 버튼 클릭 시 동작 설정
        self.yes_button.clicked.connect(self.delete_image)
        self.no_button.clicked.connect(self.cancel_deletion)

        # 버튼을 레이아웃에 추가
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.yes_button)
        button_layout.addWidget(self.no_button)
        left_layout.addLayout(button_layout)

        # 수직 분할선 추가
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.VLine)
        self.separator.setFrameShadow(QFrame.Sunken)
        self.separator.setLineWidth(1)
        self.separator.setStyleSheet("background-color: lightgray;")
        main_layout.addWidget(self.separator)

        # 오른쪽 레이아웃: 로딩 GIF, 완료 이미지 및 텍스트
        right_layout = QVBoxLayout()
        right_layout.setSpacing(0)

        # 완료 이미지를 위한 라벨
        self.completion_image = QLabel()
        completion_pixmap = QPixmap(r"ui/img/eraser.jpg").scaled(300, 300, Qt.KeepAspectRatio)
        self.completion_image.setPixmap(completion_pixmap)
        self.completion_image.setAlignment(Qt.AlignCenter)
        self.completion_image.setVisible(False)
        right_layout.addWidget(self.completion_image, alignment=Qt.AlignBottom)

        # 완료 텍스트를 위한 라벨
        self.completion_label = QLabel("완료되었습니다!", self)
        self.completion_label.setAlignment(Qt.AlignCenter)
        self.completion_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.completion_label.setVisible(False)
        right_layout.addWidget(self.completion_label, alignment=Qt.AlignTop)

        # 로딩 GIF 라벨
        self.loading_label = QLabel()
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setFixedSize(300, 300)
        right_layout.addWidget(self.loading_label, alignment=Qt.AlignCenter)

        # 프로그레스 바
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        right_layout.addWidget(self.progress_bar)

        # 로딩 라벨과 프로그레스 바를 처음에는 숨김
        self.progress_bar.hide()
        self.loading_label.hide()

        # 오른쪽 레이아웃을 메인 레이아웃에 추가
        main_layout.addLayout(right_layout, stretch=1)

        # 메인 레이아웃 설정
        self.setLayout(main_layout)

    def scan_images(self):
        # 스캔 버튼 클릭 시 로딩 GIF 및 프로그레스 바 표시
        self.show_loading_gif()
        self.progress_bar.setValue(0)
        self.progress_bar.show()

        # 파일 다이얼로그를 통해 이미지 선택
        pictures_folder = os.path.expanduser("~/Pictures")
        options = QFileDialog.Options()
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Select Images", pictures_folder, "Images (*.png *.jpg *.jpeg *.bmp)", options=options)

        if file_paths:
            # 스캔 과정 시뮬레이션
            QTimer.singleShot(100, lambda: self.progress_bar.setValue(25))
            QTimer.singleShot(600, lambda: self.progress_bar.setValue(50))
            QTimer.singleShot(1200, lambda: self.progress_bar.setValue(75))
            QTimer.singleShot(1800, lambda: self.progress_bar.setValue(100))
            QTimer.singleShot(3000, lambda: self.process_images(file_paths))

    def show_loading_gif(self):
        # 로딩 GIF 설정
        gif_path = r"ui/img/doc_erase.gif"
        self.movie = QMovie(gif_path)
        self.movie.setScaledSize(self.loading_label.size() * 1.5)
        self.loading_label.setMovie(self.movie)
        self.movie.start()
        self.loading_label.show()

    def process_images(self, image_paths):
        # 첫 번째 이미지를 화면에 표시
        pixmap = QPixmap(image_paths[0])
        if not pixmap.isNull():
            self.image_frame.setPixmap(pixmap.scaled(self.image_frame.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.log_area.append(f"Loaded image: {image_paths[0]}")
            self.log_area.append('<font color="red"><b>삭제하시겠습니까?</b></font>')
            self.yes_button.setVisible(True)
            self.no_button.setVisible(True)
        else:
            self.log_area.append(f"Failed to load image: {image_paths[0]}")

        # 로딩 GIF와 프로그레스 바 숨김
        self.loading_label.hide()
        self.progress_bar.hide()

        # 완료 메시지와 이미지 표시
        self.completion_label.setVisible(True)
        self.completion_image.setVisible(True)

    def delete_image(self):
        # 이미지 삭제 처리
        self.log_area.append("Image deleted.")
        self.reset_screen()

    def cancel_deletion(self):
        # 삭제 취소 처리
        self.log_area.append("Image deletion cancelled.")
        self.reset_screen()

    def reset_screen(self):
        # 화면 초기화
        self.completion_label.setVisible(False)
        self.completion_image.setVisible(False)
        self.image_frame.clear()
        self.log_area.clear()
        self.yes_button.setVisible(False)
        self.no_button.setVisible(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    scan_screen = ImageScanScreen()
    scan_screen.show()
    sys.exit(app.exec_())
