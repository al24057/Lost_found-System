let targetUrl = '';

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');
    
    // クラスの付け外しで表示・非表示を切り替える
    sidebar.classList.toggle('active');
    overlay.classList.toggle('active');
}

function openConfirm(url) {
  targetUrl = url;
  document.getElementById('modal').style.display = 'flex';
}

function closeModal() {
  document.getElementById('modal').style.display = 'none';
}

function goDetail() {
  window.location.href = targetUrl;
}