import os
import cv2
import numpy as np
import onnxruntime as ort
from pathlib import Path
from .analy import detect_lost_item

# --- 設定 ---
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = os.path.join(BASE_DIR, 'ml_models', 'yolo26s_best.onnx')

CLASS_NAMES = ['wallet', 'smartphone', 'book', 'umbrella', 'pen', 'eraser', 'bottle']
INPUT_WIDTH = 640
INPUT_HEIGHT = 640
CONF_THRESHOLD = 0.5

# --- モデルの読み込み（超軽量CPU設定） ---
opts = ort.SessionOptions()
opts.intra_op_num_threads = 1
opts.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL

# 👇 以下の2行を新しく追加してください
opts.enable_cpu_mem_arena = False  # メモリの事前確保（アリーナ）を無効化して消費量を削る
opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_BASIC # 基本最適化のみ（メモリ爆発を防ぐ）

session = ort.InferenceSession(MODEL_PATH, sess_options=opts)
input_name = session.get_inputs()[0].name


def classify_color_hsv(h, s, v):
    """HSV値から色名を判定（ロジック完全維持）"""
    if v < 125: 
        return "黒"
    if s < 18:
        if v > 240: 
            return "白"
        else: 
            return "灰"
    if (h < 30 or h > 160) and v < 245 and s < 150: 
        return "茶"
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


def letterbox(img, new_shape=(640, 640), color=(114, 114, 114)):
    """アスペクト比を維持した精密リサイズ"""
    shape = img.shape[:2]
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    new_unpad = (int(round(shape[1] * r)), int(round(shape[0] * r)))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]
    dw /= 2
    dh /= 2
    if shape[::-1] != new_unpad:
        img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
    return img, r, (dw, dh)


def analyze_uploaded_image(image_file):
    # メモリ上で画像を高速ロード（一時ファイルを作らないため超軽量）
    file_bytes = np.frombuffer(image_file.read(), dtype=np.uint8)
    img_orig = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if img_orig is None:
        print("画像が読み込めませんでした")
        return {'status': 'error', 'message': '画像の読み込みに失敗しました。', 'status_code': 400}

    # ──── 画像補正（元ロジックを完全維持） ────
    img_processed = cv2.convertScaleAbs(img_orig, alpha=1.2, beta=30)
    img_processed = cv2.resize(img_processed, None, fx=1.5, fy=1.5)
    h_processed, w_processed = img_processed.shape[:2]

    # ──── ONNX用の画像前処理 ────
    img_letterboxed, ratio, (dw, dh) = letterbox(img_processed, new_shape=(INPUT_HEIGHT, INPUT_WIDTH))
    img_rgb = cv2.cvtColor(img_letterboxed, cv2.COLOR_BGR2RGB)
    img_chw = img_rgb.transpose((2, 0, 1))
    img_normalized = img_chw.astype(np.float32) / 255.0
    input_data = np.expand_dims(img_normalized, axis=0)

    # ──── 推論実行 ────
    outputs = session.run(None, {input_name: input_data})
    
    # 💡 モデル内部でNMS済みのきれいなデータを取得
    detections = outputs[0][0] 

    print(f"\n--- ONNX 解析開始（モデル側での検知数: {len(detections)}） ---")

    # 有効な検出結果を高スコア順に走査
    for det in detections:
        x1_raw, y1_raw, x2_raw, y2_raw, score, class_id = det
        
        # スコアが0.5を下回った時点で、これ以降のループを見る必要はない（降順ソート済みのため）
        if score < CONF_THRESHOLD:
            break

        class_id = int(class_id)
        label = CLASS_NAMES[class_id] if class_id < len(CLASS_NAMES) else "不明"
        print(f"検証対象: {label} (conf: {score:.2f})")

        # 💡 寸分の狂いもない精密座標復元
        x1 = int(max(0, np.clip(round((x1_raw - dw) / ratio), 0, w_processed)))
        y1 = int(max(0, np.clip(round((y1_raw - dh) / ratio), 0, h_processed)))
        x2 = int(max(0, np.clip(round((x2_raw - dw) / ratio), 0, w_processed)))
        y2 = int(max(0, np.clip(round((y2_raw - dh) / ratio), 0, h_processed)))

        # 補正後画像から物体を美しく切り出す
        roi = img_processed[y1:y2, x1:x2]
        if roi.size == 0:
            continue

        h, w = roi.shape[:2]
        dy, dx = int(h * 0.3), int(w * 0.3)
        center_roi = roi[dy:h-dy, dx:w-dx]

        if center_roi.size == 0:
            center_roi = roi

        # 色判定の処理（K-means）
        center_roi = cv2.resize(center_roi, (50, 50))
        hsv = cv2.cvtColor(center_roi, cv2.COLOR_BGR2HSV)
        pixels = np.float32(hsv.reshape(-1, 3))

        K = 3
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        _, labels, centers = cv2.kmeans(pixels, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

        counts = np.bincount(labels.flatten())
        dominant = centers[np.argmax(counts)]
        color_tag = classify_color_hsv(dominant[0], dominant[1], dominant[2])

        # 判定結果のマッチング
        detection_result = detect_lost_item(label, color_tag)

        # マッチング成功したらその時点で即返却（元コードの最善の仕様を完全維持）
        if detection_result.get('status') == 'success':
            print(f"🎉 落とし物特定に成功しました: {label} ({color_tag})")
            return {
                'status': 'success',
                'item': detection_result.get('item'),
                'color': detection_result.get('color'),
            }

    # ループが終了しても何も特定できなかった場合
    print("❌ 特定できませんでした")
    return {
        'status': 'error',
        'message': '画像から落とし物を特定できませんでした。（検知限界以下、または対象外）',
        'status_code': 200
    }