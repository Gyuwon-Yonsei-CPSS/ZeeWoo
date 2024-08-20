import sys
import os
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QFileDialog, QTextEdit, QSpacerItem, QSizePolicy, QProgressBar
from PyQt5.QtGui import QPalette, QColor, QIcon, QMovie, QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer

# document_delete.py의 함수 임포트
from document_delete import delete_file_completely


class DocDelWindow(QMainWindow):
    def __init__(self):
        super(DocDelWindow, self).__init__()

        self.setFixedSize(1100, 706)
        self.setWindowTitle("문서 삭제")

        # 배경 색상을 흰색으로 설정 (전체 창)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(Qt.white))
        self.setPalette(palette)

        # 메인 위젯과 레이아웃 생성
        main_widget = QWidget(self)
        main_layout = QHBoxLayout(main_widget)

        # 좌측 레이아웃 패널
        left_panel = QWidget(self)
        left_layout = QVBoxLayout(left_panel)
        left_panel.setFixedWidth(770)  # 좌측 패널의 폭을 설정

        # 좌측 패널의 배경색 설정
        left_panel.setStyleSheet("background-color: #FFFFE0;")  # 좌측 패널 배경색 설정

        # 상단에 파일 선택 버튼과 파일 정보 텍스트 위젯 배치
        top_layout = QHBoxLayout()

        # 파일 선택 버튼에 이미지 삽입 및 투명화
        self.file_select_button = QPushButton(self)
        self.set_file_select_button_size(230, 80)  # 초기 크기 설정
        self.file_select_button.setIcon(QIcon("ui/img/select_file.png"))  # 이미지 파일 경로를 설정
        self.file_select_button.setStyleSheet("background: transparent; border: none;")  # 배경 투명화 및 테두리 제거
        self.file_select_button.clicked.connect(self.open_file_dialog)
        top_layout.addWidget(self.file_select_button, alignment=Qt.AlignLeft)

        # 파일 정보 텍스트 편집기 (높이 및 가로 길이 조정)
        self.file_info_text_edit = QTextEdit(self)
        self.file_info_text_edit.setReadOnly(True)
        self.file_info_text_edit.setFixedSize(500, 150)  # 높이를 조금 늘림
        # 네모 상자 스타일 설정
        self.file_info_text_edit.setStyleSheet("border: 2px solid black; padding: 10px; background-color: white;")  # 배경색 흰색 유지
        top_layout.addWidget(self.file_info_text_edit, alignment=Qt.AlignLeft)

        # 상단 레이아웃을 좌측 레이아웃에 추가
        left_layout.addLayout(top_layout)

        # 로그 텍스트 편집기 (파일 정보 텍스트와 오른쪽 경계 맞춤)
        log_layout = QHBoxLayout()

        # 로그창을 오른쪽으로 밀기 위한 스페이서 추가
        log_spacer = QSpacerItem(150, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        log_layout.addItem(log_spacer)

        # 로그 텍스트 편집기 스크롤 가능하도록 설정
        self.log_text_edit = QTextEdit(self)
        self.log_text_edit.setReadOnly(True)
        self.log_text_edit.setFixedSize(500, 350)  # 파일 정보 텍스트와 같은 가로 길이로 설정
        # 로그 창 스타일 설정: 검은 배경, 흰색 텍스트
        self.log_text_edit.setStyleSheet("background-color: black; color: white; border: 2px solid black; padding: 10px;")
        self.log_text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # 세로 스크롤바 필요 시 추가
        self.log_text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # 가로 스크롤바 필요 시 추가
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
        self.info_label.setStyleSheet("color: blue; border: 2px solid black; padding: 10px; background-color: white;")  # 배경색 흰색 유지
        button_layout.addWidget(self.info_label, alignment=Qt.AlignLeft)

        # 스페이서를 추가해 버튼을 오른쪽으로 이동
        button_layout.addStretch()  # 버튼을 오른쪽으로 밀기 위한 공간 추가

        # 로그 초기화 버튼 (이미지 삽입 및 투명화)
        button_layout.addSpacing(-40)  # 이 값으로 위치 조정
        self.reset_log_button = QPushButton(self)
        self.set_reset_log_button_size(150, 50)  # 버튼 크기 설정
        self.reset_log_button.setIcon(QIcon("ui/img/reset_log.png"))  # 이미지 파일 경로 설정
        self.reset_log_button.setStyleSheet("background: transparent; border: none;")  # 배경 투명화 및 테두리 제거
        self.reset_log_button.clicked.connect(self.reset_log)
        button_layout.addWidget(self.reset_log_button, alignment=Qt.AlignLeft)  # 좌측 정렬로 설정

        # 지우기 시작 버튼 (이미지 삽입 및 투명화)
        self.erase_button = QPushButton(self)
        self.set_erase_button_size(150, 50)  # 버튼 크기 설정
        self.erase_button.setIcon(QIcon("ui/img/erase.png"))  # 이미지 파일 경로 설정
        self.erase_button.setStyleSheet("background: transparent; border: none;")  # 배경 투명화 및 테두리 제거
        self.erase_button.clicked.connect(self.start_parsing)  # 지우기 시작 버튼 클릭 시 동작
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

        # 우측 패널 (로딩바와 GIF를 표시할 공간)
        right_panel = QWidget(self)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignCenter)

        # GIF 표시 라벨
        self.loading_gif_label = QLabel(self)
        self.loading_movie = QMovie("ui/img/doc_erase.gif")
        self.loading_gif_label.setMovie(self.loading_movie)
        self.loading_gif_label.setFixedSize(200, 200)  # 고정된 크기
        self.loading_movie.setScaledSize(self.loading_gif_label.size())  # GIF 크기를 고정 크기로 설정
        self.loading_gif_label.setVisible(False)  # 처음에는 보이지 않도록 설정

        # 로딩바
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setFixedWidth(200)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)  # 퍼센트 텍스트 숨기기
        self.progress_bar.setVisible(False)  # 처음에는 보이지 않도록 설정

        # 로딩 완료 후 표시할 이미지와 텍스트
        self.completion_image_label = QLabel(self)
        self.completion_image_label.setPixmap(QPixmap("ui/img/eraser.jpg").scaled(200, 200, Qt.KeepAspectRatio))
        self.completion_image_label.setVisible(False)

        self.completion_text_label = QLabel("삭제 완료!", self)
        self.completion_text_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.completion_text_label.setAlignment(Qt.AlignCenter)
        self.completion_text_label.setVisible(False)

        # GIF와 로딩바를 우측 레이아웃에 추가
        right_layout.addWidget(self.loading_gif_label, alignment=Qt.AlignCenter)
        right_layout.addWidget(self.progress_bar, alignment=Qt.AlignCenter)

        # 완료 이미지와 텍스트를 우측 레이아웃에 추가
        right_layout.addWidget(self.completion_image_label, alignment=Qt.AlignCenter)
        right_layout.addWidget(self.completion_text_label, alignment=Qt.AlignCenter)

        # 우측 레이아웃을 메인 레이아웃에 추가
        main_layout.addWidget(right_panel)

        # 메인 레이아웃을 중앙 위젯으로 설정
        self.setCentralWidget(main_widget)

        # 선택한 파일들을 저장하기 위한 리스트
        self.selected_files = []

    def set_file_select_button_size(self, width, height):
        """파일 선택 버튼 크기 조정 함수"""
        self.file_select_button.setFixedSize(width, height)
        self.file_select_button.setIconSize(self.file_select_button.size())  # 버튼 크기에 맞춰 아이콘 크기 조정

    def set_reset_log_button_size(self, width, height):
        """로그 초기화 버튼 크기 조정 함수"""
        self.reset_log_button.setFixedSize(width, height)
        self.reset_log_button.setIconSize(self.reset_log_button.size())  # 버튼 크기에 맞춰 아이콘 크기 조정

    def set_erase_button_size(self, width, height):
        """지우기 시작 버튼 크기 조정 함수"""
        self.erase_button.setFixedSize(width, height)
        self.erase_button.setIconSize(self.erase_button.size())  # 버튼 크기에 맞춰 아이콘 크기 조정

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

    def start_parsing(self):
        """파싱 작업 시작 시 호출되는 함수"""
        # GIF와 로딩바 표시
        self.loading_gif_label.setVisible(True)
        self.progress_bar.setVisible(True)
        self.loading_movie.start()

        # 타이머를 이용해 로딩바를 업데이트하면서 파일 삭제 시뮬레이션
        self.progress_bar.setValue(0)
        self.current_progress = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(100)  # 100ms마다 업데이트

    def update_progress(self):
        """로딩바 업데이트와 파일 삭제 동작을 시뮬레이션"""
        if self.current_progress < 100:
            self.current_progress += 10
            self.progress_bar.setValue(self.current_progress)
        else:
            self.timer.stop()
            self.complete_parsing()

    def complete_parsing(self):
        """파싱 완료 후 처리"""
        self.loading_movie.stop()
        self.loading_gif_label.setVisible(False)
        self.progress_bar.setVisible(False)

        # 삭제 완료 이미지와 텍스트 표시
        self.completion_image_label.setVisible(True)
        self.completion_text_label.setVisible(True)

        self.log_text_edit.append("삭제가 완료되었습니다.")

    def do_delete(self):
        # '지우기 시작' 버튼에 대한 동작: 선택된 파일들 삭제
        if not self.selected_files:
            self.log_text_edit.append("선택된 파일이 없습니다.")
            return

        for file_path in self.selected_files:
            self.log_text_edit.append(f"파일 삭제 시도 중: {file_path}")
            try:
                delete_file_completely(file_path)  # document_delete.py의 함수 호출
                self.log_text_edit.append(f"성공적으로 삭제됨: {file_path}")
            except Exception as e:
                self.log_text_edit.append(f"파일 삭제 실패: {file_path}, 오류: {str(e)}")

    def reset_log(self):
        # '로그 초기화' 버튼에 대한 동작
        self.log_text_edit.clear()


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = DocDelWindow()
    window.show()
    sys.exit(app.exec_())
