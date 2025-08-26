import cv2
import os
import numpy as np

def apply_otsu_threshold(image):
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    _, binary_mask = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary_mask

def filter_contours(contours, center_y, min_area=1000, margin=50):
    filtered_contours = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < min_area:
            continue

        x, y, w, h = cv2.boundingRect(contour)

        # 중앙 y 위치에 있는 외곽선만 선택
        if abs((y + h // 2) - center_y) > margin:
            continue

        filtered_contours.append(contour)

    return filtered_contours

def all_contours_mask(binary_image, min_area=1000):
    center_y = binary_image.shape[0] // 2
    margin = binary_image.shape[0] // 4  # 중앙에서 +/- 1/4 높이 범위 내의 외곽선만 선택

    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filtered_contours = filter_contours(contours, center_y, min_area, margin)
    mask = np.zeros(binary_image.shape, dtype=np.uint8)
    cv2.drawContours(mask, filtered_contours, -1, 255, thickness=cv2.FILLED)
    return mask

def process_images(input_dir, output_dir, overlay_dir):
    if not os.path.exists(input_dir):
        print(f"Error: Input directory '{input_dir}' does not exist.")
        return

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(overlay_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            overlay_path = os.path.join(overlay_dir, filename)

            input_image = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
            print(f"Reading image: {input_path}")

            if input_image is None:
                print(f'Error: Failed to read {input_path}')
                continue
            else:
                print(f"Image shape: {input_image.shape}")

            binary_mask = apply_otsu_threshold(input_image)

            all_masks = all_contours_mask(binary_mask, min_area=1000)

            if not cv2.imwrite(output_path, all_masks):
                print(f'Error: Failed to write {output_path}')
            else:
                print(f"Mask saved: {output_path}")

            # 빨간색 채널을 강조한 오버레이 이미지 생성
            color_mask = cv2.merge([np.zeros_like(all_masks), np.zeros_like(all_masks), all_masks])  # 빨간색 채널을 강조
            overlay = cv2.addWeighted(cv2.cvtColor(input_image, cv2.COLOR_GRAY2BGR), 0.7, color_mask, 0.3, 0)

            if not cv2.imwrite(overlay_path, overlay):
                print(f'Error: Failed to write {overlay_path}')
            else:
                print(f"Overlay saved: {overlay_path}")

            print(f'Processed {filename}')

    print('success')

input_dir = '/Users/yoonchaeyeon/PycharmProjects/vision_1/input/Case_3/이미지(png)'
output_dir = '/Users/yoonchaeyeon/PycharmProjects/vision_1/output/case_3'
overlay_dir = '/Users/yoonchaeyeon/PycharmProjects/vision_1/overlay/case_3'

process_images(input_dir, output_dir, overlay_dir)
