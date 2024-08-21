import sys
import os
import schedule
import threading
import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
    QFileDialog, QTextEdit, QFrame, QProgressBar, QDateTimeEdit, QComboBox, QLineEdit, QDialog
)
from PyQt5.QtGui import QPixmap, QMovie, QPalette, QColor, QFont, QIcon
from PyQt5.QtCore import Qt, QTimer, QDateTime
from ultralytics import YOLO

# YOLO 모델 로드
model = YOLO('data/runs/detect/train4/weights/best.pt')


class ImageScanAndScheduleScreen(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the main screen
        self.setWindowTitle('Image Scan and File Deletion Scheduler')
        self.setFixedSize(1050, 700)  # 고정된 창 크기

        # Set white background
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(Qt.white))
        self.setPalette(palette)

        # Create main layout with fixed ratio 2:1
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)  # 여백 제거

        # 왼쪽 레이아웃: 스캔 버튼, 스케줄링 버튼, 이미지 프레임, 로그 영역
        left_layout = QVBoxLayout()
        left_layout.setSpacing(0)  # 위젯 사이의 간격 제거

        # 왼쪽 컨테이너 설정
        left_widget = QWidget()
        left_widget.setStyleSheet("background-color: #FFFFE0;")  # 노란 배경
        left_widget.setLayout(left_layout)
        main_layout.addWidget(left_widget, stretch=2)

        # 스캔 및 스케줄링 버튼을 포함할 버튼 레이아웃
        button_layout = QHBoxLayout()

        # 이미지 스캔 버튼
        self.scan_button = QPushButton()
        self.scan_button.setFixedSize(200, 75)
        self.scan_button.setStyleSheet("background: transparent;")
        self.scan_button.setIcon(QIcon(r"ui/img/scan.png"))
        self.scan_button.setIconSize(self.scan_button.size())
        self.scan_button.setFont(QFont("Arial", 16, QFont.Bold))
        self.scan_button.clicked.connect(self.scan_images)
        button_layout.addWidget(self.scan_button)

        # 스케줄링 버튼 추가
        self.schedule_button = QPushButton()
        self.schedule_button.setFixedSize(200, 75)  # 스캔 버튼과 동일한 크기 설정
        self.schedule_button.setStyleSheet("background: transparent;")  # 버튼 투명화
        self.schedule_button.setIcon(QIcon(r"ui/img/schedule.png"))  # schedule.png 이미지 설정
        self.schedule_button.setIconSize(self.schedule_button.size())
        self.schedule_button.clicked.connect(self.open_scheduler_dialog)
        button_layout.addWidget(self.schedule_button)

        # 버튼 레이아웃을 왼쪽 레이아웃에 추가
        left_layout.addLayout(button_layout)

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
        self.separator.setStyleSheet("background-color: lightgray;")  # 회색 선
        main_layout.addWidget(self.separator)

        # 오른쪽 레이아웃: 로딩 GIF 및 완료 표시
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

        # 레이아웃을 메인 레이아웃에 추가
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

    def open_scheduler_dialog(self):
        # 스케줄 설정 창 열기
        self.scheduler_dialog = SchedulerDialog(self)
        self.scheduler_dialog.exec_()

    def run_scheduler(self):
        while True:
            schedule.run_pending()
            time.sleep(1)


class SchedulerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('파일 삭제 스케줄링')
        self.setGeometry(400, 400, 400, 200)

        # Layout
        layout = QVBoxLayout()

        # 날짜 선택
        self.date_time_edit = QDateTimeEdit(self)
        self.date_time_edit.setDateTime(QDateTime.currentDateTime())
        layout.addWidget(QLabel('삭제할 날짜와 시간 선택'))
        layout.addWidget(self.date_time_edit)

        # 주기 선택
        self.cycle_combo = QComboBox(self)
        self.cycle_combo.addItems(["매일", "매주", "매월"])
        layout.addWidget(QLabel('주기 선택'))
        layout.addWidget(self.cycle_combo)

        # 파일 확장자 입력
        self.file_extensions_edit = QLineEdit(self)
        layout.addWidget(QLabel('삭제할 파일 확장자 (예: .pdf, .jpg)'))
        layout.addWidget(self.file_extensions_edit)

        # 디렉터리 선택 버튼
        self.directory_button = QPushButton('디렉터리 선택', self)
        self.directory_button.clicked.connect(self.select_directory)
        layout.addWidget(self.directory_button)

        # 디렉터리 표시
        self.selected_directory = QLabel('선택된 디렉터리: 없음', self)
        layout.addWidget(self.selected_directory)

        # OK 버튼
        self.ok_button = QPushButton('확인', self)
        self.ok_button.clicked.connect(self.schedule_task)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, '디렉터리 선택')
        if directory:
            self.selected_directory.setText(f'선택된 디렉터리: {directory}')
            self.directory_path = directory

    def schedule_task(self):
        selected_datetime = self.date_time_edit.dateTime().toPyDateTime()
        cycle = self.cycle_combo.currentText()
        extensions = self.file_extensions_edit.text().split(',')
        directory = self.directory_path

        # 주기에 맞춰 스케줄링
        if cycle == "매일":
            schedule.every().day.at(selected_datetime.strftime("%H:%M")).do(self.delete_files, directory, extensions)
        elif cycle == "매주":
            schedule.every().week.at(selected_datetime.strftime("%H:%M")).do(self.delete_files, directory, extensions)
        elif cycle == "매월":
            schedule.every().month.at(selected_datetime.strftime("%H:%M")).do(self.delete_files, directory, extensions)

        # 스케줄 실행을 위한 스레드 시작
        threading.Thread(target=self.run_scheduler, daemon=True).start()

        # 창 닫기
        self.accept()

    def delete_files(self, directory, extensions):
        # 파일 삭제 로직
        print(f"Deleting files in {directory} with extensions: {', '.join(extensions)}")
        for root, dirs, files in os.walk(directory):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    try:
                        os.remove(file_path)
                        print(f"Deleted: {file_path}")
                    except Exception as e:
                        print(f"Failed to delete {file_path}: {e}")

    def run_scheduler(self):
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = ImageScanAndScheduleScreen()
    screen.show()
    sys.exit(app.exec_())
