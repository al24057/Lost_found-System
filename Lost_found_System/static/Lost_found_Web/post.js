let targetUrl = '';

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');

    // クラスの付け外しで表示・非表示を切り替える
    sidebar.classList.toggle('active');
    overlay.classList.toggle('active');
}

// ==========================================================
// 💡 画像プレビュー & 解析ボタンのPython非同期通信処理
// ==========================================================
document.addEventListener('DOMContentLoaded', function() {
    const imageInput = document.querySelector('input[type="file"]');
    const previewImage = document.getElementById('image-preview');
    const analysisBtn = document.getElementById('analysis-btn');

    // 1. 画像が選択されたらプレビューとボタンを表示
    if (imageInput) {
        imageInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(event) {
                    previewImage.src = event.target.result;
                    previewImage.style.display = 'block'; 
                    analysisBtn.style.display = 'inline-block'; 
                }
                reader.readAsDataURL(file);
            } else {
                previewImage.src = '';
                previewImage.style.display = 'none';
                analysisBtn.style.display = 'none';
            }
        });
    }

    // 2. 「解析」ボタンを押したときにPythonの関数（views.analyze_image）を呼び出す
    if (analysisBtn) {
        analysisBtn.addEventListener('click', function() {
            const file = imageInput.files[0];
            if (!file) {
                alert('画像を選択してください。');
                return;
            }

            // ボタンをローディング状態にする
            analysisBtn.innerText = '解析中...';
            analysisBtn.disabled = true;

            const formData = new FormData();
            formData.append('image', file);

            // DjangoのCSRFトークンを取得
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            // urls.py で設定したパスに画像付きでリクエストを投げる
            fetch('/post/analyze/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => {
                if (!response.ok) throw new Error('サーバーエラーが発生しました');
                return response.json();
            })
            .then(data => {
                analysisBtn.innerText = '解析';
                analysisBtn.disabled = false;

                if (data.status === 'success') {
                    // Pythonから返ってきた英語キーをフォーム欄にセットする
                    const itemField = document.querySelector('[name="item"]');
                    const colorField = document.querySelector('[name="color"]');
                    
                    if (itemField && data.item) itemField.value = data.item;
                    if (colorField && data.color) colorField.value = data.color;

                    alert('解析が完了しました！結果がフォームに自動入力されました。');
                } else {
                    alert('解析に失敗しました: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                analysisBtn.innerText = '解析';
                analysisBtn.disabled = false;
                alert('通信エラーまたは解析エラーが発生しました。');
            });
        });
    }
});