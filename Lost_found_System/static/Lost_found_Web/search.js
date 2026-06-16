let targetUrl = '';

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');

    // クラスの付け外しで表示・非表示を切り替える
    sidebar.classList.toggle('active');
    overlay.classList.toggle('active');
}

/* ==========================================================================
   ここから下に検索画面（search.html）専用のモーダル制御ロジックを追加
   ========================================================================== */

/**
 * 閲覧警告モーダルを開く
 * @param {string} url - 遷移先の詳細画面のURL
 */
function openConfirm(url) {
    targetUrl = url;
    const modal = document.getElementById('modal');
    if (modal) {
        modal.style.display = 'flex';
    }
}

/**
 * モーダルを閉じる（キャンセル時など）
 */
function closeModal() {
    const modal = document.getElementById('modal');
    if (modal) {
        modal.style.display = 'none';
    }
}

/**
 * 警告を承諾して詳細画面へ遷移する
 */
function goDetail() {
    if (targetUrl) {
        window.location.href = targetUrl;
    }
}