const myModal = document.getElementById('myModal')
const myInput = document.getElementById('myInput')

myModal.addEventListener('shown.bs.modal', () => {
  myInput.focus()
})
document.querySelector('.btn-primary').addEventListener('click', () => {
    alert('Cambios guardados');
    // Lógica para guardar datos
  });