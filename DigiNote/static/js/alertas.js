// Cerrar alertas
function cerrarAlert(boton) {
  const alerta = boton.closest('.alert');
  if (alerta) {
    alerta.remove();
  }
}

// Cerrar alertas automáticamente después de 6 segundos
document.querySelectorAll('.alert').forEach(alerta => {
  setTimeout(() => {
    alerta.remove();
  }, 6000);
});

// Quitar formato 'active' de las opciones al ir al inicio
document.querySelector('.sidebar__logo a')?.addEventListener('click', () => {
  document.querySelectorAll('.sidebar__options--link').forEach(item => item.classList.remove('active'));
});
