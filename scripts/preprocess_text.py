import os
import re

# 경로 설정
ocr_result_dir = 'data/ocr_results'
preprocessed_output_dir = 'data/preprocessed_texts'

if not os.path.exists(preprocessed_output_dir):
    os.makedirs(preprocessed_output_dir)

# 텍스트 전처리 함수
def preprocess_text(text):
    text = re.sub(r'[^\w\s]', '', text)  # 특수 문자 제거
    text = re.sub(r'\s+', ' ', text)     # 공백 정리
    return text.strip()

# OCR 결과 전처리
for ocr_file in os.listdir(ocr_result_dir):
    with open(os.path.join(ocr_result_dir, ocr_file), 'r', encoding='utf-8') as f:
        raw_text = f.read()
        clean_text = preprocess_text(raw_text)
        
        # 전처리된 텍스트 저장
        output_file_path = os.path.join(preprocessed_output_dir, ocr_file)
        with open(output_file_path, 'w', encoding='utf-8') as f_out:
            f_out.write(clean_text)

        print(f"{ocr_file} 전처리 완료.")
