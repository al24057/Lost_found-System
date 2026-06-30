/**
 * サイドバーの開閉を切り替える関数
 */
let targetUrl = '';
function toggleSidebar() {
    // サイドバー（#sidebar）に「active」クラスをつけ外しする
    const sidebar = document.getElementById('sidebar');
    if (sidebar) {
        sidebar.classList.toggle('active');
    }

    // 背景の暗い幕（#overlay）に「active」クラスをつけ外しする
    const overlay = document.getElementById('overlay');
    if (overlay) {
        overlay.classList.toggle('active');
    }
}