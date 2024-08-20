import os

# 1. 이미지에서 텍스트 추출
print("1. 이미지에서 텍스트 추출")
os.system("python scripts/extract_text.py")

# 2. 텍스트 전처리
print("2. 텍스트 전처리")
os.system("python scripts/preprocess_text.py")

# 3. 민감 정보 탐지
print("3. 민감 정보 탐지")
os.system("python scripts/detect_sensitive.py")

# 4. 파이프라인 완료
print("파이프라인 실행이 완료되었습니다.")
