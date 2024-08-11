# core/artifact_parser.py
import os

class ArtifactParser:
    def __init__(self):
        # 아티팩트 경로 매핑 (주요 아티팩트 파일 경로를 정의)
        self.artifact_paths = {
            "$MFT": "C:\\$MFT",
            "$I30": "C:\\$I30",
            "$UsnJournal": "C:\\$Extend\\$UsnJrnl\\$J",
            "$Recycle.Bin": "C:\\$Recycle.Bin\\{USER_SID}",
            "LNK": "C:\\Users\\{USERNAME}\\AppData\\Roaming\\Microsoft\\Windows\\Recent"
        }

    def find_artifacts(self, file_path):
        artifacts = []

        # 예시: 파일 이름과 확장자를 기반으로 아티팩트 파일들을 찾음
        base_name = os.path.basename(file_path)
        for artifact_name, artifact_path in self.artifact_paths.items():
            if artifact_name == "LNK":
                lnk_path = artifact_path.format(USERNAME=os.getlogin()) + f"\\{base_name}.lnk"
                if os.path.exists(lnk_path):
                    artifacts.append(lnk_path)
            else:
                if os.path.exists(artifact_path):
                    artifacts.append(artifact_path)

        return artifacts

