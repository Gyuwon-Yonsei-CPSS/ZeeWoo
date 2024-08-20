from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget

class SenDataMainWindow(QMainWindow):
    def __init__(self):
        super(SenDataMainWindow, self).__init__()

        self.setWindowTitle("Sensitive Data Detection")
        self.setFixedSize(800, 600)

        central_widget = QWidget()
        layout = QVBoxLayout()

        self.label = QLabel("This is the Sensitive Data Detection window", self)
        layout.addWidget(self.label)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
