import os
import tempfile
from .analy import detect_lost_item

def analyze_uploaded_image(image_file):
    """
    アップロードされた一時ファイルをサーバーに保存し、
    YOLO解析および Choice キーへのマッピング処理を行って結果を返すサービス関数
    """
    # 1. 渡された画像ファイルを一時ファイルとしてサーバーに保存し、パスを生成
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(image_file.name)[1]) as temp_file:
        for chunk in image_file.chunks():
            temp_file.write(chunk)
        temp_file_path = temp_file.name

    try:
        # 2. 同一階層の analy.py の関数に一時ファイルのパスを渡して解析を実行
        analysis_result = detect_lost_item(temp_file_path)
        
        if not analysis_result:
            return {'status': 'error', 'message': '物体を検出できませんでした。', 'status_code': 200}
            
        detected_label, detected_color = analysis_result
        
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
        return {'status': 'error', 'message': f'解析中にエラーが発生しました: {str(e)}', 'status_code': 500}
        
    finally:
        # 4. 用が済んだ一時ファイルを物理削除
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)