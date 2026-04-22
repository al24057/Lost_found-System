let selectedPost = '';

function openModal(text) {
  selectedPost = text;
  document.getElementById('modal-text').innerText = text;
  document.getElementById('modal').style.display = 'flex';
}

function closeModal() {
  document.getElementById('modal').style.display = 'none';
}

function confirmAction() {
  alert('ページ遷移します（仮）: ' + selectedPost);
  closeModal();
}

window.onclick = function(event) {
  const modal = document.getElementById('modal');
  if (event.target === modal) {
    closeModal();
  }
};