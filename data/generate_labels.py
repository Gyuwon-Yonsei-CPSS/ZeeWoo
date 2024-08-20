import cv2
import os

# 경로 설정
image_dir = "D:/ZeeWoo_software/data/archive"  # ID 카드 이미지가 있는 절대 경로
output_dir = "D:/ZeeWoo_software/data/labels"  # 바운딩 박스 라벨을 저장할 절대 경로

# labels 폴더가 없으면 생성
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 이미지 확장자
image_extensions = [".png", ".jpg", ".jpeg"]

# 이미지 파일 불러오기
for image_name in os.listdir(image_dir):
    if any(image_name.endswith(ext) for ext in image_extensions):
        # 이미지 경로 설정
        image_path = os.path.join(image_dir, image_name)
        img = cv2.imread(image_path)

        if img is None:
            print(f"Error loading image: {image_name}")
            continue

        # OpenCV로 이미지 처리 (흑백 변환 -> 블러 처리 -> 엣지 탐지)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 50, 150)

        # 윤곽선 찾기
        contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 윤곽선이 있을 경우
        if contours:
            # 가장 큰 윤곽선 추출 (ID 카드일 가능성이 높음)
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)

            # YOLO 형식으로 바운딩 박스 정보를 저장
            label_path = os.path.join(output_dir, f"{os.path.splitext(image_name)[0]}.txt")
            with open(label_path, "w") as label_file:
                # YOLO 형식: class_id x_center y_center width height (상대 좌표로 변환)
                img_h, img_w, _ = img.shape
                x_center = (x + w / 2) / img_w
                y_center = (y + h / 2) / img_h
                rel_width = w / img_w
                rel_height = h / img_h
                label_file.write(f"0 {x_center} {y_center} {rel_width} {rel_height}\n")

            # 결과를 이미지로 시각화하고 저장 (원하는 경우)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imshow("Detected ID Card", img)
            cv2.waitKey(100)  # 이미지를 100ms 동안 표시
        else:
            print(f"No contours found for {image_name}")

cv2.destroyAllWindows()
