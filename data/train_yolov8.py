from ultralytics import YOLO

# YOLOv8 모델 불러오기 (pre-trained weights 사용)
model = YOLO('yolov8n.pt')  # 'yolov8n.pt'는 작은 네트워크, 'yolov8s.pt' 등으로 변경 가능

# 모델 학습
model.train(
    data='D:/ZeeWoo_software/data/dataset.yaml',  # 데이터셋 설정 파일 경로
    epochs=50,                 # 학습 반복 횟수
    batch=16,                  # 배치 크기
    imgsz=640                  # 이미지 크기
)
