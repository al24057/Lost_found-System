from ultralytics import YOLO
import cv2
import numpy as np
from pathlib import Path
import os

# 💡 追加：ベースディレクトリ（Lost_found_Web の場所）を取得し、モデルの絶対パスを作成
BASE_DIR = Path(__file__).resolve().parent.parent  # Lost_found_Web ディレクトリを指します
MODEL_PATH = os.path.join(BASE_DIR, 'services', 'yolo26s_best.pt')

# 1. モデルの読み込み（絶対パスで指定）
#model = YOLO('yolo26s_best.pt')
model = YOLO(MODEL_PATH)

def classify_color_hsv(h, s, v):
    """HSV値から色名を判定"""
    # 明るさ・彩度ベース（白・黒・グレー）
    if v < 125:
        return "黒"
    if s < 18:
        if v > 240:
            return "白"
        else:
            return "灰"

    # --- 茶色（特殊ケース） ---
    # 暗め＋低彩度＋赤〜黄付近
    if (h < 30 or h > 160) and v < 245 and s < 150:
        return "茶"

    # --- 色相ベース ---
    if h < 10 or h > 170:
        return "赤"

    elif h < 25:
        return "橙"

    elif h < 31:
        return "黄"

    elif h < 70:
        return "黄緑"

    elif h < 90:
        return "緑"

    elif h < 103:
        return "水"

    elif h < 116:
        return "青"

    elif h < 165:
        return "紫"

    return "不明"


def detect_lost_item(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print("画像が読み込めませんでした")
        return

    # 明るさ調整    
    img = cv2.convertScaleAbs(img, alpha=1.2, beta=30)

    # 解像度アップ（1.5倍）
    img = cv2.resize(img, None, fx=1.5, fy=1.5)

    results = model(img, conf=0.5)
    print(f"\n--- 認識結果: {image_path} ---")
    for result in results:
        for box in result.boxes:
            conf = float(box.conf[0])

            class_id = int(box.cls[0])
            label = model.names[class_id]

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            h, w = img.shape[:2]
            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(w, x2)
            y2 = min(h, y2)
            roi = img[y1:y2, x1:x2]

            if roi.size > 0:
                h, w = roi.shape[:2]
                dy = int(h * 0.3)
                dx = int(w * 0.3)
                center_roi = roi[dy:h-dy, dx:w-dx]

                if center_roi.size == 0:
                    center_roi = roi

                # サイズ統一
                center_roi = cv2.resize(center_roi, (50, 50))

                # HSV変換
                hsv = cv2.cvtColor(center_roi, cv2.COLOR_BGR2HSV)

                # reshape
                pixels = hsv.reshape(-1, 3)
                pixels = np.float32(pixels)

                # K-means
                K = 3 # 色の数（3〜5がおすすめ）
                criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

                _, labels, centers = cv2.kmeans(
                    pixels,
                    K,
                    None,
                    criteria,
                    10,
                    cv2.KMEANS_RANDOM_CENTERS
                )

                # 各クラスタの割合
                counts = np.bincount(labels.flatten())

                # 一番多い色を選択
                dominant = centers[np.argmax(counts)]

                h_val, s_val, v_val = dominant

                # 色判定
                color_tag = classify_color_hsv(h_val, s_val, v_val)

                #print(f"【結果】 {color_tag}色の{label} (確信度: {conf:.2f})")
                #print(f"H:{h_val:.1f}, S:{s_val:.1f}, V:{v_val:.1f}")
                return label, color_tag

#if __name__ == "__main__":
    #target_image = "IMG_3209.jpg"
    #detect_lost_item(target_image)


# スマホ　財布　本　ペン　消しゴム　水筒　傘