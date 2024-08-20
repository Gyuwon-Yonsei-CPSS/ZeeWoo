import winreg
import ctypes
import os
import ntpath
import subprocess
import glob

'''
확장자 시그니처 헤더, 푸터 영역을 제거해 카빙(복구)가 어렵도록 만들고, 파일 삭제 시 최근 
'''
message = []

def replace_signature(file_path, header_signatures):
    '''각 확장자의 시그니처 헤더, 푸터를 삭제하여 카빙을 할 수 없도록 하는 함수'''
    with open(file_path, 'rb+') as file:
        content = file.read()
        for header_signature in header_signatures:
            header_bytes = header_signature.encode()
            content = content.replace(
                header_bytes, b'\x00' * len(header_bytes))
        file.seek(0)
        file.write(content)
        file.truncate()


def secure_delete_file(filepath):
    '''os.remove()를 이용해 파일을 삭제하는 함수'''
    try:
        os.remove(filepath)
        message.append(f"파일이 삭제되었습니다: {filepath}")
    except subprocess.CalledProcessError as e:
        message.append(f"파일 삭제에 실패했습니다: {filepath}, Error: {e}")


def pidl_to_path(pidl):
    '''OpenSavePidlMRU의 레지스트리 값을 디코딩하기 위한 함수'''
    SHGFP_TYPE_CURRENT = 0
    MAX_PATH = 260
    shell32 = ctypes.windll.shell32
    buf = ctypes.create_unicode_buffer(MAX_PATH)
    if shell32.SHGetPathFromIDListW(pidl, buf):
        return buf.value
    else:
        return None


def delete_registry_value(key, name, key_path, data):
    '''레지스트리 값을 삭제하는 함수'''
    try:
        winreg.DeleteValue(key, name)
        message.append(f"레지스트리 삭제 성공: {key_path} - {name}, Value: {data}")
    except OSError as e:
        message.append(
            f"레지스트리를 삭제하지 못했습니다: {key_path} - {name}, Error: {e}")


def read_and_delete_pidl_mru(key_path, target_filename):
    '''주어진 파일과 연관된 레지스트리를 삭제하는 함수'''
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             key_path, 0, winreg.KEY_ALL_ACCESS)
    except OSError:
        message.append(f"레지스트리 키 '{key_path}'를 열 수 없습니다.")
        return

    target_filename = ntpath.basename(target_filename)
    index = 0
    while True:
        try:
            # 레지스트리 키의 값을 하나씩 읽기
            name, data, type = winreg.EnumValue(key, index)

            # 'MRUListEx' 항목을 제외하고 처리
            if name == "MRUListEx":
                index += 1
                continue

            if type == winreg.REG_BINARY:
                # REG_BINARY 데이터(PIDL)를 파일 경로로 변환
                path = pidl_to_path(data)
                if path and target_filename in path:  # 파일명이 경로에 포함되는지 확인
                    # 변환 후 값 삭제
                    delete_registry_value(key, name, key_path, path)

            elif type == winreg.REG_SZ:
                # REG_SZ 데이터가 파일 경로일 가능성 있는지 체크
                if "\\" in data or "/" in data:  # 파일 경로일 가능성이 높은지 확인
                    if target_filename in data:  # 파일명이 경로에 포함되는지 확인
                        # 디코딩 후 값 삭제
                        delete_registry_value(key, name, key_path, data)

            # 값이 삭제되었으므로 index를 증가시키지 않고 계속 같은 위치를 체크
            index += 1

        except OSError:
            break

    # 하위 키들도 확인
    try:
        index = 0
        while True:
            # 하위 키 열기
            subkey_name = winreg.EnumKey(key, index)
            subkey_path = f"{key_path}\\{subkey_name}"
            read_and_delete_pidl_mru(
                subkey_path, target_filename)  # 재귀적으로 하위 키를 처리
            index += 1
    except OSError:
        pass  # 더 이상 하위 키가 없는 경우

    # 키 닫기
    winreg.CloseKey(key)


def delete_recent_link_file(file_path):
    '''최근 문서 목록 바로가기 파일을 삭제하는 함수'''
    recent_folders = [
        os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Recent"),
        os.path.expandvars(r"%APPDATA%\Microsoft\Office\Recent")
    ]
    file_name = os.path.basename(file_path)
    for recent_folder in recent_folders:
        link_pattern = os.path.join(recent_folder, f"{file_name}*.lnk")
        link_files = glob.glob(link_pattern)
        deleted_any = False
        for link_file in link_files:
            try:
                os.remove(link_file)
                message.append(f"최근 문서 경로에서 .lnk 파일 삭제 성공: {link_file}")
                deleted_any = True
            except OSError as e:
                message.append(f".lnk 파일 삭제 중 오류 발생: {e}")
        if not deleted_any:
            message.append("삭제할 .lnk 파일이 없습니다.")


def delete_file_completely(file_path):
    '''파일을 삭제하는 메인 함수'''
    ext = os.path.splitext(file_path)[1].lower()
    signatures = {
        '.pdf': ['%PDF-1', '%%EOF'],
        '.docx': ['PK', 'word/document.xml', 'word/_rels/document.xml.rels'],
        '.xlsx': ['PK', 'xl/workbook.xml', 'xl/_rels/workbook.xml.rels']
    }
    if ext in signatures:
        replace_signature(file_path, signatures[ext])

    registry_paths = [
        r"Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSavePidlMRU",
        r"Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs",
        r"Software\Microsoft\Office\16.0\Word\User MRU",
        r"Software\Microsoft\Office\16.0\Excel\User MRU",
        r"Software\Microsoft\Office\16.0\PowerPoint\User MRU"
    ]
    for path in registry_paths:
        read_and_delete_pidl_mru(path, file_path)

    if os.path.exists(file_path):
        secure_delete_file(file_path)
        delete_recent_link_file(file_path)
    else:
        message.append(f"파일이 존재하지 않습니다: {file_path}")
    
    return message


# 사용 예제
#delete_file_completely("C:\\Users\\Locava\\Documents\\newTest.pdf")
