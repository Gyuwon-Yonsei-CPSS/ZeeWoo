# core/file_manager.py
import os
from core.artifact_parser import ArtifactParser

class FileManager:
    def __init__(self):
        self.artifact_parser = ArtifactParser()

    def delete_file_and_artifacts(self, file_path):
        try:
            # 1. 파일 삭제
            os.remove(file_path)

            # 2. 관련 아티팩트 삭제
            artifacts = self.artifact_parser.find_artifacts(file_path)
            for artifact in artifacts:
                try:
                    os.remove(artifact)
                except Exception as e:
                    print(f"Failed to delete artifact {artifact}: {e}")

            # 3. 삭제 이력 기록
            with open("logs/deletion_log.txt", "a") as log_file:
                log_file.write(f"Deleted {file_path} and related artifacts.\n")

            return True
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")
            return False

