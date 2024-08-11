# core/utils.py
import os

def is_office_document(file_path):
    """
    파일이 오피스 문서인지 확인합니다.
    """
    office_extensions = ['.docx', '.xlsx', '.pptx', '.hwp']
    _, ext = os.path.splitext(file_path)
    return ext.lower() in office_extensions

def get_user_sid():
    """
    현재 사용자의 SID를 반환합니다.
    """
    import subprocess
    result = subprocess.run(['wmic', 'useraccount', 'where', 'name="%username%"', 'get', 'sid'], capture_output=True, text=True)
    return result.stdout.splitlines()[1].strip()

def delete_file(file_path):
    """
    파일을 안전하게 삭제합니다.
    """
    try:
        os.remove(file_path)
        return True
    except Exception as e:
        print(f"Error deleting file {file_path}: {e}")
        return False

