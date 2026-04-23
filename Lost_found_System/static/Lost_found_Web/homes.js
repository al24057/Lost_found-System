let targetUrl = '';

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