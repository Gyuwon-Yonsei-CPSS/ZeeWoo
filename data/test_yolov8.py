import os
from ultralytics import YOLO
import cv2

# 모델 불러오기 (학습된 모델의 경로 지정)
model = YOLO('runs/detect/train4/weights/best.pt')  # 학습된 모델 경로

# 이미지가 저장된 경로 (탐지할 이미지들이 위치한 디렉토리)
image_dir = r'C:\Users\user\Pictures\test'

# 결과 저장 경로
output_dir = r'C:\Users\user\Pictures\results'
os.makedirs(output_dir, exist_ok=True)

# 탐지된 이미지와 전체 스캔 이미지 수를 추적
total_images = 0
detected_images = 0
detected_image_paths = []

# 이미지 파일들 탐지
for image_name in os.listdir(image_dir):
    if image_name.endswith(('.jpg', '.png', '.jpeg')):  # 이미지 파일 확장자 확인
        total_images += 1  # 스캔한 이미지 수 증가
        image_path = os.path.join(image_dir, image_name)
        print(f"Processing {image_path}...")
        
        # 이미지 읽기
        img = cv2.imread(image_path)
        
        # 모델에 이미지 입력하여 탐지 실행
        results = model(img)
        
        # 탐지된 바운딩 박스 개수 출력
        print(f"탐지된 바운딩 박스 개수: {len(results[0].boxes)}")

        # 탐지된 바운딩 박스가 있는지 확인
        if len(results[0].boxes) > 0:
            detected_images += 1  # 탐지된 이미지 수 증가
            detected_image_paths.append(image_path)  # 탐지된 이미지 경로 저장
            print(f"ID 카드 탐지됨: {image_path}")
            
            # 탐지 결과를 시각화 및 저장 (results[0]에서 저장)
            results[0].save(output_dir)
            print(f"Saved results for {image_name} to {output_dir}")

            # 탐지된 이미지만 640x640 사이즈로 리사이즈하여 OpenCV 창으로 표시
            resized_img = cv2.resize(img, (640, 640))  # 이미지 크기 조정 (정사각형 프레임)
            cv2.imshow("Detected ID Card", resized_img)
            cv2.waitKey(0)  # 이미지가 화면에 나타난 후 아무 키나 누를 때까지 대기
            cv2.destroyAllWindows()  # 모든 OpenCV 창 닫기

# 결과 요약 출력
print(f"총 {total_images}장의 이미지를 스캔하였으며, {detected_images}장의 이미지에서 ID 카드가 탐지되었습니다.")
if detected_images > 0:
    print("탐지된 이미지 경로:")
    for path in detected_image_paths:
        print(path)
