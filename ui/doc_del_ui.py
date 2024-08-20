from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QFileDialog, QTextEdit, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class DocDelWindow(QMainWindow):
    def __init__(self):
        super(DocDelWindow, self).__init__()

        self.setFixedSize(1100, 706)
        self.setWindowTitle("문서 삭제")

        # 배경 이미지 설정
        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap("ui/img/mainscreen.png"))
        self.background_label.setGeometry(0, 0, 1100, 706)
        self.background_label.setScaledContents(True)

        # 메인 위젯과 레이아웃 생성
        main_widget = QWidget(self)
        main_layout = QHBoxLayout(main_widget)

        # 좌측 레이아웃 패널
        left_panel = QWidget(self)
        left_layout = QVBoxLayout(left_panel)
        left_panel.setFixedWidth(770)  # 좌측 패널의 폭을 설정

        # 상단에 파일 선택 버튼과 파일 정보 텍스트 위젯 배치
        top_layout = QHBoxLayout()

        # 파일 선택 버튼
        self.file_select_button = QPushButton("파일 선택", self)
        self.file_select_button.setFixedSize(150, 40)
        self.file_select_button.clicked.connect(self.open_file_dialog)
        top_layout.addWidget(self.file_select_button, alignment=Qt.AlignLeft)

        # 파일 정보 텍스트 편집기 (높이 및 가로 길이 조정)
        self.file_info_text_edit = QTextEdit(self)
        self.file_info_text_edit.setReadOnly(True)
        self.file_info_text_edit.setFixedSize(500, 150)  # 높이를 조금 늘림
        top_layout.addWidget(self.file_info_text_edit, alignment=Qt.AlignLeft)

        # 상단 레이아웃을 좌측 레이아웃에 추가
        left_layout.addLayout(top_layout)

        # 로그 텍스트 편집기 (파일 정보 텍스트와 오른쪽 경계 맞춤)
        log_layout = QHBoxLayout()

        # 로그창을 오른쪽으로 밀기 위한 스페이서 추가
        log_spacer = QSpacerItem(150, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        log_layout.addItem(log_spacer)

        self.log_text_edit = QTextEdit(self)
        self.log_text_edit.setReadOnly(True)
        self.log_text_edit.setFixedSize(500, 350)  # 파일 정보 텍스트와 같은 가로 길이로 설정
        log_layout.addWidget(self.log_text_edit, alignment=Qt.AlignLeft)

        left_layout.addLayout(log_layout)

        # 로그창과 버튼/문구 사이에 약간의 여백 추가
        left_layout.addSpacing(20)

        # 지우기 시작 버튼과 로그 초기화 버튼을 포함한 레이아웃
        button_layout = QHBoxLayout()

        # 파란색 안내 문구 (왼쪽에 위치)
        self.info_label = QLabel(self)
        self.info_label.setText("$UsnJournal을 보존하려면 artifact_parser.py의 로직을 수정하여 $UsnJournal을 삭제에서 제외할 수 있습니다. 파일과 아티팩트가 삭제되면 복구할 수 없을 수 있다는 점에 유의하세요.")
        self.info_label.setWordWrap(True)  # 텍스트가 여러 줄로 나뉘어 표시될 수 있도록 설정
        self.info_label.setFixedWidth(400)  # 안내 문구의 폭 설정
        self.info_label.setStyleSheet("color: blue;")  # 파란색 텍스트 설정
        button_layout.addWidget(self.info_label, alignment=Qt.AlignLeft)

        # 스페이서를 추가해 버튼을 오른쪽으로 이동
        button_layout.addStretch()  # 버튼을 오른쪽으로 밀기 위한 공간 추가

        # 로그 초기화 버튼 (지우기 시작 버튼 왼쪽에 위치)
        self.reset_log_button = QPushButton("로그 초기화", self)
        self.reset_log_button.setFixedSize(150, 50)
        self.reset_log_button.clicked.connect(self.reset_log)
        button_layout.addWidget(self.reset_log_button, alignment=Qt.AlignRight)

        # 지우기 시작 버튼 (오른쪽으로 위치)
        self.erase_button = QPushButton("지우기 시작", self)
        self.erase_button.setFixedSize(150, 50)
        self.erase_button.clicked.connect(self.do_delete)
        button_layout.addWidget(self.erase_button, alignment=Qt.AlignRight)

        # 안내 문구와 버튼 레이아웃을 좌측 레이아웃에 추가
        left_layout.addLayout(button_layout)

        # 좌측 레이아웃을 메인 레이아웃에 추가
        main_layout.addWidget(left_panel)

        # 수직선 그리기 (좌측 패널과 우측 패널 사이에)
        self.divider_line = QLabel(self)
        self.divider_line.setFixedSize(5, 706)
        self.divider_line.setStyleSheet("background-color: lightgray;")
        main_layout.addWidget(self.divider_line)

        # 우측 패널 (빈 공간)
        right_panel = QWidget(self)
        right_layout = QVBoxLayout(right_panel)

        # 우측 패널에 빈 공간 추가 (추가 레이아웃이나 버튼에 활용 가능)
        right_layout.addStretch()

        # 우측 레이아웃을 메인 레이아웃에 추가
        main_layout.addWidget(right_panel)

        # 메인 레이아웃을 중앙 위젯으로 설정
        self.setCentralWidget(main_widget)

        # 선택한 파일들을 저장하기 위한 리스트
        self.selected_files = []

    def open_file_dialog(self):
        # 파일 선택 다이얼로그를 열고 선택된 파일 정보 표시
        file_paths, _ = QFileDialog.getOpenFileNames(self, "파일 선택")
        if file_paths:
            self.selected_files.extend(file_paths)
            self.update_file_info()

    def update_file_info(self):
        # 선택된 파일들의 정보를 파일 정보 텍스트 위젯에 업데이트
        self.file_info_text_edit.clear()
        for file_path in self.selected_files:
            file_name = file_path.split('/')[-1]
            self.file_info_text_edit.append(f"{file_path}\n{file_name}")

    def do_delete(self):
        # '지우기 시작' 버튼에 대한 동작 로직 추가
        pass

    def reset_log(self):
        # '로그 초기화' 버튼에 대한 동작 로직 추가
        self.log_text_edit.clear()

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = DocDelWindow()
    window.show()
    sys.exit(app.exec_())
