import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, 
    QFileDialog, QTextEdit, QFrame, QProgressBar, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QPixmap, QMovie, QPalette, QColor, QFont
from PyQt5.QtCore import Qt, QTimer

class MainScreen(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle('Main Screen')
        self.setFixedSize(1050, 700)  # 가로 1050, 세로 700으로 고정
        
        # Create layout
        layout = QVBoxLayout()

        # Create a button to open the image scan screen
        self.scan_button = QPushButton('스캔하기')
        self.scan_button.setFixedSize(200, 75)  # 버튼 크기 조정
        self.scan_button.setFont(QFont("Arial", 16, QFont.Bold))  # 글씨 크기 및 굵기 조정
        self.scan_button.clicked.connect(self.open_image_scan_screen)
        layout.addWidget(self.scan_button, alignment=Qt.AlignLeft)

        # Set layout
        self.setLayout(layout)

    def open_image_scan_screen(self):
        # Hide the main screen and show the scan screen
        self.scan_screen = ImageScanScreen()
        self.scan_screen.show()
        self.hide()

class ImageScanScreen(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the image scan screen
        self.setWindowTitle('Image Scan Screen')
        self.setFixedSize(1050, 700)  # 가로 1050, 세로 700으로 고정

        # Set white background
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(Qt.white))
        self.setPalette(palette)
        
        # Create main layout with fixed ratio 2:1
        main_layout = QHBoxLayout()

        # Create a left layout for the scan button, image frame, and log area
        left_layout = QVBoxLayout()
        left_layout.setSpacing(0)  # Remove spacing between widgets

        # Create a button to scan images
        self.scan_button = QPushButton('스캔하기')
        self.scan_button.setFixedSize(200, 75)  # 버튼 크기 조정
        self.scan_button.setFont(QFont("Arial", 16, QFont.Bold))  # 글씨 크기 및 굵기 조정
        self.scan_button.clicked.connect(self.scan_images)
        left_layout.addWidget(self.scan_button, alignment=Qt.AlignLeft)

        # Create a large image frame to display scanned images
        self.image_frame = QLabel()
        self.image_frame.setFrameStyle(QFrame.Box | QFrame.Sunken)
        self.image_frame.setAlignment(Qt.AlignCenter)
        self.image_frame.setFixedSize(700, 400)  # 이미지 프레임 가로 700, 세로 400으로 설정
        left_layout.addWidget(self.image_frame, alignment=Qt.AlignCenter)

        # Create a log area with "Yes/No" buttons appearing when an image is loaded
        self.log_area = QTextEdit()
        self.log_area.setFixedSize(700, 120)  # 로그창의 가로 길이 조정
        self.log_area.setReadOnly(True)
        self.log_area.setStyleSheet("color: black; font-weight: normal;")  # Make log text black and normal weight
        left_layout.addWidget(self.log_area)

        # Yes/No buttons for image deletion confirmation
        self.yes_button = QPushButton('예')
        self.no_button = QPushButton('아니오')
        self.yes_button.setVisible(False)
        self.no_button.setVisible(False)
        
        # Connect buttons to functions
        self.yes_button.clicked.connect(self.delete_image)
        self.no_button.clicked.connect(self.cancel_deletion)

        # Add buttons to log area
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.yes_button)
        button_layout.addWidget(self.no_button)
        left_layout.addLayout(button_layout)

        # Add left layout to the main layout
        main_layout.addLayout(left_layout, stretch=2)

        # Create a vertical line for separation
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.VLine)
        self.separator.setFrameShadow(QFrame.Sunken)
        self.separator.setLineWidth(1)  # Make the line thinner
        self.separator.setStyleSheet("background-color: lightgray;")  # Change line color to lightgray
        main_layout.addWidget(self.separator)

        # Create a right layout for the loading GIF and progress bar
        right_layout = QVBoxLayout()
        right_layout.setSpacing(0)  # Remove spacing between widgets

        # Create a label for the completion image
        self.completion_image = QLabel()
        completion_pixmap = QPixmap(r"C:\Users\dusdn\ZeeWoo\ui\img\eraser.jpg").scaled(300, 300, Qt.KeepAspectRatio)  # Adjust image size
        self.completion_image.setPixmap(completion_pixmap)
        self.completion_image.setAlignment(Qt.AlignCenter)
        self.completion_image.setVisible(False)
        right_layout.addWidget(self.completion_image, alignment=Qt.AlignCenter)

        # Create a label for the completion message
        self.completion_label = QLabel("완료되었습니다!", self)
        self.completion_label.setAlignment(Qt.AlignCenter)
        self.completion_label.setFont(QFont("Arial", 24, QFont.Bold))  # Bigger and bolder font
        self.completion_label.setVisible(False)
        right_layout.addWidget(self.completion_label, alignment=Qt.AlignCenter)

        # Create a label to display the loading GIF
        self.loading_label = QLabel()
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setFixedSize(300, 300)  # Adjust GIF size (5 times larger)
        right_layout.addWidget(self.loading_label, alignment=Qt.AlignCenter)

        # Initially hide the loading label
        self.loading_label.hide()

        # Create a progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        right_layout.addWidget(self.progress_bar)

        # Initially hide the progress bar
        self.progress_bar.hide()

        # Add right layout to the main layout
        main_layout.addLayout(right_layout, stretch=1)

        # Set main layout
        self.setLayout(main_layout)

    def scan_images(self):
        # Show the loading GIF and progress bar immediately when the scan button is clicked
        self.show_loading_gif()
        self.progress_bar.setValue(0)  # Reset progress bar
        self.progress_bar.show()

        # Open file dialog to select images from the Pictures folder
        pictures_folder = os.path.expanduser("~/Pictures")
        options = QFileDialog.Options()
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Select Images", pictures_folder, "Images (*.png *.jpg *.jpeg *.bmp)", options=options)
        
        if file_paths:
            # Simulate the scan process with a timer (3 seconds delay)
            self.progress_bar.setValue(0)
            QTimer.singleShot(100, lambda: self.progress_bar.setValue(25))
            QTimer.singleShot(600, lambda: self.progress_bar.setValue(50))
            QTimer.singleShot(1200, lambda: self.progress_bar.setValue(75))
            QTimer.singleShot(1800, lambda: self.progress_bar.setValue(100))
            QTimer.singleShot(3000, lambda: self.process_images(file_paths))

    def show_loading_gif(self):
        # Load the GIF from the specified path
        gif_path = r"C:\Users\dusdn\ZeeWoo\ui\img\data_erase.gif"
        self.movie = QMovie(gif_path)
        
        # Set the GIF to the label and start the movie
        self.movie.setScaledSize(self.loading_label.size())
        self.loading_label.setMovie(self.movie)
        self.movie.start()

        # Show the loading label
        self.loading_label.show()

    def process_images(self, image_paths):
        # Process each image (for now, just display the first one)
        pixmap = QPixmap(image_paths[0])
        if not pixmap.isNull():
            self.image_frame.setPixmap(pixmap.scaled(self.image_frame.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.log_area.append(f"Loaded image: {image_paths[0]}")
            self.log_area.append('<font color="red"><b>삭제하시겠습니까?</b></font>')  # "삭제하시겠습니까?" 문장 빨간색으로 표시
            
            # Show Yes/No buttons
            self.yes_button.setVisible(True)
            self.no_button.setVisible(True)
        else:
            self.log_area.append(f"Failed to load image: {image_paths[0]}")
        
        # Hide the loading GIF and progress bar after processing
        self.loading_label.hide()
        self.progress_bar.hide()
        
        # Show completion message and image
        self.completion_label.setVisible(True)
        self.completion_image.setVisible(True)

    def delete_image(self):
        # Handle image deletion
        self.log_area.append("Image deleted.")
        self.reset_screen()

    def cancel_deletion(self):
        # Handle cancellation
        self.log_area.append("Image deletion cancelled.")
        self.reset_screen()

    def reset_screen(self):
        # Reset the screen to its initial state
        self.completion_label.setVisible(False)
        self.completion_image.setVisible(False)
        self.image_frame.clear()
        self.log_area.clear()
        self.yes_button.setVisible(False)
        self.no_button.setVisible(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_screen = MainScreen()
    main_screen.show()
    sys.exit(app.exec_())
