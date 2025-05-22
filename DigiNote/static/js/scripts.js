// Efecto al seleccionar una opcion, añadir la clase 'active'
function activarOpcion(elemento) {
  const items = document.querySelectorAll('.sidebar__options--link');
  items.forEach(item => item.classList.remove('active'));
  // Agregar 'active' al enlace clickeado
  const itemActivo = elemento.closest('.sidebar__options--link');
  if (itemActivo) {
    itemActivo.classList.add('active');
  }
}

// Quitar 'active' si se hace clic en el logo
document.querySelector('.sidebar__logo a')?.addEventListener('click', () => {
  document.querySelectorAll('.sidebar__options--link').forEach(item => item.classList.remove('active'));
});


const btnDelete = document.querySelectorAll('.btn-delete');
if (btnDelete) {
  const btnArray = Array.from(btnDelete);
  btnArray.forEach((btn) => {
    btn.addEventListener('click', (e) => {
      if (!confirm('Are you sure you want to delete it?')) {
        e.preventDefault();
      }
    });
  })
}
