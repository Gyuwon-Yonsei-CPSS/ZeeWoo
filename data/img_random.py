import os
import shutil
import random

# 경로 설정 절대 경로로 수정
image_dir = 'D:/ZeeWoo_software/data/archive'   # 원본 이미지 경로
label_dir = 'D:/ZeeWoo_software/data/labels'    # 라벨 파일 경로
train_image_dir = 'D:/ZeeWoo_software/data/train/images'  # 학습 이미지 경로
train_label_dir = 'D:/ZeeWoo_software/data/train/labels'  # 학습 라벨 경로
val_image_dir = 'D:/ZeeWoo_software/data/val/images'      # 검증 이미지 경로
val_label_dir = 'D:/ZeeWoo_software/data/val/labels'      # 검증 라벨 경로


# 폴더 생성
os.makedirs(train_image_dir, exist_ok=True)
os.makedirs(train_label_dir, exist_ok=True)
os.makedirs(val_image_dir, exist_ok=True)
os.makedirs(val_label_dir, exist_ok=True)

# 이미지 확장자
image_extensions = [".png", ".jpg", ".jpeg"]

# 이미지 파일 리스트 가져오기
image_files = [f for f in os.listdir(image_dir) if any(f.endswith(ext) for ext in image_extensions)]

# 이미지 파일 섞기 (랜덤하게 분배하기 위해)
random.shuffle(image_files)

# 80% 학습용, 20% 검증용으로 분리
split_ratio = 0.8
train_size = int(len(image_files) * split_ratio)

train_files = image_files[:train_size]
val_files = image_files[train_size:]

# 학습용 파일 복사
for file in train_files:
    # 이미지 파일 복사
    shutil.copy(os.path.join(image_dir, file), os.path.join(train_image_dir, file))
    
    # 라벨 파일 확장자를 이미지 확장자에서 .txt로 변경
    label_file = file.replace('.jpg', '.txt').replace('.jpeg', '.txt').replace('.png', '.txt')
    
    # 해당하는 라벨 파일도 복사
    shutil.copy(os.path.join(label_dir, label_file), os.path.join(train_label_dir, label_file))

# 검증용 파일 복사
for file in val_files:
    # 이미지 파일 복사
    shutil.copy(os.path.join(image_dir, file), os.path.join(val_image_dir, file))
    
    # 라벨 파일 확장자를 이미지 확장자에서 .txt로 변경
    label_file = file.replace('.jpg', '.txt').replace('.jpeg', '.txt').replace('.png', '.txt')
    
    # 해당하는 라벨 파일도 복사
    shutil.copy(os.path.join(label_dir, label_file), os.path.join(val_label_dir, label_file))

print("이미지와 라벨이 학습용과 검증용으로 나누어졌습니다.")