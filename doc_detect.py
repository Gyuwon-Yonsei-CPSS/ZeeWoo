import sys
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
    QFileDialog, QTextEdit, QFrame, QProgressBar
)
from PyQt5.QtGui import QPixmap, QMovie, QPalette, QColor, QFont, QIcon
from PyQt5.QtCore import Qt, QTimer


class DocumentScanScreen(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the document scan screen
        self.setWindowTitle('Document Scan Screen')
        self.setFixedSize(1050, 700)

        # Set white background
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(Qt.white))
        self.setPalette(palette)

        # Create main layout with fixed ratio 2:1
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Create left layout for the scan button, document frame, and log area
        left_layout = QVBoxLayout()
        left_layout.setSpacing(0)

        # Set background color for the left layout container
        left_widget = QWidget()
        left_widget.setStyleSheet("background-color: #FFFFE0;")  # Background color
        left_widget.setLayout(left_layout)
        left_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.addWidget(left_widget, stretch=2)

        # Create a button to scan documents
        self.scan_button = QPushButton()
        self.scan_button.setFixedSize(200, 75)
        self.scan_button.setStyleSheet("background: transparent;")
        self.scan_button.setIcon(QIcon(str(Path(r"ui/img/scan.png"))))
        self.scan_button.setIconSize(self.scan_button.size())
        self.scan_button.setFont(QFont("Arial", 16, QFont.Bold))
        self.scan_button.clicked.connect(self.scan_documents)
        left_layout.addWidget(self.scan_button, alignment=Qt.AlignCenter)

        # Create a large document frame to display scanned documents
        self.document_frame = QLabel()
        self.document_frame.setFrameStyle(QFrame.Box | QFrame.Sunken)
        self.document_frame.setAlignment(Qt.AlignCenter)
        self.document_frame.setFixedSize(700, 400)
        self.document_frame.setStyleSheet("background-color: white;")
        left_layout.addWidget(self.document_frame, alignment=Qt.AlignCenter)

        # Create a log area with "Yes/No" buttons appearing when a document is loaded
        self.log_area = QTextEdit()
        self.log_area.setFixedSize(700, 120)
        self.log_area.setReadOnly(True)
        self.log_area.setStyleSheet("background-color: white; color: black;")
        left_layout.addWidget(self.log_area)

        # Yes/No buttons for document deletion confirmation
        self.yes_button = QPushButton('예')
        self.no_button = QPushButton('아니오')
        self.yes_button.setVisible(False)
        self.no_button.setVisible(False)

        # Connect buttons to functions
        self.yes_button.clicked.connect(self.delete_document)
        self.no_button.clicked.connect(self.cancel_deletion)

        # Add buttons to log area
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.yes_button)
        button_layout.addWidget(self.no_button)
        left_layout.addLayout(button_layout)

        # Create a vertical line for separation
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.VLine)
        self.separator.setFrameShadow(QFrame.Sunken)
        self.separator.setLineWidth(1)
        self.separator.setStyleSheet("background-color: lightgray;")
        main_layout.addWidget(self.separator)

        # Create right layout for the loading GIF and progress bar
        right_layout = QVBoxLayout()
        right_layout.setSpacing(0)

        # Create a label for the completion image
        self.completion_image = QLabel()
        completion_pixmap = QPixmap(str(Path(r"ui/img/eraser.jpg"))).scaled(300, 300,
                                                                             Qt.KeepAspectRatio)
        self.completion_image.setPixmap(completion_pixmap)
        self.completion_image.setAlignment(Qt.AlignCenter)
        self.completion_image.setVisible(False)
        right_layout.addWidget(self.completion_image, alignment=Qt.AlignBottom)

        # Create a label for the completion message
        self.completion_label = QLabel("완료되었습니다!", self)
        self.completion_label.setAlignment(Qt.AlignCenter)
        self.completion_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.completion_label.setVisible(False)
        right_layout.addWidget(self.completion_label, alignment=Qt.AlignTop)

        # Create a label to display the loading GIF
        self.loading_label = QLabel()
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setFixedSize(300, 300)
        right_layout.addWidget(self.loading_label, alignment=Qt.AlignCenter)

        # Create a progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        right_layout.addWidget(self.progress_bar)

        # Initially hide the progress bar and loading label
        self.progress_bar.hide()
        self.loading_label.hide()

        # Add right layout to the main layout
        main_layout.addLayout(right_layout, stretch=1)

        # Set main layout
        self.setLayout(main_layout)  # Set the layout for the document scan screen

    def scan_documents(self):
        # Show the loading GIF and progress bar immediately when the scan button is clicked
        self.show_loading_gif()
        self.progress_bar.setValue(0)
        self.progress_bar.show()

        # Open file dialog to select documents from the Documents folder
        documents_folder = Path.home() / "Documents"
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Select Documents", str(documents_folder), "Documents (*.pdf *.docx *.txt)"
        )

        if file_paths:
            # Simulate the scan process with a timer
            self.progress_bar.setValue(0)
            QTimer.singleShot(100, lambda: self.progress_bar.setValue(25))
            QTimer.singleShot(600, lambda: self.progress_bar.setValue(50))
            QTimer.singleShot(1200, lambda: self.progress_bar.setValue(75))
            QTimer.singleShot(1800, lambda: self.progress_bar.setValue(100))
            QTimer.singleShot(3000, lambda: self.process_documents(file_paths))

    def show_loading_gif(self):
        # Load the GIF
        gif_path = Path(r"ui/img/doc_erase.gif")
        self.movie = QMovie(str(gif_path))
        self.movie.setScaledSize(self.loading_label.size() * 1.5)
        self.loading_label.setMovie(self.movie)
        self.movie.start()
        self.loading_label.show()

    def process_documents(self, document_paths):
        # Process and display the first document
        pixmap = QPixmap(document_paths[0])
        if not pixmap.isNull():
            self.document_frame.setPixmap(pixmap.scaled(self.document_frame.size(), Qt.KeepAspectRatio))
            self.log_area.append(f"Loaded document: {document_paths[0]}")
            self.log_area.append('<font color="red"><b>삭제하시겠습니까?</b></font>')
            self.yes_button.setVisible(True)
            self.no_button.setVisible(True)
        else:
            self.log_area.append(f"Failed to load document: {document_paths[0]}")

        # Hide the loading GIF and progress bar
        self.loading_label.hide()
        self.progress_bar.hide()

        # Show completion message and image
        self.completion_label.setVisible(True)
        self.completion_image.setVisible(True)

    def delete_document(self):
        # Handle document deletion
        self.log_area.append("Document deleted.")
        self.reset_screen()

    def cancel_deletion(self):
        # Handle cancellation
        self.log_area.append("Document deletion cancelled.")
        self.reset_screen()

    def reset_screen(self):
        # Reset the screen to its initial state
        self.completion_label.setVisible(False)
        self.completion_image.setVisible(False)
        self.document_frame.clear()
        self.log_area.clear()
        self.yes_button.setVisible(False)
        self.no_button.setVisible(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    scan_screen = DocumentScanScreen()
    scan_screen.show()
    sys.exit(app.exec_())
