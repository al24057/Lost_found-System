import os
from pathlib import Path
import cv2
import numpy as np
from ultralytics import YOLO

# 💡 追加：ベースディレクトリ（Lost_found_Web の場所）を取得し、モデルの絶対パスを作成
BASE_DIR = Path(__file__).resolve().parent.parent  # Lost_found_Web ディレクトリを指します
MODEL_PATH = os.path.join(BASE_DIR, 'ml_models', 'yolo26s_best.pt')

# 1. モデルの読み込み（絶対パスで指定）
# model = YOLO('yolo26s_best.pt')
model = YOLO(MODEL_PATH)


def detect_lost_item(detected_label, detected_color):
    try:
        # 3. マッピング処理：検出された文字を models.py の Choice キーに変換
        COLOR_MAP = {
            '赤': 'red', '青': 'blue', '黒': 'black', '白': 'white',
            '灰': 'gray', '茶': 'brown', '橙': 'orange', '黄': 'yellow',
            '黄緑': 'yellow_green', '緑': 'green', '水': 'light_blue', '紫': 'purple'
        }
        
        ITEM_MAP = {
            '傘': 'umbrella', 'umbrella': 'umbrella',
            'ペン': 'stationary', '消しゴム': 'stationary', 'pen': 'stationary', 'eraser': 'stationary',
            'スマホ': 'electronic_device', 'phone': 'electronic_device',
            '財布': 'valuable', 'wallet': 'valuable',
            '本': 'book', 'book': 'book',
            '水筒': 'daily',
        }
        
        # 辞書から該当するキーを取得
        mapped_color = COLOR_MAP.get(detected_color, 'black')  # デフォルト黒
        mapped_item = ITEM_MAP.get(detected_label, 'other')     # デフォルトその他
        
        return {
            'status': 'success',
            'item': mapped_item,
            'color': mapped_color,
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'解析中にエラーが発生しました: {str(e)}',
            'status_code': 500
        }