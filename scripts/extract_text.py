import pytesseract
from PIL import Image
import os

# Tesseract 경로 설정 (Windows 사용자는 tesseract.exe 경로 지정 필요)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 경로 설정
archive_dir = 'data/archive'            # 이미지 파일이 저장된 디렉터리
ocr_output_dir = 'data/ocr_results'     # OCR 결과를 저장할 디렉터리

if not os.path.exists(ocr_output_dir):
    os.makedirs(ocr_output_dir)

# 이미지 파일에서 텍스트 추출
for image_file in os.listdir(archive_dir):
    if image_file.endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(archive_dir, image_file)
        
        # 이미지 열기
        img = Image.open(image_path)
        
        # Tesseract OCR 실행 (한국어 + 영어)
        text = pytesseract.image_to_string(img, lang='kor+eng') 
        
        # OCR 결과 텍스트 파일로 저장
        output_file_path = os.path.join(ocr_output_dir, f"{os.path.splitext(image_file)[0]}.txt")
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(text)

        print(f"{image_file}에서 텍스트 추출 완료.")
